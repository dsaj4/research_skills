---
name: artificialanalysis-rankings-chart-refresh
description: Rebuild the Artificial Analysis Rankings workbook display page from the existing raw workbook data. Use this whenever the user asks to refresh charts, rebuild the dashboard page, or restyle workbook output without fetching new network data.
---

# Artificial Analysis Rankings Chart Refresh

Use this skill when the data layer already exists and the task is to rebuild the workbook presentation.

## Workflow

1. Read [layout-reference.md](references/layout-reference.md) if you need the layout intent.
2. Run `scripts/run_chart_refresh.py`.
3. Verify the display page exists and contains four charts.
4. If the user also wants fresh data, run `artificialanalysis-rankings-data-refresh` first.
