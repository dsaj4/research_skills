---
name: draft-excel-format-adapter
description: "Convert, generate, or minimally update research draft Excel workbooks / 研究底稿 Excel / 底稿修改 / 底稿生成. Use when the user asks to 套用底稿模板, 图表格式适配, 统一底稿图表格式, 新建底稿, 修改已有底稿, 在原底稿中做最小更新, 将数据收集写成底稿, 将材料整理成底稿, ARR 数据底稿, or ARR 数据收集写成底稿. For new draft creation, follow the current ARR-style best practice: structured data sheets, two-column 证据底稿, real evidence screenshots, visual validation, and Chinese final delivery. For existing draft modification, preserve the current workbook and make minimal updates. Chart template adaptation remains independent from table/page layout."
---

# Draft Excel Format Adapter

## Goal

Create or update research draft Excel workbooks so they are:

1. **Readable**: clear structure, review-friendly grouping, and Chinese-facing delivery text.
2. **Traceable**: key claims have source links, real screenshots, and notes/comments that let reviewers verify the original material.
3. **Minimally disruptive when modifying**: existing draft structure is preserved unless the user explicitly asks for a rebuild.
4. **Template-consistent for charts**: chart styling can be adapted to a provided template without tying chart formatting to sheet layout.

Use with the general `spreadsheet` skill for `.xlsx` work. Inspect `.docx`, `.pdf`, or source screenshots only as needed.

## Inputs To Find

Before asking the user, search the project with `rg --files` for:

- current draft workbook: often under `底稿修改/01_当前底稿`, project package folders, or `output/spreadsheet`
- source screenshots: often under `底稿修改/03_来源截图整理`
- generation scripts: often under `底稿修改/02_生成脚本`
- current workflow docs: `README_底稿修改说明.md`, `底稿创作规范与流程.md`, `范例说明_*.md`
- chart template workbook: often under `底稿修改/底稿模板`, named like `图表模板`, `模板案例`, or `chart template`
- evidence assets: report crops, web screenshots, PPT renders, PDF crops/text, terminal exports, downloaded source files

If there are multiple candidates, choose the newest or most complete one and state the assumption.

## Asset Bootstrap

This skill can be installed as a packaged `.skill` archive. The package includes a manifest and a bootstrap script that detects missing local assets and restores them from the current GitHub repository:

```powershell
python "<skill>/scripts/ensure_draft_excel_skill_assets.py"
```

Run it when:

- the skill folder was hand-copied or partially installed
- a referenced file under `references/`, `scripts/`, or `agents/` is missing
- you are about to use optional reference material and want to confirm the local package is complete

The default source is:

```text
https://raw.githubusercontent.com/dsaj4/research_skills/main/draft-excel-format-adapter/skills/draft-excel-format-adapter
```

Use `--dry-run` to check without downloading. Use `--raw-base-url` when testing a branch or fork.

## Scenario Decision

Choose one primary scenario before editing.

### Scenario A: New Draft Generation

Use this when the user asks to create/build/generate a new draft, when the task is "将数据收集写成底稿" or "将材料整理成底稿", or when no usable existing draft workbook exists.

Current best practice is the ARR data collection workflow:

- create a structured Excel workbook
- include a two-column `证据底稿`
- embed real screenshots as audit evidence
- keep source URLs/files/pages/dates traceable in comments, notes, or metadata columns
- visually validate screenshots before final delivery
- localize the final workbook into Chinese

Read `references/new-draft-excel-pattern.md` and, for ARR-like data collection, `references/arr-best-practice.md`.

### Scenario B: Modify Existing Draft

Use this when a current draft workbook exists and the user asks to update, modify, 套用新格式, or make a 最小更新.

Minimal update beats redesign:

- keep workbook, sheet order, sheet names, formulas, data tables, source notes, screenshots, and review layout
- update only impacted cells, charts, evidence images, comments, or source text
- when the request is "apply new chart/template format", run the chart adapter on charts only
- do not rebuild the workbook into the new-draft evidence format unless explicitly requested
- create a preview copy first when practical

Read `references/current-project-pattern.md`.

### Scenario C: Chart Template Adaptation

Use this when the user asks to adapt chart style, apply a chart template, or standardize chart formatting.

This scenario can combine with A or B, but chart formatting must stay independent from table/page layout.

## New Draft Generation Workflow

For data/material collection drafts, build the workbook around review and traceability:

1. Define the draft purpose and review audience.
2. Collect source materials, data, links, files, and screenshots.
3. Generate structured sheets for the data/materials.
4. Generate `证据底稿` with two columns: `内容` and `来源/备注`.
5. Put each reviewable claim, number, or conclusion in `内容`.
6. Embed the real source screenshot in `来源/备注`.
7. Store source URL/file/page/date in comments, notes, or adjacent metadata.
8. Add `待核验` for unclear口径, missing sources, inaccessible pages, or follow-up checks.
9. Create a contact sheet or equivalent visual validation artifact for important screenshot-heavy drafts.
10. Replace screenshots that do not show the supporting data/text.
11. Localize final sheet names, headers, enum values, notes, and file name into Chinese.

Recommended workbook structure:

- `数据总表`: all structured entries.
- topic sheets: project-specific breakdowns, e.g. `大模型公司`, `AI应用`, `分产品`, `分地区`.
- `证据底稿`: two-column evidence review sheet.
- `待核验`: unresolved or lower-confidence items.

For chart/model drafts, add the necessary calculation, assumptions, chart, or output sheets, but keep evidence clear and reviewable.

## Evidence Screenshot Rules

Screenshots are evidence, not decoration.

Each screenshot must:

- show the real webpage, report, filing, database page, or original material
- visibly contain the number, keyword, sentence, or table that supports the paired claim
- be recaptured if it only shows a title, overview, blocked page, ad, blank page, or unrelated area
- be replaced with a credible alternative source if the original page is inaccessible or unsupported

For important drafts:

- create `contact_sheet.png` or `contact_sheet_validated_final.png`
- record visual validation results in a Markdown file
- note replacements, inaccessible sources, and confidence limitations

## Chinese Final Delivery

Final deliverables should use Chinese:

- workbook filename
- main sheet names
- headers
- enum values
- notes/comments visible to reviewers
- validation records and README-style workflow notes

Development scripts, temporary paths, and intermediate artifacts may use English names.

## Chart Format Adapter

This part is independent of the draft table layout. Its only job is to make every chart in the workbook match the template workbook.

### Inspect The Template

Use `scripts/inspect_draft_excel_style.py` on the template workbook. Record:

- chart families present: column, stacked column, bar, line, combo column-line, area, pie, doughnut
- chart XML colors and style variants
- fonts for Chinese and Latin text
- title, legend, axis, gridline, marker, data label, plot area, and chart area conventions
- whether secondary axes are used for YoY/percentage lines

Common template colors in prior projects include:

```text
#2E3160, #7C80C8, #B8BFE4, #D9D9D9, #387099, #6A9BFF, #76CEF3, #AEDCFF
```

### Apply To All Chart Types

Implement a project-local chart adapter. Do not tie it to row/column positions or sheet layout.

The adapter should expose functions like:

- `style_chart(chart, chart_kind, title, y_axis_name=None, y2_axis_name=None)`
- `column_series(idx)`
- `stacked_column_series(idx)`
- `bar_series(idx)`
- `line_series(idx)`
- `area_series(idx)`
- `pie_point(idx)` / doughnut point colors

When adapting an existing generation script:

- Replace local color arrays with adapter palette methods.
- Route all chart constructors through one styling function.
- Preserve chart data ranges, formulas, sheet names, and source notes.
- Add support for every chart type found in the template, even if the current project uses only a subset.
- Keep chart formatting separate from worksheet/table formatting.

When modifying an existing workbook without a generator:

- Prefer `openpyxl` for non-destructive workbook edits.
- If editable chart XML changes are too limited through `openpyxl`, unzip the `.xlsx`, patch chart XML style/colors carefully, and rezip a preview copy.
- Do not change cell layout unless required for chart data integrity.

## Implementation Pattern

Prefer project-local scripts and adapters over shared global code.

For new drafts, a repeatable script sequence often looks like:

```powershell
python "底稿修改\02_生成脚本\generate_<topic>_excel_draft.py"
python "底稿修改\02_生成脚本\embed_evidence_screenshots.py"
python "底稿修改\02_生成脚本\reformat_<topic>_excel_evidence.py"
python "底稿修改\02_生成脚本\localize_<topic>_excel_fields.py"
```

For chart adaptation, a project-local adapter can follow this shape:

```python
class DraftChartTemplateAdapter:
    chart_palette = ["#2E3160", "#7C80C8", "#B8BFE4", "#D9D9D9"]
    line_palette = ["#2E3160", "#7C80C8", "#387099", "#6A9BFF"]

    def column_series(self, idx):
        color = self.chart_palette[idx % len(self.chart_palette)]
        return {"fill": {"color": color}, "border": {"color": color}}

    def line_series(self, idx):
        color = self.line_palette[idx % len(self.line_palette)]
        return {
            "line": {"color": color, "width": 1.75},
            "marker": {"type": "circle", "size": 4, "border": {"color": color}, "fill": {"color": color}},
        }

    def style_chart(self, chart, chart_kind, title, y_axis_name=None, y2_axis_name=None):
        chart.set_title({...})
        chart.set_legend({...})
        chart.set_x_axis({...})
        chart.set_y_axis({...})
        if y2_axis_name:
            chart.set_y2_axis({...})
```

## Verification

Run the strongest feasible checks:

```powershell
python -m py_compile "<generator>.py" "<adapter>.py"
python "<generator>.py" --output "<preview.xlsx>"
python "<skill>/scripts/inspect_draft_excel_style.py" --workbook "<preview.xlsx>"
```

For new draft generation, confirm:

- Excel can be opened/read by `openpyxl`.
- key sheets exist and match the task purpose.
- `证据底稿` uses `内容` / `来源/备注` two-column structure when evidence review is needed.
- content statements and screenshots are paired correctly.
- every screenshot visibly supports its paired content, or limitations are recorded.
- source URLs/files/pages/dates are traceable.
- final workbook name, sheet names, headers, enums, and reviewer-facing notes are Chinese.

For existing draft modification, confirm:

- sheet order and existing review structure are preserved.
- formulas, source notes, and screenshots outside the impacted area were not rebuilt.
- no formal/current draft was overwritten during validation unless requested.

For chart adaptation, confirm:

- chart XML includes template palette colors.
- every expected chart type was handled or explicitly deemed absent from the current workbook.
- chart formatting changes did not alter worksheet/table layout unnecessarily.
