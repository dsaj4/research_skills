---
name: site-rankings-factory
description: Scaffold a new website rankings skill project with crawler, sqlite snapshot storage, workbook data layer, and display page. Use this whenever the user wants to scrape a new rankings site, clone the llm-stats/openrouter pattern for another website, or quickly stand up the same crawl-plus-dashboard workflow for a fresh source.
---

# Site Rankings Factory

Use this skill to create a new website-specific rankings project without manually copying `llm-stats-rankings/`.

## What this skill creates

- a crawl entry point
- JSON and CSV exports
- a local `sqlite` snapshot database
- an Excel workbook with raw/helper/display sheets
- `data-refresh` and `chart-refresh` repo-local skills
- starter tests and README files

## Workflow

1. Read [architecture.md](references/architecture.md) if you need the design contract.
2. Run `scripts/scaffold_site_rankings_project.py` with:
   - `--project-name`
   - `--site-name`
   - `--source-url`
3. Open the generated project and fill in the site-specific extractor and normalization TODOs.
4. Run the generated tests.
5. Use the generated refresh skills for future updates.

## Notes

- The generated project is intentionally opinionated: it keeps the display layer reusable and pushes site-specific logic into extractor/normalizer functions.
- The `sqlite` snapshot database is there to preserve crawl history even when the workbook is rebuilt.
