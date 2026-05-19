# Research Draft Generation

Use this when creating a new research draft workbook from collected data, statements, web pages, reports, announcements, screenshots, or other materials.

## Workflow

1. Define the research question, review audience, data cutoff date, and deliverable scope.
2. Load `data-collection-guidance.md` to plan source order and evidence requirements.
3. Collect or inventory source materials.
4. Structure facts into `数据总表` and topic sheets.
5. Pair every key claim, metric, ranking, or statement with source evidence in `证据底稿`.
6. Put unclear, inaccessible, estimated, or conflicting items into `待核验`.
7. Localize final workbook names, sheet names, headers, source type values, and reviewer notes into Chinese.
8. Run quality checks from `quality-gates.md`.

## Recommended Workbook

```text
数据总表
主题分表（可选）
证据底稿
待核验
说明（可选）
```

Use topic sheets only when they improve reviewability. Examples:

- `公司官网`
- `公司公告`
- `微信公众号`
- `榜单数据`
- `财务数据`
- `产品数据`
- `AI应用`

## Evidence Draft Pattern

Use `workbook-contract.md` for the exact evidence contract. In short:

- `内容`: the claim, number, statement, ranking, or conclusion being reviewed.
- `来源/备注`: screenshot, source file, URL, page number, publication date, access time, and comments.

## Handling Uncertainty

Use `待核验` for:

- missing original source
- source blocked by login, anti-bot, paywall, or dynamic rendering
- screenshots that do not visibly support the claim
- conflicting values across sources
- estimates mixed with official disclosures
- unclear metric口径
- stale or missing date

## ARR Case Pattern

For ARR-like or revenue口径 data collection, load `arr-best-practice.md` as a concrete example:

- distinguish ARR, run-rate revenue, annualized revenue estimate, annual revenue estimate, projected run-rate, and undisclosed values
- keep official disclosures separate from media reports and third-party estimates
- use screenshots that visibly show the supporting number or phrase
- keep source URL comments even when screenshots are embedded

## What Not To Do

- Do not rely on links alone for key evidence.
- Do not mix official data and estimates without marking source type and confidence.
- Do not overwrite original materials.
- Do not invent data collection adapters inside this skill; use dedicated skills/projects when the source needs a maintained crawler.

