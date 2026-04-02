---
name: llm-stats-data-refresh
description: Refresh llm-stats homepage leaderboard data into the repo workbook data layer. Use this whenever the user asks to recrawl llm-stats, refresh cached homepage HTML, update raw CSV outputs, or rebuild workbook raw/helper sheets without redesigning the display page.
---

# LLM Stats Data Refresh

Use this skill when the task is about data refresh, not chart layout changes.

## What this skill does

- Fetches the `llm-stats.com` homepage HTML
- Extracts the embedded `initialHomepageLLMModels` payload
- Refreshes cache HTML and normalized JSON
- Refreshes `llm_stats_homepage_models.csv`
- Refreshes `llm_stats_top20.csv`
- Rebuilds workbook raw/helper sheets without rebuilding the chart layout

## When to use

Use this skill whenever the user mentions any of:

- refresh llm-stats data
- recrawl llm-stats
- update cached homepage HTML
- refresh raw data
- update CSV outputs
- rebuild workbook data layer only

## Workflow

1. Read [workflow.md](references/workflow.md) if you need the exact inputs and outputs.
2. Run `scripts/run_data_refresh.py`.
3. Report the workbook, CSV, and cache paths.
4. If the user also wants refreshed charts, hand off to `llm-stats-chart-refresh`.
