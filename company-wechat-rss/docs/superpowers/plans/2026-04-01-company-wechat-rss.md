# Company WeChat RSS Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wrap `wewe-rss` into a standalone repo-local skill project for collecting company公众号 article data.

**Architecture:** Vendor upstream `wewe-rss`, prepare it locally with SQLite, and add a Python export layer plus PowerShell runtime scripts and skill documentation.

**Tech Stack:** Python, PowerShell, Node.js, corepack pnpm, Prisma SQLite, vendored `wewe-rss`

---

### Task 1: Project Skeleton

**Files:**
- Create: `company-wechat-rss/README.md`
- Create: `company-wechat-rss/output/README.md`
- Create: `company-wechat-rss/tmp/README.md`
- Create: `company-wechat-rss/docs/superpowers/specs/2026-04-01-company-wechat-rss-design.md`

- [ ] Create the standalone project directories.
- [ ] Document the project goal, layout, and outputs.

### Task 2: Upstream Runtime Integration

**Files:**
- Create: `company-wechat-rss/scripts/prepare_wewe_rss_runtime.ps1`
- Create: `company-wechat-rss/scripts/start_wewe_rss.ps1`
- Create: `company-wechat-rss/scripts/stop_wewe_rss.ps1`
- Vendor: `company-wechat-rss/vendor/wewe-rss`

- [ ] Vendor the upstream `wewe-rss` source into the new project.
- [ ] Write a preparation script that switches the vendored server to SQLite and builds it locally.
- [ ] Write start and stop scripts for a repeatable background runtime.

### Task 3: Export Layer

**Files:**
- Create: `company-wechat-rss/company_wechat_rss.py`
- Create: `company-wechat-rss/config/company_accounts.template.json`

- [ ] Build a Python CLI for feed discovery and company-grouped export.
- [ ] Normalize JSON feed items into a flat record format.
- [ ] Write JSON, CSV, and manifest outputs.

### Task 4: Skill Documentation

**Files:**
- Create: `company-wechat-rss/skills/company-wechat-rss-fetch/SKILL.md`
- Create: `company-wechat-rss/skills/company-wechat-rss-fetch/references/workflow.md`

- [ ] Document the full workflow as a repo-local skill.
- [ ] Explain the manual first-login step and the scripted export path.

### Task 5: Verification

**Files:**
- Create: `company-wechat-rss/tests/test_company_wechat_rss.py`
- Create: `company-wechat-rss/tests/fixtures/sample_feed_catalog.json`
- Create: `company-wechat-rss/tests/fixtures/sample_feed_tencent.json`

- [ ] Add unit tests for config normalization and export output writing.
- [ ] Run the Python unit test suite.
- [ ] Start the local vendored service and verify `/feeds/` responds.
