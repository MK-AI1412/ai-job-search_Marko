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
- Extract: **job title**, **company**, **market** (Croatia, Netherlands, Remote EU, Relocation), **location**, **workplace model**, **remote-country eligibility**, **language requirements**, **work authorization/visa notes**, **posting date** (or "recent"), **URL**, **key requirements** (brief), **application deadline** (if listed)
- Skip if the URL or company+title combo already exists in `seen_jobs.json`
- Skip if the company+role already appears in `job_search_tracker.csv`

### Step 3: Quick Fit Assessment

For each new job, do a rapid fit check (NOT the full evaluation from `04-job-evaluation.md` - just a quick signal):

- **High match**: Role directly involves your core skills
- **Medium match**: Role is adjacent to your experience
- **Low match**: Role requires significant skills you lack

Also flag language, relocation, remote-country eligibility, and work-authorization uncertainty instead of hiding it inside the fit label.

### Step 4: Deduplicate & Store

1. Add ALL fetched jobs (new and skipped) to `seen_jobs.json` with structure:
```json
{
  "seen": {
    "<url_or_company_title_key>": {
      "title": "...",
      "company": "...",
      "url": "...",
      "first_seen": "YYYY-MM-DD",
      "fit": "high/medium/low",
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
5. **Be efficient with WebFetch.** Don't fetch every search result - use titles and snippets to pre-filter before fetching.
6. **Parallel searches.** Use the Agent tool or parallel WebSearch calls to speed up the search phase.
7. **Do not assume language, visa, or remote eligibility.** If Dutch, Croatian, work authorization, relocation, remote-country eligibility, or contract setup is unclear, flag it.
