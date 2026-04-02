from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    subprocess.run(
        [
            sys.executable,
            str(project_root / "generate_artificialanalysis_rankings_excel.py"),
            "--mode",
            "data-refresh",
        ],
        check=True,
        cwd=project_root,
    )


if __name__ == "__main__":
    main()
