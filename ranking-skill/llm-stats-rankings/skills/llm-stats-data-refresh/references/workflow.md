# Data Refresh Workflow

## Inputs

- live homepage HTML from `https://llm-stats.com/`
- existing cache under `tmp/api-cache/` if the live fetch fails

## Outputs

- `output/spreadsheet/llm_stats_models.xlsx`
- `output/spreadsheet/llm_stats_homepage_models.csv`
- `output/spreadsheet/llm_stats_top20.csv`
- `tmp/api-cache/llm_stats_homepage.html`
- `tmp/api-cache/llm_stats_homepage_models.json`

## Command

```powershell
python generate_llm_stats_rankings_excel.py --mode data-refresh
```
