# TeX-only rules

These only apply when you can see the actual `.tex` source — not a compiled PDF or a pasted excerpt without visible LaTeX commands. If you don't have the source, skip this file's checks and note in your feedback that you couldn't check them without it.

## One sentence per line

Each sentence should be on its own line in the source (this makes diffs and version control sane). Flag any paragraph in the source where two or more full sentences share a single line — quote the line and identify the file it's in.

## Tensor typesetting

- Second-order tensors should use `\ten{}` or `\boldmath{}` — not a bare bold symbol typed by hand or an undecorated italic variable.
- Fourth-order tensors should use `\tenf{}` or `\mathbb{}`.
- Quote the specific macro or symbol usage that violates this.

## Units

Numbers with units should be typeset with the `siunitx` package (`\SI{}{}`, `\si{}`, `\num{}`), not typed as a plain number followed by a unit string. Quote the offending instance and its line/file.

## Cross-references

Figures, tables, sections, equations, and other numbered elements should be referenced with `\autoref{}`, not `\ref{}` and not a hardcoded number typed into the prose. Quote the offending reference.

## Subscripts and superscripts

- Multi-character subscripts or superscripts must be wrapped in braces — `A_{ij}`, not `A_ij` (which LaTeX would render as just `A_i` followed by a stray `j`).
- Outside of transpose marks (`^T`, `^\top`) and index variables, subscripts and superscripts that represent words or abbreviations must be upright/roman, not default math italic. Any of `\mathrm{}`, `\rm{}`, `\text{}`, or the lab's `\scas{}` macro (see `preamble.tex`) satisfies this — flag any that are left in plain math italic instead (e.g., `x_{max}` should be `x_{\mathrm{max}}`).

## Bibliography

- Every reference in the text should use a LaTeX cross-reference command, never a hardcoded citation number or author name typed by hand.
- The document should use `biblatex`, not `bibtex` or `natbib` — check the preamble for `\usepackage{biblatex}` vs. `\usepackage{natbib}` or a `\bibliographystyle{}` + `\bibliography{}` pair (the bibtex-style pattern).
- Citations should use `\autocite{}` (or `\textcite{}` when the citation is the grammatical subject of the sentence, e.g. "Smith et al. showed..."), not the bare `\cite{}` or a manually typed author/year. Quote the offending citation and its location.
- If a `.bib` file is available, check its `journal`/`journaltitle` fields for abbreviated journal names (e.g. "J. Mech. Phys. Solids" instead of "Journal of the Mechanics and Physics of Solids") — the lab's Zotero export convention uses full, unabbreviated journal names. Quote the offending entry's citation key and journal field.

## Preamble

Compare the document's preamble against `preamble.tex`. Flag any of these that are missing outright (don't flag ordering or exact formatting — only presence):

- Packages: `amsfonts`, `amsmath`, `amsthm`, `amssymb`, `booktabs`, `graphicx`, `hyperref`, `siunitx`, `xcolor`
- Macros: `\sca`, `\ltr`, `\bltr`, `\mat`, `\ten`, `\tenf`, `\scas`, `\tens`, `\rev`
- The `abc` environment (lettered sub-lists)

If the document doesn't use tensors, sans-serif labels, or revision markup at all, don't flag the corresponding unused macro as missing — only flag a macro as missing if the document actually needs what it does (e.g., it writes a bare `\mathbf{}` tensor by hand instead of using `\ten{}`).
