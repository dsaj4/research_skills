# Ranking Skill

This folder groups all rankings-related skill projects in one place.

## Included projects

- `openrouter-rankings/`: OpenRouter rankings crawl, workbook generation, dashboard display refresh, and repo-local agent skills.
- `llm-stats-rankings/`: LLM Stats homepage leaderboard extraction, CSV export, workbook generation, and repo-local agent skills.
- `artificialanalysis-rankings/`: Artificial Analysis homepage main leaderboard extraction, sqlite snapshot storage, and workbook refresh skills.
- `site-rankings-factory/`: Reusable scaffold skill for bootstrapping new website rankings projects with crawler, storage layer, and workbook display layer.

## Usage

Open the specific project directory before running its commands. Each project remains self-contained and keeps its original `README.md`, `docs/`, `skills/`, `tests/`, `output/`, and `tmp/` structure.

For example:

```powershell
cd ranking-skill\openrouter-rankings
python -m unittest tests.test_openrouter_rankings_excel -v
```

New rankings-related projects should be added as sibling folders inside `ranking-skill/`.
