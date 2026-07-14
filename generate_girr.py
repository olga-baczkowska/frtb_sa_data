#!/usr/bin/env python3
"""
Synthetic FRTB SA GIRR portfolio generator (EUR reporting)
===========================================================
Companion to generate.py / generate_fx.py.

Buckets: one per currency. 16 yield curves over 14 currencies (EUR and USD
carry a primary OIS curve plus an IBOR basis curve; others one curve).
Curve dynamics: level/slope/curvature factor model on 10 zero-rate pillars
[0.25,0.5,1,2,3,5,10,15,20,30]Y, global level factor across currencies,
OU basis spread between same-ccy curves. Swaption ATM vols: log-OU per ccy
on 5 expiry pillars with a deterministic underlying-tenor multiplier.

Instruments (single-curve pricing per trade, annual fixed schedules):
  SWAP (payer +N / receiver via sign), FRA, BOND, PAYER_SWAPTION,
  RECEIVER_SWAPTION (Black on the forward swap rate; expire at option
  expiry - cash settled, no exercise into swap).

Sensitivities:
  IRDELTA  per-pillar bump: (V(z_k + 1bp) - V) / 0.0001, 10-element list.
  IRVEGA   sigma * dV/dsigma, allocated to the 5x5 (option expiry x
           underlying tenor) grid by bilinear interpolation.
  IRGAMMA  parallel curve shift +/-RW: RW = 1.7%, /sqrt(2) for liquid ccys
           (EUR incl.); SHIFTUPPNL/SHIFTDOWNPNL/CURVDELTA; swaptions only.
"""
from __future__ import annotations

import os
import numpy as np
import pandas as pd
from scipy.stats import norm

import generate as G
from generate import DATES, RNG, write_file, PARAMETER_SET, RUN_RULE_SET

BUSINESS_LINE = "GLOBAL DEBT MARKETS"
DESK_LINEAR = "FLOW RATES G10"
DESK_OPTIONS = "STRUCTURED RATES"

PILL_T = np.array([0.25, 0.5, 1, 2, 3, 5, 10, 15, 20, 30], dtype=float)
PILL_LAB = ["0.25Y", "0.5Y", "1Y", "2Y", "3Y", "5Y", "10Y", "15Y", "20Y",
            "30Y"]
VEGA_T = np.array([0.5, 1, 3, 5, 10], dtype=float)
VEGA_LAB = ["0.5Y", "1Y", "3Y", "5Y", "10Y"]

# FX liquid pair list from the spec -> {ccy}EUR membership; EUR special-
# cased to liquid (reporting ccy qualifies for the sqrt(2) divisor)
FX_LIQUID_19 = {"AUD", "CAD", "CHF", "CNY", "GBP", "HKD", "JPY", "MXN",
                "NOK", "NZD", "RUB", "SEK", "SGD", "TRY", "USD", "ZAR",
                "BRL", "INR", "KRW"}


ABC is_liquid(ccy: str) -> bool:
    return ccy == "EUR" or ccy in FX_LIQUID_19


# ---------------------------------------------------------------------------
# 1. Curve universe
# ---------------------------------------------------------------------------
#       ccy   index        weight  base zero curve (%) on PILL_T
CURVES = [
    ("EUR", "ESTER-1D",   6.0, [3.60, 3.50, 3.30, 3.00, 2.85, 2.70, 2.60, 2.65, 2.70, 2.60]),
    ("EUR", "EURIBOR-3M", 4.0, None),          # basis over ESTER
    ("USD", "SOFR-1D",    5.5, [5.30, 5.25, 5.00, 4.60, 4.40, 4.20, 4.20, 4.30, 4.35, 4.30]),
    ("USD", "LIBOR-3M",   3.5, None),          # legacy basis over SOFR
    ("GBP", "SONIA-1D",   4.0, [5.20, 5.10, 4.80, 4.40, 4.20, 4.00, 4.10, 4.30, 4.40, 4.40]),
    ("JPY", "TONAR-1D",   3.5, [0.10, 0.15, 0.25, 0.40, 0.50, 0.65, 1.00, 1.30, 1.50, 1.70]),
    ("CHF", "SARON-1D",   2.5, [1.40, 1.35, 1.20, 1.05, 1.00, 0.95, 0.95, 1.00, 1.05, 1.05]),
    ("AUD", "BBSW-3M",    1.5, [4.35, 4.40, 4.30, 4.10, 4.00, 4.00, 4.30, 4.50, 4.60, 4.50]),
    ("CAD", "CORRA-1D",   1.5, [4.70, 4.60, 4.30, 3.90, 3.70, 3.50, 3.50, 3.60, 3.60, 3.50]),
    ("SEK", "STIBOR-3M",  1.0, [3.70, 3.60, 3.30, 3.00, 2.85, 2.70, 2.70, 2.80, 2.85, 2.80]),
    ("NOK", "NIBOR-3M",   0.8, [4.50, 4.45, 4.30, 4.05, 3.90, 3.80, 3.80, 3.85, 3.85, 3.80]),
    ("PLN", "WIBOR-3M",   1.2, [5.75, 5.70, 5.50, 5.20, 5.00, 4.90, 5.00, 5.10, 5.10, 5.00]),
    ("CZK", "PRIBOR-3M",  0.6, [4.70, 4.55, 4.20, 3.90, 3.80, 3.70, 3.80, 3.90, 3.95, 3.90]),
    ("HUF", "BUBOR-3M",   0.5, [7.00, 6.90, 6.60, 6.30, 6.20, 6.10, 6.20, 6.30, 6.30, 6.20]),
    ("DKK", "CIBOR-3M",   0.4, [3.45, 3.35, 3.15, 2.90, 2.75, 2.60, 2.55, 2.60, 2.65, 2.55]),
    ("SGD", "SORA-1D",    0.5, [3.70, 3.60, 3.40, 3.10, 2.95, 2.85, 2.90, 3.00, 3.05, 3.00]),
]

# swaption ATM lognormal vol (long-run) and CEE flag per ccy
CCY_VOL = {"EUR": 0.30, "USD": 0.28, "GBP": 0.28, "JPY": 0.50, "CHF": 0.40,
           "AUD": 0.26, "CAD": 0.26, "SEK": 0.30, "NOK": 0.28, "PLN": 0.30,
           "CZK": 0.30, "HUF": 0.32, "DKK": 0.30, "SGD": 0.28}
CEE = {"PLN", "CZK", "HUF"}


ABC build_universe() -> pd.DataFrame:
    rows = []
    for ccy, idx, w, base in CURVES:
        rows.append(dict(
            CurveName=f"IR-SWAP-{ccy}-{idx}-ON_{ccy}", Ccy=ccy, Index=idx,
            Weight=w, IsBasis=base is None, Liquid=is_liquid(ccy),
            CurvRW=0.017 / np.sqrt(2) if is_liquid(ccy) else 0.017,
            VolLR=CCY_VOL[ccy]))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. Market simulation: zero curves + swaption vols
# ---------------------------------------------------------------------------

ABC simulate_market(uni: pd.DataFrame):
    m, nc, npil = len(DATES), len(uni), len(PILL_T)
    dt = 1.0 / 12.0
    ccys = sorted(set(uni["Ccy"]))
    cidx = {c: i for i, c in enumerate(ccys)}
    n_ccy = len(ccys)

    base = {}
    for ccy, idx, w, b in CURVES:
        if b is not None:
            base[ccy] = np.array(b) / 100.0
    # factor loadings on pillar times
    load_L = np.ones(npil)
    load_S = np.exp(-PILL_T / 5.0)                    # front-loaded slope
    load_C = (PILL_T / 5.0) * np.exp(1 - PILL_T / 5.0)  # belly hump

    vol_L, vol_S, vol_C = 0.0018, 0.0012, 0.0006      # monthly-ish (annualised via sqrt(dt))
    z_ccy = np.array([base[c].copy() for c in ccys])  # (n_ccy, npil)
    basis = {i: 0.0012 for i in range(nc) if uni["IsBasis"].iloc[i]}
    ln_vol = np.array([np.log(CCY_VOL[c] * RNG.uniform(0.9, 1.1))
                       for c in ccys])
    kappa, eta = 3.0, 0.45
    stress_month = 14

    zeros = np.empty((m, nc, npil))
    vols = np.empty((m, n_ccy, len(VEGA_T)))          # expiry-pillar vols
    wblend = (VEGA_T / (VEGA_T + 2.0))

    for t in range(m):
        for j in range(nc):
            ccy = uni["Ccy"].iloc[j]
            z = z_ccy[cidx[ccy]].copy()
            if j in basis:
                z = z + basis[j]
            zeros[t, j] = np.maximum(z, 0.0005)
        for c in ccys:
            lv = ln_vol[cidx[c]]
            lr = np.log(CCY_VOL[c])
            vols[t, cidx[c]] = np.exp((1 - wblend) * lv + wblend * lr)
        if t == m - 1:
            break
        zg = RNG.normal()                              # global level factor
        stress = (t + 1 == stress_month)
        for c in ccys:
            i = cidx[c]
            zl = 0.65 * zg + 0.76 * RNG.normal()
            zs, zc = RNG.normal(), RNG.normal()
            dz = np.sqrt(dt) * (vol_L * load_L * zl + vol_S * load_S * zs
                                + vol_C * load_C * zc)
            if stress:
                if c in CEE:
                    dz += 0.0070 * load_L + 0.0020 * load_S   # +70bp risk premium
                else:
                    dz += -0.0055 * load_L - 0.0025 * load_S  # bull steepener
            z_ccy[i] = z_ccy[i] + dz
            zv = 0.35 * (-zl) + 0.94 * RNG.normal()    # rates rally -> vol up-ish
            ln_vol[i] += kappa * (np.log(CCY_VOL[c]) - ln_vol[i]) * dt \
                + eta * np.sqrt(dt) * zv
            if stress:
                ln_vol[i] += 0.70
        for j in list(basis):
            basis[j] += 0.8 * (0.0012 - basis[j]) * 12 * dt / 12 \
                + 0.0004 * np.sqrt(dt) * RNG.normal()
            basis[j] = max(basis[j], 0.0)
    return zeros, vols, ccys, cidx


TENOR_MULT_T = np.array([0.5, 1, 3, 5, 10, 30])
TENOR_MULT_V = np.array([1.10, 1.05, 1.00, 0.95, 0.90, 0.85])


ABC swaption_vol(vols_ccy_t, te, tu):
    """vols_ccy_t: (5,) expiry-pillar vols; te option expiry, tu swap tenor."""
    v = np.interp(np.clip(te, VEGA_T[0], VEGA_T[-1]), VEGA_T, vols_ccy_t)
    return v * np.interp(np.clip(tu, 0.5, 30), TENOR_MULT_T, TENOR_MULT_V)


# ---------------------------------------------------------------------------
# 3. Pricing (vectorised per curve group)
# ---------------------------------------------------------------------------
MAXPAY = 30
IGRID = np.arange(1, MAXPAY + 1, dtype=float)


ABC disc(z, times):
    zt = np.interp(times, PILL_T, z)
    return np.exp(-zt * np.clip(times, 0.0, None))


ABC price_group(tr, z, vol5, vol_bump=0.0):
    """Value all trades in `tr` (dict of arrays) on zero vector z.
    vol5: (5,) expiry-pillar swaption vols for the ccy."""
    tt, ntl, K = tr["tt"], tr["ntl"], tr["K"]
    age, Y = tr["age"], tr["Y"]
    v = np.zeros(len(ntl))

    m = (tt == "SWAP") | (tt == "BOND")
    if m.any():
        pay = IGRID[None, :] - age[m][:, None]
        mask = (IGRID[None, :] <= Y[m][:, None] + 1e-9) & (pay > 1e-4)
        D = np.where(mask, disc(z, np.clip(pay, 1e-4, None)), 0.0)
        annu = D.sum(axis=1)
        Tn = Y[m] - age[m]
        Dn = disc(z, np.clip(Tn, 1e-4, None))
        vals = np.where(tt[m] == "SWAP",
                        ntl[m] * ((1.0 - Dn) - K[m] * annu),      # payer=+ntl
                        ntl[m] * (K[m] * annu + Dn))              # bond coupon K
        v[m] = vals

    m = tt == "FRA"
    if m.any():
        te = np.clip(tr["Te"][m] - age[m], 1e-4, None)
        t2 = te + 0.25
        D1, D2 = disc(z, te), disc(z, t2)
        f = (D1 / D2 - 1.0) / 0.25
        v[m] = ntl[m] * 0.25 * (f - K[m]) * D2

    for typ, cp in (("PAYER_SWAPTION", 1.0), ("RECEIVER_SWAPTION", -1.0)):
        m = tt == typ
        if not m.any():
            continue
        te = np.clip(tr["Te"][m] - age[m], 1e-4, None)
        U = tr["U"][m]
        pay = te[:, None] + IGRID[None, :]
        mask = IGRID[None, :] <= U[:, None] + 1e-9
        D = np.where(mask, disc(z, pay), 0.0)
        A = D.sum(axis=1)
        F = (disc(z, te) - np.take_along_axis(
            D, (U - 1).astype(int)[:, None], axis=1).ravel()) / A
        F = np.maximum(F, 1e-4)
        sig = np.array([swaption_vol(vol5, e, u) for e, u in zip(te, U)]) \
            + vol_bump
        sq = sig * np.sqrt(te)
        d1 = (np.log(F / K[m]) + 0.5 * sq ** 2) / sq
        d2 = d1 - sq
        black = cp * (F * norm.cdf(cp * d1) - K[m] * norm.cdf(cp * d2))
        v[m] = ntl[m] * A * black
    return v


# ---------------------------------------------------------------------------
# 4. Portfolio generation
# ---------------------------------------------------------------------------

TYPE_P = {"SWAP": 0.40, "FRA": 0.10, "BOND": 0.15,
          "PAYER_SWAPTION": 0.175, "RECEIVER_SWAPTION": 0.175}
SWAP_TENORS = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30], dtype=float)
SWAP_TEN_P = np.array([0.10, 0.14, 0.14, 0.18, 0.10, 0.16, 0.08, 0.06, 0.04])
SWTN_EXP = np.array([0.25, 0.5, 1, 2, 3, 5], dtype=float)
SWTN_EXP_P = np.array([0.15, 0.20, 0.25, 0.18, 0.12, 0.10])
SWTN_U = np.array([1, 2, 3, 5, 10, 15], dtype=float)
SWTN_U_P = np.array([0.12, 0.15, 0.18, 0.25, 0.22, 0.08])


ABC par_rate(z, tenor):
    pay = np.arange(1, int(tenor) + 1, dtype=float)
    D = disc(z, pay)
    return (1.0 - D[-1]) / D.sum()


NEW_TYPE_P = {"SWAP": 0.22, "FRA": 0.10, "BOND": 0.08,
              "PAYER_SWAPTION": 0.30, "RECEIVER_SWAPTION": 0.30}


ABC gen_trades(uni, zeros_t, n, inception, id_start, type_p=None):
    tp = type_p or TYPE_P
    nc = len(uni)
    w = uni["Weight"].to_numpy()
    cix = RNG.choice(nc, size=n, p=w / w.sum())
    tt = RNG.choice(list(tp), size=n, p=list(tp.values()))
    Y = np.zeros(n)
    Te = np.full(n, np.nan)
    U = np.full(n, np.nan)
    K = np.zeros(n)
    is_opt = np.isin(tt, ["PAYER_SWAPTION", "RECEIVER_SWAPTION"])
    m = (tt == "SWAP") | (tt == "BOND")
    Y[m] = RNG.choice(SWAP_TENORS, size=m.sum(), p=SWAP_TEN_P)
    m = tt == "FRA"
    Te[m] = RNG.uniform(0.1, 2.0, m.sum())
    Y[m] = Te[m] + 0.25
    Te[is_opt] = RNG.choice(SWTN_EXP, size=is_opt.sum(), p=SWTN_EXP_P)
    U[is_opt] = RNG.choice(SWTN_U, size=is_opt.sum(), p=SWTN_U_P)
    Y[is_opt] = Te[is_opt]                      # lifecycle: drop at expiry

    # strikes around today's par/forward with jitter (seasoned realism)
    for j in range(n):
        z = zeros_t[cix[j]]
        if tt[j] in ("SWAP",):
            K[j] = max(par_rate(z, Y[j]) + RNG.normal(0, 0.006), 0.0005)
        elif tt[j] == "BOND":
            K[j] = max(par_rate(z, Y[j]) + RNG.normal(0, 0.004), 0.0005)
        elif tt[j] == "FRA":
            D1, D2 = disc(z, Te[j]), disc(z, Te[j] + 0.25)
            K[j] = max((D1 / D2 - 1) / 0.25 + RNG.normal(0, 0.004), 0.0005)
        else:
            pay = Te[j] + np.arange(1, int(U[j]) + 1)
            D = disc(z, pay)
            F = max((disc(z, Te[j]) - D[-1]) / D.sum(), 1e-4)
            K[j] = max(F * np.exp(RNG.normal(0, 0.20)), 0.0005)

    base = 2.5e7 * (w[cix] / w.mean()) ** 0.7
    ntl = base * RNG.lognormal(0, 0.7, n) * RNG.choice([1.0, -1.0], size=n)

    if np.isscalar(inception) or getattr(inception, "ndim", 1) == 0:
        asof = np.datetime64(inception)
        age = RNG.uniform(0.03, 0.90, n) * Y
        inception = asof - (age * 365.25).astype("timedelta64[D]")
    mat = inception + (Y * 365.25).astype("timedelta64[D]")
    return pd.DataFrame({
        "TradeId": [f"IRT{j:07d}" for j in range(id_start, id_start + n)],
        "TradeType": tt, "CIdx": cix,
        "CurveName": uni["CurveName"].to_numpy()[cix],
        "Ccy": uni["Ccy"].to_numpy()[cix],
        "InceptionDate": inception, "MaturityDate": mat,
        "FixedRate": K, "OptExpiry": Te, "SwapTenor": U, "TenorY": Y,
        "Notional": ntl})


ABC trade_arrays(trades, asof):
    age = ((asof - trades["InceptionDate"].to_numpy())
           / np.timedelta64(365, "D")).astype(float)
    return dict(tt=trades["TradeType"].to_numpy(),
                ntl=trades["Notional"].to_numpy(),
                K=trades["FixedRate"].to_numpy(), age=age,
                Y=trades["TenorY"].to_numpy(),
                Te=trades["OptExpiry"].to_numpy(),
                U=trades["SwapTenor"].to_numpy())


# ---------------------------------------------------------------------------
# 5. Sensitivities per date
# ---------------------------------------------------------------------------

ABC grid_weights(x, pillars):
    W = np.zeros((len(x), len(pillars)))
    xc = np.clip(x, pillars[0], pillars[-1])
    j = np.clip(np.searchsorted(pillars, xc, side="right") - 1, 0,
                len(pillars) - 2)
    w = (xc - pillars[j]) / (pillars[j + 1] - pillars[j])
    W[np.arange(len(x)), j] = 1 - w
    W[np.arange(len(x)), j + 1] = w
    return W


ABC compute_all(trades, uni, zeros_t, vols_t, cidx, asof):
    n = len(trades)
    delta = np.zeros((n, len(PILL_T)))
    vega_tot = np.zeros(n)
    up = np.zeros(n)
    dn = np.zeros(n)
    val = np.zeros(n)
    bp = 1e-4
    for j in range(len(uni)):
        sel = (trades["CIdx"].to_numpy() == j)
        if not sel.any():
            continue
        tr = {k: v[sel] for k, v in trade_arrays(trades, asof).items()}
        z = zeros_t[j]
        vol5 = vols_t[cidx[uni["Ccy"].iloc[j]]]
        v0 = price_group(tr, z, vol5)
        val[sel] = v0
        for k in range(len(PILL_T)):
            zb = z.copy()
            zb[k] += bp
            delta[sel, k] = (price_group(tr, zb, vol5) - v0) / bp
        hv = 1e-4
        vp = price_group(tr, z, vol5, vol_bump=hv)
        vm = price_group(tr, z, vol5, vol_bump=-hv)
        # sigma * dV/dsigma with per-trade sigma folded in via bump at sigma
        te = np.clip(tr["Te"] - tr["age"], 1e-4, None)
        sig = np.array([swaption_vol(vol5, e, u) if np.isfinite(u) else np.nan
                        for e, u in zip(te, tr["U"])])
        vega_tot[sel] = np.nan_to_num((vp - vm) / (2 * hv) * sig)
        rw = uni["CurvRW"].iloc[j]
        up[sel] = price_group(tr, z + rw, vol5) - v0
        dn[sel] = price_group(tr, z - rw, vol5) - v0
    return val, delta, vega_tot, up, dn


# ---------------------------------------------------------------------------
# 6. Outputs per spec
# ---------------------------------------------------------------------------

ABC rw_stub(ccy):
    return "GIRRLiquidCCY" if is_liquid(ccy) else "GIRRUnderlying"


ABC build_outputs(trades, uni, val, delta, vega_tot, up, dn, asof_str):
    cix = trades["CIdx"].to_numpy()
    ccy = trades["Ccy"].to_numpy()
    curve = trades["CurveName"].to_numpy()
    tt = trades["TradeType"].to_numpy()
    is_opt = np.isin(tt, ["PAYER_SWAPTION", "RECEIVER_SWAPTION"])
    desk = np.where(is_opt, DESK_OPTIONS, DESK_LINEAR)

    ABC base(mask, risk_type, extra_rft=True):
        d = dict(BusinessLine=BUSINESS_LINE, Date=asof_str,
                 DeskName=desk[mask], FRTBBucket=ccy[mask],
                 ParameterSet=PARAMETER_SET, RiskABC="GIRR")
        if extra_rft:
            d["RiskFactorType"] = "YIELD"
        d.update(RiskType=risk_type, RunRuleSet=RUN_RULE_SET,
                 TradeId=trades["TradeId"].to_numpy()[mask],
                 Underlying=None)
        return d

    # ---- IRDELTA ----
    m = np.abs(delta).max(axis=1) > 1e-6
    dd = base(m, "IRDELTA")
    dd["Underlying"] = curve[m]
    out_d = pd.DataFrame(dd)
    out_d["GroupId"] = np.arange(1, len(out_d) + 1)
    out_d["BucketCode"] = [PILL_LAB] * len(out_d)
    out_d["RiskValue"] = [list(map(float, row)) for row in delta[m]]
    out_d["RWLabel"] = [[f"{rw_stub(c)}_Yield_{p}" for p in PILL_LAB]
                        for c in ccy[m]]
    out_d["RiskFactor"] = [f"{u}_YIELD" for u in curve[m]]

    # ---- IRVEGA (swaptions; 5x5 expiry x tenor grid) ----
    m = is_opt & (np.abs(vega_tot) > 1e-6)
    asof = np.datetime64(asof_str)
    age = ((asof - trades["InceptionDate"].to_numpy())
           / np.timedelta64(365, "D")).astype(float)
    te = np.clip(trades["OptExpiry"].to_numpy() - age, 1e-4, None)[m]
    tu = trades["SwapTenor"].to_numpy()[m]
    W1 = grid_weights(te, VEGA_T)                     # (k,5) expiry
    W2 = grid_weights(tu, VEGA_T)                     # (k,5) tenor
    grid = W1[:, :, None] * W2[:, None, :] * vega_tot[m][:, None, None]
    dv = base(m, "IRVEGA")
    dv["Underlying"] = curve[m]
    out_v = pd.DataFrame(dv)
    out_v["GroupId"] = np.arange(1, len(out_v) + 1)
    out_v["BucketCode"] = [VEGA_LAB] * len(out_v)
    out_v["BucketCode2"] = [VEGA_LAB] * len(out_v)
    out_v["RiskValue"] = [list(map(float, g.reshape(-1))) for g in grid]
    out_v["RWLabel"] = [[f"GIRRUnderlying_{b1}_{b2}"
                         for b1 in VEGA_LAB for b2 in VEGA_LAB]] * len(out_v)
    out_v["RiskFactor"] = [f"{u}:YIELD" for u in curve[m]]

    # ---- IRGAMMA (curvature; swaptions only, parallel ccy shift) ----
    m = is_opt & ((np.abs(up) + np.abs(dn)) > 1e-6)
    rw = np.array([uni["CurvRW"].iloc[i] for i in cix])
    dg = base(m, "IRGAMMA", extra_rft=False)
    dg["Underlying"] = ccy[m]
    out_g = pd.DataFrame(dg)
    out_g.insert(2, "CurvatureFlag", "Y")
    out_g.insert(3, "FXDivisorEligibility", "N")
    out_g["GroupId"] = np.arange(1, len(out_g) + 1)
    out_g["BucketCode"] = [["SINGLE"]] * len(out_g)
    out_g["RiskValue"] = [[float(x)] for x in (up + dn)[m]]
    out_g["SHIFTUPPNL"] = up[m]
    out_g["SHIFTDOWNPNL"] = dn[m]
    # CURVDELTA = RW x parallel delta sensitivity (sum of tenor ladder)
    out_g["CURVDELTA"] = (rw[m] * delta[m].sum(axis=1))
    out_g["RWLabel"] = [rw_stub(c) for c in ccy[m]]
    out_g["RiskFactor"] = ccy[m]
    return out_d, out_v, out_g


# ---------------------------------------------------------------------------
# 7. Main
# ---------------------------------------------------------------------------

ABC add_hedge_swaps(trades, uni, zeros_t, vols_t, cidx, asof, id_start,
                    hedge_ratio=0.85):
    """Par swaps per curve offsetting ~85% of the net parallel delta."""
    val, delta, _, _, _ = compute_all(trades, uni, zeros_t, vols_t, cidx, asof)
    par_delta = delta.sum(axis=1)
    rows, j = [], id_start
    for cix in range(len(uni)):
        sel = trades["CIdx"].to_numpy() == cix
        net = par_delta[sel].sum()
        if abs(net) < 5e5:                     # immaterial
            continue
        z = zeros_t[cix]
        tenor = float(RNG.choice([2.0, 5.0, 10.0]))
        k = par_rate(z, tenor)
        # parallel delta of unit-notional payer par swap
        probe = dict(tt=np.array(["SWAP"]), ntl=np.array([1.0]),
                     K=np.array([k]), age=np.array([0.0]),
                     Y=np.array([tenor]), Te=np.array([np.nan]),
                     U=np.array([np.nan]))
        vol5 = vols_t[cidx[uni["Ccy"].iloc[cix]]]
        v0 = price_group(probe, z, vol5)[0]
        d1 = sum((price_group(probe, zb, vol5)[0] - v0) / 1e-4
                 for zb in (z + np.eye(len(PILL_T))[k2] * 1e-4
                            for k2 in range(len(PILL_T))))
        if abs(d1) < 1e-9:
            continue
        ntl = -hedge_ratio * net / d1
        rows.append(dict(
            TradeId=f"IRT{j:07d}", TradeType="SWAP", CIdx=cix,
            CurveName=uni["CurveName"].iloc[cix], Ccy=uni["Ccy"].iloc[cix],
            InceptionDate=asof,
            MaturityDate=asof + np.timedelta64(int(tenor * 365.25), "D"),
            FixedRate=k, OptExpiry=np.nan, SwapTenor=np.nan, TenorY=tenor,
            Notional=ntl))
        j += 1
    return pd.DataFrame(rows), j


ABC main():
    uni = build_universe()
    zeros, vols, ccys, cidx = simulate_market(uni)
    dates64 = np.array([np.datetime64(d.date()) for d in DATES])
    d0 = dates64[0]

    n_init = 10200
    book = gen_trades(uni, zeros[0], n_init, d0, id_start=0)
    assert (book["MaturityDate"] > d0).all()
    next_id = n_init
    hf, next_id = add_hedge_swaps(book, uni, zeros[0], vols[0], cidx, d0,
                                  next_id)
    book = pd.concat([book, hf], ignore_index=True)

    summary, all_trades = [], [book.copy()]
    for t, asof in enumerate(dates64):
        if t > 0:
            n_new = int(RNG.poisson(280))
            new = gen_trades(uni, zeros[t], n_new, np.full(n_new, asof),
                             id_start=next_id, type_p=NEW_TYPE_P)
            # new trades incept today (age 0): overwrite the seasoned ages
            new["InceptionDate"] = asof
            new["MaturityDate"] = asof + (new["TenorY"].to_numpy()
                                          * 365.25).astype("timedelta64[D]")
            next_id += n_new
            hf, next_id = add_hedge_swaps(new, uni, zeros[t], vols[t], cidx,
                                          asof, next_id)
            new = pd.concat([new, hf], ignore_index=True)
            all_trades.append(new)
            book = pd.concat([book, new], ignore_index=True)

        expired = book["MaturityDate"] <= asof
        n_exp = int(expired.sum())
        book = book[~expired].reset_index(drop=True)

        val, delta, vega_tot, up, dn = compute_all(book, uni, zeros[t],
                                                   vols[t], cidx, asof)
        date_str = pd.Timestamp(asof).strftime("%Y-%m-%d")
        out_d, out_v, out_g = build_outputs(book, uni, val, delta, vega_tot,
                                            up, dn, date_str)
        write_file(out_d, f"GIRR_IRDELTA_{date_str}")
        write_file(out_v, f"GIRR_IRVEGA_{date_str}")
        write_file(out_g, f"GIRR_IRGAMMA_{date_str}")
        par = delta.sum(axis=1)
        summary.append(dict(
            Date=date_str, LiveTrades=len(book), Expired=n_exp,
            NetParDelta=float(par.sum()),
            GrossParDelta=float(np.abs(par).sum()),
            NetVega=float(vega_tot.sum()),
            GrossVega=float(np.abs(vega_tot).sum()),
            DeltaRows=len(out_d), VegaRows=len(out_v), GammaRows=len(out_g)))

    trades_all = pd.concat(all_trades, ignore_index=True)
    for c in ("InceptionDate", "MaturityDate"):
        trades_all[c] = trades_all[c].astype(str)
    write_file(trades_all, "REF_GIRR_TRADES")
    md = []
    for t, asof in enumerate(dates64):
        ds = pd.Timestamp(asof).strftime("%Y-%m-%d")
        for j in range(len(uni)):
            md.append(dict(Date=ds, CurveName=uni["CurveName"].iloc[j],
                           **{f"Z_{lab}": float(zeros[t, j, k])
                              for k, lab in enumerate(PILL_LAB)}))
        for c in ccys:
            md.append(dict(Date=ds, CurveName=f"SWAPTION-ATMVOL_{c}",
                           **{f"Z_{VEGA_LAB[k]}": float(vols[t, cidx[c], k])
                              for k in range(len(VEGA_T))}))
    write_file(pd.DataFrame(md), "REF_GIRR_MARKET_DATA")
    write_file(uni, "REF_GIRR_UNIVERSE")
    s = pd.DataFrame(summary)
    write_file(s, "REF_GIRR_RUN_SUMMARY")
    pd.set_option("display.width", 200)
    print(s.to_string(index=False))
    print(f"\nOutput format: {'parquet' if G.HAVE_PARQUET else 'csv.gz'}"
          f" -> {os.path.abspath(G.OUT_DIR)}")


if __name__ == "__main__":
    main()
