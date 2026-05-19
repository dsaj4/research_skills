# Existing Draft Modification Pattern

Use this pattern when the user provides or points to an existing research draft workbook and asks to modify, update, or apply a new format.

Successful existing-draft work preserves the review surface:

- Keep the original workbook, sheet order, sheet names, formulas, screenshots, source notes, and review layout.
- Update only impacted cells, charts, evidence images, comments, or source text.
- Generate a preview copy first when practical.
- Do not rebuild the workbook into the new-draft evidence-table format unless the user explicitly asks.

For chart-heavy workbooks, keep chart styling independent from worksheet/table layout. A prior successful workflow used a project-local `template_format_adapter.py` and routed chart creation through it for:

- Chinese and Latin fonts.
- Chart palettes.
- Column, stacked-column, bar, line, combo, area, pie, and doughnut series styling.
- Title, legend, axis, gridline, marker, data label, plot area, and chart area styling.

When a generator script exists, add or preserve an `--output` argument so preview workbooks can be created safely.

