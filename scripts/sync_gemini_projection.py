#!/usr/bin/env python3
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTION_ROOT = ROOT / ".gemini"
FOLDERS = ["commands", "skills", "agents", "hooks", "policies"]


def copy_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def compare_tree(source: Path, target: Path) -> list[str]:
    if not source.is_dir():
        return [f"missing source directory: {source.relative_to(ROOT)}"]
    if not target.is_dir():
        return [f"missing projection directory: {target.relative_to(ROOT)}"]
    comparison = filecmp.dircmp(source, target)
    errors: list[str] = []
    for name in comparison.left_only:
        errors.append(f"projection missing {target.relative_to(ROOT) / name}")
    for name in comparison.right_only:
        errors.append(f"projection has extra {target.relative_to(ROOT) / name}")
    for name in comparison.diff_files:
        errors.append(f"projection differs {target.relative_to(ROOT) / name}")
    for name, child in comparison.subdirs.items():
        errors.extend(compare_tree(Path(child.left), Path(child.right)))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync or validate Gemini .gemini projection folders.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="Regenerate .gemini projection folders from source folders.")
    group.add_argument("--check", action="store_true", help="Check projection folders are byte-for-byte current.")
    args = parser.parse_args()

    if args.write:
        PROJECTION_ROOT.mkdir(exist_ok=True)
        for folder in FOLDERS:
            copy_tree(ROOT / folder, PROJECTION_ROOT / folder)
        print("ok: Gemini projection folders synchronized")
        return 0

    errors: list[str] = []
    for folder in FOLDERS:
        errors.extend(compare_tree(ROOT / folder, PROJECTION_ROOT / folder))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("ok: Gemini projection folders match source folders")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
