# Workbook Contract

This is the shared research draft workbook contract. Use it across template conversion, new draft generation, existing draft updates, and complex scenario handoffs.

## Default Workbook Structure

Use the smallest structure that supports review:

- `数据总表`: structured facts, metrics, classifications, source links, notes, confidence, and口径.
- topic sheets: optional subject-specific sheets such as `公司官网`, `公告`, `微信公众号`, `榜单数据`, `财务数据`, `AI应用`.
- `证据底稿`: evidence review sheet pairing each claim/data point with source evidence.
- `待核验`: unresolved issues, missing sources, inaccessible pages, conflicting口径, estimates, and follow-up checks.
- `说明`: optional workflow notes, data cutoff date, scope, and validation summary.

For existing workbooks, do not force this structure if the workbook already has a review layout. Preserve the existing workbook unless the user asks for a rebuild.

## Global Template Assets

Template files are required local assets because they define global formatting and font conventions:

- `assets/templates/步骤3、图表模板案例.xlsx`
- `assets/templates/1、广发研究研报模板升级说明.pdf`

Use these assets when creating templates, adapting chart styles, or checking visual consistency. Do not load their full content into context unless needed; inspect the files with spreadsheet/PDF tools or scripts.

If missing, restore them with:

```powershell
python "<skill>/scripts/ensure_draft_excel_skill_assets.py" --group templates
```

## Evidence Sheet Contract

Preferred `证据底稿` format:

| 内容 | 来源/备注 |
| --- | --- |
| Reviewable claim, number, phrase, ranking, or conclusion | Real screenshot or source file reference, with metadata in comments/notes |

Rules:

- One row should represent one reviewable claim or a tightly related claim group.
- `内容` should be clear enough for a reviewer to know what is being proven.
- `来源/备注` should prioritize real screenshots, source file references, or page-level evidence over bare links.
- Store source URL, local file path, page number, announcement date, publication date, capture time, and source type in comments, notes, or adjacent columns when useful.
- If the source evidence is a cached HTML, CSV, PDF, image, or terminal export, record the local path.

## Recommended Data Fields

For structured data sheets, include fields from this set as needed:

- `主题`
- `主体名称`
- `指标/表述`
- `数值`
- `单位`
- `口径`
- `数据时间点`
- `来源类型`
- `来源名称`
- `来源链接`
- `本地文件`
- `页码/位置`
- `截图路径`
- `抓取/访问时间`
- `置信度`
- `备注`
- `核验状态`

Do not add every field mechanically. Choose the smallest set that preserves auditability.

## Source Type Values

Prefer Chinese values in final workbooks:

- `官方披露`
- `公司官网`
- `公司公告`
- `微信公众号`
- `金融终端`
- `官方榜单`
- `第三方榜单`
- `券商研报`
- `媒体报道`
- `第三方估算`
- `人工补充`
- `历史底稿`
- `待核验`

## Screenshot Rules

Screenshots are evidence, not decoration:

- Capture the real page/report/filing/database/export/source material.
- Capture the exact area containing the supporting number, keyword, table, or sentence.
- Re-capture screenshots that only show titles, generic overviews, ads, blank pages, blocked pages, or unrelated content.
- If a page is blocked or inaccessible, use a trusted alternative source or put the item in `待核验`.
- For screenshot-heavy drafts, create a contact sheet or visual validation record.

## Existing Workbook Rule

When modifying an existing draft:

- Preserve sheet names, order, formulas, source notes, screenshots, images, comments, and review layout.
- Update only impacted cells, charts, evidence images, comments, and source text.
- Create a preview copy first when practical.
- Do not merge/delete sheets or rebuild the workbook unless explicitly requested.

## Chinese Final Delivery

Final deliverables should use Chinese:

- file name
- sheet names
- headers
- enum values
- notes and visible reviewer-facing comments
- validation records
