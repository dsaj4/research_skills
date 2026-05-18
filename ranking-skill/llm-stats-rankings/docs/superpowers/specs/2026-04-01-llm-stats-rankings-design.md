# LLM Stats Rankings Workbook Design

## Goal

Create a repo-local skill project that extracts the LLM leaderboard snapshot from `https://llm-stats.com/`, caches the source payload, exports normalized CSV data, and generates an Excel workbook with a presentation sheet and four native charts.

The implementation should mirror the project shape used by `openrouter-rankings`:

- one standalone project directory
- one main Python entry point
- one skill for data refresh
- one skill for chart refresh
- tests, output, and tmp directories kept inside the project

## Source Boundaries

### Accepted direct sources

- the server-rendered HTML returned by `https://llm-stats.com/`
- the `initialHomepageLLMModels` payload embedded in that HTML

### Rejected sources

- manual copy-paste from the rendered table
- OCR or pixel-based extraction
- inferred or synthesized model metrics that are not present in the embedded payload

## Confirmed Findings

On April 1, 2026, the homepage HTML includes an escaped JSON array keyed as `initialHomepageLLMModels`.

That payload is sufficient for the first version of this project. It contains, per model:

- model id
- model name
- organization
- organization id
- `gpqa_score`
- `swe_bench_verified_score`
- `hle_score`
- `context`
- `input_price`
- `output_price`
- open-source flag
- announcement date
- nested `arena_scores`, including `chat-arena` and `coding-arena`

The payload order matches the homepage leaderboard order, so rank can be assigned by array position.

The embedded array currently contains 275 rows, which is enough to:

- preserve the full homepage snapshot as raw data
- export a normalized all-model CSV
- derive the current Top 20 leaderboard snapshot
- build chart-specific helper sheets without additional network APIs

## Normalized Dataset

The normalized record written to the workbook and CSV should include:

- `rank`
- `model_id`
- `name`
- `organization`
- `organization_id`
- `chat_arena_score`
- `coding_arena_score`
- `gpqa_score`
- `swe_bench_verified_score`
- `hle_score`
- `context`
- `context_display`
- `input_price`
- `input_price_display`
- `output_price`
- `output_price_display`
- `license`
- `announcement_date`
- `source_url`
- `generated_at`

Rules:

- `rank` is derived from the original array order and starts at `1`
- `license` is derived from `is_open_source`
- display fields are helper fields for CSV readability and workbook tables
- missing numeric values remain empty, not zero-filled

## Project Layout

The project will live in `llm-stats-rankings/` and include:

- `README.md`
- `generate_llm_stats_rankings_excel.py`
- `skills/llm-stats-data-refresh/`
- `skills/llm-stats-chart-refresh/`
- `tests/`
- `output/spreadsheet/`
- `tmp/api-cache/`
- `docs/`

## Output Contract

Generated files should be written to:

- `output/spreadsheet/llm_stats_models.xlsx`
- `output/spreadsheet/llm_stats_homepage_models.csv`
- `output/spreadsheet/llm_stats_top20.csv`

Temporary fetch and cache files should be written to:

- `tmp/api-cache/llm_stats_homepage.html`
- `tmp/api-cache/llm_stats_homepage_models.json`

## Workbook Design

### Display sheet

Workbook front page title: `LLM Stats Dashboard`

This page should contain:

- a summary block with source URL and refresh timestamp
- a compact Top 20 snapshot table
- four native Excel charts

### Raw and helper sheets

- `Meta`
- `Raw_Models`
- `Data_Top20`
- `Data_Coding`
- `Data_Chat`
- `Data_Benchmarks`
- `Data_PriceContext`

The `Data_*` sheets should be hidden after population.

## Chart Plan

The workbook should contain four charts:

1. `Coding Arena Top 20`
   - horizontal bar chart
   - source: `Data_Coding`
   - sorted by `coding_arena_score`

2. `Chat Arena Top 20`
   - horizontal bar chart
   - source: `Data_Chat`
   - sorted by `chat_arena_score`

3. `GPQA vs SWE-Bench Verified`
   - clustered bar chart
   - source: `Data_Benchmarks`
   - uses the Top 20 homepage models with available values

4. `Input Price vs Context Window`
   - scatter chart
   - source: `Data_PriceContext`
   - plots models that have both `input_price` and `context`

The Top 20 rank order itself will be preserved as a table on the display sheet rather than turned into a synthetic score chart.

## Modes

The main script should support:

- `full`
  - fetch and cache homepage HTML
  - refresh normalized data outputs
  - rebuild the display page and charts

- `data-refresh`
  - fetch and cache homepage HTML
  - rebuild raw and helper sheets
  - export CSV files
  - leave the display page as a placeholder note if chart refresh is not requested

- `chart-refresh`
  - read existing workbook raw data
  - rebuild the display page and four charts
  - do not perform network fetches

## Error Handling

- If a live fetch fails and the cached homepage HTML exists, use the cache.
- If the embedded payload marker is missing, fail loudly instead of guessing.
- If chart-refresh is requested without a workbook containing `Raw_Models`, return a clear error.
- If some metric values are missing, keep the rows and leave those cells blank.

## Verification

The initial automated verification should confirm:

- the HTML parser extracts the embedded array correctly
- fetch fallback uses cache when the network path fails
- the workbook contains the expected sheet names
- the display sheet contains four charts
- CSV exports are written and include normalized rank fields

## Out of Scope

- incremental historical tracking across refreshes
- pixel-perfect recreation of the llm-stats website
- non-homepage benchmark families that are not present in the embedded homepage payload
- interactive or web-based chart rendering
