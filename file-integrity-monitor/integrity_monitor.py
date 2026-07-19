#!/usr/bin/env python3
"""
File Integrity Monitor.

Hashes every file under a directory and compares against a saved baseline
to detect additions, deletions, and modifications - the same idea behind
tools like Tripwire or OSSEC's FIM module.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path

BASELINE_FILE = ".fim_baseline.json"


def hash_file(path: Path, chunk_size: int = 65536) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def walk_hashes(root: Path) -> dict:
    hashes = {}
    for dirpath, _, filenames in os.walk(root):
        if BASELINE_FILE in filenames:
            filenames.remove(BASELINE_FILE)
        for name in filenames:
            path = Path(dirpath) / name
            rel = str(path.relative_to(root))
            hashes[rel] = hash_file(path)
    return hashes


def baseline_path(root: Path) -> Path:
    return root / BASELINE_FILE


def cmd_init(root: Path):
    hashes = walk_hashes(root)
    baseline_path(root).write_text(json.dumps(hashes, indent=2))
    print(f"Baseline saved for {len(hashes)} files.")


def cmd_check(root: Path):
    bpath = baseline_path(root)
    if not bpath.exists():
        print("No baseline found. Run with --init first.")
        return

    baseline = json.loads(bpath.read_text())
    current = walk_hashes(root)

    added = sorted(set(current) - set(baseline))
    removed = sorted(set(baseline) - set(current))
    modified = sorted(f for f in set(current) & set(baseline) if current[f] != baseline[f])

    if not (added or removed or modified):
        print("No changes detected. All files match the baseline.")
        return

    if added:
        print("Added files:")
        for f in added:
            print(f"  + {f}")
    if removed:
        print("Removed files:")
        for f in removed:
            print(f"  - {f}")
    if modified:
        print("Modified files:")
        for f in modified:
            print(f"  * {f}")


def main():
    parser = argparse.ArgumentParser(description="Monitor a directory for file changes.")
    parser.add_argument("directory", help="Directory to monitor")
    parser.add_argument("--init", action="store_true", help="Save a new baseline instead of checking")
    args = parser.parse_args()

    root = Path(args.directory).resolve()
    if args.init:
        cmd_init(root)
    else:
        cmd_check(root)


if __name__ == "__main__":
    main()
