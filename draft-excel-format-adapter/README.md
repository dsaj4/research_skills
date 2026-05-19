# industry-research-draft-workflow

Repo-local development home for the `industry-research-draft-workflow` skill.

The skill supports research draft workbook work in two modes:

- Create a new Excel research draft from collected data/materials.
- Modify an existing draft workbook with minimal changes.

Current best practice for new draft creation is based on the workflow in:

- `docs/README_底稿修改说明.md`
- `docs/底稿创作规范与流程.md`
- `docs/范例说明_ARR数据收集.md`

The installable skill entrypoint is:

- `skills/industry-research-draft-workflow/SKILL.md`

## Packaging

Create an installable `.skill` archive with:

```powershell
python .\scripts\package_draft_excel_skill.py
```

The package is written to:

```text
output/skill-packages/industry-research-draft-workflow.skill
```

The packaged skill includes `scripts/ensure_draft_excel_skill_assets.py`, which checks local bundled assets and restores missing files from the current GitHub repository by default:

```powershell
python .\skills\industry-research-draft-workflow\scripts\ensure_draft_excel_skill_assets.py --dry-run
python .\skills\industry-research-draft-workflow\scripts\ensure_draft_excel_skill_assets.py
```

Default asset source:

```text
https://raw.githubusercontent.com/dsaj4/research_skills/main/draft-excel-format-adapter/skills/industry-research-draft-workflow
```
