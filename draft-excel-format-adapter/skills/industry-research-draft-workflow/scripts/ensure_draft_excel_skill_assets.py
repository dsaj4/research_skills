#!/usr/bin/env python
"""Check and restore industry-research-draft-workflow skill assets.

The packaged skill should include all core files. This script is a safety net for
partial installs, hand-copied folders, or future lightweight packages: it checks
the local skill folder against references/asset-manifest.json and downloads any
missing assets from the current GitHub repository by default.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_RAW_BASE_URL = (
    "https://raw.githubusercontent.com/dsaj4/research_skills/main/"
    "draft-excel-format-adapter/skills/industry-research-draft-workflow"
)


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest(skill_root: Path) -> dict:
    manifest_path = skill_root / "references" / "asset-manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing asset manifest: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def normalize_raw_base_url(raw_base_url: str) -> str:
    return raw_base_url.rstrip("/")


def download_text(url: str, timeout: int) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "industry-research-draft-workflow/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
    return data.decode("utf-8")


def restore_asset(skill_root: Path, raw_base_url: str, rel_path: str, timeout: int) -> None:
    target = skill_root / rel_path
    url_path = rel_path.replace("\\", "/")
    url = f"{normalize_raw_base_url(raw_base_url)}/{url_path}"
    text = download_text(url, timeout=timeout)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="")


def check_assets(skill_root: Path, raw_base_url: str, dry_run: bool, timeout: int) -> int:
    manifest = load_manifest(skill_root)
    raw_base_url = raw_base_url or manifest.get("default_raw_base_url") or DEFAULT_RAW_BASE_URL

    restored = []
    missing = []
    failed = []

    for asset in manifest.get("assets", []):
        rel_path = asset["path"]
        target = skill_root / rel_path
        if target.exists():
            continue

        missing.append(rel_path)
        if dry_run:
            continue

        try:
            restore_asset(skill_root, raw_base_url, rel_path, timeout)
            restored.append(rel_path)
        except (OSError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            failed.append((rel_path, str(exc)))

    if missing:
        print("Missing assets:")
        for rel_path in missing:
            print(f"  - {rel_path}")
    else:
        print("All manifest assets are present.")

    if restored:
        print("Restored assets:")
        for rel_path in restored:
            print(f"  - {rel_path}")

    if failed:
        print("Failed to restore assets:", file=sys.stderr)
        for rel_path, error in failed:
            print(f"  - {rel_path}: {error}", file=sys.stderr)
        return 2

    if dry_run and missing:
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or restore draft Excel skill assets.")
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=skill_root_from_script(),
        help="Installed industry-research-draft-workflow skill folder.",
    )
    parser.add_argument(
        "--raw-base-url",
        default="",
        help="Raw GitHub base URL for the skill folder. Defaults to this repo's main branch.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Only report missing assets.")
    parser.add_argument("--timeout", type=int, default=30, help="Download timeout in seconds.")
    args = parser.parse_args()

    return check_assets(args.skill_root.resolve(), args.raw_base_url, args.dry_run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
