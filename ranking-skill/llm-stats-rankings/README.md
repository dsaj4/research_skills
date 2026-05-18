# LLM Stats Rankings

This project extracts the homepage LLM leaderboard snapshot from `https://llm-stats.com/`, caches the embedded data payload, exports normalized CSV files, and builds an Excel workbook with a display page and native charts.

## What is included

- `generate_llm_stats_rankings_excel.py`: main entry point
- `skills/`: repo-local skills for data refresh and chart refresh
- `tests/`: unit tests for parsing, cache fallback, CSV export, and workbook structure
- `docs/`: local design and implementation notes

## Main commands

From this project directory:

```powershell
python -m unittest tests.test_llm_stats_rankings_excel -v
python generate_llm_stats_rankings_excel.py --mode full
python generate_llm_stats_rankings_excel.py --mode data-refresh
python generate_llm_stats_rankings_excel.py --mode chart-refresh
```

## Output contract

Generated files are written to:

- `output/spreadsheet/llm_stats_models.xlsx`
- `output/spreadsheet/llm_stats_homepage_models.csv`
- `output/spreadsheet/llm_stats_top20.csv`

Temporary fetch and cache files are written to:

- `tmp/api-cache/llm_stats_homepage.html`
- `tmp/api-cache/llm_stats_homepage_models.json`

## Data source

The first version intentionally stays close to the homepage itself:

- fetch the homepage HTML
- extract the embedded `initialHomepageLLMModels` payload
- normalize that payload into flat records

This keeps the workflow stable even when direct API requests are restricted.
