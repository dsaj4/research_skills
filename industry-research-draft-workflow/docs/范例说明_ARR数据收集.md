# 范例说明：ARR 数据收集底稿

本范例对应文件：

- `01_当前底稿/ARR数据收集.xlsx`
- `03_来源截图整理/ARR数据收集_来源截图/contact_sheet_validated_final.png`

## 背景

本次任务是收集：

1. 大模型公司的 ARR / 年化运行收入。
2. AI 应用的 ARR / 年化运行收入，包括 Claude Code、Codex、Cursor、Lovable、Perplexity 等。

由于不同公司披露口径不一致，本范例特别强调区分：

- 年度经常性收入
- 年化运行收入
- 年化收入估算
- 年度收入估算
- 未披露/目标 ARR

## 最终底稿结构

`ARR数据收集.xlsx` 包含 5 张表：

- `数据总表`：汇总所有条目。
- `大模型公司`：公司层面的收入口径。
- `AI应用`：应用/产品层面的收入口径。
- `证据底稿`：两列结构，左侧为数据表述，右侧为真实截图。
- `待核验`：记录未来需要继续确认的问题。

## 本案例中的关键最佳实践

### 1. 不混用收入口径

例如：

- OpenAI 的官方口径为 `年度经常性收入`。
- Anthropic 的官方口径为 `年化运行收入`。
- Sacra 等第三方页面中的数据标为 `分析师/第三方估算`。

### 2. 截图必须命中数据

第一轮截图中有些只截到标题、广告、公司概览或反爬页。最终版进行了视觉校验和重截：

- Anthropic：重截到 `$30 billion` 正文段落。
- OpenAI：重截到 `$20B+ in 2025` 正文段落。
- Cohere：重截到 `$240M` 标题与正文。
- Cursor：Bloomberg 反爬，改用 TechCrunch 可访问来源。
- Replit：官方博客被 Cloudflare 拦截，改用 TechCrunch 可访问来源。
- Runway：原融资新闻不能支撑 ARR 估算，改用 Sacra 数据页。

### 3. 证据截图和来源链接同时保留

`证据底稿` 右列嵌入截图，原始链接保存在单元格批注里。这样审阅时能直接看图，也能回到原始网页复核。

### 4. 最终交付中文化

表头和枚举值均为中文，例如：

- `source_type` 改为 `来源类型`
- `confidence` 改为 `置信度`
- `official` 改为 `官方披露`
- `media` 改为 `媒体报道`
- `run-rate revenue` 改为 `年化运行收入`

最终文件命名为 `ARR数据收集.xlsx`。

## 可复用脚本

本案例脚本保存在 `02_生成脚本/`：

- `generate_arr_excel_draft.py`：生成初版结构化 Excel。
- `embed_evidence_screenshots.py`：将截图嵌入证据底稿。
- `reformat_arr_excel_evidence.py`：转换为两列证据结构。
- `visual_validate_and_recapture.py`：定位关键词并重截截图。
- `recapture_remaining.py`：补截失败或被拦截页面。
- `recapture_cohere.py`：单项补截示例。
- `localize_arr_excel_fields.py`：字段和枚举值中文化。

## 交付标准

本案例交付前完成了以下校验：

- Excel 可读取。
- `证据底稿` 为 16 行 x 2 列。
- 内嵌 15 张真实网页截图。
- 每张截图均经视觉校验，包含对应数据或支撑信息。
- 表头、枚举值和最终文件名均已中文化。
