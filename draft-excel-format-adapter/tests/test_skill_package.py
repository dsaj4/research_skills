import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / "skills" / "draft-excel-format-adapter"
PACKAGE_SCRIPT = PROJECT_ROOT / "scripts" / "package_draft_excel_skill.py"
ENSURE_SCRIPT = SKILL_ROOT / "scripts" / "ensure_draft_excel_skill_assets.py"


class DraftExcelSkillPackageTests(unittest.TestCase):
    def test_manifest_assets_exist_in_repo_copy(self):
        manifest_path = SKILL_ROOT / "references" / "asset-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        for asset in manifest["assets"]:
            path = SKILL_ROOT / asset["path"]
            self.assertTrue(path.exists(), f"Missing manifest asset: {asset['path']}")

    def test_asset_checker_reports_complete_local_install(self):
        result = subprocess.run(
            [
                "python",
                str(ENSURE_SCRIPT),
                "--skill-root",
                str(SKILL_ROOT),
                "--dry-run",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("All manifest assets are present.", result.stdout)

    def test_package_contains_skill_and_bootstrap_assets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft-excel-format-adapter.skill"
            result = subprocess.run(
                [
                    "python",
                    str(PACKAGE_SCRIPT),
                    "--output",
                    str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.exists())

            with zipfile.ZipFile(output) as zf:
                names = set(zf.namelist())

            expected = {
                "draft-excel-format-adapter/SKILL.md",
                "draft-excel-format-adapter/references/asset-manifest.json",
                "draft-excel-format-adapter/references/new-draft-excel-pattern.md",
                "draft-excel-format-adapter/references/arr-best-practice.md",
                "draft-excel-format-adapter/scripts/ensure_draft_excel_skill_assets.py",
                "draft-excel-format-adapter/scripts/inspect_draft_excel_style.py",
            }
            self.assertTrue(expected.issubset(names), expected - names)


if __name__ == "__main__":
    unittest.main()
