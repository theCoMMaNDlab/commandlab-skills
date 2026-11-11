# Identities (document notation)

Unless stated otherwise, $\ten{A}$ is non-symmetric and the derivative is the plain component derivative.
Where a symmetric argument is involved, symmetrize as in `notation.md`.

## Dyadic products

| definition | components |
|---|---|
| $\ten{A}\otimes\ten{B}$ | $A_{ij}B_{kl}$ |
| $\ten{A}\overline{\otimes}\ten{B}$ | $A_{ik}B_{jl}$ |
| $\ten{A}\underline{\otimes}\ten{B}$ | $A_{il}B_{jk}$ |

Contractions:

\begin{align}
[\ten{A}\otimes\ten{B}]:\ten{C} ={}& \ten{A}\,[\ten{B}:\ten{C}] \, , &
\ten{C}:[\ten{A}\otimes\ten{B}] ={}& [\ten{C}:\ten{A}]\,\ten{B} \, ,
\\
[\ten{A}\overline{\otimes}\ten{B}]:\ten{C} ={}& \ten{A}\,\ten{C}\,\ten{B}^{\scas{T}} \, , &
\ten{C}:[\ten{A}\overline{\otimes}\ten{B}] ={}& \ten{A}^{\scas{T}}\,\ten{C}\,\ten{B} \, ,
\\
[\ten{A}\underline{\otimes}\ten{B}]:\ten{C} ={}& \ten{A}\,\ten{C}^{\scas{T}}\,\ten{B}^{\scas{T}} \, , &
\ten{C}:[\ten{A}\underline{\otimes}\ten{B}] ={}& \ten{B}^{\scas{T}}\,\ten{C}^{\scas{T}}\,\ten{A} \, ,
\end{align}
and $[\ten{I}\otimes\ten{I}]:\ten{A}=\mathrm{tr}(\ten{A})\,\ten{I}$, $[\ten{I}\overline{\otimes}\ten{I}]:\ten{A}=\ten{A}$, $[\ten{I}\underline{\otimes}\ten{I}]:\ten{A}=\ten{A}^{\scas{T}}$.

## Derivatives (non-symmetric argument)

\begin{align}
\frac{\partial\ten{A}_{ij}}{\partial\ten{A}_{kl}} ={}& \delta_{ik}\delta_{jl} \, ,
&
\frac{\partial\ten{A}_{ji}}{\partial\ten{A}_{kl}} ={}& \delta_{il}\delta_{jk} \, ,
\\
\frac{\partial\ten{A}^{-1}_{ij}}{\partial\ten{A}_{kl}} ={}& -\ten{A}^{-1}_{ik}\ten{A}^{-1}_{lj} \, ,
&
\frac{\partial\ten{A}^{-1}}{\partial\ten{A}} ={}& -\ten{A}^{-1}\overline{\otimes}\ten{A}^{-\scas{T}} \, ,
\\
\frac{\partial\ten{A}^{-\scas{T}}}{\partial\ten{A}} ={}& -\ten{A}^{-\scas{T}}\underline{\otimes}\ten{A}^{-1} \, .
\end{align}

## Derivatives (symmetric argument, symmetrized)

\begin{align}
\frac{\partial\ten{X}}{\partial\ten{X}} ={}& \tfrac12\left[\ten{I}\overline{\otimes}\ten{I}+\ten{I}\underline{\otimes}\ten{I}\right] \, ,
\\
\frac{\partial\ten{X}^{-1}}{\partial\ten{X}} ={}& -\tfrac12\left[\ten{X}^{-1}\overline{\otimes}\ten{X}^{-1}+\ten{X}^{-1}\underline{\otimes}\ten{X}^{-1}\right] \, .
\end{align}

## Invariants and determinants

\begin{align}
\frac{\partial\,\mathrm{tr}(\ten{C})}{\partial\ten{C}} ={}& \ten{I} \, ,
&
\frac{\partial J}{\partial\ten{F}} ={}& J\,\ten{F}^{-\scas{T}} \, ,
\\
\frac{\partial J}{\partial\ten{C}} ={}& \frac{J}{2}\,\ten{C}^{-1} \, ,
&
\frac{\partial\ln J}{\partial\ten{C}} ={}& \frac12\,\ten{C}^{-1} \, ,
\\
\frac{\partial J^{-2/3}}{\partial\ten{C}} ={}& -\frac13\,J^{-2/3}\,\ten{C}^{-1} \, .
\end{align}

## Time derivatives and rates

\begin{align}
\dot{\ten{F}} ={}& \ten{l}\cdot\ten{F} \, , \qquad
\frac{\partial\ten{F}^{-1}}{\partial t} = -\ten{F}^{-1}\cdot\ten{l} \, , \qquad
\dot{J} = J\,\mathrm{tr}(\ten{l}) \, ,
\\
\dot{\ten{E}} ={}& \ten{F}^{\scas{T}}\cdot\ten{d}\cdot\ten{F} \, ,
\qquad \ten{l}=\ten{d}+\ten{w} \, ,
\\
\ten{\sigma}^{\circ} ={}& \dot{\ten{\sigma}}-\ten{l}\ten{\sigma}-\ten{\sigma}\ten{l}^{\scas{T}}+\mathrm{tr}(\ten{l})\,\ten{\sigma} \, ,
\qquad
\ten{\tau}^{\circ} = J\,\ten{\sigma}^{\circ} = \ten{F}\,\dot{\ten{S}}\,\ten{F}^{\scas{T}} \, ,
\\
\ten{\tau}^{\circ} ={}& \ten{\tau}^{\nabla}-\ten{d}\ten{\tau}-\ten{\tau}\ten{d} \, ,
\qquad
\ten{A}^{\nabla}=\dot{\ten{A}}-\ten{w}\ten{A}+\ten{A}\ten{w} \, .
\end{align}

Growth: $\dot{J}^{\scas{g}} = J^{\scas{g}}\,\mathrm{tr}(\ten{L}^{\scas{g}})$ with $\ten{L}^{\scas{g}}=\dot{\ten{F}}^{\scas{g}}\ten{F}^{\scas{g}-1}$.
If $\vartheta^{\scas{g}}=\det\ten{F}^{\scas{g}}$ then $\ten{F}^{\scas{g}-1}_{MN}\,\partial\ten{F}^{\scas{g}}_{MN}/\partial\vartheta^{\scas{g}}=1/\vartheta^{\scas{g}}$.

## Push-forward / pull-back (rules of thumb; derive each quantity)

- Piola (stress-like, contravariant 2-tensor): $\ten{\sigma}=J^{-1}\ten{F}\ten{S}\ten{F}^{\scas{T}}$; derive the factor for each additional configuration.
- Strain-like (covariant): $\ten{C}^{\scas{e}}=\ten{F}^{\scas{g}-\scas{T}}\ten{C}\ten{F}^{\scas{g}-1}$, $\ten{E}=\ten{F}^{\scas{T}}\ten{e}\ten{F}$.
- Fourth-order tangent (Lagrangian $\to$ Eulerian): $\tenf{c}_{ijkl}=J^{-1}\tenf{C}_{IJKL}\ten{F}_{iI}\ten{F}_{jJ}\ten{F}_{kK}\ten{F}_{lL}$; same pattern with $\ten{F}^{\scas{g}}$ between reference and intermediate.

## Derivative of a push-forward / pull-back factor

- $\partial\ten{F}^{\scas{g}-1}_{IA}/\partial\ten{F}^{\scas{g}}_{MN} = -\tfrac12\left[\ten{F}^{\scas{g}-1}_{IM}\ten{F}^{\scas{g}-1}_{AN}+\ten{F}^{\scas{g}-1}_{IN}\ten{F}^{\scas{g}-1}_{AM}\right]$ (symmetric $\ten{F}^{\scas{g}}$).
- $\partial J^{\scas{g}}/\partial\ten{F}^{\scas{g}}_{MN} = J^{\scas{g}}\ten{F}^{\scas{g}-1}_{NM}$.
- $\partial\ten{C}^{\scas{e}}_{PQ}/\partial\ten{C}_{KL}|_{\vartheta^{\scas{g}}}=\tfrac12\left[\ten{F}^{\scas{g}-1}_{KP}\ten{F}^{\scas{g}-1}_{LQ}+\ten{F}^{\scas{g}-1}_{LP}\ten{F}^{\scas{g}-1}_{KQ}\right]$.
