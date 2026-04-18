# Workflow

## 1. Bootstrap a project in the current workspace

Run the bundled bootstrap script from the installed skill directory:

```powershell
python <skill-dir>\scripts\bootstrap_company_wechat_rss.py --workspace .
```

Useful options:

```powershell
python <skill-dir>\scripts\bootstrap_company_wechat_rss.py --workspace . --project-name wechat-data
python <skill-dir>\scripts\bootstrap_company_wechat_rss.py --project-dir E:\data\company-wechat-rss
python <skill-dir>\scripts\bootstrap_company_wechat_rss.py --workspace . --skip-clone
```

The script copies `assets/company-wechat-rss-project/` into the target project and clones upstream `wewe-rss` into `vendor/wewe-rss`. Existing files are preserved unless `--force` is passed.

## 2. Prepare the runtime

Enter the generated project, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\prepare_wewe_rss_runtime.ps1
```

This step:

- switches upstream `wewe-rss` to the SQLite Prisma schema
- writes local `.env` files for the server and web app
- installs dependencies with `corepack pnpm`
- runs Prisma generate and initializes the SQLite schema
- builds the dashboard and server

## 3. Start the local server

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_wewe_rss.ps1
```

The dashboard is served at:

```text
http://127.0.0.1:4000/dash
```

## 4. Add data sources

In the dashboard:

1. Open the account page and log in with a WeRead QR code.
2. Open the feeds page.
3. Paste one or more public article share links to subscribe public accounts.

## 5. Inspect feed ids

Run:

```powershell
python .\company_wechat_rss.py list-feeds --output .\output\feed_catalog.json
```

Use this catalog to fill your company-to-feed mapping file.

## 6. Export company-grouped data

Run:

```powershell
python .\company_wechat_rss.py export-company-data --config .\config\company_accounts.template.json
```

Optional refresh:

```powershell
python .\company_wechat_rss.py export-company-data --config .\config\company_accounts.template.json --update
```

Outputs are written under `output/company-data/<run-label-or-timestamp>/`:

- `company_articles.json`
- `company_articles.csv`
- `feed_catalog.json`
- `export_manifest.json`

## 7. Stop the local service

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop_wewe_rss.ps1
```

## Recovery notes

- If `prepare_wewe_rss_runtime.ps1` says `corepack` or `pnpm` is missing, install/enable a current Node.js runtime and rerun.
- If bootstrap was run with `--skip-clone`, rerun without it before preparing the runtime.
- If the server starts but the health check is not ready, inspect `tmp/wewe-rss/server.log`.
