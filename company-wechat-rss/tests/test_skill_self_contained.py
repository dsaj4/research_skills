import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / "skills" / "company-wechat-rss-fetch"


class SelfContainedSkillTests(unittest.TestCase):
    def test_skill_bundles_required_cross_project_resources(self):
        required_paths = [
            SKILL_ROOT / "scripts" / "bootstrap_company_wechat_rss.py",
            SKILL_ROOT / "assets" / "company-wechat-rss-project" / "company_wechat_rss.py",
            SKILL_ROOT
            / "assets"
            / "company-wechat-rss-project"
            / "scripts"
            / "prepare_wewe_rss_runtime.ps1",
            SKILL_ROOT
            / "assets"
            / "company-wechat-rss-project"
            / "config"
            / "company_accounts.template.json",
        ]

        for path in required_paths:
            self.assertTrue(path.exists(), f"Missing bundled skill resource: {path}")

    def test_bootstrap_scaffolds_project_without_repo_dependency(self):
        bootstrap_script = SKILL_ROOT / "scripts" / "bootstrap_company_wechat_rss.py"

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            result = subprocess.run(
                [
                    "python",
                    str(bootstrap_script),
                    "--workspace",
                    str(workspace),
                    "--project-name",
                    "wechat-rss-workspace",
                    "--skip-clone",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(
                result.returncode,
                0,
                f"bootstrap failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
            )

            scaffold_root = workspace / "wechat-rss-workspace"
            self.assertTrue((scaffold_root / "company_wechat_rss.py").exists())
            self.assertTrue(
                (scaffold_root / "scripts" / "prepare_wewe_rss_runtime.ps1").exists()
            )
            self.assertTrue(
                (scaffold_root / "config" / "company_accounts.template.json").exists()
            )
            self.assertTrue((scaffold_root / "vendor").exists())

    def test_skill_instructions_are_cross_project_oriented(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("bootstrap_company_wechat_rss.py", skill_text)
        self.assertIn("self-contained", skill_text)
        self.assertIn("current workspace", skill_text)
        self.assertNotIn("Run the local `company-wechat-rss` workflow", skill_text)


if __name__ == "__main__":
    unittest.main()
