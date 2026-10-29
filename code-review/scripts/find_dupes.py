"""Report exact and near-duplicate files in a folder (read-only).

Implements the code-review skill's "single source of truth" check: anything
used in two places should have one definition and multiple calls to it.
Works on a git repo (tracked files only) or on a plain folder.

Usage:
    python3 -I find_dupes.py /path/to/folder [--ratio 0.85]
"""
import argparse
import difflib
import hashlib
import itertools
import os
import subprocess
from collections import defaultdict
from pathlib import Path

SOURCE_EXT = {".py", ".f", ".f90", ".f08", ".bash", ".sh", ".ijm", ".txt", ".md"}
SKIP_DIRS = {".git", "__pycache__", ".ipynb_checkpoints", "node_modules"}
DEFAULT_NEAR_DUP_RATIO = 0.85  # line-diff similarity above which two files are "close copies"
MAX_LENGTH_MISMATCH = 0.5  # skip pairs whose line counts differ by more than this fraction
BYTES_PER_MB = 1e6


def list_files(root: Path) -> list[Path]:
    """Files tracked by git if `root` is a git work tree, otherwise every file under it."""
    try:
        out = subprocess.run(
            ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
        ).stdout
        return [root / line for line in out.splitlines()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # not a git repo (or git missing): fall back to walking the folder
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        files.extend(Path(dirpath) / name for name in filenames)
    return files


def redundant_mb(groups: list[list[Path]]) -> float:
    """Size of all copies beyond the first in each group, in MB."""
    return sum(g[0].stat().st_size * (len(g) - 1) for g in groups) / BYTES_PER_MB


def exact_duplicates(files: list[Path]) -> list[list[Path]]:
    """Group files with byte-identical content (SHA-1 of the contents)."""
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for f in files:
        by_hash[hashlib.sha1(f.read_bytes()).hexdigest()].append(f)
    return [sorted(g) for g in by_hash.values() if len(g) > 1]


def near_duplicates(files: list[Path], ratio: float) -> list[tuple[float, Path, Path]]:
    """Pairs of same-extension text files, not byte-identical, whose line diff ratio >= `ratio`."""
    texts = {f: f.read_text(errors="replace").splitlines() for f in files if f.suffix in SOURCE_EXT}
    pairs = []
    for a, b in itertools.combinations(texts, 2):
        if a.suffix != b.suffix:
            continue
        longer = max(len(texts[a]), len(texts[b]), 1)
        if abs(len(texts[a]) - len(texts[b])) > MAX_LENGTH_MISMATCH * longer:
            continue
        r = difflib.SequenceMatcher(None, texts[a], texts[b], autojunk=False).ratio()
        if r >= ratio:
            pairs.append((r, a, b))
    return sorted(pairs, key=lambda t: -t[0])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--ratio", type=float, default=DEFAULT_NEAR_DUP_RATIO)
    args = parser.parse_args()
    root = args.folder.resolve()
    if not root.is_dir():
        raise SystemExit(f"error: {root} is not a folder, so there is nothing to scan.")

    files = list_files(root)
    groups = exact_duplicates(files)
    print(f"{len(files)} files; {len(groups)} groups of byte-identical copies "
          f"({redundant_mb(groups):.1f} MB redundant)\n")
    for g in groups:
        print(f"  x{len(g)} ({g[0].stat().st_size / BYTES_PER_MB:.2f} MB each)")
        for p in g:
            print(f"      {p.relative_to(root)}")

    # One representative per identical group so near-dup pairs aren't reported once per copy.
    dup_members = {p for g in groups for p in g[1:]}
    candidates = [f for f in files if f not in dup_members]
    pairs = near_duplicates(candidates, args.ratio)
    print(f"\n{len(pairs)} near-duplicate pairs (similarity >= {args.ratio:.2f}, not identical):")
    for r, a, b in pairs:
        print(f"  {r:.2f}  {a.relative_to(root)}  <->  {b.relative_to(root)}")


if __name__ == "__main__":
    main()
