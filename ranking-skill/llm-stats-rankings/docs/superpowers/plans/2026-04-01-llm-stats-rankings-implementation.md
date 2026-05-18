# LLM Stats Rankings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone `llm-stats-rankings` project that extracts the embedded homepage leaderboard payload from `llm-stats.com`, exports normalized CSV files, and generates an Excel workbook with a display page and four native charts.

**Architecture:** Use a single Python entry point to fetch and cache homepage HTML, extract `initialHomepageLLMModels`, normalize the rows, and write both CSV outputs and workbook sheets. Split the repo-local skills into a data-refresh wrapper and a chart-refresh wrapper so the project follows the same operational shape as `openrouter-rankings`.

**Tech Stack:** Python 3.14, standard library, `openpyxl`, `unittest`

---

### Task 1: Add Red Tests And Fixture

**Files:**
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/tests/test_llm_stats_rankings_excel.py`
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/tests/fixtures/homepage_fragment.html`
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/tests/__init__.py`
- Test: `E:/Project/实习/research_skills/llm-stats-rankings/tests/test_llm_stats_rankings_excel.py`

- [ ] **Step 1: Write a failing parser test for the embedded homepage payload.**

```python
def test_extract_initial_homepage_models_from_html():
    html = (FIXTURES_DIR / "homepage_fragment.html").read_text(encoding="utf-8")
    rows = rankings.extract_initial_homepage_models_from_html(html)
    assert len(rows) == 2
    assert rows[0]["model_id"] == "claude-opus-4-6"
```

- [ ] **Step 2: Run the parser test and verify it fails because the parser does not exist yet.**

```powershell
python -m unittest tests.test_llm_stats_rankings_excel.LLMStatsExtractionTests.test_extract_initial_homepage_models_from_html -v
```

- [ ] **Step 3: Write a failing workbook structure test for the display page and chart count.**

```python
def test_build_workbook_creates_expected_sheets_and_four_charts():
    rankings.build_workbook(sample_rows(), workbook_path, generated_at="2026-04-01 20:00:00 CST")
    wb = load_workbook(workbook_path)
    assert wb.sheetnames == [
        rankings.DISPLAY_SHEET_TITLE,
        "Meta",
        "Raw_Models",
        "Data_Top20",
        "Data_Coding",
        "Data_Chat",
        "Data_Benchmarks",
        "Data_PriceContext",
    ]
    assert len(wb[rankings.DISPLAY_SHEET_TITLE]._charts) == 4
```

- [ ] **Step 4: Run the full test module and verify it fails for missing implementation.**

```powershell
python -m unittest tests.test_llm_stats_rankings_excel -v
```

### Task 2: Implement Fetch, Cache, Extraction, And Normalization

**Files:**
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/generate_llm_stats_rankings_excel.py`
- Modify: `E:/Project/实习/research_skills/llm-stats-rankings/tests/test_llm_stats_rankings_excel.py`
- Test: `E:/Project/实习/research_skills/llm-stats-rankings/tests/test_llm_stats_rankings_excel.py`

- [ ] **Step 1: Implement curl-based HTML fetching with cache fallback.**

```python
def load_homepage_html(cache_path: Path) -> str:
    try:
        html = fetch_homepage_html()
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(html, encoding="utf-8")
        return html
    except Exception:
        if cache_path.exists():
            return cache_path.read_text(encoding="utf-8")
        raise
```

- [ ] **Step 2: Implement balanced-block extraction for `initialHomepageLLMModels`.**

```python
marker = 'initialHomepageLLMModels\\\\":'
marker_idx = html.find(marker)
array_start = html.find("[", marker_idx)
raw_array = extract_balanced_block(html, array_start, "[", "]")
decoded_array = bytes(raw_array, "utf-8").decode("unicode_escape")
rows = json.loads(decoded_array)
```

- [ ] **Step 3: Normalize the extracted rows into flat workbook-ready records.**

```python
normalized.append(
    {
        "rank": idx + 1,
        "model_id": row["model_id"],
        "name": row["name"],
        "chat_arena_score": row.get("arena_scores", {}).get("chat-arena"),
        "coding_arena_score": row.get("arena_scores", {}).get("coding-arena"),
        "license": "Open Source" if row.get("is_open_source") else "Proprietary",
    }
)
```

- [ ] **Step 4: Re-run the extraction tests and make sure they pass.**

```powershell
python -m unittest tests.test_llm_stats_rankings_excel.LLMStatsExtractionTests -v
```

### Task 3: Implement Workbook And CSV Outputs

**Files:**
- Modify: `E:/Project/实习/research_skills/llm-stats-rankings/generate_llm_stats_rankings_excel.py`
- Modify: `E:/Project/实习/research_skills/llm-stats-rankings/tests/test_llm_stats_rankings_excel.py`
- Output: `E:/Project/实习/research_skills/llm-stats-rankings/output/spreadsheet/llm_stats_models.xlsx`
- Output: `E:/Project/实习/research_skills/llm-stats-rankings/output/spreadsheet/llm_stats_homepage_models.csv`
- Output: `E:/Project/实习/research_skills/llm-stats-rankings/output/spreadsheet/llm_stats_top20.csv`

- [ ] **Step 1: Build workbook sheets for raw data and chart helpers.**

```python
wb.create_sheet(META_SHEET)
wb.create_sheet(RAW_MODELS_SHEET)
wb.create_sheet(DATA_TOP20_SHEET)
wb.create_sheet(DATA_CODING_SHEET)
wb.create_sheet(DATA_CHAT_SHEET)
wb.create_sheet(DATA_BENCHMARKS_SHEET)
wb.create_sheet(DATA_PRICE_CONTEXT_SHEET)
```

- [ ] **Step 2: Add the display page summary block, Top 20 table, and four charts.**

```python
coding_chart = BarChart()
chat_chart = BarChart()
benchmarks_chart = BarChart()
price_context_chart = ScatterChart()
```

- [ ] **Step 3: Export normalized CSV files for all models and Top 20.**

```python
write_csv(all_models_csv_path, normalized_rows)
write_csv(top20_csv_path, normalized_rows[:20])
```

- [ ] **Step 4: Re-run the full unit test module and make sure it passes.**

```powershell
python -m unittest tests.test_llm_stats_rankings_excel -v
```

### Task 4: Add Skill Wrappers, Docs, And Verification

**Files:**
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/README.md`
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/skills/llm-stats-data-refresh/SKILL.md`
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/skills/llm-stats-data-refresh/references/workflow.md`
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/skills/llm-stats-data-refresh/scripts/run_data_refresh.py`
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/skills/llm-stats-chart-refresh/SKILL.md`
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/skills/llm-stats-chart-refresh/references/layout-reference.md`
- Create: `E:/Project/实习/research_skills/llm-stats-rankings/skills/llm-stats-chart-refresh/scripts/run_chart_refresh.py`
- Modify: `E:/Project/实习/research_skills/README.md`

- [ ] **Step 1: Document commands, outputs, and project structure in the project README.**
- [ ] **Step 2: Add a data-refresh skill that wraps `--mode data-refresh`.**
- [ ] **Step 3: Add a chart-refresh skill that wraps `--mode chart-refresh`.**
- [ ] **Step 4: Register the new project in the repository root README.**

### Task 5: Smoke Verify Real Outputs

**Files:**
- Modify: `E:/Project/实习/research_skills/llm-stats-rankings/generate_llm_stats_rankings_excel.py`
- Output: `E:/Project/实习/research_skills/llm-stats-rankings/output/spreadsheet/llm_stats_models.xlsx`
- Output: `E:/Project/实习/research_skills/llm-stats-rankings/output/spreadsheet/llm_stats_homepage_models.csv`
- Output: `E:/Project/实习/research_skills/llm-stats-rankings/output/spreadsheet/llm_stats_top20.csv`
- Output: `E:/Project/实习/research_skills/llm-stats-rankings/tmp/api-cache/llm_stats_homepage.html`
- Output: `E:/Project/实习/research_skills/llm-stats-rankings/tmp/api-cache/llm_stats_homepage_models.json`

- [ ] **Step 1: Run a full refresh against the live site.**

```powershell
python generate_llm_stats_rankings_excel.py --mode full
```

- [ ] **Step 2: Inspect the workbook sheet names and chart count.**

```powershell
@'
from openpyxl import load_workbook
wb = load_workbook("output/spreadsheet/llm_stats_models.xlsx")
print(wb.sheetnames)
print(len(wb["展示页"]._charts))
'@ | python -
```

- [ ] **Step 3: Inspect the CSV row counts and Top 20 rank range.**

```powershell
@'
import csv
from pathlib import Path
for name in ["llm_stats_homepage_models.csv", "llm_stats_top20.csv"]:
    rows = list(csv.DictReader((Path("output/spreadsheet") / name).open(encoding="utf-8-sig")))
    print(name, len(rows), rows[0]["rank"], rows[-1]["rank"])
'@ | python -
```

- [ ] **Step 4: If any live fetch issue appears, fix the fetch/cache path and rerun verification.**
