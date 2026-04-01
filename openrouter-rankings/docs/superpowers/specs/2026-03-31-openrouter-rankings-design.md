# OpenRouter Rankings Excel Reproduction Design

## Goal

Rebuild the `Top Models` section from `https://openrouter.ai/rankings` into Excel with the highest possible data fidelity under a strict rule:

- Only use data that can be directly extracted from the page or its runtime state.
- Do not estimate, digitize from pixels, or infer missing values from the chart image.

The workbook should cover both:

1. The top `Top Models` weekly time-series chart.
2. The `This Week` leaderboard shown below it.

## Source Boundaries

### Accepted direct sources

- Rendered DOM content on `https://openrouter.ai/rankings`
- Runtime React / Recharts props attached to the rendered page
- Static HTML / embedded RSC payload if needed as a fallback

### Rejected sources

- Manual visual approximation
- OCR or chart digitization
- Guessed backfills for hidden or missing points

## Confirmed Findings

### Top chart

The top `Top Models` chart is rendered with Recharts and exposes a direct `data` array in runtime component props.

Confirmed properties:

- Section: `Top Models`
- Date granularity: weekly
- Point count: 52
- Date range: `2025-04-07` through `2026-03-30`
- Structure: one row per week, with `__RECHARTS_X_LABEL__` plus multiple model-series keys and `Others`

Observed current final row includes keys such as:

- `xiaomi/mimo-v2-pro-20260318`
- `stepfun/step-3.5-flash:free`
- `deepseek/deepseek-v3.2-20251201`
- `minimax/minimax-m2.7-20260318`
- `anthropic/claude-4.6-sonnet-20260217`
- `anthropic/claude-4.6-opus-20260205`
- `google/gemini-3-flash-preview-20251217`
- `z-ai/glm-5-turbo-20260315`
- `x-ai/grok-4.1-fast`
- `Others`

There is also a `forecast-1w` field present in the chart data. This field will be preserved in raw data and clearly labeled as provided by the page runtime.

### Leaderboard

The `This Week` leaderboard rows are directly extractable from rendered DOM after expanding `Show more`.

Confirmed fields:

- rank
- model name
- provider / author
- model URL
- provider URL
- weekly tokens display string
- week-over-week change direction and magnitude

Current extraction target remains the visible top 20 rows after expansion.

## Workbook Design

### Sheet 1: `Meta`

Purpose:

- Record source URL
- Record scrape timestamp
- Record extraction method
- Record constraints and fidelity notes

Fields:

- source_url
- scraped_at
- extraction_method_top_chart
- extraction_method_leaderboard
- allowed_data_policy
- notes

### Sheet 2: `Raw_TimeSeries`

Purpose:

- Preserve the directly extracted weekly chart dataset with minimal transformation

Structure:

- One row per week
- First column: `week_start`
- Remaining columns: each series key exactly as exposed by runtime data

Rules:

- Keep raw series keys unchanged
- Keep `Others` if present
- Keep `forecast-1w` if present
- No synthetic totals or imputed values

### Sheet 3: `Raw_Leaderboard`

Purpose:

- Preserve current leaderboard rows exactly as shown after `Show more`

Fields:

- rank
- model
- provider
- model_url
- provider_url
- weekly_tokens_display
- weekly_tokens_billions
- wow_change_percent
- wow_change_direction

Rules:

- `weekly_tokens_billions` is a derived helper field for charting only
- Display string remains preserved verbatim

### Sheet 4: `Charts`

Purpose:

- Recreate the section in a way that is faithful to original structure while staying within Excel native chart constraints

Planned charts:

1. `Top Models Weekly Usage`
   - Source: `Raw_TimeSeries`
   - Type: stacked area chart
   - X-axis: weekly dates
   - Series: direct runtime chart series
   - Styling goal: dark background, muted gridlines, bright stacked fills, closer to OpenRouter visual hierarchy

2. `This Week Leaderboard`
   - Source: `Raw_Leaderboard`
   - Type: horizontal bar chart
   - X-axis: weekly token volume
   - Y-axis: model names ordered by rank

3. `WoW Change`
   - Source: `Raw_Leaderboard`
   - Type: line or column chart
   - Goal: show current week change magnitude cleanly

## Styling Strategy

The priority is data truth, not pixel-perfect imitation. Within Excel native chart limits, styling will move toward OpenRouter:

- Dark chart backgrounds
- Low-contrast axis and grid colors
- Stronger accent fills for key series
- Compact chart titles and subtitles
- Top chart emphasized visually over supporting charts

Known limitation:

- Excel native charts cannot fully replicate Recharts glow, tooltip behavior, hover interaction, and custom SVG effects.

## Data Flow

1. Open the rankings page in a browser context.
2. Read the top chart's Recharts runtime `data` prop directly from the mounted component tree.
3. Expand `Show more` in the leaderboard.
4. Read leaderboard rows from rendered DOM.
5. Normalize helper numeric fields only where needed for Excel plotting.
6. Write raw sheets first.
7. Build Excel charts from those raw sheets.

## Error Handling

- If top chart runtime data is unavailable, leave `Raw_TimeSeries` empty and record failure in `Meta`.
- If leaderboard expansion fails, preserve available rows only and record row count in `Meta`.
- No fallback estimation is allowed.

## Verification Plan

1. Re-open workbook with `openpyxl` and verify expected sheet names.
2. Verify `Raw_TimeSeries` row count is 52 unless the source changed.
3. Verify `Raw_Leaderboard` row count matches extracted visible rows.
4. Verify `Charts` sheet contains native Excel charts.
5. Verify metadata documents source and extraction method.

## Out of Scope

- Pixel-perfect webpage recreation
- Hidden API reverse engineering beyond direct runtime data access
- Approximation of unavailable chart values
- Historical leaderboard backfill beyond what is directly exposed

## Implementation Recommendation

Use browser runtime extraction plus `openpyxl` workbook generation:

- Browser runtime extraction for fidelity
- `openpyxl` for workbook editing and native Excel chart creation

This is the best fit because it satisfies the no-estimation rule and keeps the output reproducible from the live page.

## Environment Note

The current workspace is not a git repository, so this design document cannot be committed here. The file is still written locally for review and implementation guidance.
