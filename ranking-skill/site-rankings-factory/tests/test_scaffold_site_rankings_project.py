from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "skills" / "site-rankings-factory" / "scripts" / "scaffold_site_rankings_project.py"


class SiteRankingsFactoryTests(unittest.TestCase):
    def test_scaffold_creates_project_and_generated_tests_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_root = Path(tmp_dir)

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--project-name",
                    "example-rankings",
                    "--site-name",
                    "Example Rankings",
                    "--source-url",
                    "https://example.com",
                    "--target-root",
                    str(target_root),
                ],
                check=True,
                cwd=PROJECT_ROOT,
            )

            generated_project = target_root / "example-rankings"
            self.assertTrue((generated_project / "README.md").exists())
            self.assertTrue((generated_project / "output" / "README.md").exists())
            self.assertTrue((generated_project / "tmp" / "README.md").exists())
            self.assertTrue(
                (
                    generated_project
                    / "skills"
                    / "example-rankings-data-refresh"
                    / "scripts"
                    / "run_data_refresh.py"
                ).exists()
            )
            self.assertTrue(
                (
                    generated_project
                    / "skills"
                    / "example-rankings-chart-refresh"
                    / "scripts"
                    / "run_chart_refresh.py"
                ).exists()
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "unittest",
                    "tests.test_example_rankings_rankings_excel",
                    "-v",
                ],
                check=True,
                cwd=generated_project,
            )


if __name__ == "__main__":
    unittest.main()
