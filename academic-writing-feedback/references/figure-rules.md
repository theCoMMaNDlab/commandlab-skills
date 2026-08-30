# Figure design rules

Optional pass — only run when offered and accepted, or when asked for general/full feedback. Covers what's actually checkable from source/labels; overlaps with the personal `plotting` skill (`~/.claude/skills/plotting/SKILL.md`), which has the fuller set of matplotlib-code conventions (color scales, layout, hard-coded style values, axis defaults) — apply that skill too if matplotlib source is available.

## Checkable here

- **Axis units in brackets.** Axis labels should include units in brackets, e.g. `[mm]`, `[-]` for dimensionless. Quote any axis label with a unit written another way (parentheses, no brackets, unit missing entirely where one is clearly needed).
- **No title on the figure itself.** A paper figure should never have a plot title — the first sentence of the figure caption serves as the title. This is unconditional for paper figures (stricter than the `plotting` skill's general "skip decorative titles if axis labels are self-explanatory" — for a paper, always flag an embedded title regardless of whether the axes are self-explanatory). Quote the figure/subfigure that has one.
- **Subfigure lettering, ordering, and finding-before-citation in text** — these are the same rules as the main skill's style-and-formatting section (do not duplicate them here as a separate finding; they're listed there because they apply to the document text, not the figure files themselves).

## Not checkable — human items

These require inspecting rendered image files (unreliable to verify from text/code) or are workflow/production conventions, not properties of a finished document. They're on the human checklist in the lab's Writing style guide doc, not here:

- Raw images saved as PNG/TIFF, with the code that generated them kept alongside
- Lettering added in Keynote/Illustrator set in Computer Modern, bold sans serif
- Figures reworked (simplified, resized) for presentations rather than reused as-is from the paper
