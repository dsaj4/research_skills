# research_skills

This repository is a container for multiple standalone skill projects.

## Top-level layout

- `ranking-skill/`: All rankings-related skill projects, including OpenRouter, LLM Stats, Artificial Analysis, and the reusable site rankings factory.
- `company-wechat-rss/`: WeWe RSS wrapper for collecting company WeChat public account data and exporting company-grouped JSON/CSV snapshots.
- `industry-research-draft-workflow/`: Development project for the `industry-research-draft-workflow` skill, covering industry research draft workflows, evidence workbooks, PPT/draft synchronization, and chart-template guidance.
- `_shared/`: Reserved for utilities, references, or assets reused by multiple skill projects.
- `_templates/`: Reserved for starter scaffolds and conventions for future skill projects.

## Convention for future projects

Add each new non-ranking skill project as its own top-level folder beside `ranking-skill/`.

Add rankings-related projects under `ranking-skill/` so crawler, workbook, display refresh, and factory skills for ranking sites stay together.

Each project should stay self-contained and preferably include:

- `README.md`
- `docs/`
- `skills/`
- `tests/`
- `output/`
- `tmp/`

This keeps the repo easy to extend without forcing unrelated skill projects into one shared codebase.
