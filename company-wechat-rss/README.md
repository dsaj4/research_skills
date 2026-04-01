# Company WeChat RSS

This project wraps [wewe-rss](https://github.com/cooderl/wewe-rss) into a repo-local workflow for collecting company WeChat public account data.

It keeps the upstream service source in `vendor/wewe-rss/`, starts it locally with SQLite, and exports company-grouped article metadata into JSON and CSV files.

## What Is Included

- `vendor/wewe-rss/`: vendored upstream source cloned from `cooderl/wewe-rss`
- `company_wechat_rss.py`: Python CLI for feed discovery and company data export
- `scripts/prepare_wewe_rss_runtime.ps1`: prepare the local `wewe-rss` runtime with SQLite
- `scripts/init_wewe_rss_sqlite.py`: initialize the local SQLite schema used by the vendored server
- `scripts/start_wewe_rss.ps1`: start `wewe-rss` in the background
- `scripts/stop_wewe_rss.ps1`: stop the local background service
- `skills/company-wechat-rss-fetch/`: repo-local skill that documents the workflow
- `tests/`: unit tests for the export layer

## Upstream Source

- Upstream repository: `https://github.com/cooderl/wewe-rss`
- Vendored snapshot commit: `e751c64294080d83deb1610d2667bed3cfa4b393`

## Quick Start

From this project directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\prepare_wewe_rss_runtime.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\start_wewe_rss.ps1
python .\company_wechat_rss.py list-feeds --output .\output\feed_catalog.json
python .\company_wechat_rss.py export-company-data --config .\config\company_accounts.template.json
```

## First-Time Onboarding

1. Run the prepare and start scripts.
2. Open `http://127.0.0.1:4000/dash`.
3. In the dashboard, add a WeRead account by scanning the QR code.
4. Add target public accounts by pasting one or more article share links.
5. Run `list-feeds` to inspect the current feed ids.
6. Fill `config/company_accounts.template.json` with the company-to-feed mapping.
7. Run `export-company-data` to generate structured outputs.

## Main CLI Commands

```powershell
python .\company_wechat_rss.py list-feeds --base-url http://127.0.0.1:4000
python .\company_wechat_rss.py export-company-data --config .\config\company_accounts.template.json
python -m unittest tests.test_company_wechat_rss -v
```

## Output Contract

Exports are written under `output/company-data/<timestamp>/`:

- `company_articles.json`: normalized article records
- `company_articles.csv`: spreadsheet-friendly flat export
- `feed_catalog.json`: feed catalog snapshot used during the run
- `export_manifest.json`: metadata for the export

Temporary runtime files are written under `tmp/wewe-rss/`.

## Notes

- `wewe-rss` requires a manual QR-code login step for the first account connection.
- `export-company-data --update` can trigger async feed refreshes, but the HTTP response may still reflect the current cached snapshot. Use it when you want to kick off an update before the next export, not as a strict freshness guarantee.
