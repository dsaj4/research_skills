import argparse
import shutil
import subprocess
from pathlib import Path


DEFAULT_PROJECT_NAME = "company-wechat-rss"
DEFAULT_WEWE_RSS_REPO = "https://github.com/cooderl/wewe-rss.git"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def template_root() -> Path:
    return skill_root() / "assets" / "company-wechat-rss-project"


def resolve_project_dir(args: argparse.Namespace) -> Path:
    if args.project_dir:
        return Path(args.project_dir).expanduser().resolve()
    return (Path(args.workspace).expanduser().resolve() / args.project_name).resolve()


def copy_template_tree(source_root: Path, target_root: Path, *, force: bool) -> dict[str, int]:
    if not source_root.exists():
        raise FileNotFoundError(f"Missing bundled template directory: {source_root}")

    copied = 0
    skipped = 0
    for source_path in source_root.rglob("*"):
        relative_path = source_path.relative_to(source_root)
        target_path = target_root / relative_path
        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        if target_path.exists() and not force:
            skipped += 1
            continue

        shutil.copy2(source_path, target_path)
        copied += 1

    return {"copied": copied, "skipped": skipped}


def clone_wewe_rss(project_dir: Path, repo_url: str, *, skip_clone: bool) -> str:
    vendor_root = project_dir / "vendor"
    vendor_root.mkdir(parents=True, exist_ok=True)
    repo_root = vendor_root / "wewe-rss"

    if skip_clone:
        return f"Skipped clone. Expected upstream path: {repo_root}"

    if repo_root.exists():
        return f"Upstream already exists: {repo_root}"

    result = subprocess.run(
        ["git", "clone", repo_url, str(repo_root)],
        cwd=str(project_dir),
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "git clone failed\n"
            f"Command: git clone {repo_url} {repo_root}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    return f"Cloned upstream wewe-rss into: {repo_root}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a workspace-local Company WeChat RSS runtime from the bundled skill assets."
    )
    parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace directory where the project folder should be created. Default: current directory.",
    )
    parser.add_argument(
        "--project-name",
        default=DEFAULT_PROJECT_NAME,
        help=f"Project folder name under --workspace. Default: {DEFAULT_PROJECT_NAME}",
    )
    parser.add_argument(
        "--project-dir",
        default=None,
        help="Explicit project directory. Overrides --workspace and --project-name.",
    )
    parser.add_argument(
        "--wewe-rss-url",
        default=DEFAULT_WEWE_RSS_REPO,
        help=f"Git URL for upstream wewe-rss. Default: {DEFAULT_WEWE_RSS_REPO}",
    )
    parser.add_argument(
        "--skip-clone",
        action="store_true",
        help="Create only the wrapper project and vendor directory without cloning upstream.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing scaffold files. By default, existing files are preserved.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    project_dir = resolve_project_dir(args)
    project_dir.mkdir(parents=True, exist_ok=True)

    copy_stats = copy_template_tree(template_root(), project_dir, force=args.force)
    clone_message = clone_wewe_rss(
        project_dir,
        args.wewe_rss_url,
        skip_clone=args.skip_clone,
    )

    print(f"Project ready: {project_dir}")
    print(f"Template files copied: {copy_stats['copied']}")
    print(f"Template files skipped: {copy_stats['skipped']}")
    print(clone_message)
    print("")
    print("Next commands:")
    print(
        "powershell -ExecutionPolicy Bypass -File "
        f"'{project_dir / 'scripts' / 'prepare_wewe_rss_runtime.ps1'}'"
    )
    print(
        "powershell -ExecutionPolicy Bypass -File "
        f"'{project_dir / 'scripts' / 'start_wewe_rss.ps1'}'"
    )
    print(f"Open dashboard: http://127.0.0.1:4000/dash")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
