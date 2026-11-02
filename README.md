# CoMMaND lab Claude skills

Shared Claude Code skills for the lab — reviewing paper drafts, reviewing code, and plotting conventions. These encode the CoMMaND lab's own conventions and are provided as-is with no support: fork freely and adapt them to your own group.

- **writing-review** — review a paper/thesis draft against the lab's writing guidelines (formatting, style, LaTeX typesetting, author/funding checklist).
- **code-review** — review Fortran or Python code (including Abaqus UEL subroutines) against the lab's coding conventions.
- **figure-review** — conventions for matplotlib figures (layout, color, axes, math typesetting, hard-coded values).
- **presentation-review** — review a slide deck exported to PDF from Keynote (slide numbers, capitalization consistency, color use, text density, figures, references, length). Bundles `scripts/check_slides.py`, which does the mechanical checks without an LLM (needs the Python dependency in [Python dependencies](#python-dependencies)).

The lab's [Writing style guide](https://drive.google.com/open?id=1JjN-z04sPDuR-2nwmUV6B3Vk3tdtVNaU4u-D1NsQYBs) doc covers what's *not* in these skills — things that need a person to decide or do (author list completeness, CRediT assignment, code-run sign-off, etc.), not a mechanical check.

## Setup

Clone this repo, then symlink each skill into your personal Claude Code skills directory so edits to your clone are picked up automatically:

```bash
git clone https://github.com/theCoMMaNDlab/commandlab-skills.git ~/commandlab-skills
mkdir -p ~/.claude/skills
for skill in writing-review code-review figure-review presentation-review; do
  ln -s ~/commandlab-skills/$skill ~/.claude/skills/$skill
done
```

To pick up updates later, just `git pull` in `~/commandlab-skills` — no need to redo the symlinks.

### Python dependencies

Most skills are instructions only, but some bundle scripts that need Python packages, listed in [requirements.txt](requirements.txt) (currently just `pymupdf`, used by `presentation-review`). Install them into a virtual environment:

```bash
cd ~/commandlab-skills
python3 -m venv .venv                # create an isolated environment in .venv/
source .venv/bin/activate            # use it for this terminal session
pip install -r requirements.txt      # install everything listed in requirements.txt
```

Then run the slide checker with that environment active:

```bash
python presentation-review/scripts/check_slides.py talk.pdf --minutes 15
```

`.venv/` is local to your clone and is not meant to be committed.
