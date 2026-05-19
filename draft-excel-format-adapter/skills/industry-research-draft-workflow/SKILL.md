---
name: industry-research-draft-workflow
description: "Industry research draft workflow / 行业研究底稿工作流. Use when the user asks to build, modify, verify, or template research drafts, including 研究底稿 Excel, 底稿修改, 底稿生成, 行研数据收集, 表述核验, 材料整理成底稿, 公司官网/微信公众号/公告/rankings 数据采集底稿, 现有文件改造为底稿模板, 套用底稿模板, 图表格式适配, PPT 修改同步底稿的底稿规范, or 在原底稿中做最小更新. This skill provides draft-specific contracts, evidence rules, data collection guidance, and complex-scenario registry entries; it does not replace dedicated data-collection, rankings, or PPT-editing skills."
---

# Industry Research Draft Workflow

## Purpose

Use this skill to make industry research work reviewable and traceable through a research draft workbook. The skill focuses on draft-related contracts:

- how to turn existing files into reusable draft templates
- how to generate evidence-first research draft workbooks
- how to collect and record source evidence for company websites, WeChat public accounts, announcements, reports, rankings, and other data sources
- how to minimally update existing drafts and chart styles
- how complex scenario skills can register their draft requirements here

This skill does not implement full data crawlers, rankings adapters, PPT editing engines, or company-specific workflows. If a dedicated skill owns that full workflow, use this skill only for the draft contract and evidence requirements.

## Start Here

1. Search local files first with `rg --files`.
2. Classify the task with `references/scenario-router.md`.
3. Load only the relevant reference files.
4. Preserve original files and create preview copies when modifying existing deliverables.
5. Verify the workbook and evidence chain with `references/quality-gates.md`.

## Asset Bootstrap

If the installed skill folder looks incomplete, run:

```powershell
python "<skill>/scripts/ensure_draft_excel_skill_assets.py" --dry-run
python "<skill>/scripts/ensure_draft_excel_skill_assets.py"
```

Template and example assets are part of the expected local install because they define global formatting, font conventions, and workbook comparison examples:

```powershell
python "<skill>/scripts/ensure_draft_excel_skill_assets.py" --group templates
python "<skill>/scripts/ensure_draft_excel_skill_assets.py" --group examples
```

The default asset source is:

```text
https://raw.githubusercontent.com/dsaj4/research_skills/main/draft-excel-format-adapter/skills/industry-research-draft-workflow
```

## Scenario Router

Load `references/scenario-router.md` first when the task is ambiguous.

| Scenario | Use When | Load |
| --- | --- | --- |
| A. Existing file to draft template | User wants to turn an Excel/PPT/draft/file package into a reusable draft template or format reference. | `references/existing-file-to-template.md`, then `references/workbook-contract.md` |
| B. Research draft generation | User wants to collect data/materials, verify statements, or produce a new research evidence draft. | `references/research-draft-generation.md`, `references/data-collection-guidance.md`, `references/workbook-contract.md` |
| C. Data collection guidance | User needs source order/channel guidance for company websites, WeChat, announcements, rankings, reports, terminal exports, etc. | `references/data-collection-guidance.md` |
| D. Complex scenario registry | User mentions PPT modification sync or another complex workflow that needs draft rules but should be owned by another skill. | `references/complex-scenario-registry.md`, then scenario-specific owning skill if available |
| E. Existing draft minimal update / chart template adaptation | User asks to update an existing draft, apply chart template, or make minimal traceable changes. | `references/current-project-pattern.md`, `references/workbook-contract.md` |

## Common Draft Contract

All scenarios should converge on the same review logic:

- preserve original materials and formal deliverables
- keep source links, source files, page numbers, dates, screenshots, and comments traceable
- pair each key claim or data point with evidence
- record unclear, inaccessible, estimated, or conflicting items in `待核验`
- use Chinese workbook names, sheet names, headers, notes, and reviewer-facing text for final deliverables
- do not overwrite current/formal workbooks unless the user explicitly requests it

For workbook structure, sheet contracts, and evidence fields, load `references/workbook-contract.md`.

For visual/format reference, use:

- `assets/templates/步骤3、图表模板案例.xlsx`
- `assets/templates/1、广发研究研报模板升级说明.pdf`
- `assets/examples/research-draft-generation/通用数据收集底稿示例_ARR.xlsx`

The ARR workbook is a generic data-collection draft example. Its ARR/revenue business content is not the point; use it to compare sheet structure, evidence layout, screenshot placement, comments, and Chinese formatting.

## Verification

Run the strongest feasible checks:

```powershell
python -m py_compile "<script>.py"
python "<skill>/scripts/inspect_draft_excel_style.py" --workbook "<workbook.xlsx>"
```

Also check:

- workbook opens through `openpyxl`
- key sheets exist
- evidence screenshots or original files are traceable
- `证据底稿` pairs content and source evidence
- existing-draft modifications preserve unrelated sheets, formulas, screenshots, and notes
- no current/formal file was overwritten during validation unless requested
