#!/usr/bin/env python
"""Check and restore industry-research-draft-workflow skill assets.

The packaged skill should include all core files, template assets, and example
assets. This script is a safety net for partial installs, hand-copied folders,
or future lightweight packages: it checks the local skill folder against
references/asset-manifest.json and downloads any missing assets from the current
GitHub repository by default.
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
    "industry-research-draft-workflow/skills/industry-research-draft-workflow"
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


def download_bytes(url: str, timeout: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "industry-research-draft-workflow/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def restore_asset(skill_root: Path, raw_base_url: str, asset: dict, timeout: int) -> None:
    rel_path = asset["path"]
    target = skill_root / rel_path
    url_path = rel_path.replace("\\", "/")
    url = f"{normalize_raw_base_url(raw_base_url)}/{url_path}"
    data = download_bytes(url, timeout=timeout)
    target.parent.mkdir(parents=True, exist_ok=True)
    if asset.get("type") == "binary":
        target.write_bytes(data)
    else:
        target.write_text(data.decode("utf-8"), encoding="utf-8", newline="")


def asset_in_group(asset: dict, selected_group: str) -> bool:
    if selected_group == "all":
        return True
    return asset.get("group", "core") == selected_group


def check_assets(skill_root: Path, raw_base_url: str, group: str, dry_run: bool, timeout: int) -> int:
    manifest = load_manifest(skill_root)
    raw_base_url = raw_base_url or manifest.get("default_raw_base_url") or DEFAULT_RAW_BASE_URL

    restored = []
    missing = []
    failed = []

    for asset in manifest.get("assets", []):
        if not asset_in_group(asset, group):
            continue
        rel_path = asset["path"]
        target = skill_root / rel_path
        if target.exists():
            continue

        missing.append(rel_path)
        if dry_run:
            continue

        try:
            restore_asset(skill_root, raw_base_url, asset, timeout)
            restored.append(rel_path)
        except (OSError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            failed.append((rel_path, str(exc)))

    if missing:
        print(f"Missing assets in group '{group}':")
        for rel_path in missing:
            print(f"  - {rel_path}")
    else:
        print(f"All manifest assets are present for group '{group}'.")

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
    parser.add_argument(
        "--group",
        choices=["all", "core", "templates", "examples"],
        default="all",
        help="Asset group to check/download. Default: all.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Only report missing assets.")
    parser.add_argument("--timeout", type=int, default=30, help="Download timeout in seconds.")
    args = parser.parse_args()

    return check_assets(args.skill_root.resolve(), args.raw_base_url, args.group, args.dry_run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
