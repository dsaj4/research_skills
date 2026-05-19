#!/usr/bin/env python
"""Package industry-research-draft-workflow as a .skill zip archive."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL_ROOT = PROJECT_ROOT / "skills" / "industry-research-draft-workflow"
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "skill-packages" / "industry-research-draft-workflow.skill"


EXCLUDED_PARTS = {"__pycache__", ".pytest_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def iter_package_files(skill_root: Path):
    for path in sorted(skill_root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            continue
        yield path


def package_skill(skill_root: Path, output_path: Path) -> Path:
    skill_root = skill_root.resolve()
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    package_root_name = skill_root.name
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in iter_package_files(skill_root):
            rel_path = path.relative_to(skill_root)
            zf.write(path, Path(package_root_name) / rel_path)

    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Package industry-research-draft-workflow skill.")
    parser.add_argument("--skill-root", type=Path, default=DEFAULT_SKILL_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    packaged = package_skill(args.skill_root, args.output)
    print(packaged)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
