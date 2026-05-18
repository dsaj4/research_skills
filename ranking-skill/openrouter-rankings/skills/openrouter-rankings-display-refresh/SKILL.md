---
name: openrouter-rankings-display-refresh
description: Rebuild the OpenRouter rankings dashboard display page from the existing workbook data layer. Use this whenever the user asks to redesign the workbook display, restyle charts, rebuild the display page, or apply the example-charts.xlsx layout without fetching new network data.
---

# OpenRouter Rankings Display Refresh

Use this skill when the data layer is already present and the task is to rebuild the dashboard presentation.

## What this skill does

- Reads the existing workbook data layer
- Rebuilds the workbook display page
- Refreshes chart layout, chart anchors, and summary tables
- Keeps the workbook as a single front-facing output
- Does not fetch new rankings data

## When to use

Use this skill whenever the user mentions any of:

- rebuild display page
- restyle workbook
- adjust dashboard layout
- reference `example-charts.xlsx`
- refresh charts without recrawling data

## Workflow

1. Read [layout-reference.md](references/layout-reference.md) if you need the layout intent.
2. Run `scripts/run_display_refresh.py`.
3. Verify the display page exists and contains the four dashboard charts.
4. If the user also wants new data, run `openrouter-rankings-data-refresh` first.
