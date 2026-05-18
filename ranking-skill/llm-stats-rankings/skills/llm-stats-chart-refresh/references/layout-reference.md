# Chart Refresh Layout Reference

The display page should keep a practical workbook-first layout:

- title and refresh metadata at the top
- a compact Top 20 snapshot table on the left
- four charts arranged in a two-by-two grid

Current chart set:

1. Coding Arena Top 20
2. Chat Arena Top 20
3. GPQA vs SWE-Bench Verified
4. Input Price vs Context Window

## Command

```powershell
python generate_llm_stats_rankings_excel.py --mode chart-refresh
```
