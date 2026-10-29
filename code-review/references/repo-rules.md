# GitHub repository rules

Apply these whenever the person points you at a folder: treat any folder as a repo, whether or not it has a paper, a remote, or its own `.git` (a repo link, a local clone, a zip, or a plain directory all count).

Check that the repository includes:

- An appropriate **license** file (e.g., `LICENSE` or `LICENSE.md`) with a real license identified — not an empty placeholder. The lab default is GNU GPL v3.0; flag a missing license the same way regardless of which one is eventually chosen, and if a different license is present, just note that it's not the default rather than calling it wrong — there can be a good reason for it.
- A **`.gitignore`** appropriate to the project's language/tooling (e.g., ignoring `__pycache__/`, build artifacts, virtual environments, `.DS_Store`, etc. — not just an empty or default file that doesn't match what's actually in the repo).
- A **README** that at minimum explains what the repository contains and how to run/reproduce the code. Specifically, every command needed to actually test or run the code must be present in the README — if you have to infer a command from the source rather than find it stated there, flag it as missing.
- A **requirements file** appropriate to the language (`requirements.txt` or `pyproject.toml` for Python, `environment.yml` for conda, `renv.lock` for R, etc.) that lists the dependencies actually imported/used in the code.
- No **duplicate or generated files** committed. Use `scripts/find_dupes.py` and list each group of byte-identical copies with paths and redundant size, including data and binaries (for example a mirrored `comparing_results/` folder of `.odb`/`.inp` files). For large binaries, say whether they belong in git, in Git LFS, or in an external archive linked from the README. Say if a copy looks intentional (for example a snapshot of the inputs that produced a result), but still name it.
- A reasonable **folder structure** rather than everything dumped in the repo root — expect separate subfolders by role (e.g. `code`/`src`, `data`, `results`, `figures`), not a flat mix of scripts, raw data files, and output plots side by side. Judge by what's actually in the repo: a handful of files with no meaningful role split doesn't need this, but once there's a real mix of inputs/outputs/scripts they should be separated. Name the specific mixing when flagging it (e.g., "scripts, `.csv` input data, and generated `.png` plots are all in the repo root — split into `code/`, `data/`, and `figures/`") rather than a generic "improve organization."

For each missing or inadequate item, name the specific gap (e.g., "no `.gitignore` — the repo currently tracks `__pycache__/` and a `.ipynb_checkpoints/` directory") rather than a generic "add a .gitignore."
