# OpenRouter Rankings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the OpenRouter rankings workbook so it uses directly extracted weekly `Top Models` time-series data plus the current expanded leaderboard snapshot.

**Architecture:** Parse the top chart dataset directly from the saved/fetched rankings HTML, keep the expanded leaderboard as a directly extracted snapshot, and generate a new workbook with raw sheets plus native Excel charts. Keep raw extracted data separate from chart-friendly helper fields.

**Tech Stack:** Python 3.14, standard library, `openpyxl`, `unittest`

---

### Task 1: Add Red Tests

**Files:**
- Create: `E:/Project/实习/Openrouter/tests/test_openrouter_rankings_excel.py`
- Create: `E:/Project/实习/Openrouter/tests/fixtures/top_models_fragment.html`
- Test: `E:/Project/实习/Openrouter/tests/test_openrouter_rankings_excel.py`

- [ ] Step 1: Write a failing parser test for top chart extraction.
- [ ] Step 2: Run `python -m unittest tests.test_openrouter_rankings_excel -v` and verify failure.
- [ ] Step 3: Write a failing workbook structure test for `Meta`, `Raw_TimeSeries`, `Raw_Leaderboard`, and `Charts`.
- [ ] Step 4: Run `python -m unittest tests.test_openrouter_rankings_excel -v` and verify failure.

### Task 2: Implement Parser And Workbook Redesign

**Files:**
- Modify: `E:/Project/实习/Openrouter/generate_openrouter_rankings_excel.py`
- Test: `E:/Project/实习/Openrouter/tests/test_openrouter_rankings_excel.py`

- [ ] Step 1: Add HTML extraction helpers for the top chart dataset and forecast key.
- [ ] Step 2: Add normalization helpers for time-series rows and leaderboard rows.
- [ ] Step 3: Replace the old workbook layout with `Meta`, `Raw_TimeSeries`, `Raw_Leaderboard`, and `Charts`.
- [ ] Step 4: Re-run `python -m unittest tests.test_openrouter_rankings_excel -v` and verify tests pass.

### Task 3: Generate And Verify Deliverables

**Files:**
- Modify: `E:/Project/实习/Openrouter/generate_openrouter_rankings_excel.py`
- Output: `E:/Project/实习/Openrouter/output/spreadsheet/openrouter_top_models.xlsx`
- Output: `E:/Project/实习/Openrouter/output/spreadsheet/openrouter_top_models.csv`
- Output: `E:/Project/实习/Openrouter/output/spreadsheet/openrouter_top_models_timeseries.csv`

- [ ] Step 1: Run `python generate_openrouter_rankings_excel.py`.
- [ ] Step 2: Run a workbook inspection command to verify sheet names and chart count.
- [ ] Step 3: Run a raw data inspection command to verify weekly row count and leaderboard row count.
