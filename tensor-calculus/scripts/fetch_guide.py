#!/usr/bin/env python3
"""Fetch (or refresh) the latest Hitchhiker's Guide to Abaqus from GitHub.

The tensor-calculus skill must read the *current* default branch of the Guide,
never a stale or locally modified copy, so this script keeps a shallow clone
in ``<skill>/.guide`` (git-ignored) and fast-forwards it every time it runs.

Usage:
    python fetch_guide.py            # refresh, print commit + path
    python fetch_guide.py --outline  # also list chapters/sections with line numbers

Standard library only; requires ``git`` on the PATH.

Source of the Guide: M. Holland, "The Hitchhiker's Guide to Abaqus",
https://github.com/mholla/hitchhikers-guide-to-abaqus
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

GUIDE_URL = "https://github.com/mholla/hitchhikers-guide-to-abaqus.git"
GUIDE_TEX = "documentation.tex"
CLONE_DEPTH = "1"  # only the newest commit is needed
SKILL_DIR = Path(__file__).resolve().parent.parent  # resolves through symlinks
GUIDE_DIR = SKILL_DIR / ".guide"
OUTLINE_PATTERN = re.compile(r"^\\(chapter|section)\{(.*?)\}")


def fail(message: str) -> None:
    """Exit with a clear message on stderr (never fail silently)."""
    sys.exit(f"fetch_guide.py: ERROR: {message}")


def git(*args: str, cwd: Path | None = None) -> str:
    """Run a git command, returning stdout; raise CalledProcessError on failure."""
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def refresh() -> bool:
    """Clone or update the Guide. Returns True if up to date, False if stale."""
    if shutil.which("git") is None:
        fail("git is not installed; install it (e.g. `xcode-select --install`).")
    try:
        if not (GUIDE_DIR / ".git").is_dir():
            git("clone", "--depth", CLONE_DEPTH, GUIDE_URL, str(GUIDE_DIR))
        else:
            # Fetch the remote default branch (HEAD) and make the clone match it
            # exactly, whatever the branch is called and whatever state the
            # working tree is in.
            git("fetch", "--depth", CLONE_DEPTH, "origin", "HEAD", cwd=GUIDE_DIR)
            git("reset", "--hard", "FETCH_HEAD", cwd=GUIDE_DIR)
        return True
    except subprocess.CalledProcessError as err:
        if (GUIDE_DIR / GUIDE_TEX).is_file():
            print(
                "fetch_guide.py: WARNING: could not reach GitHub "
                f"({err.stderr.strip()}). Using the STALE copy below; tell the "
                "user the Guide version may be out of date.",
                file=sys.stderr,
            )
            return False
        fail(
            f"could not clone {GUIDE_URL} and no earlier copy exists "
            f"({err.stderr.strip()}). Check your network connection."
        )
    return False  # unreachable; keeps type checkers happy


def print_outline(tex_path: Path) -> None:
    """List chapters and sections with line numbers, to navigate the big file."""
    for number, line in enumerate(tex_path.read_text().splitlines(), start=1):
        match = OUTLINE_PATTERN.match(line)
        if match:
            kind, title = match.groups()
            indent = "" if kind == "chapter" else "  "
            print(f"{number:6d}  {indent}{kind}: {title}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--outline", action="store_true", help="list chapters/sections with line numbers"
    )
    args = parser.parse_args()

    up_to_date = refresh()
    tex_path = GUIDE_DIR / GUIDE_TEX
    if not tex_path.is_file():
        fail(f"{tex_path} not found after fetching; the repository layout changed?")

    commit = git("log", "-1", "--format=%h  %ad  %s", "--date=short", cwd=GUIDE_DIR)
    status = "up to date" if up_to_date else "STALE (offline)"
    print(f"Guide version: {commit}  [{status}]")
    print(f"Source file:   {tex_path}")
    if args.outline:
        print_outline(tex_path)


if __name__ == "__main__":
    main()
