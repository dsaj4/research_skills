# OpenRouter Rankings

This project extracts OpenRouter rankings data, stores a raw data layer in an Excel workbook, and rebuilds a presentation-oriented display page from that data.

The data layer is incremental: weekly refreshes merge into existing raw history instead of overwriting prior runs.

## What is included

- `generate_openrouter_rankings_excel.py`: main entry point
- `skills/`: repo-local skills for data refresh and display refresh
- `tests/`: unit and smoke tests
- `docs/`: specs and plan notes used during implementation
- `example-charts.xlsx`: layout reference for the workbook display page

## Main commands

From this project directory:

```powershell
python -m unittest tests.test_openrouter_rankings_excel -v
python generate_openrouter_rankings_excel.py --mode full
python generate_openrouter_rankings_excel.py --mode data-refresh
python generate_openrouter_rankings_excel.py --mode display-refresh
```

## Output contract

Generated files are written to:

- `output/spreadsheet/openrouter_top_models.xlsx`
- `output/spreadsheet/openrouter_top_models.csv`
- `output/spreadsheet/openrouter_top_models_timeseries.csv`

Temporary crawl and render files are written under `tmp/spreadsheets/`.

## Incremental history behavior

- `Raw_TimeSeries` keeps cumulative weekly history by `week_start`
- `Raw_Leaderboard` keeps cumulative leaderboard snapshot history by `snapshot_captured_at`
- `display-refresh` reads cumulative raw history but only renders the latest leaderboard snapshot on the display page

## Local skills

- `skills/openrouter-rankings-data-refresh/`
- `skills/openrouter-rankings-display-refresh/`

These skills wrap the existing workflow rather than introducing a second code path.
