---
name: llm-stats-chart-refresh
description: Rebuild the llm-stats workbook display page from the existing raw workbook data. Use this whenever the user asks to refresh charts, rebuild the dashboard page, or restyle the Excel output without fetching new network data.
---

# LLM Stats Chart Refresh

Use this skill when the data layer already exists and the task is to rebuild the workbook presentation.

## What this skill does

- Reads the existing workbook raw model sheet
- Rebuilds the dashboard display page
- Refreshes the four native Excel charts
- Keeps the workbook as the single front-facing output
- Does not fetch new homepage data

## When to use

Use this skill whenever the user mentions any of:

- refresh llm-stats charts
- rebuild display page
- restyle workbook charts
- refresh dashboard without recrawling data

## Workflow

1. Read [layout-reference.md](references/layout-reference.md) if you need the layout intent.
2. Run `scripts/run_chart_refresh.py`.
3. Verify the display page exists and contains four charts.
4. If the user also wants fresh data, run `llm-stats-data-refresh` first.
