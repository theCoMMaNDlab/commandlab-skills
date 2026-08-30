# CoMMaND lab Claude skills

Shared Claude Code skills for the lab — reviewing paper drafts, reviewing code, and plotting conventions.

- **writing-review** — review a paper/thesis draft against the lab's writing guidelines (formatting, style, LaTeX typesetting, author/funding checklist).
- **code-review** — review Fortran or Python code (including Abaqus UEL subroutines) against the lab's coding conventions.
- **figure-review** — conventions for matplotlib figures (layout, color, axes, math typesetting, hard-coded values).

The lab's [Writing style guide](https://drive.google.com/open?id=1JjN-z04sPDuR-2nwmUV6B3Vk3tdtVNaU4u-D1NsQYBs) doc covers what's *not* in these skills — things that need a person to decide or do (author list completeness, CRediT assignment, code-run sign-off, etc.), not a mechanical check.

## Setup

Clone this repo, then symlink each skill into your personal Claude Code skills directory so edits to your clone are picked up automatically:

```bash
git clone <this-repo-url> ~/commandlab-skills
mkdir -p ~/.claude/skills
for skill in writing-review code-review figure-review; do
  ln -s ~/commandlab-skills/$skill ~/.claude/skills/$skill
done
```

To pick up updates later, just `git pull` in `~/commandlab-skills` — no need to redo the symlinks.
