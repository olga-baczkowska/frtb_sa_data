---
description: Rules for FRTB SA (SBM) capital code
applyTo: "src/frtb/sa/**,tests/**"
---
- Load every RW, ρ and γ from params/*.yaml; never type one. Why: GIRR weights changed 2016→2019; training data holds both.
- Return low, medium and high scenarios; take the max only on the SBM total (MAR21.7).
- Floor the √ argument of K_b at 0; if the across-bucket sum < 0, use the alternative S_b (MAR21.4). Both can bind: see golden cases G4 and G5.
- GIRR √2 divisor (MAR21.44): not elected.
- Cite the MAR21 ¶ in every docstring.
- Done = make test green, incl. tests/golden/.
