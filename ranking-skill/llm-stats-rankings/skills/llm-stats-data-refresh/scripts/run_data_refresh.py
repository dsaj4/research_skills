from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    command = [sys.executable, str(repo_root / "generate_llm_stats_rankings_excel.py"), "--mode", "data-refresh", *sys.argv[1:]]
    subprocess.run(command, check=True, cwd=repo_root)


if __name__ == "__main__":
    main()
