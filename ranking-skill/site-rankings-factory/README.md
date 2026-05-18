# Site Rankings Factory

This project packages the current `crawler + storage layer + workbook display page` pattern into a reusable repo-local skill.

Use it when you want to bootstrap another website-specific rankings project that looks like `llm-stats-rankings/`, but without hand-copying files again.

## What it creates

The scaffold creates a new top-level project with:

- a site-specific crawl and workbook entry point
- a local snapshot database (`sqlite`) plus JSON/CSV outputs
- a workbook data layer and display layer
- two repo-local skills: `data-refresh` and `chart-refresh`
- starter tests and documentation files

## Main command

From this project directory:

```powershell
python skills/site-rankings-factory/scripts/scaffold_site_rankings_project.py --project-name example-rankings --site-name "Example Rankings" --source-url https://example.com
```

## Recommended workflow

1. Generate a new project with the scaffold script.
2. Fill in the generated extractor and normalization functions for the target site.
3. Run the starter tests.
4. Use the generated `data-refresh` and `chart-refresh` skills for future updates.
