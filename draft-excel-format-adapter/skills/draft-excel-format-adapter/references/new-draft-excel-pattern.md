# New Draft Excel Pattern

Use this pattern when generating a new research draft from collected data, materials, web pages, reports, filings, databases, news, or screenshots.

The current best practice is the ARR data collection example. A new draft should be reviewable and traceable:

- `数据总表` or equivalent: structured facts, metrics, classifications,口径, source links, notes.
- Topic sheets when useful, such as `大模型公司` and `AI应用` in the ARR example.
- `证据底稿`: a two-column evidence sheet.
- `待核验`: unresolved issues, unclear口径, inaccessible sources, or follow-up checks.

## Evidence Sheet

Prefer this two-column structure:

| 内容 | 来源/备注 |
|---|---|
| The statement, number, or conclusion to review | Real source screenshot, with source metadata in comments/notes when useful |

Rules:

- Put the exact claim or data point in `内容`.
- Put a real screenshot in `来源/备注`; do not rely on links alone.
- Keep source URL, file name, page number, and date in comments, notes, or adjacent metadata.
- Ensure every screenshot visibly supports its paired content.
- Use one row per reviewable claim when possible.

## Screenshots

Screenshots are audit evidence, not decoration:

- Capture the real page/report/filing/database/source material.
- Capture the page area containing the supporting keyword, number, or phrase.
- If the first screen does not contain support, scroll or search within the page and recapture.
- If a page is blocked by anti-bot, paywall, blank content, or ads, use a trusted alternative source or document the limitation.
- For important drafts, create a contact sheet or equivalent visual summary and record validation results.

## Chinese Deliverable

Final deliverables should use Chinese names and Chinese-facing text:

- workbook name
- key sheet names
- headers
- enum values
- notes and validation records

Development scripts and temporary files may use English names for easier debugging.

