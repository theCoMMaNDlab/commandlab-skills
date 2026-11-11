# Numerical checks

Offer these; do not run or save unless the user accepts (or explicitly asked to "verify").
Prefer a standalone Python/NumPy script that runs without an LLM.

## Recipe: directional-derivative (finite-difference) check

For a tensor-valued $\ten{G}(\ten{X})$ with claimed derivative $\tenf{D}=\partial\ten{G}/\partial\ten{X}$:

1. Choose a random but physically admissible state (e.g. $\ten{F}=\ten{I}+0.3\,\ten{R}$ with $\det\ten{F}>0$; $\ten{F}^{\scas{g}}$ symmetric positive definite).
2. Choose a random perturbation $\sca{d}\ten{X}$ with the same symmetry as $\ten{X}$ (symmetric if $\ten{X}$ is symmetric).
3. Central difference: $\left[\ten{G}(\ten{X}+h\,\sca{d}\ten{X})-\ten{G}(\ten{X}-h\,\sca{d}\ten{X})\right]/(2h)$.
4. Compare with $\tenf{D}:\sca{d}\ten{X}$ (`np.einsum("ijkl,kl->ij", D, dX)`).
5. Report the max absolute difference.
   Typical: $h\sim10^{-6}$, agreement $\sim10^{-8}$ to $10^{-9}$.
   A wrong formula typically misses by $O(1)$.

For a *tangent* defined as $2\,\partial\ten{S}/\partial\ten{C}$, compare $\tfrac12\tenf{C}:\sca{d}\ten{C}$ with $\sca{d}\ten{S}$ (the factor of 2 is part of the definition).

Also useful:
- Compare two routes to the same quantity (e.g. $\ten{\sigma}$ from $\ten{S}$ vs. from $\overline{\ten{S}}$; $\tenf{c}^{\scas{e}}$ pushed forward from $\tenf{C}^{\scas{e}}$ vs. from $\tenf{L}^{\scas{e}}$) — these should agree to machine precision.
- Separate failing terms: evaluate the formula with and without a suspect term and compare both errors to the finite difference.
- Re-run at a second random seed; an accidental match at one state is possible.

## Template (adapt; keep constants named)

```python
"""Finite-difference check of a tensor derivative (template).

Method: central-difference directional derivative compared with the claimed
derivative contracted with an admissible (symmetry-respecting) perturbation.
See e.g. Holzapfel (2000), Nonlinear Solid Mechanics, Sec. 2.4 for directional derivatives.
"""
import numpy as np

STEP = 1e-6          # finite-difference step h
TOLERANCE = 1e-7     # accept if max |FD - formula| below this
SEED = 0


def symmetrize(a: np.ndarray) -> np.ndarray:
    """Return the symmetric part of a second-order tensor."""
    return 0.5 * (a + a.T)


def directional_check(g, D, X: np.ndarray, dX: np.ndarray) -> float:
    """Max abs difference between FD of g along dX and D : dX.

    g: callable, second-order tensor -> second-order tensor.
    D: claimed derivative, array of shape (3, 3, 3, 3).
    """
    fd = (g(X + STEP * dX) - g(X - STEP * dX)) / (2 * STEP)
    analytic = np.einsum("ijkl,kl->ij", D, dX)
    return float(np.abs(fd - analytic).max())


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    # Replace with the function, state, and claimed derivative under test.
    raise SystemExit(
        "Template only: fill in g, D, X, dX for the derivative being checked."
    )
```

## Orthogonal derivations (menu)

- **Gateaux vs. index calculus**: derive $\sca{d}\ten{G}[\sca{d}\ten{X}]$ by differentiating along $\ten{X}+\varepsilon\,\sca{d}\ten{X}$, then read off the fourth-order tensor.
- **Spectral / principal axes** for isotropic functions: $\ten{S}=\sum_a 2\,\partial W/\partial\lambda_a^2\,\ten{N}_a\otimes\ten{N}_a$; useful to check log neo-Hookean results.
- **Special cases**: $\ten{F}^{\scas{g}}=\ten{I}$ must reproduce Ch. 3 results; isotropic growth $\ten{F}^{\scas{g}}=\vartheta^{1/3}\ten{I}$; uniaxial stretch; simple shear.
- **Energy / power consistency**: $\ten{S}:\tfrac12\dot{\ten{C}}=\ten{\tau}:\ten{d}$.
- **Objectivity**: replace $\ten{F}\to\ten{Q}\ten{F}$; $\ten{\sigma}\to\ten{Q}\ten{\sigma}\ten{Q}^{\scas{T}}$, $\ten{C}$, $\ten{S}$ unchanged.
- **Symbolic**: SymPy for a component-wise derivative with a diagonal or simple-shear $\ten{F}$.
