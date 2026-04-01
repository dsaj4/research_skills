# OpenRouter Kimi Highlight Workbook Design

## Goal

Create a second workbook derived from the same directly extracted OpenRouter `Top Models` data, with a visual emphasis on the Kimi model series.

This workbook must:

- Not replace the existing `openrouter_top_models.xlsx`
- Reuse the same direct-extraction data policy
- Apply a new palette based on the user-provided 10-color reference
- Highlight the Kimi series more strongly than other series

## Output

New workbook filename:

- `output/spreadsheet/openrouter_top_models_kimi_emphasis.xlsx`

The original workbook remains unchanged.

## Source Policy

Same as the main workbook:

- Top time-series data must come directly from extracted `Top Models` runtime / embedded page data
- No estimated values
- No synthetic Kimi backfill

## Scope

### Included

- Reuse `Meta`, `Raw_TimeSeries`, and `Raw_Leaderboard`
- Add a Kimi-emphasized chart presentation
- Add a Kimi-specific spotlight chart

### Excluded

- Re-scraping different source data
- Changing the original workbook output
- Pixel-perfect chart recreation

## Kimi Target

Kimi series key:

- `moonshotai/kimi-k2.5-0127`

If this key is present in the extracted weekly series, it will be explicitly emphasized.

If the key is missing in a future source snapshot, the workbook should still be generated and record the missing-key condition in `Meta`.

## Workbook Structure

### Sheet 1: `Meta`

Adds Kimi-specific notes:

- variant_name
- highlighted_series_key
- palette_source
- kimi_series_found

### Sheet 2: `Raw_TimeSeries`

Same directly extracted weekly series dataset as the main workbook.

### Sheet 3: `Raw_Leaderboard`

Same leaderboard snapshot approach as the main workbook.

### Sheet 4: `Charts`

Contains:

1. `Top Models Weekly Usage (Kimi Highlighted)`
2. `Kimi Usage Spotlight`
3. Existing supporting leaderboard / WoW charts may remain if convenient

## Color System

Base palette from the user-provided image:

1. `#196BA5`
2. `#E4C864`
3. `#B6B6B6`
4. `#7699C8`
5. `#B9CDE5`
6. `#948A54`
7. `#7F7F7F`
8. `#FAC090`
9. `#F1EADA`
10. `#98CEDD`

### Assignment rule

- Kimi gets a dedicated emphasis color first
- Remaining series consume the base palette in order
- If series count exceeds 10, extend with visually similar neighboring shades
- `Others` should not compete with Kimi visually; it should use a muted palette slot

## Chart Design

### Chart 1: `Top Models Weekly Usage (Kimi Highlighted)`

- Keep the same weekly time axis
- Keep the same direct series values
- Use stacked vertical columns
- Kimi must stand out through color priority
- Other series must remain readable but visually secondary

### Chart 2: `Kimi Usage Spotlight`

- Single-series chart using `moonshotai/kimi-k2.5-0127`
- Use the same Kimi emphasis color
- Purpose is to make Kimi usage easy to inspect without losing the comparison chart

## Error Handling

- If Kimi series exists: render both charts normally
- If Kimi series is absent: keep the workbook valid, note absence in `Meta`, and do not fabricate a spotlight series

## Verification Plan

1. Generate the new workbook without overwriting the original workbook
2. Verify output file exists at the new path
3. Verify workbook sheet structure is valid
4. Verify the `Charts` sheet contains a Kimi-highlighted top chart
5. Verify the spotlight chart uses the Kimi series when the key exists

## Environment Note

This workspace is not a git repository, so the design doc cannot be committed here. The file is saved locally for review and implementation guidance.
