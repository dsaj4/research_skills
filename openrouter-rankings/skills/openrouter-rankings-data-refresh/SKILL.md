---
name: openrouter-rankings-data-refresh
description: Refresh OpenRouter rankings data into the repo workbook data layer. Use this whenever the user asks to re-crawl OpenRouter rankings, update cached HTML, refresh CSV outputs, or update raw/helper workbook sheets without redesigning the display page.
---

# OpenRouter Rankings Data Refresh

Use this skill when the task is about data refresh, not dashboard redesign.

## What this skill does

- Reuse the existing OpenRouter crawl and HTML cache fallback
- Refresh `openrouter_top_models.csv`
- Refresh `openrouter_top_models_timeseries.csv`
- Refresh workbook data-layer sheets: `Meta`, `Raw_TimeSeries`, `Raw_Leaderboard`, `Data_*`
- Merge new data into existing weekly history instead of overwriting prior raw runs
- Preserve the current display page layout if it already exists

## When to use

Use this skill whenever the user mentions any of:

- refresh rankings data
- recrawl OpenRouter
- update raw data
- refresh cached HTML
- update CSVs
- update workbook data layer only

## Workflow

1. Read [workflow.md](references/workflow.md) if you need the exact inputs and outputs.
2. Run `scripts/run_data_refresh.py`.
3. Report the output workbook and CSV paths.
4. If the user also wants a visual redesign, hand off to `openrouter-rankings-display-refresh`.
