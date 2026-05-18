# ARR Data Collection Best Practice

Current reference case:

- Final workbook: `01_当前底稿/ARR数据收集.xlsx`
- Evidence screenshots: `03_来源截图整理/ARR数据收集_来源截图/`
- Visual validation record: `截图视觉校验记录.md`

Reusable lessons:

- Do not mix revenue metrics. Distinguish ARR, run-rate revenue, annualized revenue estimate, annual revenue estimate, projected run-rate, and undisclosed values.
- Keep both source links and evidence screenshots. Embed screenshots in `证据底稿`; store source URLs in comments or notes.
- Re-capture screenshots that only show titles, ads, anti-bot pages, company overview pages, or unrelated content.
- Replace inaccessible or unsupported sources with credible alternatives when needed.
- Localize final workbook headers and enum values into Chinese.

Example final workbook structure:

- `数据总表`
- `大模型公司`
- `AI应用`
- `证据底稿`
- `待核验`

Example reusable scripts from the reference workflow:

- `generate_arr_excel_draft.py`: generate initial structured workbook.
- `embed_evidence_screenshots.py`: embed screenshots into the evidence sheet.
- `reformat_arr_excel_evidence.py`: convert to the final two-column evidence structure.
- `visual_validate_and_recapture.py`: locate keywords and recapture bad screenshots.
- `recapture_remaining.py`: retry failed or blocked captures.
- `localize_arr_excel_fields.py`: localize headers and enum values.

