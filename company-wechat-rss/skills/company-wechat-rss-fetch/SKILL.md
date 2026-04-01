---
name: company-wechat-rss-fetch
description: Use when the user wants to collect company WeChat public account data, subscribe to company公众号 sources through a local WeWe RSS instance, export公众号 article metadata into JSON or CSV, or maintain a company-to-feed mapping for repeated WeChat data collection.
---

# Company WeChat RSS Fetch

Use this skill to run the local `company-wechat-rss` workflow that wraps `wewe-rss`.

## What this skill covers

- Prepare the vendored `wewe-rss` runtime with SQLite
- Start the local dashboard and API
- Add public accounts through the `wewe-rss` dashboard
- Discover feed ids from the current subscription catalog
- Export company-grouped article data into JSON and CSV

## When to use

Use this skill whenever the user asks to:

- crawl company公众号 content
- collect WeChat public account article metadata
- build or refresh a company公众号 dataset
- list current `wewe-rss` subscriptions
- export company-to-feed article snapshots

## Workflow

1. Read [workflow.md](references/workflow.md) for the exact command sequence.
2. Prepare the runtime:
   `powershell -ExecutionPolicy Bypass -File .\scripts\prepare_wewe_rss_runtime.ps1`
3. Start the service:
   `powershell -ExecutionPolicy Bypass -File .\scripts\start_wewe_rss.ps1`
4. Open `http://127.0.0.1:4000/dash`, then add a WeRead account and target public accounts.
5. Save the current feed catalog:
   `python .\company_wechat_rss.py list-feeds --output .\output\feed_catalog.json`
6. Fill `config\company_accounts.template.json` or create a project-specific copy.
7. Export grouped data:
   `python .\company_wechat_rss.py export-company-data --config .\config\company_accounts.template.json`
8. Report the generated JSON and CSV paths.

## Important note

The first account login step is manual because upstream `wewe-rss` requires QR-code authentication against WeRead. After that, feed discovery and data export are scriptable.
