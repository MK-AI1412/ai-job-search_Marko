---
name: job-scraper
description: >
  Scrapes Croatia and Netherlands job sources for new positions matching your profile. Deduplicates across runs.
  Triggers on: job scrape, find jobs, search jobs, new jobs, job search, scrape jobs, /scrape
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Agent, AskUserQuestion
---

# Job Scraper

---

## How It Works

This skill searches Croatia and Netherlands job sources using targeted queries based on your profile, deduplicates against previously seen jobs and the application tracker, and presents new matches with a quick fit assessment.

## Invocation

The user triggers this skill by saying things like:
- "Find new jobs"
- "Scrape for jobs"
- "Any new positions?"
- "/scrape"

Optional arguments:
- A focus area, e.g. "/scrape data science" or "/scrape geophysics"
- "broad" to run all search categories, e.g. "/scrape broad"

---

## Execution Steps

### Step 0: Load State

1. Read `job_scraper/seen_jobs.json` (create if missing - start with `{"seen": {}}`)
2. Read `job_search_tracker.csv` to extract already-applied companies+roles
3. Read `search-queries.md` (this directory) for the search strategy

### Step 1: Search

Run **WebSearch** queries from `search-queries.md`. By default, run the top 3 priority categories. If the user said "remote", "relocation", "visa", or the search config from the CV audit targets remote EU/relocation, include the remote/relocation category too. If the user said "broad", run all categories.

If the user specified a focus area (e.g. "data science"), prioritize queries from that category.

For each search:
- Use `WebSearch` with site-specific queries from `search-queries.md` (LinkedIn, Croatia/Netherlands boards, remote boards, relocation boards, and target company career pages)
- Target Croatia, the Netherlands, or remote EU according to the configured search category
- Look for postings from the last 14 days

### Step 2: Fetch & Parse

For each promising result from Step 1:
- Use `WebFetch` to retrieve the job posting page
- Normalize every posting to the schema below. Use `tools/job_scraper_utils.py` when you have raw LinkedIn detail JSON or fetched portal text.
- Skip if the URL or company+title combo already exists in `seen_jobs.json`
- Skip if the company+role already appears in `job_search_tracker.csv`

#### Normalized Job Schema

Use these fields for every source, even when the value is `"unknown"`:

```json
{
  "title": "",
  "company": "",
  "source": "linkedin|euremotejobs|relocate.me|iamexpat|englishjobsearch|remote.com|remotive|other",
  "url": "",
  "market": "Croatia|Netherlands|Remote EU|Relocation|Other",
  "location": "",
  "workplace_model": "onsite|hybrid|remote|unknown",
  "remote_country_eligibility": "",
  "language_requirements": [],
  "work_authorization": "",
  "contract_type": "employee|temporary|internship|contractor|freelance|part-time|unknown",
  "seniority": "",
  "posting_date": "",
  "deadline": "",
  "required_skills": [],
  "nice_to_have_skills": [],
  "fit": "high|medium|low",
  "fit_score": 0,
  "status": "new|skipped|evaluated|ranked|expired",
  "flags": [],
  "blockers": []
}
```

#### Portal Parsers

- **LinkedIn**: prefer the bundled `linkedin-search` CLI `detail --format json`; pass the JSON through `normalize_job`.
- **EU Remote Jobs**: fetch the detail page, then parse title, company, location, job type, posting age, tags, and "Applications have closed" from the page text.
- **Relocate.me**: fetch the job page or category page; parse title, company, city/country, relocation/visa text, seniority words, and whether the listing is a real job or partner/paywalled aggregate.
- **IamExpat / EnglishJobSearch / Undutchables**: fetch detail pages only when the search snippet already matches title + Netherlands + language; parse required languages and current-residence requirements before scoring.
- **Other remote boards**: fetch detail pages only if the snippet says Europe, EU, EMEA, EEA, Netherlands, Croatia, or worldwide employee employment.

### Step 3: Quick Fit Assessment

For each new job, do a rapid fit check (NOT the full evaluation from `04-job-evaluation.md` - just a quick signal):

- **High match**: Role directly involves your core skills
- **Medium match**: Role is adjacent to your experience
- **Low match**: Role requires significant skills you lack

Score the normalized job before presenting it:
- Role/title match to target roles: up to 30 points
- Market/logistics match: up to 20 points
- Supported skills match: up to 25 points
- Seniority fit: up to 15 points
- Fresh/open posting: up to 10 points

Hard blockers set `status: "skipped"` unless the user explicitly asks to review them:
- Contractor/freelance-only when the profile requires employee roles
- Required language not in the candidate profile
- Remote role that is not eligible for the configured country/region
- Current-residence requirement the candidate does not meet
- Expired/closed listing

Fit labels: high = 70+ and no blockers, medium = 45-69 and no hard blockers, low = everything else. Always flag language, relocation, remote-country eligibility, and work-authorization uncertainty instead of hiding it inside the fit label.

### Step 4: Deduplicate & Store

1. Add ALL fetched jobs (new and skipped) to `seen_jobs.json` with structure:
```json
{
  "seen": {
    "<url_or_company_title_key>": {
      "title": "...",
      "company": "...",
      "source": "...",
      "url": "...",
      "market": "...",
      "location": "...",
      "first_seen": "YYYY-MM-DD",
      "fit": "high/medium/low",
      "fit_score": 0,
      "status": "new/skipped/evaluated/ranked/expired"
    }
  }
}
```
2. Only present jobs NOT already in the seen list or tracker.

### Step 5: Present Results

Present new jobs in a table sorted by fit (high first):

```
## New Job Matches - YYYY-MM-DD

Found X new positions (Y high, Z medium, W low match).

| # | Fit | Market | Title | Company | Location | Language/Logistics | Deadline | URL |
|---|-----|--------|-------|---------|----------|--------------------|----------|-----|
| 1 | High | Croatia | ... | ... | Zagreb / hybrid | English OK, visa unclear | ... | [Link](...) |

### High-Match Highlights
For each high-match job, add 2-3 bullet points:
- Why it matches your profile
- Key requirements to check
- Any red flags
```

After presenting, ask:
> "Want me to evaluate any of these in detail? Just give me the number(s)."

If the user picks a number, invoke the **job-application-assistant** skill workflow (fit evaluation first, then CV + cover letter if approved).

If the run found many new jobs (roughly 8+), also suggest `/rank` - it batch-scores all new postings against the full fit framework and returns a ranked shortlist, which beats eyeballing a long table. (`/rank` sets the `ranked` and `expired` status values in `seen_jobs.json`; treat both as already-seen for dedup purposes.)

### Step 6: Update Tracker (Optional)

If the user decides to apply to any job, add a row to `job_search_tracker.csv`.

---

## Important Rules

1. **Never fabricate job postings.** Only present jobs found via actual WebSearch/WebFetch results.
2. **Respect deduplication.** Always check seen_jobs.json AND job_search_tracker.csv before presenting.
3. **Focus on configured target markets.** Keep Croatia, Netherlands, and remote EU roles; skip other countries unless explicitly requested.
4. **Only open positions.** Skip postings with expired deadlines or those marked as closed.
5. **Remote filtering is strict.** Do not present a generic "Remote" role unless the posting explicitly allows the configured country/region (for example EU, EEA, EMEA, Europe, Croatia, Netherlands, or worldwide employee employment). Generic LinkedIn `Remote` searches are noisy; prefer remote-specific boards plus region terms.
6. **Be efficient with WebFetch.** Don't fetch every search result - use titles and snippets to pre-filter before fetching.
7. **Parallel searches.** Use the Agent tool or parallel WebSearch calls to speed up the search phase.
8. **Do not assume language, visa, or remote eligibility.** If Dutch, Croatian, work authorization, relocation, remote-country eligibility, or contract setup is unclear, flag it.
