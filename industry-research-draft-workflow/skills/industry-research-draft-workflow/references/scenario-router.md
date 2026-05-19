# Scenario Router

Use this file first when the user's request touches research drafts but the exact workflow is unclear.

## Core Scenarios

### A. Existing File To Draft Template

Use when the user says:

- 把这个文件改造成底稿模板
- 从这个 Excel/PPT/底稿沉淀模板
- 以后按这个格式复用
- 提取底稿结构、图表样式、证据表格式

Load:

- `existing-file-to-template.md`
- `workbook-contract.md`
- `quality-gates.md`

Goal: extract reusable draft contracts without carrying one-off company/task data into the template.

### B. Research Draft Generation

Use when the user says:

- 把数据收集写成底稿
- 把材料整理成底稿
- 做表述核验底稿
- 为某个研究问题生成证据底稿
- 收集行业/公司/产品数据并生成底稿

Load:

- `research-draft-generation.md`
- `data-collection-guidance.md`
- `workbook-contract.md`
- `quality-gates.md`

Goal: produce a reviewable, traceable workbook with structured data, evidence, and unresolved items.

### C. Data Collection Guidance

Use when the user primarily asks where/how to collect data for a draft.

Common source types:

- company website / IR / product pages
- WeChat public account / official social channels
- company announcements / annual reports / quarterly reports
- industry reports / broker research / media reports
- terminal exports and screenshots
- rankings / benchmark / leaderboard sources

Load:

- `data-collection-guidance.md`
- `workbook-contract.md` if the data will be written into a workbook

Goal: guide collection order, source recording, evidence screenshots, and `待核验` handling. Do not implement dedicated crawlers or adapters here.

### D. Complex Scenario Registry

Use when the request belongs to a larger workflow, but this skill should only supply draft rules.

Examples:

- PPT 修改同步底稿
- future valuation model update sync
- future database crawl + draft sync
- future interview transcript verification draft

Load:

- `complex-scenario-registry.md`
- `workbook-contract.md`
- `quality-gates.md`

Goal: identify the owning skill/workflow and provide only the draft contract, evidence fields, and handoff requirements.

### E. Existing Draft Minimal Update / Chart Template Adaptation

Use when the user says:

- 修改已有底稿
- 套用新格式
- 图表格式适配
- 最小更新
- 不重建，只更新受影响内容

Load:

- `current-project-pattern.md`
- `workbook-contract.md`
- `quality-gates.md`

Goal: preserve workbook structure and make minimal traceable changes.

## Tie Breakers

- If there is a usable current workbook and the user asks to update it, choose E over B.
- If the user asks for a reusable template, choose A even if an existing workbook is present.
- If the request involves data source choices but not workbook creation yet, choose C.
- If a complex workflow has a dedicated skill, choose D and hand off full execution to that skill.
- If the user asks for a new deliverable from collected materials, choose B.

