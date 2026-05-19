import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / "skills" / "industry-research-draft-workflow"
PACKAGE_SCRIPT = PROJECT_ROOT / "scripts" / "package_draft_excel_skill.py"
ENSURE_SCRIPT = SKILL_ROOT / "scripts" / "ensure_draft_excel_skill_assets.py"


class DraftExcelSkillPackageTests(unittest.TestCase):
    def test_manifest_assets_exist_in_repo_copy(self):
        manifest_path = SKILL_ROOT / "references" / "asset-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        for asset in manifest["assets"]:
            path = SKILL_ROOT / asset["path"]
            self.assertTrue(path.exists(), f"Missing manifest asset: {asset['path']}")

    def test_manifest_groups_required_template_and_example_assets(self):
        manifest_path = SKILL_ROOT / "references" / "asset-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assets_by_path = {asset["path"]: asset for asset in manifest["assets"]}

        required_assets = {
            "assets/templates/步骤3、图表模板案例.xlsx": ("templates", "binary"),
            "assets/templates/1、广发研究研报模板升级说明.pdf": ("templates", "binary"),
            "assets/examples/research-draft-generation/通用数据收集底稿示例_ARR.xlsx": (
                "examples",
                "binary",
            ),
            "assets/examples/research-draft-generation/contact_sheet_validated_final.png": (
                "examples",
                "binary",
            ),
            "assets/examples/research-draft-generation/截图视觉校验记录.md": (
                "examples",
                "text",
            ),
        }

        for path, (group, asset_type) in required_assets.items():
            self.assertIn(path, assets_by_path)
            self.assertEqual(assets_by_path[path]["group"], group)
            self.assertEqual(assets_by_path[path]["type"], asset_type)
            self.assertTrue(assets_by_path[path]["required"])

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
        self.assertIn("All manifest assets are present for group 'all'.", result.stdout)

    def test_asset_checker_supports_group_checks(self):
        for group in ["core", "templates", "examples"]:
            result = subprocess.run(
                [
                    "python",
                    str(ENSURE_SCRIPT),
                    "--skill-root",
                    str(SKILL_ROOT),
                    "--group",
                    group,
                    "--dry-run",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f"All manifest assets are present for group '{group}'.", result.stdout)

    def test_package_contains_skill_and_bootstrap_assets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "industry-research-draft-workflow.skill"
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
                "industry-research-draft-workflow/SKILL.md",
                "industry-research-draft-workflow/references/asset-manifest.json",
                "industry-research-draft-workflow/references/scenario-router.md",
                "industry-research-draft-workflow/references/workbook-contract.md",
                "industry-research-draft-workflow/references/existing-file-to-template.md",
                "industry-research-draft-workflow/references/research-draft-generation.md",
                "industry-research-draft-workflow/references/data-collection-guidance.md",
                "industry-research-draft-workflow/references/complex-scenario-registry.md",
                "industry-research-draft-workflow/references/quality-gates.md",
                "industry-research-draft-workflow/assets/templates/步骤3、图表模板案例.xlsx",
                "industry-research-draft-workflow/assets/templates/1、广发研究研报模板升级说明.pdf",
                "industry-research-draft-workflow/assets/examples/research-draft-generation/README.md",
                "industry-research-draft-workflow/assets/examples/research-draft-generation/通用数据收集底稿示例_ARR.xlsx",
                "industry-research-draft-workflow/assets/examples/research-draft-generation/contact_sheet_validated_final.png",
                "industry-research-draft-workflow/assets/examples/research-draft-generation/截图视觉校验记录.md",
                "industry-research-draft-workflow/scripts/ensure_draft_excel_skill_assets.py",
                "industry-research-draft-workflow/scripts/inspect_draft_excel_style.py",
            }
            self.assertTrue(expected.issubset(names), expected - names)


if __name__ == "__main__":
    unittest.main()
