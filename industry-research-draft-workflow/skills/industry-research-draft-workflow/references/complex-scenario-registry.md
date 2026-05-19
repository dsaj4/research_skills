# Complex Scenario Registry

Use this registry when a larger workflow needs research draft rules, but this skill should not execute the full workflow.

The registry lets future dedicated skills read and reuse draft contracts from `industry-research-draft-workflow`.

## Registry Contract

Each complex scenario should record:

- `scenario_id`: stable English ID
- `display_name`: Chinese scenario name
- `trigger_phrases`: common user wording
- `owning_skill`: dedicated skill name, or `planned:<name>` when not created yet
- `draft_role`: what the research draft does in the scenario
- `required_draft_sections`: required sheets or fields
- `evidence_requirements`: source evidence requirements
- `handoff_contract`: inputs/outputs between this skill and the owning skill
- `quality_gates`: scenario-specific checks beyond common gates
- `out_of_scope`: what this skill must not execute

## Handling Flow

1. Identify whether the user's request matches a registered complex scenario.
2. If `owning_skill` exists, use that skill for the full workflow.
3. Use this skill only for workbook contract, evidence fields, and draft quality checks.
4. Do not move full business workflow steps into this skill.

## Registered Scenario: PPT Modification Draft Sync

`scenario_id`: `ppt-modification-draft-sync`

`display_name`: PPT 修改同步底稿

`owning_skill`: `planned:ppt-modification-draft-sync`

### Trigger Phrases

- 按材料改 PPT 并补底稿
- PPT 修改需要同步底稿
- 生成 PPT 修改对应的底稿
- 更新路演材料并保留来源
- PPT 更新点要有底稿证据

### Draft Role

The draft records why each PPT update was made, what changed, which source supports it, and how reviewers can verify the change.

### Required Draft Fields

- `PPT页码`
- `更新对象`
- `原表述/原数据`
- `新表述/新数据`
- `更新原因`
- `来源文件/链接/页码`
- `证据截图`
- `PPT截图`
- `核验状态`
- `备注`

### Evidence Requirements

- Every material update needs source evidence.
- Every changed slide should have a PPT screenshot or rendered preview path.
- Key numbers and wording should trace back to source file, URL, page number, or screenshot.
- Unclear values or missing screenshots go to `待核验`.

### Handoff Contract

Inputs from owning skill:

- PPT file path
- changed slide/page list
- original and updated text/data
- source material list
- source screenshot paths
- rendered PPT screenshot paths
- unresolved issues

Outputs from this skill:

- draft workbook contract
- suggested sheet/field layout
- evidence requirements
- quality gate checklist
- optional validation findings

### Quality Gates

- PPT, text draft, and research draft use consistent numbers and口径.
- Each updated slide has an evidence row or evidence block.
- Source screenshots or original files are traceable.
- Final PPT and draft are not overwritten without explicit request.

### Out Of Scope

This skill does not:

- edit PPT files
- render slides
- rebuild charts
- manage full PPT project workflow
- store company-specific update data as reusable skill content

