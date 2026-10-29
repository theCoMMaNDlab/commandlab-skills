---
date_created: 2026-08-29 Sat
date_modified: 2026-08-29 Sat
description: Review Fortran or Python code (including Abaqus/UEL subroutines) against the CoMMaND lab's coding conventions — naming/capitalization consistency, Fortran declarations, spelling, formatting, dead code, documentation, magic numbers, potential bugs, repeated calculations, efficiency, loop consolidation, Python/Fortran best practices, modularity, and alignment with a reference paper when one is provided. Use whenever someone shares code and asks for a review, wants it checked before showing an advisor, or asks to check it against the lab's conventions.
name: code-review
---

## Code review

This skill encodes the CoMMaND lab's code review conventions, covering both Python and the lab's legacy/scientific Fortran (including Abaqus UEL subroutines, which follow different conventions than idiomatic Python and shouldn't be forced into Python idioms).

Same precision standard as the lab's `writing-review` skill: every point must be anchored to an exact location (quote the line, name the variable/function, give the line number if visible) — never a vague "check for X" that just pushes the work back onto the person. Don't mention what's already fine. No closing summary — the list of specific points is the entire deliverable.

Some things a lab checklist asks for (does the code actually reproduce every result in the paper, has the mesh-refinement/validation study actually been done, has someone actually run it end to end and signed off) require running the code or judging finished scientific work — not something reviewable from source alone. Those live in the "Code" addendum of the lab's [Writing style guide](https://drive.google.com/open?id=1JjN-z04sPDuR-2nwmUV6B3Vk3tdtVNaU4u-D1NsQYBs) as a human checklist. Mention it exists when relevant, don't try to check its items yourself.

## Workflow

1. If the person provides a reference paper the code implements, keep it open for the **Paper alignment** check below — otherwise skip that check entirely rather than guessing at intended behavior.
2. Run all of Sections 1–4 below by default — this is a full review, not an opt-in checklist.
3. If you have a way to actually execute the code (an available interpreter/compiler and its inputs), try running it and report the real outcome — errors, warnings, or success — rather than assuming it works. If you can't run it, say so rather than silently skipping the claim.
4. If the person points you at a folder (not just a single source file), treat it as a repo and also apply `references/repo-rules.md` — the same license/`.gitignore`/README/requirements checks apply whether or not the folder has a paper attached, a remote, or its own `.git`.
5. For a folder or repo, run `python3 -I <this skill's folder>/scripts/find_dupes.py <folder>` first and use its output for the **Single source of truth** check in Section 4 and the **Duplicate and generated files** item in `references/repo-rules.md`. It is read-only and needs no LLM; the judgment (is this copy intentional? what is the shared home?) is yours.
6. Write up findings grouped by section, same output format as `writing-review`: location → quote/reference → what's wrong. Skip any section with nothing to report.

## Section 1 — Style & declarations

- **Naming consistency.** Scan every variable and function name across all of its usages. If the same identifier appears with different capitalization in different places (e.g., declared as `Kuu` but used as `KUU` elsewhere), flag it.
- **Abaqus/UEL interface variables** (`NDOFEL`, `NRHS`, `LFLAGS`, `RHS`, `AMATRX`, `SVARS`, `PROPS`, `COORDS`, `JTYPE`, `KSTEP`, `KINC`, `JELEM`, etc.) should be ALL CAPS. User-defined variables and subroutines should be consistently lowercase or camelCase — flag a mix.
- **Comment case.** Comments should be lowercase or sentence case; flag ALL CAPS comments.
- Short or mathematical names (`Ru`, `Kuu`, `u`, `K`, `F`, `x`, `n`, `i`, `j`) are fine when used consistently, and names matching a provided reference paper's notation are correct — don't flag either.
- Only flag names that are actually inconsistent, cryptic with no domain meaning, or arbitrarily mix conventions.
- **Fortran variable declarations.** Flag a variable typed on one line and dimensioned separately via a `DIMENSION` statement (e.g., `REAL(8) :: TIME` followed by `DIMENSION TIME(2)`) — it should be combined (`REAL(8) :: TIME(2)`). List every affected variable.
- **Spelling.** Check comments, variable/function names, and string literals for actual misspellings.
- **American spelling.** The lab uses American English, so flag British variants in comments, identifiers, string literals, and plot labels, and give the American form. Cover whole families, not just examples: -our/-or (colour, behaviour), -ise/-isation (normalise, optimise, regularisation), -yse (analyse), -re (centre, fibre, metre), ae/oe medical terms (faeces, foetus, oedema, anaemia, oesophagus), and others (modelling, labelled, grey, ageing, artefact, programme). For identifiers, a rename can touch every usage, so list all occurrences. Exception: don't flag a name that must match an external API, file format, or library (e.g., a `colour` keyword some package requires); note it instead.
- **Formatting/indentation.** Flag inconsistent indentation or formatting that meaningfully harms readability — not every minor stylistic variation.

## Section 2 — Dead code & documentation

- **Dead code — be exhaustive.** Check every declared variable, array, parameter, and function. If it's never used in a computation, condition, output, or call after declaration, flag it — don't give the benefit of the doubt; if you can't find a usage, flag it.
- **Documentation.** Every function/subroutine should have a header comment explaining its purpose, and non-obvious logic should have inline comments. Flag what's missing.
- **Magic numbers.** Don't flag simple constants (0, 1, 2, 0.5, 0.25, 1.0, 1/3-style fractions) or hardcoded Abaqus/UEL interface flag integers (e.g. `lflags` values). Flag non-obvious literals (e.g. 0.84, 1.732) that appear with no comment or explanation.

## Section 3 — Logic & efficiency

- **Potential bugs.** Look for off-by-one index errors, inverted conditions, and copy-paste mistakes.
- **Repeated calculations.** Flag an expression computed multiple times in the same scope when its inputs haven't changed between computations. Don't flag calculations that legitimately vary per integration point or time step.
- **Efficiency.** Flag unnecessary work or clearly inefficient patterns, but only where the fix is straightforward and doesn't require restructuring the underlying logic.
- **Loop consolidation.** Look for separate loops over identical index ranges with no data dependency between them, where merging would clearly improve readability. Show the loop ranges and describe what each computes. Don't flag deep nesting that's structurally necessary (e.g. 4th-order tensor operations, nested integration-point loops).

## Section 4 — Best practices & modularity

- **Python:** flag global variables, missing type hints, and PEP 8 violations, including a missing `if __name__ == "__main__":` guard.
- **Fortran:** flag implicit typing (missing `IMPLICIT NONE`) and poor use of common blocks.
- Any `STOP` statement should be preceded by a descriptive `WRITE`/print explaining why execution is stopping — flag one that isn't.
- **Modularity — Fortran:** only flag if the code is extremely monolithic in a way that genuinely hurts readability. **Python:** flag logic that's clearly reusable but hasn't been broken into functions.
- **Single source of truth.** Anything used in more than one place should have one definition and multiple calls to it. Across a folder or repo, flag (a) byte-identical files in different locations, (b) near-identical source files (about 85% or more similar by line diff) that differ only in a few parameters, names or file paths, and (c) a routine, constant or block repeated within or between files. Name each pair or group with paths, say what differs, and suggest the shared home (a `common/` folder, a shared module or include, or one parameterized script). Constants repeated across files (a pressure, a time, a mesh radius) count too, since they must be edited in lockstep. Don't flag copies that diverge in real logic (for example a UMAT with a different constitutive model), but do say what base they share that could be factored out.
- **Paper alignment:** only when a reference paper has been explicitly provided. Flag any significant discrepancy between the paper's formulation and the implementation.
