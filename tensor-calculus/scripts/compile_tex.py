#!/usr/bin/env python3
"""Compile a derivation with real LaTeX and the lab macros, and render PNGs.

Purpose: guarantee that math shown to the user is genuine LaTeX output (correct
symbols, correct macros), not an approximation.  The script

  1. wraps a body fragment in a minimal document that loads the lab preamble
     (``writing-review/references/preamble.tex``: ``\\ten``, ``\\tenf``, ...),
  2. runs ``latexmk``,
  3. FAILS LOUDLY on any LaTeX error, undefined control sequence, or missing
     glyph (a "Missing character" warning means a stand-in symbol was used),
  4. renders every page to PNG so the result can be inspected visually.

Usage:
    python compile_tex.py derivation.tex                 # body fragment
    python compile_tex.py paper_snippet.tex --full       # already a full document
    python compile_tex.py derivation.tex --out-dir DIR --dpi 120

Standard library only.  Requires ``latexmk`` (MacTeX) and ``pdftoppm`` (poppler:
``brew install poppler``).
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent  # resolves through symlinks
REPO_DIR = SKILL_DIR.parent
DEFAULT_PREAMBLE = REPO_DIR / "writing-review" / "references" / "preamble.tex"
DEFAULT_DPI = 110
OVERFULL_LIMIT_PT = 1.0  # ignore overfull boxes smaller than this (points)
LOG_EXCERPT_LINES = 25

WRAPPER = r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{xcolor}
\input{preamble.tex}
\begin{document}
\input{body.tex}
\end{document}
"""

# Log patterns that mean the output is NOT trustworthy.
ERROR_PATTERNS = (
    re.compile(r"^! .*", re.MULTILINE),                  # any TeX error
    re.compile(r"^.*Missing character:.*$", re.MULTILINE),  # substituted glyph
    re.compile(r"^.*Undefined control sequence.*$", re.MULTILINE),
    re.compile(r"^.*LaTeX Warning: Reference .* undefined.*$", re.MULTILINE),
)
OVERFULL = re.compile(r"Overfull \\hbox \(([\d.]+)pt too wide\).*")


def fail(message: str) -> None:
    """Exit with a clear message on stderr (never fail silently)."""
    sys.exit(f"compile_tex.py: ERROR: {message}")


def check_tools() -> None:
    """Make sure the external programs exist, with install hints."""
    hints = {
        "latexmk": "install MacTeX (https://tug.org/mactex/) or `brew install --cask mactex`",
        "pdftoppm": "install poppler: `brew install poppler`",
    }
    for tool, hint in hints.items():
        if shutil.which(tool) is None:
            fail(f"`{tool}` not found on PATH; {hint}.")


def run_latex(build_dir: Path, main_tex: str) -> str:
    """Run latexmk in ``build_dir``; return the log text (even on failure)."""
    subprocess.run(
        [
            "latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
            "-file-line-error", main_tex,
        ],
        cwd=build_dir, capture_output=True, text=True,
    )
    log_path = build_dir / (Path(main_tex).stem + ".log")
    return log_path.read_text(errors="replace") if log_path.is_file() else ""


def report_problems(log: str) -> list[str]:
    """Collect error lines and too-wide equations from the LaTeX log."""
    errors: list[str] = []
    for pattern in ERROR_PATTERNS:
        errors.extend(m.group(0).strip() for m in pattern.finditer(log))
    for match in OVERFULL.finditer(log):
        if float(match.group(1)) > OVERFULL_LIMIT_PT:
            errors.append(f"line runs off the page: {match.group(0).strip()}")
    return errors


def render_pages(pdf: Path, out_dir: Path, dpi: int) -> list[Path]:
    """Render each PDF page to PNG with pdftoppm; return the file list."""
    prefix = out_dir / pdf.stem
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(prefix)], check=True
    )
    return sorted(out_dir.glob(f"{pdf.stem}-*.png"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tex_file", type=Path, help="body fragment (or full document with --full)")
    parser.add_argument("--full", action="store_true", help="tex_file is already a complete document")
    parser.add_argument("--out-dir", type=Path, default=None, help="where to put the PDF and PNGs (default: new temp dir)")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI)
    parser.add_argument("--preamble", type=Path, default=DEFAULT_PREAMBLE, help="preamble file with the lab macros")
    args = parser.parse_args()

    check_tools()
    if not args.tex_file.is_file():
        fail(f"{args.tex_file} does not exist.")
    if not args.full and not args.preamble.is_file():
        fail(
            f"lab preamble not found at {args.preamble}. The tensor-calculus skill "
            "expects the `writing-review` skill from the same commandlab-skills "
            "clone; install it (see the repo README) or pass --preamble."
        )

    out_dir = args.out_dir or Path(tempfile.mkdtemp(prefix="tensor-calculus-"))
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.tex_file.stem

    with tempfile.TemporaryDirectory(prefix="tc-build-") as tmp:
        build = Path(tmp)
        if args.full:
            main_tex = f"{stem}.tex"
            shutil.copy(args.tex_file, build / main_tex)
        else:
            main_tex = "main.tex"
            shutil.copy(args.preamble, build / "preamble.tex")  # avoids spaces-in-path issues
            shutil.copy(args.tex_file, build / "body.tex")
            (build / main_tex).write_text(WRAPPER)
        log = run_latex(build, main_tex)
        pdf_built = build / (Path(main_tex).stem + ".pdf")
        problems = report_problems(log)
        if problems or not pdf_built.is_file():
            excerpt = "\n".join(log.splitlines()[-LOG_EXCERPT_LINES:])
            fail(
                "LaTeX did not compile cleanly:\n  "
                + "\n  ".join(problems or ["no PDF produced"])
                + f"\n--- end of log ---\n{excerpt}"
            )
        pdf = out_dir / f"{stem}.pdf"
        shutil.copy(pdf_built, pdf)

    pages = render_pages(pdf, out_dir, args.dpi)
    print(f"OK: compiled cleanly with real LaTeX ({len(pages)} page(s)).")
    print(f"PDF:  {pdf}")
    for page in pages:
        print(f"PNG:  {page}")
    print(f"Source (copyable, uses lab macros): {args.tex_file}")


if __name__ == "__main__":
    main()
