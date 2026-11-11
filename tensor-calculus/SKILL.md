---
name: tensor-calculus
description: Derive, check, or explain tensor calculus and continuum-mechanics results (derivatives of scalar/tensor functions with respect to tensors, chain rules, push-forward/pull-back, Piola transforms, stress and tangent derivations, finite-growth kinematics, index <-> direct <-> Voigt notation, fourth-order tensor symmetries) using the notation of Holland's "Hitchhiker's Guide to Abaqus" (fetched fresh from GitHub). Output is compiled with real LaTeX using the lab macros, so it is guaranteed to be correct, copyable LaTeX. Use whenever the user asks to derive, verify, simplify, or typeset a tensor expression, tangent, or stress; asks "what is d(...)/d(...)" for tensor arguments; asks anything about Abaqus subroutines or the Hitchhiker's Guide; or wants to convert between tensor, index, and Voigt forms, even if they do not say "tensor calculus".
---

## Tensor calculus (Holland / Hitchhiker's Guide notation)

Goal: derivations a student can read and a reviewer can verify, delivered as **genuine LaTeX** (never an approximation).
Every result is accompanied by an *offer* of an independent check.

### Step 0: get the Guide (every session that touches growth or Abaqus)

The Hitchhiker's Guide to Abaqus is the single source of truth for notation, growth theory (Ch. 4, "Mechanics of growth"), tangents, symmetry, and anything about Abaqus.
Never answer those from memory and never use a local copy someone happens to have.
Run

```bash
python3 <skill dir>/scripts/fetch_guide.py --outline
```

It shallow-clones/refreshes the **default branch** from `https://github.com/mholla/hitchhikers-guide-to-abaqus` into `<skill dir>/.guide/documentation.tex`, prints the commit hash and date, and lists chapters and sections with line numbers.
Read the relevant part of that file with the line numbers (it is about 3000 lines; do not read it all).
Cite the chapter/section and the commit hash in the answer.
If the script warns the copy is STALE (offline), say so to the user.
If the Guide and this skill disagree, the Guide wins; tell the user about the discrepancy.

### Output: compile real LaTeX, look at it, then show it

The terminal and many chat clients do not render LaTeX reliably, so **do not rely on chat rendering**.
For every derivation:

1. **Write the derivation to a `.tex` file** (a body fragment, no preamble) using the lab macros (see Macros below).
   Put it in the session scratchpad (or any temp directory), not in the user's repository.
2. **Compile it:** `python3 <skill dir>/scripts/compile_tex.py derivation.tex --out-dir <dir>`.
   The script runs real `latexmk` with the lab preamble (`../writing-review/references/preamble.tex` in the same `commandlab-skills` clone) and fails loudly on any LaTeX error, undefined macro, missing glyph (a stand-in symbol), or a line running off the page.
   Fix every reported problem; never show output that did not compile.
3. **Look at it yourself.**
   Read the PNG(s) the script prints, check index placement, hats/bars, sub/superscripts, and that nothing is cramped or cut off, then fix and recompile.
4. **Show it to the user.**
   - If the `SendUserFile` tool is available, send the PDF with `display: "render"` (it appears in the app window as typeset math) and send the `.tex` source as an attachment so the user can copy it.
   - Otherwise tell the user the PDF and `.tex` paths (on macOS, `open <pdf>` shows it).
   - In chat, give a one- to three-line summary of the result with **no math symbols** beyond a couple of trivial ones.
     Never write math in chat as Unicode/ASCII pseudo-math (for example `∂W₀/∂C`).
5. **A short result may also go in chat as plain LaTeX in the lab macros** (for copy-paste) if the user asks, but the compiled PDF is always the version that has been checked.

If the user asks for a web page, build an artifact page (see `references/artifact-page.md`) that renders with MathJax and has a "copy LaTeX (lab macros)" button; the compiled PDF remains the exact version.

If `compile_tex.py` reports a missing tool, tell the user the install command it prints (MacTeX for `latexmk`, `brew install poppler` for `pdftoppm`); do not fall back to approximate rendering.

### Macros (use them)

Use the lab macros so the user can paste the LaTeX straight into the paper: `\ten{C}` (1st/2nd-order tensors), `\tenf{C}` (4th-order), `\scas{e}` (upright script-size labels, e.g. `\ten{F}^{\scas{e}}`), `\tens{C}` (held-fixed subscripts, e.g. `\left.\cdot\right|_{\tens{C}}`), `\sca{d}` (upright differentials), `\mat{}` (matrices).
Definitions and conventions: `references/notation.md`.
Do not redefine them and do not mix in `\boldsymbol`/`\mathbf` for tensors.
Do not use Unicode math in LaTeX.

### Formatting of the derivation

- One sentence per line in prose.
- Equations are punctuated as part of the sentence (comma or period), using `align` with `={}&` so spacing is correct.
- Every displayed equation that introduces a symbol is followed by "where ..." defining it.
- Upper-case indices = material/reference/intermediate, lower-case = spatial; two-point tensors (e.g. $F_{iJ}$) carry one of each.
- Express everything in terms of the independent variables (below) and write the full argument list of every function.

### Derivation method

- **Derive in indicial notation**, step by step, one operation per line, saying what each step does (product rule, chain rule, $\partial A_{ij}/\partial A_{kl}=\delta_{ik}\delta_{jl}$, etc.).
  Do not skip from the definition to the answer.
- **No proxies.**
  Never introduce shorthand symbols such as "let $\ten{G}=\ten{A}\ten{B}\ten{C}$" to avoid writing something out.
  Carry the full expression, and use only symbols that are defined in the Guide.
- **Show the result in both forms:** indicial *and* direct (tensor) notation, using the dyadic products in `references/identities.md`.
  The derivation itself stays indicial; the direct form is the converted result.
- **Growth conventions** (confirm details in Ch. 4 of the fetched Guide):
  - the growth tensor $\ten{F}^{\scas{g}}$ is always symmetric (diagonal in the reference basis), so the intermediate configuration uses *capital* indices, same as the reference configuration;
  - the independent variables are $\ten{C}$ and $\ten{F}^{\scas{g}}$; everything else ($\ten{F}^{\scas{e}}$, $\ten{C}^{\scas{e}}$, $J^{\scas{e}}$, $J^{\scas{g}}$, $\overline{\ten{S}}$, ...) is expressed in terms of them, nested so that no function reuses a symbol with a different argument list;
  - state what is held fixed in every partial derivative with a subscript, e.g. $\left.\cdot\right|_{\ten{F}^{\scas{g}}}$, and a bar belongs on a factor only if the held-fixed quantity is an argument of that factor's own function.
- **Abaqus questions** (UMAT/UHYPER/UEL conventions, Jacobian options, tangent requirements, Voigt ordering, input files): read the relevant chapter of the fetched Guide and point to it by chapter/section; do not answer from memory.

### Workflow for every derivation

1. **List the arguments.** Each function with its *full* argument list; declare the independent variables once; one symbol per function.
2. **Check for hidden dependence.** Any factor (a Jacobian, growth variable, structural tensor) that depends on the differentiation variable needs a product-rule term; see `references/pitfalls.md`.
3. **Derive** in index notation, then convert to direct notation (`references/identities.md`).
4. **State symmetries** (major/minor); if an argument is symmetric, use the symmetrized derivative from `references/notation.md`.
5. **State the configuration and Jacobian** for any push-forward or pull-back.
6. **Compile, look, show** (above).
7. **Offer independent checks**, always, at the end, as a short menu.
   Do not run or write them unless the user accepts, with one exception: if the user explicitly asked to "verify" or "check", run the numerical check.

### Offering checks

End every derivation with a brief offer that names the *specific* check that fits, as a question with the options named (not a generic "want me to verify?").
Choose from:

- **Numerical (finite-difference) check** with the *admissible* variation (symmetric if the argument is symmetric).
  Template and tolerances in `references/numerical-checks.md`.
- **Orthogonal derivation:** directional-derivative form versus index calculus; spectral derivation for isotropic functions; a limiting case ($\ten{F}^{\scas{g}}=\ten{I}$ recovers the non-growth result; isotropic growth; uniaxial or simple shear); consistency identities (energy conjugacy, objectivity under $\ten{F}\to\ten{Q}\ten{F}$, $\ten{\sigma}$ from $\ten{S}$ versus from $\overline{\ten{S}}$); SymPy.
- **Dimension / index audit:** free indices match, repeated indices appear exactly twice, units consistent.

### Reviewing equations in the user's own paper or the Guide

When the user asks about specific equations in a `.tex` document, locate each item by **equation number and page first** (for example "Eq. (4.34), p. 30"), then the `.tex` line number.
Never modify the user's repository to get these numbers:

1. `rsync` the repo (including figure PDFs, excluding `.git` and the `documentation*.pdf` outputs) into a temp directory.
2. In the copy, prepend `\label{ln:N}` to each cited line (two labels in one `equation`/`align` row cause "Multiple \label's"; drop one).
3. Run `latexmk -pdf` and read `\newlabel{ln:N}{{eq}{page}...}` from the `.aux`.
4. Check against the user's own PDF (`pdfinfo` page count, `pdftotext -f P -l P` for a few equation tags) before trusting the numbers.
5. Rebuild every time you cite, because the user edits the `.tex` between turns.

A label inside a `\notag` row takes the next numbered row's number; say "unnumbered row above Eq. (x)".
A cited line inside a commented-out block is not in the PDF; point to the nearest active equation and say so.

### Python scripts

Follow the user's global rules: type hints, PEP8, no magic numbers (name tolerances and step sizes), cite the source of any published method, fail loudly, and *ask before saving a script to disk*.
Prefer a standalone script that runs without an LLM in the loop, and say so.
Do not write unit tests unless asked.

### Files in this skill

- `scripts/fetch_guide.py`: refresh the Guide from GitHub (standard library only).
- `scripts/compile_tex.py`: compile a derivation with real LaTeX and the lab macros, render PNGs, fail loudly.
- `references/notation.md`, `identities.md`, `pitfalls.md`, `numerical-checks.md`, `artifact-page.md`.
- Requires `latexmk` (MacTeX), `pdftoppm` (`brew install poppler`), `git`, and the `writing-review` skill from the same `commandlab-skills` clone (it holds the lab preamble).
