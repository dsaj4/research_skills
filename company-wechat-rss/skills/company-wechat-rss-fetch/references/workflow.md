# Workflow

## 1. Prepare the vendored runtime

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\prepare_wewe_rss_runtime.ps1
```

This step:

- switches the vendored upstream server to the SQLite Prisma schema
- writes local `.env` files for the server and web app
- installs dependencies with `corepack pnpm`
- runs Prisma generate and initializes the SQLite schema
- builds the dashboard and server

## 2. Start the local server

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_wewe_rss.ps1
```

The dashboard is served at:

```text
http://127.0.0.1:4000/dash
```

## 3. Add data sources

In the dashboard:

1. Open the account page and log in with a WeRead QR code.
2. Open the feeds page.
3. Paste one or more public article share links to subscribe public accounts.

## 4. Inspect feed ids

Run:

```powershell
python .\company_wechat_rss.py list-feeds --output .\output\feed_catalog.json
```

Use this catalog to fill your company-to-feed mapping file.

## 5. Export company-grouped data

Run:

```powershell
python .\company_wechat_rss.py export-company-data --config .\config\company_accounts.template.json
```

Optional:

```powershell
python .\company_wechat_rss.py export-company-data --config .\config\company_accounts.template.json --update
```

`--update` triggers async refresh calls before reading the current feed snapshot.

## 6. Stop the local service

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop_wewe_rss.ps1
```
