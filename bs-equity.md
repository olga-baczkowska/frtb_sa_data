# Model specification: Black–Scholes–Merton, European equity options

Model ID: [EQ-BS-001] · Owner: [team] · Version: [1.0] · Status: [draft]

## 1. Scope

1.1 European calls and puts on single stocks and equity indices.

1.2 Out of scope: American or Bermudan exercise (use the tree pricer), discrete dividends, barriers and other path-dependent payoffs.

## 2. Assumptions and limitations

2.1 Lognormal spot; volatility, rate and dividend yield constant to expiry.

2.2 Dividends are a continuous yield q. Material discrete dividends during the option's life make the price unreliable (see 1.2).

2.3 No smile dynamics: σ is the implied volatility for this strike and expiry, supplied by market data.

## 3. Inputs and units

3.1 S spot and K strike in the option's currency; both > 0.

3.2 T year fraction to expiry from `pricing/dates.year_fraction()`; T ≥ 0.

3.3 r continuously compounded zero rate to expiry and q continuous dividend yield, both decimals.

3.4 σ annualised implied volatility as a decimal (0.20 = 20%); σ ≥ 0.

3.5 Invalid inputs raise `ValueError`. The pricer never returns NaN.

## 4. Pricing

4.1 F = S·exp((r − q)·T), DF = exp(−r·T)

4.2 d1 = [ln(F/K) + σ²·T/2] / (σ·√T), d2 = d1 − σ·√T

4.3 Call = DF·[F·N(d1) − K·N(d2)]; Put = DF·[K·N(−d2) − F·N(−d1)]

4.4 Limits: if T = 0 or σ = 0, Call = DF·max(F − K, 0) and Put = DF·max(K − F, 0).

## 5. Greeks and units

N is the standard normal distribution function and n its density.

| Greek | Call | Put | Unit |
|---|---|---|---|
| Delta | e^(−qT)·N(d1) | −e^(−qT)·N(−d1) | per unit of S |
| Gamma | e^(−qT)·n(d1) / (S·σ·√T) | same as call | per unit of S |
| Vega | S·e^(−qT)·n(d1)·√T / 100 | same as call | per 1% vol |
| Theta | [−S·e^(−qT)·n(d1)·σ / (2√T) − r·K·DF·N(d2) + q·S·e^(−qT)·N(d1)] / 365 | [−S·e^(−qT)·n(d1)·σ / (2√T) + r·K·DF·N(−d2) − q·S·e^(−qT)·N(−d1)] / 365 | per calendar day |
| Rho | K·T·DF·N(d2) / 100 | −K·T·DF·N(−d2) / 100 | per 1% rate |

## 6. Validation benchmarks

Tolerances: prices 1e-6, Greeks 1e-5.

6.1 Hull, Options, Futures, and Other Derivatives, 9th ed., Example 15.6: S = 42, K = 40, T = 0.5, r = 10%, q = 0, σ = 20% gives call 4.759422 and put 0.808599.

6.2 Dividend yield: S = K = 100, T = 1, r = 5%, q = 2%, σ = 25% gives:

| | Price | Delta | Gamma | Vega | Theta | Rho |
|---|---|---|---|---|---|---|
| Call | 11.123762 | 0.584955 | 0.015179 | 0.379481 | −0.016280 | 0.473717 |
| Put | 8.226837 | −0.395244 | 0.015179 | 0.379481 | −0.008620 | −0.477512 |

6.3 Put–call parity: Call − Put = S·e^(−qT) − K·DF, to 1e-10.

6.4 Limits: with the 6.2 inputs and σ = 0, call 2.896925 and put 0; with T = 0 and S = 105, call 5 and put 0.

6.5 Every Greek agrees with a central bump-and-reprice to 1e-5.

## 7. Change log

| Version | Date | Change |
|---|---|---|
| [1.0] | [date] | Initial version |
