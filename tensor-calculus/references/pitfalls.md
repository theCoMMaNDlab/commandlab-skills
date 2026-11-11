# Pitfalls

## General lessons

- **Hidden-factor rule.** Any multiplicative factor (Jacobian, density ratio, growth variable, structural tensor) that depends on the differentiation variable adds a product-rule term in *every* downstream derivative: stress, tangent, dissipation, and any local Newton linearization.
- **Which $J$.** Push forward with the Jacobian that matches the reference measure of the quantity: total $J=J^{\scas{e}}J^{\scas{g}}$ for quantities per unit reference volume; $J^{\scas{e}}$ only for quantities per unit grown volume.
- **Absorbed versus explicit factors.** After pulling a factor into a defined symbol (e.g. a tangent whose definition already contains $J^{-1}$), do not apply it again.
- **Held-fixed variables.** State what is held fixed in each partial derivative (e.g. $|_{\vartheta^{\scas{g}}}$ versus $|_{\ten{C}}$); the same symbol differentiated at different fixed variables gives different results.
- **Symmetric perturbations.** Check derivatives with respect to a symmetric argument by contracting with a symmetric perturbation; the symmetrized derivative is unique only on symmetric directions.

## Checklist before presenting a result

1. Full argument list written down; "held fixed" stated.
2. Every factor scanned for dependence on the differentiation variable.
3. Jacobian factors counted once, with the right $J$.
4. Free/dummy indices audited on both sides.
5. Symmetries stated.
6. Independent check offered (numerical and/or orthogonal derivation).
