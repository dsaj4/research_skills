# Data Refresh Workflow

## Purpose

Refresh the OpenRouter rankings data layer while keeping the existing display page layout unchanged.

## Inputs

- `tmp/spreadsheets/rankings_page.html` as cache fallback
- Embedded HTML chart payload from `https://openrouter.ai/rankings`
- Repo snapshot leaderboard constant for the current ranking period

## Outputs

- `output/spreadsheet/openrouter_top_models.xlsx`
- `output/spreadsheet/openrouter_top_models.csv`
- `output/spreadsheet/openrouter_top_models_timeseries.csv`

## Contract

- Update `Meta`, `Raw_TimeSeries`, `Raw_Leaderboard`, and `Data_*`
- Do not rebuild `展示页`
- Do not create `openrouter_top_models_kimi_emphasis.xlsx`
