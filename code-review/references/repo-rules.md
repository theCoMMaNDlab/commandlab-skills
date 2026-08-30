# GitHub repository rules

Apply these when the paper has an accompanying code/data repository (the person shares a repo link, a local clone, or a zip of one alongside the manuscript).

Check that the repository includes:

- An appropriate **license** file (e.g., `LICENSE` or `LICENSE.md`) with a real license identified — not an empty placeholder. The lab default is GNU GPL v3.0; flag a missing license the same way regardless of which one is eventually chosen, and if a different license is present, just note that it's not the default rather than calling it wrong — there can be a good reason for it.
- A **`.gitignore`** appropriate to the project's language/tooling (e.g., ignoring `__pycache__/`, build artifacts, virtual environments, `.DS_Store`, etc. — not just an empty or default file that doesn't match what's actually in the repo).
- A **README** that at minimum explains what the repository contains and how to run/reproduce the code.
- A **requirements file** appropriate to the language (`requirements.txt` or `pyproject.toml` for Python, `environment.yml` for conda, `renv.lock` for R, etc.) that lists the dependencies actually imported/used in the code.

For each missing or inadequate item, name the specific gap (e.g., "no `.gitignore` — the repo currently tracks `__pycache__/` and a `.ipynb_checkpoints/` directory") rather than a generic "add a .gitignore."
