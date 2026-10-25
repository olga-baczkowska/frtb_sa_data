# Methodology: FRTB SA GIRR delta capital

Model ID: [FRTB-SA-GIRR-D] · Owner: [team] · Version: [1.0] · Status: [draft]

Rule text: BCBS MAR21, in force 1 Jan 2023, version published 23 Mar 2026 (extracts in `docs/reg/`). Parameters: `params/girr_delta.yaml`.

## 1. Scope

1.1 Delta capital for general interest rate risk (GIRR) under the sensitivities-based method: risk-free yield curves, inflation and cross-currency basis (MAR21.8(1)–(3)).

1.2 Out of scope: GIRR vega and curvature, other risk classes, DRC and RRAO. The SBM total across risk classes and the choice of binding scenario (MAR21.7) belong to the aggregation layer.

## 2. Inputs and units

2.1 One net sensitivity s_k per risk factor k, in the reporting currency per unit of rate: s_k = [V(r_t + 0.0001) − V(r_t)] / 0.0001 (MAR21.19). A PV01 quoted per basis point is the numerator; divide it by 0.0001 before use.

2.2 Yield-curve tenors: 0.25, 0.5, 1, 2, 3, 5, 10, 15, 20 and 30 years (MAR21.8(1)). Map other points to them by linear interpolation or the method most consistent with pricing (MAR21.8, footnote 3); never compute on internal tenors (FAQ to MAR21.8).

2.3 Curves: an OIS curve and each BOR tenor curve are different curves, and so are onshore and offshore curves (MAR21.8(1)(c)). Inflation: one flat curve per currency. Cross-currency basis: over USD or over EUR, flat (MAR21.8(2)–(3)).

2.4 Buckets: one per currency (MAR21.41). Sensitivities to the same risk factor are netted before weighting (MAR21.4(2)).

## 3. Risk weights (MAR21.42–21.44)

| Tenor (years) | 0.25 | 0.5 | 1 | 2 | 3 | 5 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| Risk weight | 1.7% | 1.7% | 1.6% | 1.3% | 1.2% | 1.1% | 1.1% | 1.1% | 1.1% | 1.1% |

3.1 Inflation and cross-currency basis: 1.6% (MAR21.43).

3.2 The optional division by √2 for EUR, USD, GBP, AUD, JPY, SEK, CAD and the domestic reporting currency (MAR21.44) is an election: see §7.

## 4. Correlations

4.1 Same curve, different tenors: ρ = max(exp(−θ · |T_k − T_l| / min(T_k, T_l)), 40%), θ = 3% (MAR21.46, footnote 13).

4.2 Different curves: 99.9% at the same tenor (MAR21.45); 4.1 × 99.9% at different tenors (MAR21.47); 99.9% between two inflation curves (FAQ to MAR21.47).

4.3 Inflation and a yield-curve tenor: 40% (MAR21.48). Cross-currency basis and anything else: 0% (MAR21.49).

4.4 Across currencies: γ = 50% (MAR21.50).

4.5 The matrix in 4.1 is not positive semi-definite: MAR21.46 Table 2 has a smallest eigenvalue of about −0.165. The sum under the root in 5.2 can therefore be negative for real positions (G5).

## 5. Aggregation (MAR21.4)

5.1 WS_k = RW_k · s_k

5.2 K_b = √max(0, Σ_k WS_k² + Σ_k Σ_{l≠k} ρ_kl · WS_k · WS_l)

5.3 S_b = Σ_k WS_k, and capital = √(Σ_b K_b² + Σ_b Σ_{c≠b} γ_bc · S_b · S_c)

5.4 If the sum under the root in 5.3 is negative, recompute it with S_b = max(min(Σ_k WS_k, K_b), −K_b) (MAR21.4(5)(b)).

## 6. Correlation scenarios (MAR21.6–21.7)

6.1 Compute §5 three times: medium (correlations as in §4), high (each ρ and γ multiplied by 1.25, capped at 100%) and low (each replaced by max(2·ρ − 100%, 75%·ρ)).

6.2 Return all three. The binding scenario is the one with the largest SBM total across all risk classes (MAR21.7), never a maximum per risk class.

## 7. Elections and interpretations

| Item | Choice | Reference |
|---|---|---|
| √2 divisor | [Not elected]. If elected, settle whether it also applies to the 1.6% weights in MAR21.43. | MAR21.44 |
| Reporting currency | [EUR] | MAR21.15 |
| Bases with neither leg in USD or EUR | [Computed over EUR] | MAR21.8(3)(b) |
| Zero or market rate sensitivities | [As in our pricing models] | FAQ to MAR21.17 |
| Tenor correlations | From the formula in 4.1; Table 2 shows the same values rounded to 0.1% | MAR21.46 |

## 8. Validation (golden cases)

Each case gives net sensitivities s (EUR per unit of rate) and GIRR delta capital in EUR per scenario. Tolerance: EUR 0.01. [The values were computed for this example; confirm them with an independent calculation before sign-off.]

| Case | Sensitivities | Low | Medium | High | Tests |
|---|---|---|---|---|---|
| G1 | EUR-ESTR 10y +1.0e8 | 1,100,000.00 | 1,100,000.00 | 1,100,000.00 | Weighting, one factor |
| G2 | EUR-ESTR 2y −9.0e7, 10y +9.0e7 | 745,868.78 | 542,549.64 | 180,000.00 | Tenor correlation; high capped at 100% |
| G3 | EUR-ESTR 10y +1.0e8; USD-SOFR 10y −1.0e8 | 1,229,837.39 | 1,100,000.00 | 952,627.94 | γ across currencies |
| G4 | EUR: ESTR 10y +1.0e8, HICP inflation +6.875e7, EUR/USD basis +6.875e7. USD: SOFR 10y, CPI inflation and USD/EUR basis, same sizes, opposite signs | 737,902.43 | 2,144,294.76 | 1,905,255.89 | Alternative S_b in medium and high (5.4) |
| G5 | EUR-ESTR 1y +1.0e8, 5y −2.0e8, 30y +1.0e8 | 881,214.58 | 0.00 | 0.00 | K_b floor in medium and high (5.2, 4.5) |

Also test that capital scales linearly when every s is multiplied by a positive number, and that a currency with zero sensitivities changes nothing.

## 9. Change log

| Version | Date | Change |
|---|---|---|
| [1.0] | [date] | Initial version |
