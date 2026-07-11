#!/usr/bin/env python3
"""Normalize and rank fetched job postings for the job-scraper skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SCHEMA_DEFAULTS: dict[str, Any] = {
    "title": "unknown",
    "company": "unknown",
    "source": "other",
    "url": "",
    "market": "Other",
    "location": "unknown",
    "workplace_model": "unknown",
    "remote_country_eligibility": "unknown",
    "language_requirements": [],
    "work_authorization": "unknown",
    "contract_type": "unknown",
    "seniority": "unknown",
    "posting_date": "",
    "deadline": "",
    "required_skills": [],
    "nice_to_have_skills": [],
    "fit": "low",
    "fit_score": 0,
    "status": "new",
    "flags": [],
    "blockers": [],
}

SKILLS = (
    "python",
    "sql",
    "postgresql",
    "power bi",
    "tableau",
    "looker",
    "excel",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "mlflow",
    "airflow",
    "dbt",
    "spark",
    "databricks",
    "aws",
    "azure",
    "gcp",
    "kubernetes",
    "docker",
    "terraform",
    "grafana",
    "prometheus",
)

LANGUAGE_ALIASES = {
    "english": "English",
    "dutch": "Dutch",
    "nederlands": "Dutch",
    "german": "German",
    "deutsch": "German",
    "croatian": "Croatian",
    "hrvatski": "Croatian",
}

REMOTE_ACCEPT = (
    "croatia",
    "netherlands",
    "europe",
    "european",
    "eu",
    "eea",
    "emea",
    "worldwide",
    "anywhere",
)

REMOTE_REJECT = (
    "us only",
    "usa only",
    "united states only",
    "india only",
    "latam only",
    "apac only",
    "philippines only",
    "canada only",
)


def normalize_job(raw: dict[str, Any], profile: dict[str, Any] | None = None) -> dict[str, Any]:
    job = dict(SCHEMA_DEFAULTS)
    if _looks_like_linkedin(raw):
        job.update(parse_linkedin_detail(raw))
    elif raw.get("text"):
        job.update(parse_portal_text(raw["text"], raw.get("url", "")))
    else:
        job.update({k: v for k, v in raw.items() if k in job})

    text = _job_text(raw, job)
    job["source"] = job["source"] or infer_source(job["url"])
    job["market"] = infer_market(job["location"], text)
    job["workplace_model"] = infer_workplace(job["location"], text)
    job["remote_country_eligibility"] = infer_remote_eligibility(job["location"], text)
    job["language_requirements"] = infer_required_languages(text)
    job["work_authorization"] = infer_work_authorization(text)
    job["contract_type"] = infer_contract_type(f"{job.get('contract_type', '')} {text}")
    job["required_skills"] = infer_skills(text)
    job["flags"] = sorted(set(job.get("flags", []) + infer_flags(job, text)))
    return score_job(job, profile or {})


def parse_linkedin_detail(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": raw.get("title") or "unknown",
        "company": raw.get("company") or "unknown",
        "source": "linkedin",
        "url": raw.get("url") or (f"https://www.linkedin.com/jobs/view/{raw['id']}" if raw.get("id") else ""),
        "location": raw.get("location") or "unknown",
        "contract_type": raw.get("employmentType") or "unknown",
        "seniority": raw.get("seniority") or "unknown",
        "posting_date": raw.get("date") or "",
    }


def parse_portal_text(text: str, url: str = "") -> dict[str, Any]:
    source = infer_source(url)
    title = _first_match(text, r"(?m)^#\s+(.+)$") or _first_match(text, r"(?m)^Title:\s+(.+)$")
    company = _company_from_text(text)
    location = _location_from_text(text)
    status = "expired" if re.search(r"applications have closed|listing has expired|position is closed", text, re.I) else "new"
    return {
        "title": title or "unknown",
        "company": company or "unknown",
        "source": source,
        "url": url,
        "location": location or "unknown",
        "contract_type": infer_contract_type(text),
        "seniority": infer_seniority(text),
        "status": status,
    }


def score_job(job: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    text = _norm(" ".join(str(job.get(k, "")) for k in ("title", "company", "location", "market")) + " " + " ".join(job.get("required_skills", [])))
    target_roles = [_norm(x) for x in profile.get("target_roles", [])]
    target_markets = [_norm(x) for x in profile.get("target_markets", [])]
    profile_skills = [_norm(x) for x in profile.get("skills", [])]
    target_seniority = [_norm(x) for x in profile.get("seniority", [])]

    score = 0
    if any(role and role in _norm(job["title"]) for role in target_roles):
        score += 30
    elif any(part and part in _norm(job["title"]) for role in target_roles for part in role.split()):
        score += 12

    if any(market and market in _norm(f"{job['market']} {job['location']} {job['remote_country_eligibility']}") for market in target_markets):
        score += 20

    score += min(25, 5 * sum(1 for skill in profile_skills if skill and skill in text))

    seniority_text = _norm(f"{job['title']} {job['seniority']}")
    if any(level and level in seniority_text for level in target_seniority):
        score += 15
    elif "junior" in target_seniority or "entry" in target_seniority:
        if re.search(r"\b(senior|lead|principal|staff|manager|5\+ years)\b", seniority_text):
            score -= 20
        elif re.search(r"\b(junior|entry|graduate|starter|associate)\b", seniority_text):
            score += 10

    if job.get("status") != "expired":
        score += 10

    blockers = sorted(set(job.get("blockers", []) + infer_blockers(job, profile)))
    job["blockers"] = blockers
    job["fit_score"] = max(0, min(100, score))
    if blockers:
        job["status"] = "expired" if "expired or closed" in blockers else "skipped"
        job["fit"] = "low"
    elif job["fit_score"] >= 70:
        job["fit"] = "high"
    elif job["fit_score"] >= 45:
        job["fit"] = "medium"
    else:
        job["fit"] = "low"
    return job


def infer_source(url: str) -> str:
    host = urlparse(url).netloc.lower()
    for source in ("linkedin", "euremotejobs", "relocate.me", "iamexpat", "englishjobsearch", "remote.com", "remotive"):
        if source in host:
            return source
    return "other"


def infer_market(location: str, text: str) -> str:
    haystack = _norm(f"{location} {text}")
    if "croatia" in haystack or "zagreb" in haystack:
        return "Croatia"
    if "netherlands" in haystack or "amsterdam" in haystack or "utrecht" in haystack or "rotterdam" in haystack:
        return "Netherlands"
    if "relocation" in haystack or "visa sponsorship" in haystack:
        return "Relocation"
    if any(term in haystack for term in ("remote", "europe", "emea", "eea")):
        return "Remote EU"
    return "Other"


def infer_workplace(location: str, text: str) -> str:
    haystack = _norm(f"{location} {text}")
    if "hybrid" in haystack:
        return "hybrid"
    if "remote" in haystack or "work from home" in haystack:
        return "remote"
    if "office" in haystack or "onsite" in haystack or "on-site" in haystack:
        return "onsite"
    return "unknown"


def infer_remote_eligibility(location: str, text: str) -> str:
    haystack = _norm(f"{location} {text}")
    hits = [term for term in REMOTE_ACCEPT if _has_term(haystack, term)]
    rejects = [term for term in REMOTE_REJECT if _has_term(haystack, term)]
    if rejects:
        return f"blocked: {', '.join(rejects)}"
    if hits:
        return ", ".join(sorted(set(hits)))
    return "unknown"


def infer_required_languages(text: str) -> list[str]:
    found: set[str] = set()
    lowered = _norm(text)
    requirement_words = r"(required|must|fluent|native|near-native|professional|excellent|vloeiend|goede beheersing|c1|c2)"
    for alias, language in LANGUAGE_ALIASES.items():
        if alias not in lowered:
            continue
        pattern = rf"(.{{0,45}}{requirement_words}.{{0,45}}{alias}|{alias}.{{0,45}}{requirement_words}.{{0,45}})"
        if re.search(pattern, lowered, re.I):
            found.add(language)
    return sorted(found)


def infer_work_authorization(text: str) -> str:
    lowered = _norm(text)
    if "visa sponsorship not included" in lowered or "will not require visa sponsorship" in lowered:
        return "no sponsorship"
    if "visa sponsorship" in lowered or "relocation support" in lowered:
        return "sponsorship/relocation mentioned"
    return "unknown"


def infer_contract_type(text: str) -> str:
    lowered = _norm(text)
    if "freelance" in lowered or "zzp" in lowered:
        return "freelance"
    if "contractor" in lowered:
        return "contractor"
    if "internship" in lowered or "intern " in lowered:
        return "internship"
    if "temporary" in lowered or "fixed-term" in lowered or "fixed term" in lowered:
        return "temporary"
    if "part-time" in lowered or "part time" in lowered:
        return "part-time"
    if "full-time" in lowered or "full time" in lowered or "permanent" in lowered or "vast contract" in lowered:
        return "employee"
    return "unknown"


def infer_seniority(text: str) -> str:
    lowered = _norm(text)
    for term in ("internship", "entry", "junior", "associate", "mid", "senior", "lead", "principal", "staff"):
        if term in lowered:
            return term
    return "unknown"


def infer_skills(text: str) -> list[str]:
    lowered = _norm(text)
    return [skill for skill in SKILLS if skill in lowered]


def infer_flags(job: dict[str, Any], text: str) -> list[str]:
    flags = []
    if job["remote_country_eligibility"] == "unknown" and job["workplace_model"] == "remote":
        flags.append("remote eligibility unclear")
    if job["work_authorization"] == "unknown":
        flags.append("work authorization unclear")
    if job["remote_country_eligibility"] in {"anywhere", "worldwide"} and job["contract_type"] == "unknown":
        flags.append("worldwide contract setup unclear")
    if not job["language_requirements"]:
        flags.append("language requirements unclear")
    if re.search(r"current(?:ly)? based|already based|must be based", text, re.I):
        flags.append("current residence requirement")
    return flags


def infer_blockers(job: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    blockers = []
    if job.get("status") == "expired":
        blockers.append("expired or closed")
    if job["contract_type"] in set(profile.get("blocked_contracts", [])):
        blockers.append(f"{job['contract_type']}-only")
    profile_languages = {language.lower() for language in profile.get("languages", [])}
    for language in job["language_requirements"]:
        if language.lower() not in profile_languages:
            blockers.append(f"requires {language}")
    if job["remote_country_eligibility"].startswith("blocked:"):
        blockers.append(job["remote_country_eligibility"])
    if "current residence requirement" in job["flags"] and not profile.get("current_location"):
        blockers.append("current residence unclear")
    return blockers


def _looks_like_linkedin(raw: dict[str, Any]) -> bool:
    return "description" in raw and ("companyUrl" in raw or "employmentType" in raw or "jobFunction" in raw)


def _job_text(raw: dict[str, Any], job: dict[str, Any]) -> str:
    return " ".join(str(x or "") for x in (raw.get("description"), raw.get("text"), job.get("title"), job.get("company"), job.get("location")))


def _company_from_text(text: str) -> str | None:
    return (
        _first_match(text, r"(?m)^\s*\*\s*(?:Posted .*?\n\s*\*\s*)?([A-Z][^\n]{1,80})\s*$")
        or _first_match(text, r"(?m)^Company:\s+(.+)$")
    )


def _location_from_text(text: str) -> str | None:
    return (
        _first_match(text, r"(?m)^\s*\*\s*([A-Z][A-Za-z ,/+-]*(?:Europe|EMEA|Netherlands|Croatia|Remote|Worldwide)[^\n]*)$")
        or _first_match(text, r"(?m)^Location:\s+(.+)$")
    )


def _first_match(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _has_term(text: str, term: str) -> bool:
    if len(term) <= 4 or " " in term:
        return re.search(rf"\b{re.escape(term)}\b", text) is not None
    return term in text


def _load_profile(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def self_check() -> None:
    profile = {
        "target_roles": ["data analyst", "machine learning engineer"],
        "target_markets": ["netherlands", "remote eu"],
        "skills": ["python", "sql", "postgresql", "kubernetes"],
        "languages": ["English"],
        "seniority": ["junior", "entry"],
        "blocked_contracts": ["contractor", "freelance"],
    }
    dutch_job = normalize_job(
        {
            "title": "Junior Data Analyst",
            "company": "Example",
            "location": "Amsterdam, Netherlands",
            "employmentType": "Full-time",
            "seniority": "Entry level",
            "description": "Fluent Dutch and English required. Python and SQL.",
            "companyUrl": "https://linkedin.com/company/example",
            "url": "https://www.linkedin.com/jobs/view/1",
        },
        profile,
    )
    remote_job = normalize_job(
        {
            "text": "# Data Analyst\n* Full Time\n* India only\nPython SQL\n",
            "url": "https://remote.example/jobs/2",
        },
        profile,
    )
    good_job = normalize_job(
        {
            "title": "Junior Machine Learning Engineer",
            "company": "Example",
            "location": "Amsterdam, Netherlands",
            "employmentType": "Full-time",
            "seniority": "Entry level",
            "description": "English. Python, PostgreSQL and Kubernetes.",
            "companyUrl": "https://linkedin.com/company/example",
            "url": "https://www.linkedin.com/jobs/view/3",
        },
        profile,
    )
    assert dutch_job["status"] == "skipped" and "requires Dutch" in dutch_job["blockers"]
    assert remote_job["status"] == "skipped" and any("india only" in b for b in remote_job["blockers"])
    assert good_job["fit"] in {"medium", "high"} and good_job["status"] == "new"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", help="JSON file with target_roles, target_markets, skills, languages, seniority, blocked_contracts")
    parser.add_argument("--check", action="store_true", help="run self-check")
    args = parser.parse_args()
    if args.check:
        self_check()
        print("ok")
        return 0
    raw = json.load(sys.stdin)
    profile = _load_profile(args.profile)
    if isinstance(raw, list):
        json.dump([normalize_job(item, profile) for item in raw], sys.stdout, indent=2)
    else:
        json.dump(normalize_job(raw, profile), sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
