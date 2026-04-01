# research_skills

This repository is a container for multiple standalone skill projects.

## Top-level layout

- `openrouter-rankings/`: OpenRouter rankings crawl, workbook generation, dashboard display refresh, and repo-local agent skills.
- `_shared/`: Reserved for utilities, references, or assets reused by multiple skill projects.
- `_templates/`: Reserved for starter scaffolds and conventions for future skill projects.

## Convention for future projects

Add each new skill project as its own top-level folder beside `openrouter-rankings/`.

Each project should stay self-contained and preferably include:

- `README.md`
- `docs/`
- `skills/`
- `tests/`
- `output/`
- `tmp/`

This keeps the repo easy to extend without forcing unrelated skill projects into one shared codebase.
