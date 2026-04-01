# Company WeChat RSS Design

## Goal

Create a standalone skill project that wraps `wewe-rss` so the repo can collect company WeChat public account data with a repeatable local workflow.

## Architecture

- Vendor the upstream `wewe-rss` source under this project so the integration stays self-contained.
- Prepare the upstream runtime locally with SQLite and `corepack pnpm`.
- Keep feed subscription management in the upstream dashboard because the first login requires QR-code authentication.
- Add a repo-local export layer that reads public JSON feeds from `wewe-rss` and writes company-grouped JSON and CSV outputs.
- Document the complete workflow as a repo-local skill.

## Key Decisions

- Use SQLite for local setup because it avoids introducing MySQL or Docker as required dependencies.
- Treat `wewe-rss` as the source-of-truth service for feed discovery and article collection.
- Use Python for the export layer because the repository already includes Python-based skill projects and tests.

## Non-Goals

- Re-implement upstream WeRead login or article crawling logic.
- Replace the upstream dashboard UI.
- Guarantee synchronous freshness when using `update=true`, because upstream refresh calls are asynchronous.
