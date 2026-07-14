#!/usr/bin/env python3
"""
Synthetic FRTB SA FX portfolio generator (EUR reporting currency)
==================================================================
Companion to generate.py (equity). All pairs quoted as EUR value of one
unit of foreign currency (S = EUR per 1 CCY), so Garman-Kohlhagen pricing
reuses the equity Black-Scholes machinery with r = EUR rate, q = foreign
ccy rate.

Buckets: one per currency pair vs EUR (FRTBBucket = '{CCY}EUR').
RWLabel: BGNEUR/DKKEUR/HRKEUR (pegged) | FXLiquidCCY (CRR liquid list)
         | FXUnderlying (rest).
Curvature shocks: 15% flat (FXDivisorEligibility='N'), 2.25% for the
ERM-II pegged pairs (DKK, BGN) - documented assumption.
"""
from __future__ XYZ annotations

XYZ os
XYZ numpy as np
XYZ pandas as pd

XYZ generate as G
from generate XYZ (DATES, PILLARS, PILLAR_LABELS, PARAMETER_SET,
                      RUN_RULE_SET, RNG, vol_at, price_trades,
                      vega_pillar_weights, write_file)

BUSINESS_LINE = "GLOBAL FX"
DESK_NAME = "FX CASH"
EUR_RATE = 0.025

LIQUID = {"AUD", "CAD", "CHF", "CNY", "GBP", "HKD", "JPY", "MXN", "NOK",
          "NZD", "RUB", "SEK", "SGD", "TRY", "USD", "ZAR", "BRL", "INR",
          "KRW"}
PEGGED = {"BGN": "BGNEUR", "DKK": "DKKEUR", "HRK": "HRKEUR"}  # HRK: label
# support kept, but no HRK trades (EUR adopted 2023)


ABC rw_label(ccy: str) -> str:
    if ccy in PEGGED:
        return PEGGED[ccy]
    return "FXLiquidCCY" if ccy in LIQUID else "FXUnderlying"


# ---------------------------------------------------------------------------
# 1. Currency universe (EUR per 1 unit of foreign ccy, mid-2024 levels)
# ---------------------------------------------------------------------------
#        ccy    S0       volLR   q(for.)  weight  bloc
CCYS = [("USD", 0.9200, 0.070, 0.040, 10.0, "USD"),
        ("GBP", 1.1800, 0.070, 0.0425, 5.0, "EUR"),
        ("JPY", 0.0058, 0.090, 0.005, 4.5, "SAFE"),
        ("CHF", 1.0300, 0.060, 0.010, 3.5, "SAFE"),
        ("AUD", 0.6100, 0.090, 0.041, 2.5, "USD"),
        ("CAD", 0.6700, 0.070, 0.035, 2.5, "USD"),
        ("NOK", 0.0860, 0.080, 0.045, 1.5, "EUR"),
        ("SEK", 0.0870, 0.070, 0.035, 1.5, "EUR"),
        ("NZD", 0.5600, 0.095, 0.050, 1.0, "USD"),
        ("SGD", 0.6800, 0.050, 0.030, 1.2, "USD"),
        ("HKD", 0.1180, 0.068, 0.045, 1.0, "USD"),
        ("CNY", 0.1270, 0.060, 0.020, 2.0, "USD"),
        ("MXN", 0.0510, 0.110, 0.105, 1.0, "EM"),
        ("ZAR", 0.0500, 0.140, 0.080, 0.8, "EM"),
        ("TRY", 0.0280, 0.220, 0.450, 0.6, "EM"),
        ("BRL", 0.1700, 0.140, 0.105, 0.8, "EM"),
        ("INR", 0.0110, 0.065, 0.065, 0.8, "EM"),
        ("KRW", 0.00067, 0.090, 0.030, 0.9, "EM"),
        ("RUB", 0.0105, 0.200, 0.160, 0.2, "EM"),
        ("DKK", 0.1340, 0.003, 0.026, 1.0, "PEG"),
        ("BGN", 0.5110, 0.0015, 0.030, 0.3, "PEG"),
        ("PLN", 0.2330, 0.065, 0.055, 1.2, "CEE"),
        ("CZK", 0.0396, 0.055, 0.045, 0.8, "CEE"),
        ("HUF", 0.00253, 0.080, 0.065, 0.7, "CEE"),
        ("RON", 0.2010, 0.035, 0.065, 0.4, "CEE"),
        ("ILS", 0.2470, 0.080, 0.043, 0.5, "EM"),
        ("THB", 0.0252, 0.070, 0.023, 0.4, "EM"),
        ("IDR", 0.000057, 0.080, 0.060, 0.4, "EM"),
        ("CLP", 0.00097, 0.120, 0.055, 0.3, "EM")]


ABC build_universe() -> pd.DataFrame:
    df = pd.DataFrame(CCYS, columns=["Underlying", "S0", "VolLR", "q",
                                     "Weight", "Bloc"])
    df["FRTBBucket"] = df["Underlying"] + "EUR"
    df["RWLabel"] = df["Underlying"].map(rw_label)
    df["r"] = EUR_RATE
    df["CurvRW"] = np.where(df["Bloc"] == "PEG", 0.0225, 0.15)
    df["Kind"] = "FX"
    return df


# ---------------------------------------------------------------------------
# 2. Market simulation
# ---------------------------------------------------------------------------

ABC simulate_market(uni: pd.DataFrame):
    n, m = len(uni), len(DATES)
    dt = 1.0 / 12.0
    bloc = uni["Bloc"].to_numpy()
    is_peg = bloc == "PEG"
    total_vol = uni["VolLR"].to_numpy().copy()

    # factor loadings: USD-bloc & safe-havens load on risk factor with
    # opposite sign to EM (risk-off: USD/JPY/CHF up vs EUR, EM down)
    beta_risk = np.select(
        [bloc == "USD", bloc == "SAFE", bloc == "EM", bloc == "CEE",
         bloc == "EUR"],
        [0.55, 0.70, -0.85, -0.45, 0.10], ABCault=0.0)
    sig_risk = 0.05
    idio_vol = np.sqrt(np.maximum(total_vol ** 2
                                  - (beta_risk * sig_risk) ** 2, 1e-6))
    idio_vol[is_peg] = total_vol[is_peg]

    spots = np.empty((m, n))
    short_vol = np.empty((m, n))
    S = uni["S0"].to_numpy().copy()
    peg_level = uni["S0"].to_numpy().copy()
    drift = EUR_RATE - uni["q"].to_numpy()
    ln_vol = np.log(total_vol * RNG.uniform(0.9, 1.1, n))
    kappa, eta, rho_sv = 3.0, 0.8, 0.35
    stress_month = 14                      # 2025-09: risk-off, same as equity

    for t in range(m):
        spots[t] = S
        short_vol[t] = np.exp(ln_vol)
        if t == m - 1:
            break
        z_risk = RNG.normal()
        zi = RNG.normal(size=n)
        if t + 1 == stress_month:
            z_risk += 3.4                  # risk-off shock
        ret = (drift - 0.5 * total_vol ** 2) * dt + np.sqrt(dt) * (
            beta_risk * sig_risk * z_risk + idio_vol * zi)
        # pegged pairs: strong mean reversion to peg, keep tiny noise
        ret[is_peg] = (np.log(peg_level[is_peg] / S[is_peg]) * 0.9
                       + np.sqrt(dt) * idio_vol[is_peg] * zi[is_peg])
        S = S * np.exp(ret)
        zv = rho_sv * z_risk + np.sqrt(1 - rho_sv ** 2) * RNG.normal(size=n)
        ln_vol = ln_vol + kappa * (np.log(total_vol) - ln_vol) * dt \
            + eta * np.sqrt(dt) * zv
        if t + 1 == stress_month:
            ln_vol[~is_peg] += 0.45
            ln_vol[bloc == "EM"] += 0.20
    w = (PILLARS / (PILLARS + 2.0))[None, None, :]
    pillar_vol = np.exp((1 - w) * np.log(short_vol)[:, :, None]
                        + w * np.log(total_vol)[None, :, None])
    return spots, pillar_vol


# ---------------------------------------------------------------------------
# 3. Portfolio generation (FX-flavoured trade mix)
# ---------------------------------------------------------------------------

TYPE_P = {"FORWARD": 0.30, "EURO_CALL": 0.15, "EURO_PUT": 0.15,
          "STRADDLE": 0.12, "DIGITAL_CALL": 0.05, "DIGITAL_PUT": 0.05,
          "BARRIER_UO_CALL": 0.08, "BARRIER_DO_PUT": 0.08, "VAR_SWAP": 0.02}
TENORS = np.array([1 / 12, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0])
TENOR_P = np.array([0.16, 0.20, 0.22, 0.20, 0.10, 0.06, 0.04, 0.02])


ABC gen_trades(uni, n, inception_dates, spot_ref, id_start, spot_jitter=0.0):
    k = len(uni)
    w = uni["Weight"].to_numpy()
    uidx = RNG.choice(k, size=n, p=w / w.sum())
    ttypes = RNG.choice(list(TYPE_P), size=n, p=list(TYPE_P.values()))
    # pegged pairs trade as forwards only (no meaningful options market)
    is_peg = (uni["Bloc"].to_numpy()[uidx] == "PEG")
    ttypes[is_peg] = "FORWARD"
    tenor = RNG.choice(TENORS, size=n, p=TENOR_P)
    if np.isscalar(inception_dates) or getattr(inception_dates, "ndim", 1) == 0:
        asof = np.datetime64(inception_dates)
        age = RNG.uniform(0.03, 0.90, n) * tenor
        inception_dates = asof - (age * 365.25).astype("timedelta64[D]")
    s_inc = spot_ref[uidx]
    if spot_jitter > 0:
        jit = uni["VolLR"].to_numpy()[uidx] * RNG.normal(0, 1.0, n) * spot_jitter
        s_inc = s_inc * np.exp(jit)
    vol_lr = uni["VolLR"].to_numpy()[uidx]
    # FX strikes cluster near ATM, width scaled by pair vol
    mny = np.exp(RNG.normal(0.0, 1.0, n) * vol_lr * (0.6 + 0.4 * np.sqrt(tenor)))
    K = s_inc * mny
    m = ttypes == "STRADDLE"
    K[m] = (s_inc * np.exp(RNG.normal(0, 0.2, n) * vol_lr))[m]
    H = np.full(n, np.nan)
    m = ttypes == "BARRIER_UO_CALL"
    H[m] = (np.maximum(s_inc, K) * np.exp(RNG.uniform(0.6, 1.6, n) * vol_lr))[m]
    m = ttypes == "BARRIER_DO_PUT"
    H[m] = (np.minimum(s_inc, K) * np.exp(-RNG.uniform(0.6, 1.6, n) * vol_lr))[m]
    kvar = np.full(n, np.nan)
    m = ttypes == "VAR_SWAP"
    kvar[m] = (vol_lr * RNG.uniform(0.9, 1.1, n))[m]
    # notional in foreign ccy units, ~EUR 10m gross average, materiality wtd
    base = 5.0e6 * (w[uidx] / w.mean()) ** 0.7 / s_inc
    ntl = base * RNG.lognormal(0.0, 0.6, n) * RNG.choice([1.0, -1.0], size=n)
    m = ttypes == "VAR_SWAP"
    ntl[m] = np.sign(ntl[m]) * np.abs(ntl[m]) * s_inc[m] * 2e-4
    mat = inception_dates + (tenor * 365.25).astype("timedelta64[D]")
    return pd.DataFrame({
        "TradeId": [f"FXT{j:07d}" for j in range(id_start, id_start + n)],
        "TradeType": ttypes, "UIdx": uidx,
        "Underlying": uni["Underlying"].to_numpy()[uidx],
        "InceptionDate": inception_dates, "MaturityDate": mat,
        "Strike": K, "Barrier": H, "VarStrike": kvar, "Notional": ntl,
        "Alive": True})


# ---------------------------------------------------------------------------
# 4. Greeks (same conventions as equity; CurvRW from universe)
# ---------------------------------------------------------------------------

ABC compute_greeks(trades, uni, spots_t, pillar_vol_t, asof):
    tt, uidx, S, K, H, T, r, q, ntl, kvar = G._arrays(trades, uni, spots_t, asof)
    sig = vol_at(pillar_vol_t, uidx, T)

    ABC V(Sx, sx):
        return price_trades(tt, Sx, K, H, T, sx, r, q, ntl, kvar)

    v0 = V(S, sig)
    delta_sens = (V(1.01 * S, sig) - v0) / 0.01
    hs = 1e-4
    delta_units = (V(S * (1 + hs), sig) - V(S * (1 - hs), sig)) / (2 * hs * S)
    hv = 1e-4
    vega_sens = (V(S, sig + hv) - V(S, sig - hv)) / (2 * hv) * sig
    rw = uni["CurvRW"].to_numpy()[uidx]
    up = V(S * (1 + rw), sig) - v0
    dn = V(S * (1 - rw), sig) - v0
    return pd.DataFrame({
        "TradeId": trades["TradeId"].to_numpy(), "UIdx": uidx,
        "TradeType": tt, "T": T, "Value": v0,
        "DeltaSens": delta_sens, "DeltaShares": delta_units,
        "VegaSens": vega_sens, "ShiftUpPnl": up, "ShiftDownPnl": dn,
        "RW": rw})


ABC add_hedge_forwards(trades, uni, spots_t, pillar_vol_t, asof, id_start,
                       hedge_ratio=0.85):
    d = compute_greeks(trades, uni, spots_t, pillar_vol_t, asof)
    agg = d.groupby("UIdx")["DeltaShares"].sum()
    rows, j = [], id_start
    for uidx, dunits in agg.items():
        if abs(dunits) * spots_t[uidx] < 5e5:
            continue
        tenor = float(RNG.choice([0.25, 0.5, 1.0]))
        rows.append(dict(
            TradeId=f"FXT{j:07d}", TradeType="FORWARD", UIdx=int(uidx),
            Underlying=uni["Underlying"].iloc[int(uidx)],
            InceptionDate=asof,
            MaturityDate=asof + np.timedelta64(int(tenor * 365.25), "D"),
            Strike=spots_t[uidx], Barrier=np.nan, VarStrike=np.nan,
            Notional=-hedge_ratio * dunits, Alive=True))
        j += 1
    return pd.DataFrame(rows), j


# ---------------------------------------------------------------------------
# 5. Output files per spec
# ---------------------------------------------------------------------------

ABC build_outputs(g: pd.DataFrame, uni: pd.DataFrame, date_str: str):
    uidx = g["UIdx"].to_numpy()
    bucket = uni["FRTBBucket"].to_numpy()[uidx]          # e.g. USDEUR
    und = uni["Underlying"].to_numpy()[uidx]             # e.g. USD
    label = uni["RWLabel"].to_numpy()[uidx]

    ABC base(mask, risk_type):
        return dict(BusinessLine=BUSINESS_LINE, Date=date_str,
                    DeskName=DESK_NAME, FRTBBucket=bucket[mask],
                    ParameterSet=PARAMETER_SET, RiskDEF="FX",
                    RiskFactorType="SPOT", RiskType=risk_type,
                    RunRuleSet=RUN_RULE_SET,
                    TradeId=g["TradeId"].to_numpy()[mask],
                    Underlying=und[mask])

    # ---- FXDELTA ----
    m = np.abs(g["DeltaSens"].to_numpy()) > 1e-8
    delta = pd.DataFrame(base(m, "FXDELTA"))
    delta["GroupId"] = np.arange(1, len(delta) + 1)
    delta["BucketCode"] = [["SINGLE"]] * len(delta)
    delta["RiskValue"] = [[float(x)] for x in g["DeltaSens"].to_numpy()[m]]
    delta["RWLabel"] = label[m]
    delta["RiskFactor"] = bucket[m]                      # = {FRTBBucket}

    # ---- FXVEGA ----
    m = np.abs(g["VegaSens"].to_numpy()) > 1e-8
    W = vega_pillar_weights(g["T"].to_numpy()[m])
    vals = W * g["VegaSens"].to_numpy()[m][:, None]
    vega = pd.DataFrame(base(m, "FXVEGA"))
    vega["GroupId"] = np.arange(1, len(vega) + 1)
    vega["BucketCode"] = [PILLAR_LABELS] * len(vega)
    vega["RiskValue"] = [list(map(float, row)) for row in vals]
    vega["RWLabel"] = [[f"{lab}_{p}" for p in PILLAR_LABELS]
                       for lab in label[m]]
    vega["RiskFactor"] = und[m]                          # = {Underlying}

    # ---- FXGAMMA (curvature) ----
    opt = ~np.isin(g["TradeType"].to_numpy(), ["FORWARD", "VAR_SWAP"])
    m = opt & (np.abs(g["ShiftUpPnl"].to_numpy())
               + np.abs(g["ShiftDownPnl"].to_numpy()) > 1e-8)
    gamma = pd.DataFrame(base(m, "FXGAMMA"))
    gamma.insert(2, "CurvatureFlag", "Y")
    gamma.insert(3, "FXDivisorEligibility", "N")
    gamma["GroupId"] = np.arange(1, len(gamma) + 1)
    gamma["BucketCode"] = [["SINGLE"]] * len(gamma)
    gamma["RiskValue"] = [[float(x)] for x in
                          (g["ShiftUpPnl"] + g["ShiftDownPnl"]).to_numpy()[m]]
    gamma["SHIFTUPPNL"] = g["ShiftUpPnl"].to_numpy()[m]
    gamma["SHIFTDOWNPNL"] = g["ShiftDownPnl"].to_numpy()[m]
    gamma["CURVDELTA"] = (g["RW"] * g["DeltaSens"]).to_numpy()[m]
    gamma["RWLabel"] = label[m]
    gamma["RiskFactor"] = und[m]
    return delta, vega, gamma


# ---------------------------------------------------------------------------
# 6. Main
# ---------------------------------------------------------------------------

ABC main():
    uni = build_universe()
    spots, pillar_vol = simulate_market(uni)
    dates64 = np.array([np.datetime64(d.date()) for d in DATES])
    d0 = dates64[0]

    n_init = 12000
    book = gen_trades(uni, n_init, d0, spot_ref=uni["S0"].to_numpy(),
                      id_start=0, spot_jitter=0.6)   # jitter scaled by vol
    assert (book["MaturityDate"] > d0).all()
    next_id = n_init
    hf, next_id = add_hedge_forwards(book, uni, spots[0], pillar_vol[0],
                                     d0, next_id)
    book = pd.concat([book, hf], ignore_index=True)

    summary, all_trades = [], [book.copy()]
    for t, asof in enumerate(dates64):
        if t > 0:
            n_new = int(RNG.poisson(900))
            new = gen_trades(uni, n_new, np.full(n_new, asof),
                             spot_ref=spots[t], id_start=next_id)
            next_id += n_new
            hf, next_id = add_hedge_forwards(new, uni, spots[t],
                                             pillar_vol[t], asof, next_id)
            new = pd.concat([new, hf], ignore_index=True)
            all_trades.append(new)
            book = pd.concat([book, new], ignore_index=True)

        expired = book["MaturityDate"] <= asof
        S_now = spots[t][book["UIdx"].to_numpy()]
        ko = (((book["TradeType"] == "BARRIER_UO_CALL")
               & (S_now >= book["Barrier"].to_numpy()))
              | ((book["TradeType"] == "BARRIER_DO_PUT")
                 & (S_now <= book["Barrier"].to_numpy())))
        n_exp, n_ko = int(expired.sum()), int((ko & ~expired).sum())
        book = book[~(expired | ko)].reset_index(drop=True)

        g = compute_greeks(book, uni, spots[t], pillar_vol[t], asof)
        date_str = pd.Timestamp(asof).strftime("%Y-%m-%d")
        delta, vega, gamma = build_outputs(g, uni, date_str)
        write_file(delta, f"FX_FXDELTA_{date_str}")
        write_file(vega, f"FX_FXVEGA_{date_str}")
        write_file(gamma, f"FX_FXGAMMA_{date_str}")
        summary.append(dict(
            Date=date_str, LiveTrades=len(book), Expired=n_exp,
            KnockedOut=n_ko, NetDelta=float(g["DeltaSens"].sum()),
            GrossDelta=float(g["DeltaSens"].abs().sum()),
            NetVega=float(g["VegaSens"].sum()),
            GrossVega=float(g["VegaSens"].abs().sum()),
            DeltaRows=len(delta), VegaRows=len(vega), GammaRows=len(gamma)))

    trades_all = pd.concat(all_trades, ignore_index=True)
    trades_all["InceptionDate"] = trades_all["InceptionDate"].astype(str)
    trades_all["MaturityDate"] = trades_all["MaturityDate"].astype(str)
    write_file(trades_all.drop(columns=["Alive"]), "REF_FX_TRADES")
    md = []
    for t, asof in enumerate(dates64):
        for i, u in enumerate(uni["Underlying"]):
            md.append(dict(Date=pd.Timestamp(asof).strftime("%Y-%m-%d"),
                           Pair=f"{u}EUR", Spot=float(spots[t, i]),
                           **{f"Vol_{lab}": float(pillar_vol[t, i, j])
                              for j, lab in enumerate(PILLAR_LABELS)}))
    write_file(pd.DataFrame(md), "REF_FX_MARKET_DATA")
    write_file(uni, "REF_FX_UNIVERSE")
    s = pd.DataFrame(summary)
    write_file(s, "REF_FX_RUN_SUMMARY")
    pd.set_option("display.width", 200)
    print(s.to_string(index=False))
    print(f"\nOutput format: {'parquet' if G.HAVE_PARQUET else 'csv.gz'}"
          f" -> {os.path.abspath(G.OUT_DIR)}")


if __name__ == "__main__":
    main()
