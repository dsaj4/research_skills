# Existing File To Draft Template

Use this when the user wants to convert an existing file or project package into a reusable research draft template.

## Supported Inputs

- existing research draft workbook
- Excel workbook with charts/tables/source notes
- PPT or rendered slide images used as a review layout reference
- project package containing materials, scripts, screenshots, and final deliverables
- chart template workbook or style case

## Workflow

1. Locate candidate files with `rg --files`.
2. Identify the current/formal deliverable and preserve it.
3. Create a preview/template copy rather than editing the original.
4. Inspect structure:
   - workbook sheets
   - table layout
   - chart types and styles
   - evidence sheet pattern
   - comments and source notes
   - screenshot placement
   - Chinese naming conventions
5. Separate reusable template elements from one-off task data.
6. Produce a template contract or template workbook.
7. Record what was intentionally excluded.

## What To Extract

Reusable:

- sheet roles and ordering
- required headers
- evidence sheet layout
- source metadata fields
- chart palette and font conventions
- screenshot sizing/placement conventions
- validation checklist

Not reusable:

- company-specific numbers
- one-off screenshots
- task dates
- specific analyst notes
- temporary paths
- single-project assumptions

## Output

At minimum, output:

- template/workbook path or template contract
- source file used as reference
- reusable sheet contract
- evidence requirements
- excluded one-off content
- remaining manual decisions

## Verification

- Original files are preserved.
- Template contains no accidental company-specific data unless intentionally kept as examples.
- Template still opens in Excel.
- Evidence fields are sufficient to support future review.

