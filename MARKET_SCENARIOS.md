# Market Data Scenarios — Synthetic FRTB SA Dataset

Realized market paths for the 24 monthly snapshots (2024-07-31 … 2026-06-30)
underlying the EQUITY / FX / GIRR / CSR NON-SEC sensitivity files and the
DRC NON-SEC JTD files. All figures below are taken from the shipped
`REF_*_MARKET_DATA` reference files (fixed seed — a regeneration with the
same seed reproduces them exactly).

The scenario set has two layers: **stochastic baseline paths** (factor
models per asset class) and **scripted discrete events** (one coordinated
cross-asset stress, three rating migrations, and pegged-pair controls).
An important property of this seed's realization: the scripted shock landed
inside a stochastic downtrend that the simulated paths produced on their
own — the stress is a sharp step within a broader bear market, not an
isolated V-shaped event.

---

## Phase 1 — Benign grind higher (Jul 2024 – May 2025)

- Equities rally ~19% (SPX proxy 5,500 → 6,535 peak at 2025-05-31);
  short-dated vol drifts from 14.6 down to 11.8.
- Credit tightens: iTraxx Main 50 → 34–38bp; Crossover oscillates
  250–420bp on stochastic noise.
- Rates range-bound: EUR 10Y ≈ 2.55–2.70%; PLN 2Y ≈ 5.1–5.3%.
- FX quiet; mild EUR strength late in the phase.
- Attribution drivers in this phase are dominated by lifecycle effects
  (the seasoned book's expiry wave) and idiosyncratic single-name moves,
  not the market.
- **Scripted event within this phase**: BAYER downgrade BBB → BB at
  2025-05-31 (CSR bucket 7 → 15, Underlying `BAYER_7` → `BAYER_15`,
  RWLabel `7_BBB` → `15_BB`, 5Y spread 88 → 190bp). Deliberately placed in
  the calm phase so its capital impact is isolated from market noise.

## Phase 2 — Stochastic deterioration (Jun – Aug 2025)

Purely emergent from the factor draws; pre-dates the scripted stress:

- Equities give back ~16% from the peak (6,535 → 5,493); vol rises.
- USD weakens vs EUR (USDEUR 0.885 → 0.817).
- Crossover re-widens toward 400bp.
- **Test property**: an agent explaining the September move must not
  attribute the June–August drift to the September event — the
  deterioration has no discrete cause.
- **Scripted event**: RENAULT upgrade BB → BBB at 2025-07-31
  (bucket 13 → 5, spread ×0.65) — an upgrade landing in a weakening tape.

## Phase 3 — Scripted global risk-off, 2025-09-30

One coordinated shock, expressed consistently but heterogeneously per class:

| Class | Realized signature at 2025-09-30 |
|---|---|
| EQUITY | −8% global-factor leg (SPX 5,493 → 4,941); short vol 15.8 → 17.5; cluster of 47 barrier knockouts |
| FX | Risk-off reversal: USD +7.3% vs EUR, JPY/CHF appreciate, TRY −19%; FX vols spike (USDEUR 0.5Y vol ×~1.5); pegged DKK/BGN unmoved |
| GIRR | Bull steepener in majors: EUR 2Y −71bp / 10Y −57bp; **opposite-signed** CEE risk premium: PLN 2Y +86bp; swaption ATM vols +49% |
| CSR NON-SEC | iTraxx Main 48 → 79bp (+63%); Crossover 341 → 772bp; index option vol 0.62 → 1.35; **gross CS01 falls slightly** — RPV01 shortens as hazard rises (see adversarial cases below) |

## Phase 4 — Aftermath and regime divergence (Oct 2025 – Jun 2026)

The classes deliberately behave differently after the shock because their
processes differ:

- **Rates persist** (factor random walk, no mean reversion): EUR 10Y stays
  at 1.88–2.00%, PLN 2Y stays above 6.1% through the end of the window —
  a permanent level shift.
- **Spreads and vols retrace** (OU processes): iTraxx Main back to 43bp by
  Feb 2026; equity short vol overshoots down to 9.7 in Dec 2025.
- **Equities keep bleeding** stochastically to the window trough
  (4,274 at 2026-03-31), ending −18.5% over the full 24 months.
- **Second, purely stochastic credit widening** in spring 2026 (Crossover
  back to ~700bp at 2026-04-30) with no scripted cause — a contrast case:
  the correct explanation is market drift, not a discrete event.
- **Scripted event**: GLENCORE downgrade BBB → BB at 2025-11-30
  (bucket 4 → 12, spread ×1.8), landing in the aftermath where it must be
  disentangled from stress decay.

---

## Controls and adversarial cases

1. **Pegged-pair non-event**: DKK and BGN hold their EUR pegs throughout,
   including through the stress (vols ~0.3% / ~0.15%) — a zero-move control
   for FX attribution.
2. **Falling gross CS01 under widening spreads** (2025-09-30): the
   sensitivity metric shrinks while risk increases, because risky duration
   shortens. A narrative reading falling gross CS01 as "de-risking" is
   confidently wrong; the REF market data holds the ground truth.
3. **Pre-stress drift vs event attribution**: phase 2's −16% equity move
   has no discrete cause; only the September step does.
4. **Sign-divergent rates within one risk class**: majors rally while CEE
   sells off at the same date — a "rates moved" summary loses the
   offsetting-capital story.
5. **Cross-sectional dispersion**: the global event has genuinely
   heterogeneous per-name magnitudes (NKY −6.6% over the full window vs
   SPX −18.5%; TRY −69%) — bucket-level attributions differ materially
   from the headline.

## Lifecycle events interacting with the scenarios

Beyond market moves, per-date capital changes are driven by: monthly new
business in every class; expiries throughout (heaviest in the seasoned
books' first ~6 months); equity/FX barrier knockouts clustering at the
stress (47 equity KOs at 2025-09-30); swaption and index-option expiries;
and the three rating migrations above, which change bucket, rating,
RWLabel and the Underlying's `_{bucket}` suffix while the trade population
is unchanged.

## Caveats

- Everything above describes **this seed's realization**. The phase
  structure (bull, deterioration, shock, divergent aftermath) is partly
  designed and partly luck of the draw — only the September shock, the
  three migrations, and the pegs are guaranteed by construction. If the
  dataset is regenerated with a different seed, re-derive this narrative
  from the `REF_*_MARKET_DATA` files rather than reusing this document.
- Model-level simplifications (flat smiles, single-curve GIRR pricing,
  flat hazard/recovery, etc.) are itemised per asset class in the main
  README's deviation lists.
