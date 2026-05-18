from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference, ScatterChart, Series
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


SOURCE_URL = "https://artificialanalysis.ai/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
)

DISPLAY_SHEET_TITLE = "Display"
META_SHEET = "Meta"
RAW_MODELS_SHEET = "Raw_Models"
DATA_TOP20_SHEET = "Data_Top20"
DATA_PRIMARY_SHEET = "Data_Primary"
DATA_SECONDARY_SHEET = "Data_Secondary"
DATA_BENCHMARKS_SHEET = "Data_Benchmarks"
DATA_PRICE_CONTEXT_SHEET = "Data_PriceContext"

DISPLAY_PAGE_TITLE = "Artificial Analysis Main Leaderboards"
DISPLAY_PAGE_SUBTITLE = "Homepage Intelligence, Speed, and Price highlight datasets captured into a reusable workbook."
DISPLAY_TOP_LEFT_TITLE = "[Intelligence] Top 10"
DISPLAY_TOP_RIGHT_TITLE = "[Speed] Top 10"
DISPLAY_BOTTOM_LEFT_TITLE = "[Price] Lowest 10"
DISPLAY_BOTTOM_RIGHT_TITLE = "[Intelligence vs Price] Snapshot"
DISPLAY_REFRESHED_AT_LABEL = "Display refreshed: "
DISPLAY_DATA_REFRESHED_LABEL = "Data refreshed: "
DISPLAY_PLACEHOLDER_NOTE = "Data layer refreshed. Run chart-refresh to rebuild the display page."
DISPLAY_MODEL_COUNT_LABEL = "Model count: "
DISPLAY_CHART_SCOPE_LABEL = "Chart scope: "

PRIMARY_METRIC_KEY = "primary_score"
PRIMARY_METRIC_LABEL = "Intelligence Index"
SECONDARY_METRIC_KEY = "secondary_score"
SECONDARY_METRIC_LABEL = "Output Tokens / s"
BENCHMARK_ONE_KEY = "benchmark_one_score"
BENCHMARK_ONE_LABEL = "USD / 1M Tokens"
BENCHMARK_TWO_KEY = "benchmark_two_score"
BENCHMARK_TWO_LABEL = "Unused"

RAW_MODEL_HEADERS = [
    "rank",
    "model_id",
    "name",
    "organization",
    "organization_id",
    "primary_score",
    "secondary_score",
    "benchmark_one_score",
    "benchmark_two_score",
    "reference_score",
    "context",
    "context_display",
    "input_price",
    "input_price_display",
    "output_price",
    "output_price_display",
    "license",
    "announcement_date",
    "source_url",
    "generated_at",
]

TITLE_FILL = PatternFill("solid", fgColor="0F172A")
HEADER_FILL = PatternFill("solid", fgColor="E2E8F0")
TABLE_HEADER_FILL = PatternFill("solid", fgColor="1E293B")
SUMMARY_HEADER_FILL = PatternFill("solid", fgColor="E8EEF7")
SUMMARY_NOTE_FILL = PatternFill("solid", fgColor="F8FAFC")
HIGHLIGHT_BLUE = "196BA5"
ACCENT_BLUE = "7699C8"
ACCENT_GOLD = "948A54"


def current_timestamp() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S %Z")


def fetch_source_html(url: str = SOURCE_URL) -> str:
    command = [
        "curl.exe",
        "-L",
        url,
        "-H",
        f"User-Agent: {USER_AGENT}",
        "-H",
        f"Referer: {SOURCE_URL}",
        "--max-time",
        "180",
        "--silent",
        "--show-error",
    ]
    result = subprocess.run(command, check=True, capture_output=True)
    return result.stdout.decode("utf-8", errors="replace")


def load_source_html(cache_path: Path) -> str:
    try:
        html = fetch_source_html()
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(html, encoding="utf-8")
        return html
    except Exception:
        if cache_path.exists():
            return cache_path.read_text(encoding="utf-8")
        raise


def extract_balanced_block(text: str, start_idx: int, open_char: str = "[", close_char: str = "]") -> str:
    depth = 0
    in_string = False
    escaped = False
    for idx in range(start_idx, len(text)):
        char = text[idx]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return text[start_idx : idx + 1]
    raise ValueError("Unbalanced block while extracting source payload")


def extract_homepage_datasets_from_html(html: str) -> dict[str, dict[str, object]]:
    datasets: dict[str, dict[str, object]] = {}
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        raw_payload = match.group(1).strip()
        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict):
            continue
        if payload.get("@type") != "Dataset":
            continue
        name = payload.get("name")
        if name in {"Intelligence", "Speed", "Price"}:
            datasets[str(name)] = payload
    return datasets


def extract_source_rows_from_html(html: str) -> list[dict[str, object]]:
    datasets = extract_homepage_datasets_from_html(html)
    required = {"Intelligence", "Speed", "Price"}
    missing = required - set(datasets)
    if missing:
        raise ValueError(f"Missing homepage datasets: {sorted(missing)}")

    merged_rows: dict[str, dict[str, object]] = {}
    dataset_specs = [
        ("Intelligence", "intelligenceIndex", "intelligence_index"),
        ("Speed", "medianOutputSpeed", "output_speed"),
        ("Price", "pricePerMillionTokens", "price_per_million_tokens"),
    ]

    for dataset_name, source_key, target_key in dataset_specs:
        for item in datasets[dataset_name].get("data", []):
            if not isinstance(item, dict):
                continue
            details_url = str(item.get("detailsUrl") or "").strip()
            if not details_url:
                continue
            row = merged_rows.setdefault(
                details_url,
                {
                    "details_url": details_url,
                    "model_id": details_url.rsplit("/", 1)[-1],
                    "name": item.get("modelName"),
                    "organization": "",
                    "organization_id": "",
                    "license": "",
                    "announcement_date": None,
                },
            )
            if item.get("modelName") and not row.get("name"):
                row["name"] = item.get("modelName")
            row[target_key] = item.get(source_key)

    rows = list(merged_rows.values())
    rows.sort(
        key=lambda row: (
            -(float(row["intelligence_index"]) if row.get("intelligence_index") is not None else -1),
            -(float(row["output_speed"]) if row.get("output_speed") is not None else -1),
            float(row["price_per_million_tokens"]) if row.get("price_per_million_tokens") is not None else 999999.0,
            str(row.get("name") or ""),
        )
    )
    return rows


def format_context(value: int | float | None) -> str:
    if value in (None, ""):
        return ""
    numeric = float(value)
    if numeric >= 1_000_000:
        return f"{numeric / 1_000_000:.1f}M"
    if numeric >= 1_000:
        return f"{numeric / 1_000:.0f}K"
    return f"{numeric:.0f}"


def format_price(value: int | float | None) -> str:
    if value in (None, ""):
        return ""
    return f"${float(value):.2f}"


def normalize_source_rows(raw_rows: list[dict[str, object]], generated_at: str) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    for idx, row in enumerate(raw_rows):
        intelligence_index = row.get("intelligence_index")
        price_per_million_tokens = row.get("price_per_million_tokens")
        normalized.append(
            {
                "rank": idx + 1,
                "model_id": row.get("model_id"),
                "name": row.get("name"),
                "organization": row.get("organization"),
                "organization_id": row.get("organization_id"),
                "primary_score": intelligence_index,
                "secondary_score": row.get("output_speed"),
                "benchmark_one_score": price_per_million_tokens,
                "benchmark_two_score": None,
                "reference_score": price_per_million_tokens,
                "context": intelligence_index,
                "context_display": format_score(intelligence_index),
                "input_price": price_per_million_tokens,
                "input_price_display": format_price(price_per_million_tokens),
                "output_price": None,
                "output_price_display": "",
                "license": row.get("license") or "",
                "announcement_date": row.get("announcement_date"),
                "source_url": SOURCE_URL,
                "generated_at": generated_at,
            }
        )
    return normalized


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RAW_MODEL_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in RAW_MODEL_HEADERS})


def init_snapshot_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS model_snapshots (
                snapshot_at TEXT NOT NULL,
                rank INTEGER,
                model_id TEXT,
                name TEXT,
                organization TEXT,
                organization_id TEXT,
                primary_score REAL,
                secondary_score REAL,
                benchmark_one_score REAL,
                benchmark_two_score REAL,
                reference_score REAL,
                context REAL,
                input_price REAL,
                output_price REAL,
                license TEXT,
                announcement_date TEXT,
                source_url TEXT,
                generated_at TEXT
            )
            '''
        )


def append_snapshot_rows(db_path: Path, rows: list[dict[str, object]], generated_at: str) -> None:
    init_snapshot_db(db_path)
    payload = [
        (
            generated_at,
            row.get("rank"),
            row.get("model_id"),
            row.get("name"),
            row.get("organization"),
            row.get("organization_id"),
            row.get("primary_score"),
            row.get("secondary_score"),
            row.get("benchmark_one_score"),
            row.get("benchmark_two_score"),
            row.get("reference_score"),
            row.get("context"),
            row.get("input_price"),
            row.get("output_price"),
            row.get("license"),
            row.get("announcement_date"),
            row.get("source_url"),
            row.get("generated_at"),
        )
        for row in rows
    ]
    with sqlite3.connect(db_path) as conn:
        conn.executemany(
            '''
            INSERT INTO model_snapshots (
                snapshot_at, rank, model_id, name, organization, organization_id,
                primary_score, secondary_score, benchmark_one_score, benchmark_two_score,
                reference_score, context, input_price, output_price, license,
                announcement_date, source_url, generated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            payload,
        )
def safe_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def format_score(value: object, decimals: int = 2) -> str:
    numeric = safe_float(value)
    if numeric is None:
        return "-"
    return f"{numeric:.{decimals}f}"


def clear_sheet(worksheet) -> None:
    for merged_range in list(worksheet.merged_cells.ranges):
        worksheet.unmerge_cells(str(merged_range))
    if worksheet.max_row:
        worksheet.delete_rows(1, worksheet.max_row)
    worksheet._charts = []
    worksheet.freeze_panes = None


def create_workbook_skeleton() -> Workbook:
    workbook = Workbook()
    workbook.active.title = DISPLAY_SHEET_TITLE
    for title in (
        META_SHEET,
        RAW_MODELS_SHEET,
        DATA_TOP20_SHEET,
        DATA_PRIMARY_SHEET,
        DATA_SECONDARY_SHEET,
        DATA_BENCHMARKS_SHEET,
        DATA_PRICE_CONTEXT_SHEET,
    ):
        workbook.create_sheet(title)
    workbook.active = workbook.sheetnames.index(DISPLAY_SHEET_TITLE)
    return workbook


def ensure_workbook_skeleton(workbook: Workbook) -> Workbook:
    required_titles = [
        DISPLAY_SHEET_TITLE,
        META_SHEET,
        RAW_MODELS_SHEET,
        DATA_TOP20_SHEET,
        DATA_PRIMARY_SHEET,
        DATA_SECONDARY_SHEET,
        DATA_BENCHMARKS_SHEET,
        DATA_PRICE_CONTEXT_SHEET,
    ]
    for title in required_titles:
        if title not in workbook.sheetnames:
            workbook.create_sheet(title)
    workbook.active = workbook.sheetnames.index(DISPLAY_SHEET_TITLE)
    return workbook


def load_rows_from_worksheet(worksheet) -> list[dict[str, object]]:
    headers = [cell.value for cell in worksheet[1]]
    if not any(headers):
        return []
    rows: list[dict[str, object]] = []
    for values in worksheet.iter_rows(min_row=2, values_only=True):
        if not any(value is not None for value in values):
            continue
        rows.append(
            {
                str(headers[idx]): value
                for idx, value in enumerate(values)
                if idx < len(headers) and headers[idx] is not None
            }
        )
    return rows


def write_table_sheet(worksheet, headers: list[str], rows: list[list[object]], number_formats: dict[int, str] | None = None) -> None:
    clear_sheet(worksheet)
    for col_idx, header in enumerate(headers, start=1):
        cell = worksheet.cell(row=1, column=col_idx, value=header)
        cell.font = Font(bold=True, color="F8FAFC")
        cell.fill = TABLE_HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center")
    for row_idx, row_values in enumerate(rows, start=2):
        for col_idx, value in enumerate(row_values, start=1):
            cell = worksheet.cell(row=row_idx, column=col_idx, value=value)
            if number_formats and col_idx in number_formats:
                cell.number_format = number_formats[col_idx]
    worksheet.freeze_panes = "A2"
    for col_idx in range(1, len(headers) + 1):
        worksheet.column_dimensions[get_column_letter(col_idx)].width = 18


def write_raw_models_sheet(worksheet, rows: list[dict[str, object]]) -> None:
    values = [[row.get(header) for header in RAW_MODEL_HEADERS] for row in rows]
    write_table_sheet(worksheet, RAW_MODEL_HEADERS, values)


def write_meta_sheet(worksheet, generated_at: str, row_count: int, data_refreshed_at: str, display_refreshed_at: str) -> None:
    clear_sheet(worksheet)
    worksheet["A1"] = "Artificial Analysis Rankings Snapshot"
    worksheet["A1"].font = Font(size=16, bold=True, color="F8FAFC")
    worksheet["A1"].fill = TITLE_FILL
    meta_rows = [
        ("source_url", SOURCE_URL),
        ("generated_at", generated_at),
        ("data_refreshed_at", data_refreshed_at),
        ("display_refreshed_at", display_refreshed_at),
        ("row_count", row_count),
        ("extraction_method", "Merged homepage JSON-LD datasets: Intelligence, Speed, and Price."),
    ]
    for row_idx, (label, value) in enumerate(meta_rows, start=2):
        worksheet.cell(row=row_idx, column=1, value=label).fill = HEADER_FILL
        worksheet.cell(row=row_idx, column=1).font = Font(bold=True)
        worksheet.cell(row=row_idx, column=2, value=value).fill = HEADER_FILL
    worksheet.column_dimensions["A"].width = 28
    worksheet.column_dimensions["B"].width = 96


def top_n_by_metric(rows: list[dict[str, object]], metric: str, limit: int = 10) -> list[dict[str, object]]:
    filtered = [row for row in rows if row.get(metric) is not None]
    filtered.sort(key=lambda row: float(row[metric]), reverse=True)
    return filtered[:limit]


def top_n_by_context(rows: list[dict[str, object]], limit: int = 10) -> list[dict[str, object]]:
    filtered = [row for row in rows if row.get("context") is not None and row.get("input_price") is not None]
    filtered.sort(key=lambda row: (float(row["context"]), -float(row["input_price"])), reverse=True)
    return filtered[:limit]


def lowest_n_by_metric(rows: list[dict[str, object]], metric: str, limit: int = 10) -> list[dict[str, object]]:
    filtered = [row for row in rows if row.get(metric) is not None]
    filtered.sort(key=lambda row: float(row[metric]))
    return filtered[:limit]


def prepare_display_datasets(rows: list[dict[str, object]]) -> dict[str, object]:
    top20_rows = rows[:20]
    primary_rows = top_n_by_metric(rows, PRIMARY_METRIC_KEY, limit=10)
    secondary_rows = top_n_by_metric(rows, SECONDARY_METRIC_KEY, limit=10)
    benchmark_rows = lowest_n_by_metric(rows, BENCHMARK_ONE_KEY, limit=10)
    price_context_rows = top_n_by_context(top20_rows, limit=10)
    return {
        "top20": top20_rows,
        "primary": primary_rows,
        "secondary": secondary_rows,
        "benchmarks": benchmark_rows,
        "price_context": price_context_rows,
        "model_count": len(rows),
        "chart_scope": "Homepage Intelligence / Speed / Price highlights",
    }


def write_ranked_metric_sheet(worksheet, rows: list[dict[str, object]], metric_key: str, metric_header: str) -> None:
    values = [[row.get("name"), row.get(metric_key)] for row in rows]
    write_table_sheet(worksheet, ["model", metric_header], values, number_formats={2: "0.00"})
    worksheet.column_dimensions["A"].width = 28


def write_benchmark_chart_sheet(worksheet, rows: list[dict[str, object]]) -> None:
    values = [[row.get("name"), row.get(BENCHMARK_ONE_KEY)] for row in rows]
    write_table_sheet(worksheet, ["model", BENCHMARK_ONE_LABEL], values, number_formats={2: "$0.00"})
    worksheet.column_dimensions["A"].width = 28


def write_price_context_chart_sheet(worksheet, rows: list[dict[str, object]]) -> None:
    values = [[row.get("name"), row.get("context"), row.get("input_price")] for row in rows]
    write_table_sheet(worksheet, ["name", "context", "input_price"], values, number_formats={2: "#,##0", 3: "$0.00"})
    worksheet.column_dimensions["A"].width = 28


def write_display_helper_sheets(workbook: Workbook, display_data: dict[str, object]) -> None:
    top20_rows = [
        [row.get("rank"), row.get("name"), row.get("organization"), row.get(PRIMARY_METRIC_KEY), row.get(SECONDARY_METRIC_KEY), row.get(BENCHMARK_ONE_KEY), row.get(BENCHMARK_TWO_KEY)]
        for row in display_data["top20"]
    ]
    write_table_sheet(workbook[DATA_TOP20_SHEET], ["rank", "name", "organization", PRIMARY_METRIC_KEY, SECONDARY_METRIC_KEY, BENCHMARK_ONE_KEY, BENCHMARK_TWO_KEY], top20_rows)
    write_ranked_metric_sheet(workbook[DATA_PRIMARY_SHEET], display_data["primary"], PRIMARY_METRIC_KEY, PRIMARY_METRIC_KEY)
    write_ranked_metric_sheet(workbook[DATA_SECONDARY_SHEET], display_data["secondary"], SECONDARY_METRIC_KEY, SECONDARY_METRIC_KEY)
    write_benchmark_chart_sheet(workbook[DATA_BENCHMARKS_SHEET], display_data["benchmarks"])
    write_price_context_chart_sheet(workbook[DATA_PRICE_CONTEXT_SHEET], display_data["price_context"])
    for sheet_name in (DATA_TOP20_SHEET, DATA_PRIMARY_SHEET, DATA_SECONDARY_SHEET, DATA_BENCHMARKS_SHEET, DATA_PRICE_CONTEXT_SHEET):
        workbook[sheet_name].sheet_state = "hidden"
def write_display_placeholder(worksheet, generated_at: str) -> None:
    clear_sheet(worksheet)
    worksheet.sheet_view.showGridLines = False
    worksheet["A1"] = DISPLAY_PAGE_TITLE
    worksheet["A1"].font = Font(size=16, bold=True)
    worksheet["A2"] = DISPLAY_PLACEHOLDER_NOTE
    worksheet["A3"] = f"{DISPLAY_DATA_REFRESHED_LABEL}{generated_at}"
    configure_display_page_setup(worksheet)


def write_display_summary_headers(worksheet, start_row: int, start_col: int, headers: list[str]) -> None:
    for offset, header in enumerate(headers):
        cell = worksheet.cell(row=start_row, column=start_col + offset, value=header)
        cell.font = Font(bold=True, size=9)
        cell.fill = SUMMARY_HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center")


def style_display_summary_range(worksheet, start_row: int, end_row: int, start_col: int, end_col: int) -> None:
    for row_idx in range(start_row, end_row + 1):
        worksheet.row_dimensions[row_idx].height = 15
        for col_idx in range(start_col, end_col + 1):
            cell = worksheet.cell(row=row_idx, column=col_idx)
            cell.font = Font(size=9)
            cell.alignment = Alignment(vertical="center", shrink_to_fit=True)
            if cell.value is not None:
                cell.fill = SUMMARY_NOTE_FILL


def add_ranked_bar_chart(worksheet, data_sheet, anchor: str, color: str, axis_title: str) -> None:
    chart = BarChart()
    chart.type = "bar"
    chart.style = 10
    chart.legend = None
    chart.width = 13.6
    chart.height = 6.0
    chart.gapWidth = 35
    chart.x_axis.title = axis_title
    chart.y_axis.reverseOrder = True
    chart.add_data(Reference(data_sheet, min_col=2, min_row=1, max_row=data_sheet.max_row), titles_from_data=True)
    chart.set_categories(Reference(data_sheet, min_col=1, min_row=2, max_row=data_sheet.max_row))
    if chart.series:
        chart.series[0].graphicalProperties.solidFill = color
        chart.series[0].graphicalProperties.line.solidFill = color
    worksheet.add_chart(chart, anchor)


def add_benchmark_chart(worksheet, data_sheet, anchor: str) -> None:
    chart = BarChart()
    chart.type = "bar"
    chart.style = 11
    chart.legend = None
    chart.width = 13.6
    chart.height = 6.0
    chart.gapWidth = 35
    chart.x_axis.title = BENCHMARK_ONE_LABEL
    chart.y_axis.reverseOrder = True
    chart.add_data(Reference(data_sheet, min_col=2, min_row=1, max_row=data_sheet.max_row), titles_from_data=True)
    chart.set_categories(Reference(data_sheet, min_col=1, min_row=2, max_row=data_sheet.max_row))
    if chart.series:
        chart.series[0].graphicalProperties.solidFill = HIGHLIGHT_BLUE
        chart.series[0].graphicalProperties.line.solidFill = HIGHLIGHT_BLUE
    worksheet.add_chart(chart, anchor)


def add_price_context_chart(worksheet, data_sheet, anchor: str) -> None:
    chart = ScatterChart()
    chart.scatterStyle = "marker"
    chart.legend = None
    chart.width = 13.6
    chart.height = 6.0
    chart.x_axis.title = PRIMARY_METRIC_LABEL
    chart.y_axis.title = BENCHMARK_ONE_LABEL
    xvalues = Reference(data_sheet, min_col=2, min_row=2, max_row=data_sheet.max_row)
    yvalues = Reference(data_sheet, min_col=3, min_row=2, max_row=data_sheet.max_row)
    chart.series.append(Series(yvalues, xvalues, title="Models"))
    if chart.series:
        chart.series[0].graphicalProperties.solidFill = HIGHLIGHT_BLUE
        chart.series[0].graphicalProperties.line.noFill = True
        chart.series[0].marker.symbol = "circle"
        chart.series[0].marker.size = 7
    worksheet.add_chart(chart, anchor)


def build_display_sheet(worksheet, display_data: dict[str, object], generated_at: str) -> None:
    clear_sheet(worksheet)
    worksheet.sheet_view.showGridLines = False
    worksheet["A1"] = DISPLAY_PAGE_TITLE
    worksheet["A1"].font = Font(size=16, bold=True)
    worksheet["A2"] = DISPLAY_PAGE_SUBTITLE
    worksheet["A3"] = f"{DISPLAY_REFRESHED_AT_LABEL}{generated_at}"
    worksheet["B4"] = DISPLAY_TOP_LEFT_TITLE
    worksheet["M4"] = DISPLAY_TOP_RIGHT_TITLE
    worksheet["B30"] = DISPLAY_BOTTOM_LEFT_TITLE
    worksheet["M30"] = DISPLAY_BOTTOM_RIGHT_TITLE
    for cell_ref in ("B4", "M4", "B30", "M30"):
        worksheet[cell_ref].font = Font(bold=True, size=11)
    worksheet["B19"] = f"{DISPLAY_MODEL_COUNT_LABEL}{display_data['model_count']}"
    worksheet["M19"] = f"{DISPLAY_CHART_SCOPE_LABEL}{display_data['chart_scope']}"
    write_display_summary_headers(worksheet, 20, 2, ["Rank", "Model", PRIMARY_METRIC_LABEL])
    for row_idx, row in enumerate(display_data["primary"][:8], start=21):
        worksheet.cell(row=row_idx, column=2, value=row_idx - 20)
        worksheet.cell(row=row_idx, column=3, value=row.get("name"))
        worksheet.cell(row=row_idx, column=4, value=format_score(row.get(PRIMARY_METRIC_KEY)))
    style_display_summary_range(worksheet, 21, 28, 2, 4)
    write_display_summary_headers(worksheet, 20, 13, ["Rank", "Model", SECONDARY_METRIC_LABEL])
    for row_idx, row in enumerate(display_data["secondary"][:8], start=21):
        worksheet.cell(row=row_idx, column=13, value=row_idx - 20)
        worksheet.cell(row=row_idx, column=14, value=row.get("name"))
        worksheet.cell(row=row_idx, column=15, value=format_score(row.get(SECONDARY_METRIC_KEY)))
    style_display_summary_range(worksheet, 21, 28, 13, 15)
    write_display_summary_headers(worksheet, 46, 2, ["Rank", "Model", "Price"])
    for row_idx, row in enumerate(display_data["benchmarks"][:4], start=47):
        worksheet.cell(row=row_idx, column=2, value=row_idx - 46)
        worksheet.cell(row=row_idx, column=3, value=row.get("name"))
        worksheet.cell(row=row_idx, column=4, value=format_price(row.get(BENCHMARK_ONE_KEY)))
    style_display_summary_range(worksheet, 47, 50, 2, 4)
    write_display_summary_headers(worksheet, 46, 13, ["Rank", "Model", "Context / Price"])
    for row_idx, row in enumerate(display_data["price_context"][:8], start=47):
        worksheet.cell(row=row_idx, column=13, value=row_idx - 46)
        worksheet.cell(row=row_idx, column=14, value=row.get("name"))
        worksheet.cell(row=row_idx, column=15, value=f"{row.get('context_display')} / {format_price(row.get('input_price'))}")
    style_display_summary_range(worksheet, 47, 54, 13, 15)
    add_ranked_bar_chart(worksheet, worksheet.parent[DATA_PRIMARY_SHEET], "B6", ACCENT_BLUE, PRIMARY_METRIC_LABEL)
    add_ranked_bar_chart(worksheet, worksheet.parent[DATA_SECONDARY_SHEET], "M6", ACCENT_GOLD, SECONDARY_METRIC_LABEL)
    add_benchmark_chart(worksheet, worksheet.parent[DATA_BENCHMARKS_SHEET], "B32")
    add_price_context_chart(worksheet, worksheet.parent[DATA_PRICE_CONTEXT_SHEET], "M32")
    configure_display_page_setup(worksheet)


def configure_display_page_setup(worksheet) -> None:
    worksheet.print_area = "A1:Q55"
    worksheet.page_setup.orientation = worksheet.ORIENTATION_LANDSCAPE
    worksheet.page_setup.paperSize = worksheet.PAPERSIZE_A3
    worksheet.page_setup.fitToWidth = 1
    worksheet.page_setup.fitToHeight = 1
    worksheet.sheet_properties.pageSetUpPr.fitToPage = True


def write_data_layers(workbook: Workbook, rows: list[dict[str, object]], generated_at: str, display_refreshed_at: str) -> None:
    ensure_workbook_skeleton(workbook)
    display_data = prepare_display_datasets(rows)
    write_meta_sheet(workbook[META_SHEET], generated_at, len(rows), generated_at, display_refreshed_at)
    write_raw_models_sheet(workbook[RAW_MODELS_SHEET], rows)
    write_display_helper_sheets(workbook, display_data)


def refresh_display_layer(workbook: Workbook, generated_at: str) -> None:
    ensure_workbook_skeleton(workbook)
    rows = load_rows_from_worksheet(workbook[RAW_MODELS_SHEET])
    display_data = prepare_display_datasets(rows)
    build_display_sheet(workbook[DISPLAY_SHEET_TITLE], display_data, generated_at)
def build_workbook(rows: list[dict[str, object]], workbook_path: Path, generated_at: str, include_display: bool = True) -> None:
    workbook = create_workbook_skeleton()
    write_data_layers(workbook, rows, generated_at, generated_at if include_display else "")
    if include_display:
        refresh_display_layer(workbook, generated_at)
    else:
        write_display_placeholder(workbook[DISPLAY_SHEET_TITLE], generated_at)
    workbook_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(workbook_path)


def default_paths(repo_root: Path) -> dict[str, Path]:
    output_dir = repo_root / "output"
    return {
        "workbook": output_dir / "spreadsheet" / "artificialanalysis_rankings_models.xlsx",
        "all_models_csv": output_dir / "spreadsheet" / "artificialanalysis_rankings_all_models.csv",
        "top20_csv": output_dir / "spreadsheet" / "artificialanalysis_rankings_top20.csv",
        "snapshot_db": output_dir / "data" / "artificialanalysis_rankings_snapshots.sqlite",
        "cache_html": repo_root / "tmp" / "api-cache" / "artificialanalysis_rankings_source.html",
        "cache_json": repo_root / "tmp" / "api-cache" / "artificialanalysis_rankings_normalized_rows.json",
    }


def fetch_and_normalize_rows(paths: dict[str, Path], generated_at: str) -> list[dict[str, object]]:
    html = load_source_html(paths["cache_html"])
    raw_rows = extract_source_rows_from_html(html)
    normalized_rows = normalize_source_rows(raw_rows, generated_at)
    write_json(paths["cache_json"], normalized_rows)
    write_csv(paths["all_models_csv"], normalized_rows)
    write_csv(paths["top20_csv"], normalized_rows[:20])
    append_snapshot_rows(paths["snapshot_db"], normalized_rows, generated_at)
    return normalized_rows


def run_data_refresh(paths: dict[str, Path]) -> None:
    generated_at = current_timestamp()
    rows = fetch_and_normalize_rows(paths, generated_at)
    if paths["workbook"].exists():
        workbook = load_workbook(paths["workbook"])
        write_data_layers(workbook, rows, generated_at, "")
    else:
        workbook = create_workbook_skeleton()
        write_data_layers(workbook, rows, generated_at, "")
        write_display_placeholder(workbook[DISPLAY_SHEET_TITLE], generated_at)
    paths["workbook"].parent.mkdir(parents=True, exist_ok=True)
    workbook.save(paths["workbook"])


def run_chart_refresh(paths: dict[str, Path]) -> None:
    if not paths["workbook"].exists():
        raise FileNotFoundError(f"Workbook not found for chart-refresh: {paths['workbook']}")
    workbook = load_workbook(paths["workbook"])
    refresh_display_layer(workbook, current_timestamp())
    workbook.save(paths["workbook"])


def run_full_refresh(paths: dict[str, Path]) -> None:
    generated_at = current_timestamp()
    rows = fetch_and_normalize_rows(paths, generated_at)
    build_workbook(rows, paths["workbook"], generated_at=generated_at, include_display=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["full", "data-refresh", "chart-refresh"], default="full")
    args = parser.parse_args()
    paths = default_paths(Path(__file__).resolve().parent)
    if args.mode == "full":
        run_full_refresh(paths)
        return
    if args.mode == "data-refresh":
        run_data_refresh(paths)
        return
    run_chart_refresh(paths)


if __name__ == "__main__":
    main()
