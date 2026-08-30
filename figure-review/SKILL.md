---
name: figure-review
description: Conventions for creating plots and figures in Python (matplotlib) — layout, color usage, axes, math typesetting, avoiding hard-coded style values. Use when writing or reviewing any plotting/visualization code.
---

# Plotting conventions

## Layout
- Compact by default: trim unnecessary whitespace at figure edges, keep labels close to their axes rather than floating with a lot of margin.
- No decorative titles that don't add information — if axis labels already make the figure self-explanatory, skip the title. For a figure destined for a paper, never include a plot title regardless of how self-explanatory the axes are — the first sentence of the figure caption serves as the title instead.
- Axis labels should include units in brackets (e.g. `[mm]`, `[-]` for dimensionless), not parentheses or a bare unit string.

## Color
- Use color sensibly and sparingly — it should mean something, and the same color should mean the same thing everywhere it appears (within a figure and across a set of related figures).
- Think about whether the data calls for a linear, discrete/categorical, or diverging color scale — and ask if it's not obvious which applies.
- Never use jet or other non-perceptually-uniform "rainbow" colormaps. Prefer perceptually uniform options (e.g. viridis/cividis for sequential, a proper diverging map like coolwarm/RdBu for signed data).

## Math & typography
- Render math properly in LaTeX, not plain-text approximations — e.g. `$\sigma_{ij}$` in axis labels/titles, not `sigma_ij`.

## Axes
- Y-axes should include 0 by default. If zero doesn't make sense for the data (e.g. a ratio, a narrow-range physical quantity where the baseline would waste most of the plot), ask before dropping it rather than silently choosing a non-zero baseline.

## Hard-coded values
- Cosmetic constants — font sizes, line widths, colors, DPI, padding — belong in one named settings block at the top of the file, not scattered as inline literals.
- Never duplicate the same palette or constant (e.g. a custom colormap) across multiple files — define it once in a shared location and import it.
- If a plotted physical constant (e.g. a baseline value) doesn't have a clear source in the code, flag it and ask rather than silently treating it as correct.

## Style consistency
- Use `ax` (not `axis` or other names) for matplotlib Axes objects, consistently across files.
- One shared DPI constant per project — don't let different plotting functions hardcode different DPI values independently.
