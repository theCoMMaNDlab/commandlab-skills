# Notation and conventions

Source: M. Holland, *The Hitchhiker's Guide to Abaqus* (Preface, Ch. 3, Ch. 4, Appendices on continuum mechanics and symmetry), https://github.com/mholla/hitchhikers-guide-to-abaqus.
This file is a convenience summary; the freshly fetched Guide (`scripts/fetch_guide.py`) is authoritative and wins on any disagreement.

## Macros

Defined in `writing-review/references/preamble.tex` in the same `commandlab-skills` clone (single source of truth, identical to the macros in the Guide's `documentation.tex` — do not redefine).
These are what the skill's output uses, so the user can paste it into a paper.

| macro | use | example |
|---|---|---|
| `\ten{A}` | first- and second-order tensors (bold italic) | `\ten{F}`, `\ten{\sigma}` |
| `\tenf{C}` | fourth-order tensors (bold sans-serif) | `\tenf{C}_{IJKL}` |
| `\scas{e}` | roman label at script size, for sub/superscripts | `\ten{F}^{\scas{e}}` |
| `\tens{C}` | bold script-size, for subscripts after a bar | `\left.\cdot\right|_{\tens{C}}` |
| `\sca{d}` | roman upright (differentials) | `\sca{d}V_0` |
| `\mat{}` | matrices (Voigt, FE arrays) | |
| `\rev{}` | red revision markup | |

## Configurations and indices

- Reference (material): upper-case indices, $\ten{X}$, $V_0$, $M_0$.
- Intermediate (grown): bar, $\overline{\ten{X}}$, $\overline{V}$, $\overline{M}$; indices written upper-case (the document assumes diagonal/symmetric $\ten{F}^{\scas{g}}$ so intermediate and reference directions coincide).
- Current (spatial): lower-case indices, $\ten{x}$, $v$, $m$.
- $\ten{F}=\ten{F}^{\scas{e}}\cdot\ten{F}^{\scas{g}}$; $\ten{F}^{\scas{g}}$ maps reference$\to$intermediate, $\ten{F}^{\scas{e}}$ maps intermediate$\to$current.
- $J=\det\ten{F}=J^{\scas{e}}J^{\scas{g}}$; $\vartheta^{\scas{g}}=\det\ten{F}^{\scas{g}}$ in the single-variable model.
- $\ten{C}=\ten{F}^{\scas{T}}\ten{F}$, $\ten{C}^{\scas{e}}=\ten{F}^{\scas{eT}}\ten{F}^{\scas{e}}=\ten{F}^{\scas{g}-1}\,\ten{C}\,\ten{F}^{\scas{g}-1}$ (for symmetric $\ten{F}^{\scas{g}}$).

## Energy with growth

- Per unit reference volume: $W_0$ (and per mass $\psi_0$).
  Per unit *grown* volume: $\overline{W}$ (and $\overline{\psi}$).
  Related by $W_0 = J^{\scas{g}}\,\overline{W}$, $\psi_0 = J^{\scas{g}}\,\overline{\psi}$.
- $\ten{S} = 2\,\partial W_0/\partial\ten{C}|_{\vartheta^{\scas{g}}}$.

## Tangents (Ch. 3)

- Lagrangian: $\tenf{C}_{IJKL} = 2\,\partial\ten{S}_{IJ}/\partial\ten{C}_{KL}$.
- Eulerian: $\tenf{c}_{ijkl} = J^{-1}\tenf{C}_{IJKL}\ten{F}_{iI}\ten{F}_{jJ}\ten{F}_{kK}\ten{F}_{lL}$.
- Abaqus (Jaumann, per unit current volume): $\tenf{c}^{\scas{Abaqus}} = \tenf{c}+\tenf{c}'$, with $\tenf{c}'_{ijkl}=\tfrac12\left[\delta_{ik}\sigma_{jl}+\delta_{il}\sigma_{jk}+\delta_{jk}\sigma_{il}+\delta_{jl}\sigma_{ik}\right]$.
- The growth tangent has minor but generally not major symmetry; use the unsymmetric Jacobian option in Abaqus.
- Growth-specific stress and tangent relations are in Ch. 4 ("Mechanics of growth") of the Guide; read them from the fetched copy rather than from this file.
- Growth conventions: $\ten{F}^{\scas{g}}$ is symmetric, intermediate-configuration indices are capital, and the independent variables are $\ten{C}$ and $\ten{F}^{\scas{g}}$ (everything else expressed in them).

## Derivatives with respect to tensors

- Definition: $\left.\frac{\sca{d}}{\sca{d}\varepsilon}f(\ten{X}+\varepsilon\,\sca{d}\ten{X})\right|_{\varepsilon=0} = f_{,\ten{X}} : \sca{d}\ten{X}$ for all *admissible* $\sca{d}\ten{X}$.
- Non-symmetric $\ten{X}$: $\{\partial\ten{A}/\partial\ten{X}\}_{IJKL}=\partial\ten{A}_{IJ}/\partial\ten{X}_{KL}$.
- Symmetric $\ten{X}$ (e.g. $\ten{C}$, $\ten{S}$): the derivative is only defined up to a skew part, so impose symmetry in every slot whose tensor is symmetric:
  $\partial\ten{X}/\partial\ten{X} = \tfrac12\left[\ten{I}\overline{\otimes}\ten{I}+\ten{I}\underline{\otimes}\ten{I}\right]$.
  Consequence for checking: finite differences must use *symmetric* perturbations, and a formula is verified by comparing the contraction with $\sca{d}\ten{X}$, not component by component.
- Voigt (Abaqus/Standard): order 11, 22, 33, 12, 13, 23; only tensors with minor symmetry can be stored as $6\times6$.

## Style for derivations

- Use `={}&` so the equals sign aligns and spaces correctly.
- Elided derivations in the source document appear as `\cdots{}& \notag`; in answers, show the steps instead.
