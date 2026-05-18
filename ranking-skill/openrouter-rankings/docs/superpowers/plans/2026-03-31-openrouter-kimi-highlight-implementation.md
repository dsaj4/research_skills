# OpenRouter Kimi Highlight Workbook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a second OpenRouter rankings workbook that keeps the same directly extracted data but applies a Kimi-emphasis presentation and palette.

**Architecture:** Keep the existing extraction and default workbook intact, then add a second workbook path driven by variant-specific chart configuration. Share the raw-sheet generation path, but make chart colors, meta notes, and spotlight rendering configurable so the Kimi variant can emphasize `moonshotai/kimi-k2.5-0127` without diverging from the source data.

**Tech Stack:** Python 3.14, standard library, `openpyxl`, `unittest`

---

### Task 1: Add Red Tests For The Kimi Variant

**Files:**
- Modify: `E:/Project/实习/Openrouter/tests/test_openrouter_rankings_excel.py`
- Test: `E:/Project/实习/Openrouter/tests/test_openrouter_rankings_excel.py`

- [ ] Step 1: Add a failing unit test for the Kimi palette assignment helper so the Kimi series gets the dedicated emphasis color and `Others` gets a muted slot.
- [ ] Step 2: Run `python -m unittest tests.test_openrouter_rankings_excel -v` and verify the new palette test fails because the helper does not exist yet.
- [ ] Step 3: Add a failing workbook test that expects a separate Kimi workbook builder, Kimi-specific meta rows, and a spotlight chart.
- [ ] Step 4: Run `python -m unittest tests.test_openrouter_rankings_excel -v` and verify the workbook test fails before implementation.

### Task 2: Implement Variant-Aware Workbook Generation

**Files:**
- Modify: `E:/Project/实习/Openrouter/generate_openrouter_rankings_excel.py`
- Modify: `E:/Project/实习/Openrouter/tests/test_openrouter_rankings_excel.py`

- [ ] Step 1: Add Kimi palette constants, palette extension helpers, and a deterministic Kimi-emphasis color assignment helper.
- [ ] Step 2: Refactor workbook generation so the existing default workbook remains unchanged while the Kimi variant gets its own meta rows, top chart colors, and spotlight chart.
- [ ] Step 3: Add a dedicated `build_kimi_emphasis_workbook(...)` entry point and a second output path in `main()`.
- [ ] Step 4: Re-run `python -m unittest tests.test_openrouter_rankings_excel -v` and verify the full suite passes.

### Task 3: Generate And Verify Deliverables

**Files:**
- Modify: `E:/Project/实习/Openrouter/generate_openrouter_rankings_excel.py`
- Output: `E:/Project/实习/Openrouter/output/spreadsheet/openrouter_top_models.xlsx`
- Output: `E:/Project/实习/Openrouter/output/spreadsheet/openrouter_top_models_kimi_emphasis.xlsx`

- [ ] Step 1: Run `python generate_openrouter_rankings_excel.py`.
- [ ] Step 2: Inspect both workbooks and verify the default workbook still has the original chart set and the Kimi workbook exists separately.
- [ ] Step 3: Inspect the Kimi workbook metadata, chart count, and Kimi highlight color to confirm the variant matches the approved design.
