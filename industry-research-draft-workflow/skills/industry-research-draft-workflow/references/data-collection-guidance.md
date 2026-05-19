# Data Collection Guidance

Use this when a research draft needs source data or evidence. This skill guides collection order and evidence recording; it does not implement dedicated crawlers, platform logins, API clients, rankings adapters, or WeChat collection systems.

## Source Priority

### 1. Project-Local Materials And History

Check these before going online:

- current project package `01_材料收集` or `01_材料`
- existing draft workbooks
- existing PPT/text drafts
- prior screenshots
- `材料清单`
- `采集记录`
- `数据源清单`
- `output/spreadsheet/`
- local CSV/JSON/SQLite/cache files
- historical workbook, cached HTML, terminal exports

### 2. Official Entity Sources

Prefer official sources when they exist:

- company website
- investor relations page
- official news release
- product or developer documentation
- annual report / quarterly report / prospectus / announcement
- exchange or legal disclosure platform
- official WeChat public account or official social media account

### 3. Platform And First-Party Data Sources

Use for structured or benchmark-like data:

- official rankings or leaderboard pages
- benchmark websites
- official APIs
- downloadable CSV/JSON files
- embedded page JSON or script payload
- financial terminal exports and terminal screenshots
- government, regulator, or industry association databases

### 4. Trusted Secondary Sources

Use when official sources are unavailable, incomplete, or used for estimates:

- broker research
- industry reports
- consulting reports
- traceable media reports
- third-party data service pages
- analyst estimates

### 5. Pending Verification Sources

Put these in `待核验` unless confirmed:

- unclear third-party estimates
- screenshots without source identity
- inaccessible dynamic pages
- blocked/paywalled/anti-bot pages
- data without date
- values conflicting with official disclosure

## Source-Specific Rules

### Company Website

Collect:

- page title
- URL
- access date
- supporting screenshot
- downloaded file name when applicable
- publication date and page number for PDFs

Prefer IR, news, product, documentation, and downloads pages over generic homepage text.

### WeChat Public Account

Collect:

- account name
- article title
- publication time
- original link or exported file path
- screenshot showing the supporting claim
- collection service and crawl time if using RSS/WeWe RSS or another intermediary

Limitations:

- If login, anti-bot, or screenshot-only access blocks verification, record this in `待核验`.
- Do not treat unidentified screenshots as strong evidence.

### Company Announcements

Collect:

- announcement title
- announcement date
- disclosure platform
- security code or entity name
- URL or local PDF/HTML path
- page number
- screenshot of the supporting table/paragraph

Prefer legal disclosure platforms and company IR copies over reposted PDFs.

### Financial Terminal Exports

Collect:

- terminal/source name
- exported workbook path
- screenshot path when relevant
- indicator name and口径
- period range
- export time
- manual adjustment notes

Terminal exports are evidence only when the file/screenshot and口径 are traceable.

### Rankings / Leaderboard Data

Rankings are one source type under this general data-collection guidance. Do not implement rankings adapters here.

First check:

- `ranking-skill/`
- `openrouter-rankings/`
- `llm-stats-rankings/`
- `artificialanalysis-rankings/`
- historical workbook/CSV/SQLite snapshot/cached HTML

Then check:

- official rankings page
- embedded JSON/script payload
- official API
- official CSV/JSON export
- cached HTML or raw response

Record:

- ranking name
- metric口径
- entity name
- rank/value
- data date
- URL or local file
- access/crawl time
- source type
- screenshot/cache/export path
- unresolved notes

If a rankings source needs long-term maintenance, hand it off to the rankings project or a dedicated skill.

## Bottom-Up Evidence Recording

For each collected item, record enough metadata to recreate the evidence:

- source type
- source name
- URL or local file path
- publication date
- access/capture time
- page number or page position
- screenshot path
- claim/data supported
- uncertainty or limitation

Write structured facts to `数据总表` or topic sheets. Write supporting evidence to `证据底稿`. Write unresolved issues to `待核验`.

