# Incremental Data Layer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade the workbook data layer so weekly refreshes preserve history and incrementally merge new data instead of overwriting prior runs.

**Architecture:** Keep the single-workbook design, but treat `Raw_TimeSeries` as a cumulative week-level history table and `Raw_Leaderboard` as a cumulative snapshot history table. During refresh, merge new payloads into existing workbook history, then rebuild helper sheets and display data from the merged history while filtering leaderboard display inputs to the latest snapshot only.

**Tech Stack:** Python, openpyxl, csv, unittest

---

### Task 1: Add failing tests for history merge semantics

**Files:**
- Modify: `tests/test_openrouter_rankings_excel.py`

**Step 1: Write the failing test**

Add tests that assert:
- overlapping timeseries weeks are replaced by the newest payload while older weeks outside the new window are preserved
- leaderboard history can keep multiple snapshot dates and the display loader returns only the latest snapshot

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_openrouter_rankings_excel -v`

Expected: new merge/history tests fail because merge helpers do not exist yet and workbook loading still assumes a single snapshot table.

### Task 2: Implement merge helpers and workbook history loading

**Files:**
- Modify: `generate_openrouter_rankings_excel.py`

**Step 1: Write minimal implementation**

Add helper functions for:
- resolving the run snapshot date
- enriching leaderboard rows with snapshot metadata
- merging timeseries history by `week_start`
- merging leaderboard history by `snapshot_captured_at + rank + model_url`
- loading all leaderboard history and filtering to the latest snapshot for display

**Step 2: Run targeted tests**

Run: `python -m unittest tests.test_openrouter_rankings_excel.DatasetTests -v`

Expected: merge behavior tests pass.

### Task 3: Wire incremental merge into full/data-refresh flows

**Files:**
- Modify: `generate_openrouter_rankings_excel.py`
- Modify: `tests/test_openrouter_rankings_excel.py`

**Step 1: Update refresh paths**

Change `write_data_layers`, `run_data_refresh`, and `run_full` so they:
- load existing workbook history when present
- merge new timeseries and leaderboard snapshots into history
- write cumulative CSV outputs
- build display data from merged history plus latest leaderboard snapshot

**Step 2: Add/adjust integration tests**

Assert:
- `data-refresh` preserves older raw history rows
- leaderboard raw sheet now contains snapshot metadata
- display refresh still works from cumulative raw sheets

**Step 3: Run full test suite**

Run: `python -m unittest tests.test_openrouter_rankings_excel -v`

Expected: all tests pass.

### Task 4: Regenerate workbook and verify outputs

**Files:**
- Runtime output: `output/spreadsheet/openrouter_top_models.xlsx`
- Runtime output: `output/spreadsheet/openrouter_top_models.csv`
- Runtime output: `output/spreadsheet/openrouter_top_models_timeseries.csv`

**Step 1: Run generation**

Run: `python generate_openrouter_rankings_excel.py --mode full`

**Step 2: Sanity-check output**

Confirm the workbook still opens, the display page rebuilds, and raw sheets now represent cumulative history rather than a single overwritten snapshot.
