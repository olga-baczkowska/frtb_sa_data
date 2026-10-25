---
description: Rules for analytic option pricers
applyTo: "src/pricing/**,tests/**"
---
- European exercise only. American: route to the tree pricer and say so; never approximate.
- Dividends: continuous yield q from market data. Discrete dividends: stop and ask.
- Vega and rho per 1% move, theta per calendar day. Why: the risk system reports those units.
- T → 0 or σ → 0: return DF·max(F − K, 0) for a call (put alike); never NaN.
- Cite the model spec section in every docstring.
- Done = make test green, incl. tests/benchmark/.
