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

## Format Example Workbook

Use this required local example as the generic Excel format reference for data-collection drafts:

- `assets/examples/research-draft-generation/通用数据收集底稿示例_ARR.xlsx`
- `assets/examples/research-draft-generation/contact_sheet_validated_final.png`
- `assets/examples/research-draft-generation/截图视觉校验记录.md`

The ARR/revenue subject matter is not important. Use the workbook to compare:

- sheet order and naming
- `数据总表`, topic sheets, `证据底稿`, and `待核验` roles
- Chinese headers and enum values
- evidence sheet two-column layout
- screenshot placement, row heights, column widths, and comments
- contact sheet and visual validation record style

If the example is missing, restore it with:

```powershell
python "<skill>/scripts/ensure_draft_excel_skill_assets.py" --group examples
```

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

For ARR-like or revenue口径 data collection, load `arr-best-practice.md` for business口径 cautions:

- distinguish ARR, run-rate revenue, annualized revenue estimate, annual revenue estimate, projected run-rate, and undisclosed values
- keep official disclosures separate from media reports and third-party estimates
- use screenshots that visibly show the supporting number or phrase
- keep source URL comments even when screenshots are embedded

## What Not To Do

- Do not rely on links alone for key evidence.
- Do not mix official data and estimates without marking source type and confidence.
- Do not overwrite original materials.
- Do not invent data collection adapters inside this skill; use dedicated skills/projects when the source needs a maintained crawler.
