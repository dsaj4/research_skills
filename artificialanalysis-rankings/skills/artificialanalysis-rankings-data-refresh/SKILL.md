---
name: artificialanalysis-rankings-data-refresh
description: Refresh Artificial Analysis Rankings source data into the local sqlite snapshot store, CSV outputs, and workbook data layer. Use this whenever the user asks to recrawl Artificial Analysis Rankings, refresh raw fetch caches, update normalized exports, or rebuild raw/helper sheets without redesigning the display page.
---

# Artificial Analysis Rankings Data Refresh

Use this skill when the task is about fetching or refreshing source data.

## Workflow

1. Read [workflow.md](references/workflow.md) if you need the exact inputs and outputs.
2. Run `scripts/run_data_refresh.py`.
3. Confirm the homepage `Intelligence`, `Speed`, and `Price` datasets were merged into one normalized table.
4. Report the workbook, CSV, sqlite, and cache paths.
5. If the user also wants the display page rebuilt, run `artificialanalysis-rankings-chart-refresh`.
