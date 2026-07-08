# CV Audit to Search Setup Workflow

Use this when the user uploads a CV/resume or asks to improve a CV before searching for jobs.

## Step 0: Intake Questions

Ask concise questions before analysis unless the answers are already in the profile:
- Target roles and seniority.
- Target markets: Croatia, Netherlands, remote EU, relocation, or a priority order.
- Languages the candidate can honestly work in.
- Work authorization, visa sponsorship, relocation, tax residence, and contractor constraints.
- Salary range, contract type, and must-have or deal-breaker conditions.
- Industries, company types, or work styles to prioritize or avoid.

## Step 1: Read the CV

Read the uploaded file or the latest file in `documents/cv/`. Extract only supported facts:
- identity and contact details
- education
- experience
- skills and tools
- projects
- publications, awards, certifications
- languages
- role/title signals

If a fact is unclear, mark it as a question. Do not invent impact numbers, skills, dates, titles, or language proficiency.

## Step 2: Research Best Practices

Use WebSearch/WebFetch for current guidance each run. Check:
- ATS parseability and PDF text-layer requirements
- European CV expectations
- Croatia and Netherlands market expectations
- remote, relocation, and visa-friendly job-search positioning
- role-specific CV expectations for the target field

Use sources as guidance, not as permission to fabricate. Cite sources in the audit summary when best-practice claims materially affect a recommendation.

## Step 3: Audit the CV

Present findings before rewriting:
- strengths to preserve
- factual gaps or unclear claims
- weak bullets that need evidence, metrics, or clearer scope
- ATS/layout risks
- market-fit issues for Croatia, Netherlands, remote EU, or relocation
- missing search keywords that are truthfully supported by the CV
- questions that block a strong rewrite

Separate "can fix now from the CV" from "needs user answer." Never bury questions inside prose.

## Step 4: Generate the Improved Master CV

After the audit, write a non-destructive improved master CV:
- Use `05-cv-templates.md` and the stock moderncv/banking pattern.
- Write to `cv/main_improved.tex` unless the user explicitly asks for another file.
- Keep all claims traceable to the source CV or user answers.
- Position the profile for the chosen Croatia/Netherlands/remote/relocation strategy.
- Mention Codex by name only if the source profile supports agentic coding or AI tooling.

Compile and verify the CV using the mandatory loop in `05-cv-templates.md`: `lualatex`, exactly 2 pages, visual PDF inspection, no orphaned entries, and `pdftotext -layout` ATS check when available.

## Step 5: Update Profile and Search Inputs

After the improved CV is accepted, update the profile/search inputs with the derived facts:
- `01-candidate-profile.md` for structured candidate facts
- `04-job-evaluation.md` for strong/moderate/weak skill match areas and constraints
- `05-cv-templates.md` for reusable profile statement templates when useful
- both `.claude/skills/job-scraper/search-queries.md` and `.agents/skills/job-scraper/search-queries.md` so the two active copies stay aligned

Derive search terms from the improved CV:
- 3-8 role titles
- 3-5 distinctive skills
- domain keywords
- adjacent role titles
- target companies or company types
- Croatia/Netherlands city tiers
- remote EU, relocation, visa, language, salary, and contract filters

## Step 6: Start Scraping

Do not start live scraping until the user accepts the improved CV and search configuration. Then run the job-scraper workflow. Use `/scrape broad` or include the remote/relocation category when relocation or remote EU is part of the stated target.
