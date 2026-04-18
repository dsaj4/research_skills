---
name: company-wechat-rss-fetch
description: Use when collecting company WeChat public account data, crawling gongzhonghao articles through WeWe RSS, exporting WeChat article metadata/content to JSON or CSV, or maintaining a company-to-feed mapping for repeatable public-account data collection.
---

# Company WeChat RSS Fetch

Use this self-contained skill to create and operate a workspace-local wrapper around `wewe-rss`.

## Core rule

Do not assume the current repository already contains `company_wechat_rss.py` or runtime scripts. If the current workspace does not already have a prepared project, bootstrap one from this skill first.

## Quick workflow

1. Read [workflow.md](references/workflow.md) when you need command details.
2. Bootstrap the project into the current workspace:
   `python <skill-dir>\scripts\bootstrap_company_wechat_rss.py --workspace .`
3. Enter the generated project:
   `cd company-wechat-rss`
4. Prepare the local SQLite `wewe-rss` runtime:
   `powershell -ExecutionPolicy Bypass -File .\scripts\prepare_wewe_rss_runtime.ps1`
5. Start the dashboard/API:
   `powershell -ExecutionPolicy Bypass -File .\scripts\start_wewe_rss.ps1`
6. Open `http://127.0.0.1:4000/dash`, log in with WeRead QR code, and add target public accounts.
7. List current feeds:
   `python .\company_wechat_rss.py list-feeds --output .\output\feed_catalog.json`
8. Fill `config\company_accounts.template.json` or create a project-specific config copy.
9. Export company-grouped article data:
   `python .\company_wechat_rss.py export-company-data --config .\config\company_accounts.template.json`
10. Report the generated JSON, CSV, feed catalog, and manifest paths.

## Bundled resources

- `scripts/bootstrap_company_wechat_rss.py`: creates a project in the current workspace, copies wrapper scripts/config, and clones `https://github.com/cooderl/wewe-rss`.
- `assets/company-wechat-rss-project/`: template project copied by the bootstrap script.
- `references/workflow.md`: detailed command sequence and recovery notes.

## Safety notes

- The bootstrap script preserves existing files by default. Use `--force` only when the user wants to overwrite scaffold files.
- The upstream WeRead login step is manual because `wewe-rss` requires QR-code authentication.
- Exported data covers article metadata and feed JSON content available from `wewe-rss`; deeper engagement metrics such as reads/likes/comments are not guaranteed.
