# Data Refresh Contract

Source URL: `https://artificialanalysis.ai/`

Running data refresh should:

- fetch and cache the latest source payload
- normalize records into the standard workbook schema
- append the crawl to the local sqlite snapshot database
- refresh JSON and CSV outputs
- rebuild workbook raw/helper sheets

Current implementation reads the homepage JSON-LD datasets named:

- `Intelligence`
- `Speed`
- `Price`

Main entry point:

- `generate_artificialanalysis_rankings_excel.py`
