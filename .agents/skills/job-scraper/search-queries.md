# Search Queries for Job Scraper

<!-- SETUP: Customize role titles, skills, language levels, and city priorities. -->

## Search Sites

Primary reusable tool:
- **linkedin.com/jobs** - use the bundled `linkedin-search` CLI with explicit locations: `Croatia`, `Netherlands`, `Zagreb, Croatia`, `Amsterdam, Netherlands`, `Remote`

Croatia:
- **moj-posao.net** - broad Croatian job board
- **posao.hr** - broad Croatian job board
- **burzarada.hzz.hr** - Croatian Employment Service job portal
- **hr.jooble.org** - Croatian job aggregator, useful for remote/hybrid terms
- **joberty.com/IT-jobs** - IT/developer-focused jobs and company signal
- **wellfound.com/location/croatia** - startup and tech jobs in Croatia
- **jobs.workable.com/search/croatia** - company career-page aggregate
- **eures.europa.eu** - EU mobility portal; use for Croatia and cross-border roles

Netherlands:
- **werk.nl** - Dutch public employment job portal
- **nationalevacaturebank.nl** - broad Dutch job board
- **iamexpat.nl/career/jobs-netherlands** - English-language/international roles
- **welcome-to-nl.nl/jobs** - international jobs in the Netherlands
- **jobbird.nl** - broad Dutch job board
- **monsterboard.nl** - broad Dutch job board
- **indeed.nl** - broad Dutch job aggregator
- **werkzoeken.nl** - broad Dutch job board
- **nlwerkt.nl** - broad Dutch job board
- **undutchables.nl** - multilingual/international roles
- **togetherabroad.nl** - international and multilingual roles
- **englishjobsearch.nl** - English-language Netherlands jobs
- **jobinamsterdam.com** - Amsterdam-focused English/international jobs
- **nofluffjobs.com/amsterdam** - transparent tech jobs, Amsterdam/remote
- **wellfound.com/location/europe** - startup jobs; filter Netherlands/Europe

Remote, relocation, and visa-friendly:
- **relocate.me** - tech jobs and relocation/living-abroad guidance
- **landing.jobs** - European tech jobs, remote and relocation-friendly roles
- **jaabz.com** - visa sponsorship, relocation, and remote tech jobs
- **remote.com/jobs** - remote jobs with Europe-only and country filters
- **euremotejobs.com** - remote jobs dedicated to European time zones
- **remotive.com/remote-europe-jobs** - remote Europe jobs
- **remoteok.com** - broad remote job board
- **weworkremotely.com** - broad remote job board
- **workingnomads.com/jobs** - broad remote job board
- **himalayas.app/jobs** - remote jobs with country filters
- **wearedistributed.org** - verified remote jobs, often "anywhere" or region-specific
- **jobs.workable.com** - company career-page aggregate with remote/country searches

Secondary:
- Company career pages for target employers, using `site:<company-careers-domain>` searches
- Recruiter pages only when a posting clearly matches the target role and location

## LinkedIn CLI Quick Searches

```bash
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "[YOUR_PRIMARY_JOB_TITLE]" -l "Croatia" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "[YOUR_PRIMARY_JOB_TITLE]" -l "Netherlands" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "[YOUR_KEY_SKILL]" -l "Zagreb, Croatia" --jobage 14 --remote hybrid --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "[YOUR_KEY_SKILL]" -l "Amsterdam, Netherlands" --jobage 14 --remote hybrid --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "[YOUR_PRIMARY_JOB_TITLE]" -l "Remote" --jobage 14 --remote remote --format table
```

## Query Categories

Queries are grouped by priority. Replace placeholders after `/setup --section search`.

### Priority 1: [YOUR_PRIMARY_ROLE_TYPE] in Croatia and the Netherlands

These match the strongest and most desired career direction.

```
site:linkedin.com/jobs "[YOUR_PRIMARY_JOB_TITLE]" Croatia
site:linkedin.com/jobs "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:moj-posao.net "[YOUR_PRIMARY_JOB_TITLE]" Zagreb
site:posao.hr "[YOUR_PRIMARY_JOB_TITLE]" Croatia
site:burzarada.hzz.hr "[YOUR_PRIMARY_JOB_TITLE]"
site:hr.jooble.org "[YOUR_PRIMARY_JOB_TITLE]" Croatia
site:joberty.com/IT-jobs "[YOUR_PRIMARY_JOB_TITLE]" Croatia
site:wellfound.com/location/croatia "[YOUR_PRIMARY_JOB_TITLE]"
site:jobs.workable.com/search/croatia "[YOUR_PRIMARY_JOB_TITLE]"
site:werk.nl/nl/vacatures "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:nationalevacaturebank.nl/vacatures "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:iamexpat.nl/career/jobs-netherlands "[YOUR_PRIMARY_JOB_TITLE]"
site:welcome-to-nl.nl/jobs "[YOUR_PRIMARY_JOB_TITLE]"
site:jobbird.nl "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:monsterboard.nl "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:indeed.nl "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:werkzoeken.nl "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:nlwerkt.nl "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
```

### Priority 2: [YOUR_DOMAIN_EXPERTISE]

These match domain expertise and distinctive skills.

```
site:linkedin.com/jobs [YOUR_DOMAIN_KEYWORD_1] Croatia
site:linkedin.com/jobs [YOUR_DOMAIN_KEYWORD_1] Netherlands
site:moj-posao.net [YOUR_DOMAIN_KEYWORD_1] [YOUR_KEY_SKILL]
site:posao.hr [YOUR_DOMAIN_KEYWORD_2] [YOUR_KEY_SKILL]
site:hr.jooble.org [YOUR_DOMAIN_KEYWORD_1] [YOUR_KEY_SKILL] Croatia
site:joberty.com/IT-jobs [YOUR_DOMAIN_KEYWORD_1] [YOUR_KEY_SKILL]
site:nationalevacaturebank.nl/vacatures [YOUR_DOMAIN_KEYWORD_1] [YOUR_KEY_SKILL]
site:iamexpat.nl/career/jobs-netherlands [YOUR_DOMAIN_KEYWORD_2]
site:nofluffjobs.com/amsterdam [YOUR_DOMAIN_KEYWORD_1] [YOUR_KEY_SKILL]
site:wellfound.com/location/europe [YOUR_DOMAIN_KEYWORD_1] Netherlands
```

### Priority 3: [YOUR_ADJACENT_ROLE_TYPE]

Adjacent roles worth considering if the core market is thin.

```
site:linkedin.com/jobs "[YOUR_ADJACENT_TITLE_1]" [YOUR_KEY_SKILL] Croatia
site:linkedin.com/jobs "[YOUR_ADJACENT_TITLE_1]" [YOUR_KEY_SKILL] Netherlands
site:moj-posao.net "[YOUR_ADJACENT_TITLE_2]" [YOUR_KEY_SKILL]
site:jobs.workable.com/search/croatia "[YOUR_ADJACENT_TITLE_2]" [YOUR_KEY_SKILL]
site:nationalevacaturebank.nl/vacatures "[YOUR_ADJACENT_TITLE_2]" [YOUR_KEY_SKILL]
site:undutchables.nl "[YOUR_ADJACENT_TITLE_2]" [YOUR_KEY_SKILL]
site:togetherabroad.nl "[YOUR_ADJACENT_TITLE_2]" [YOUR_KEY_SKILL]
```

### Priority 4: English-Friendly, Remote, and Hybrid Roles

Use this when language requirements or relocation are the main constraint.

```
site:linkedin.com/jobs "[YOUR_PRIMARY_JOB_TITLE]" "English" Croatia
site:linkedin.com/jobs "[YOUR_PRIMARY_JOB_TITLE]" "English" Netherlands
site:iamexpat.nl/career/jobs-netherlands "[YOUR_KEY_SKILL]"
site:englishjobsearch.nl "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:jobinamsterdam.com "[YOUR_PRIMARY_JOB_TITLE]" [YOUR_KEY_SKILL]
site:moj-posao.net "[YOUR_KEY_SKILL]" "remote"
site:hr.jooble.org "[YOUR_KEY_SKILL]" "remote" Croatia
site:nationalevacaturebank.nl/vacatures "[YOUR_KEY_SKILL]" "hybrid"
site:jobs.workable.com/search/croatia "remote" "[YOUR_PRIMARY_JOB_TITLE]"
site:jobs.workable.com "remote" "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
```

### Priority 5: Remote EU, Relocation, and Visa-Friendly

These sources are noisier, so fetch fewer results and verify country eligibility before ranking.

```
site:relocate.me "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:relocate.me "[YOUR_PRIMARY_JOB_TITLE]" "relocation"
site:landing.jobs "[YOUR_PRIMARY_JOB_TITLE]" "remote"
site:landing.jobs "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:jaabz.com "[YOUR_PRIMARY_JOB_TITLE]" "visa sponsorship"
site:jaabz.com "[YOUR_PRIMARY_JOB_TITLE]" "relocation"
site:remote.com/jobs "[YOUR_PRIMARY_JOB_TITLE]" "Europe only"
site:remote.com/jobs "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:euremotejobs.com "[YOUR_PRIMARY_JOB_TITLE]"
site:remotive.com/remote-europe-jobs "[YOUR_PRIMARY_JOB_TITLE]"
site:remoteok.com "[YOUR_PRIMARY_JOB_TITLE]" Europe
site:weworkremotely.com "[YOUR_PRIMARY_JOB_TITLE]" Europe
site:workingnomads.com/jobs "[YOUR_PRIMARY_JOB_TITLE]" Europe
site:himalayas.app/jobs "[YOUR_PRIMARY_JOB_TITLE]" Croatia
site:himalayas.app/jobs "[YOUR_PRIMARY_JOB_TITLE]" Netherlands
site:wearedistributed.org "[YOUR_PRIMARY_JOB_TITLE]" "Remote Europe"
```

### Priority 6: Target Companies

Add concrete company career sites during setup.

```
site:[TARGET_COMPANY_CAREERS_DOMAIN] "[YOUR_PRIMARY_JOB_TITLE]"
site:[TARGET_COMPANY_CAREERS_DOMAIN] "[YOUR_KEY_SKILL]"
site:[TARGET_COMPANY_CAREERS_DOMAIN] remote
site:[TARGET_COMPANY_CAREERS_DOMAIN] hybrid
site:[TARGET_COMPANY_CAREERS_DOMAIN] visa
site:[TARGET_COMPANY_CAREERS_DOMAIN] relocation
site:[TARGET_COMPANY_CAREERS_DOMAIN] sponsorship
```

## Location, Language, and Logistics Filter

Default market tiers:
- Croatia ideal: [CROATIA_IDEAL_CITIES], remote Croatia, or hybrid roles with realistic travel.
- Croatia acceptable: [CROATIA_ACCEPTABLE_CITIES] if the role is strong enough.
- Netherlands ideal: [NETHERLANDS_IDEAL_CITIES], remote Netherlands, or hybrid roles near good transit.
- Netherlands acceptable: [NETHERLANDS_ACCEPTABLE_REGIONS] if relocation or commute is realistic.
- Remote EU: PASS when contract, tax, and work-authorization setup are explicit enough to evaluate.
- Relocation to the Netherlands or Croatia: FLAG until visa/work permit, relocation support, salary range, and start-location expectations are explicit.

Flag before recommending:
- Dutch-only or Croatian-only requirements that exceed the candidate's language profile.
- Work authorization, visa sponsorship, or residence requirements.
- Relocation requirements. In this two-country search, relocation is a FLAG unless the candidate profile says it is a hard no.
- Salary period and currency. Record exactly what the posting says; do not normalize without a source.
- Contract type: employee, contractor, agency, fixed-term, internship, or freelance.
- Remote-country eligibility. "Remote" is not enough; verify Croatia, Netherlands, EU, EEA, Europe, or worldwide eligibility.

## Date Filter

Only include jobs posted within the last 14 days, or with an application deadline that has not yet passed. If a posting date cannot be determined, include it but flag as "date unknown".

## Adapting Queries

If the user specifies a focus area, select queries from the matching category and generate 2-3 custom queries for that focus. For example:
- "/scrape [focus_area]" -> relevant category queries + custom focus-specific queries
