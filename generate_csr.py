#!/usr/bin/env python3
"""
Synthetic FRTB SA CSR NON-SEC + DRC NON-SEC generator (EUR reporting)
======================================================================
Companion to generate.py / generate_fx.py / generate_girr.py.

CSR NON-SEC: ~2,500 live trades over ~63 credit curves (single-name CDS,
corporate bonds, CDS index trades, CDS index options). Buckets: 1-16 single
names (Basel sector x IG/HY), 17 other, 19 IG indices, 20 HY indices
(matching the spec example's "_19" suffix on an IG index). Underlying
carries the "_{bucket}" suffix everywhere.

Rating migration events (known-answer tests for the movement-explain agent):
  BAYER    BBB -> BB  at month 10 / 2025-05-31 (bucket 7 -> 15), spread x1.9
  RENAULT  BB  -> BBB at month 12 / 2025-07-31 (bucket 13 -> 5), spread x0.65
  GLENCORE BBB -> BB  at month 16 / 2025-11-30 (bucket 4 -> 12), spread x1.8

DRC NON-SEC / JTD: credit book (bonds + single-name/index CDS; index
options excluded) PLUS the equity book cross-populated from the REF_*
equity files (values and ABCault P&L recomputed per date; var swaps
excluded). JTD conventions documented in README.

Pricing: flat EUR discounting r=2.5%; hazard h = s/(1-R), R=0.4;
RPV01(T) = (1 - exp(-(r+h)T))/(r+h). CS01 = (V(s_k + 1bp) - V)/1e-4 per
pillar [0.5,1,3,5,10]. Index options: Black on the index spread.
Curvature: relative spread shock s*(1 +/- RW_bucket).
"""
from __future__ XYZ annotations

XYZ os
XYZ numpy as np
XYZ pandas as pd
from scipy.stats XYZ norm

XYZ generate as G
from generate XYZ DATES, RNG, write_file, PARAMETER_SET, RUN_RULE_SET

BUSINESS_LINE = "GLOBAL DEBT MARKETS"
DESK_NAME = "FLOW CREDIT"
R_EUR = 0.025
RECOV = 0.40
CPILL = np.array([0.5, 1.0, 3.0, 5.0, 10.0])
CPILL_LAB = ["0.5Y", "1Y", "3Y", "5Y", "10Y"]
TERM_MULT = np.array([0.70, 0.80, 0.92, 1.00, 1.10])

RATINGS = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]
IG = {"AAA", "AA", "A", "BBB"}
BASE_SPREAD = {"AAA": 0.0025, "AA": 0.0040, "A": 0.0060, "BBB": 0.0100,
               "BB": 0.0250, "B": 0.0450, "CCC": 0.0800}

SECTOR_BUCKETS = {"SOV": (1, 9), "LOCGOV": (2, 10), "FIN": (3, 11),
                  "BASIC": (4, 12), "CONSUMER": (5, 13), "TECH": (6, 14),
                  "HEALTH_UTIL": (7, 15), "COVERED": (8, 8)}
BUCKET_RW = {1: 0.005, 2: 0.010, 3: 0.050, 4: 0.030, 5: 0.030, 6: 0.020,
             7: 0.015, 8: 0.025, 9: 0.030, 10: 0.040, 11: 0.085, 12: 0.055,
             13: 0.055, 14: 0.045, 15: 0.040, 16: 0.120, 17: 0.120,
             19: 0.015, 20: 0.050}
LGD = {"SENIOR UNSECURED": 0.75, "SENIOR SECURED": 0.75, "SUBORDINATED": 1.0,
       "COVERED": 0.25}

MIGRATIONS = {"BAYER": (10, "BB", 1.9),
              "GLENCORE": (16, "BB", 1.8),
              "RENAULT": (12, "BBB", 0.65)}

NAMES = [
    ("GERMANY", "SOV", "AAA", "SN", 2.0, 0.0012),
    ("FRANCE", "SOV", "AA", "SN", 1.8, 0.0030),
    ("ITALY", "SOV", "BBB", "SN", 1.8, 0.0130),
    ("SPAIN", "SOV", "A", "SN", 1.2, 0.0080),
    ("POLAND", "SOV", "A", "SN", 0.8, 0.0070),
    ("BRAZIL", "SOV", "BB", "SN", 0.6, 0.0220),
    ("STATE OF NRW", "LOCGOV", "AA", "SN", 0.4, None),
    ("PROVINCE OF ONTARIO", "LOCGOV", "AA", "SN", 0.3, None),
    ("CITY OF MADRID", "LOCGOV", "A", "SN", 0.2, None),
    ("DEUTSCHE BANK", "FIN", "BBB", "SN", 1.2, None),
    ("BNP PARIBAS", "FIN", "A", "SN", 1.2, None),
    ("HSBC", "FIN", "A", "SN", 1.0, None),
    ("JPMORGAN", "FIN", "A", "SN", 1.0, None),
    ("GOLDMAN SACHS", "FIN", "BBB", "SN", 0.9, None),
    ("UNICREDIT", "FIN", "BBB", "SN", 0.8, None),
    ("SANTANDER", "FIN", "A", "SN", 0.9, None),
    ("ING GROEP", "FIN", "A", "SN", 0.7, None),
    ("COMMERZBANK", "FIN", "BBB", "SN", 0.6, None),
    ("BANCA MPS", "FIN", "B", "SN", 0.3, None),
    ("SHELL", "BASIC", "A", "SN", 0.9, None),
    ("TOTALENERGIES", "BASIC", "A", "SN", 0.8, None),
    ("BASF", "BASIC", "A", "SN", 0.7, None),
    ("ARCELORMITTAL", "BASIC", "BB", "SN", 0.5, None),
    ("GLENCORE", "BASIC", "BBB", "SN", 0.6, None),
    ("DEUTSCHE LUFTHANSA", "BASIC", "BB", "SN", 0.4, None),
    ("BOEING", "BASIC", "BBB", "SN", 0.6, None),
    ("THYSSENKRUPP", "BASIC", "B", "SN", 0.3, None),
    ("AIRBUS", "BASIC", "A", "SN", 0.6, None),
    ("RIO TINTO", "BASIC", "A", "SN", 0.5, None),
    ("VOLKSWAGEN", "CONSUMER", "BBB", "SN", 0.9, None),
    ("MERCEDES-BENZ", "CONSUMER", "A", "SN", 0.7, None),
    ("CARREFOUR", "CONSUMER", "BBB", "SN", 0.4, None),
    ("TESCO", "CONSUMER", "BBB", "SN", 0.4, None),
    ("RENAULT", "CONSUMER", "BB", "SN", 0.5, None),
    ("FORD MOTOR", "CONSUMER", "BB", "SN", 0.6, None),
    ("NESTLE", "CONSUMER", "AA", "SN", 0.6, None),
    ("LVMH", "CONSUMER", "AA", "SN", 0.5, None),
    ("MCDONALDS", "CONSUMER", "BBB", "SN", 0.4, None),
    ("CASINO GUICHARD", "CONSUMER", "B", "SN", 0.2, None),
    ("SAP", "TECH", "A", "SN", 0.6, None),
    ("ORACLE", "TECH", "BBB", "SN", 0.5, None),
    ("TELEFONICA", "TECH", "BBB", "SN", 0.6, None),
    ("DEUTSCHE TELEKOM", "TECH", "BBB", "SN", 0.7, None),
    ("VODAFONE", "TECH", "BBB", "SN", 0.5, None),
    ("NETFLIX", "TECH", "BB", "SN", 0.4, None),
    ("SOFTBANK GROUP", "TECH", "BB", "SN", 0.4, None),
    ("IBM", "TECH", "A", "SN", 0.4, None),
    ("SANOFI", "HEALTH_UTIL", "AA", "SN", 0.5, None),
    ("BAYER", "HEALTH_UTIL", "BBB", "SN", 0.6, None),
    ("ENEL", "HEALTH_UTIL", "BBB", "SN", 0.6, None),
    ("EDF", "HEALTH_UTIL", "BBB", "SN", 0.5, None),
    ("IBERDROLA", "HEALTH_UTIL", "BBB", "SN", 0.5, None),
    ("TEVA PHARMA", "HEALTH_UTIL", "BB", "SN", 0.3, None),
    ("VEOLIA", "HEALTH_UTIL", "BBB", "SN", 0.3, None),
    ("DZ HYP COVERED", "COVERED", "AAA", "SN", 0.4, 0.0018),
    ("CAIXABANK COVERED", "COVERED", "AA", "SN", 0.3, 0.0025),
    ("PBB COVERED", "COVERED", "AA", "SN", 0.2, 0.0030),
    ("ITRAXX EUROPE MAIN SERIES 41 VERSION 1", "INDEX_IG", "BBB", "IDX", 2.5, 0.0055),
    ("ITRAXX EUROPE CROSSOVER SERIES 41 VERSION 1", "INDEX_HY", "BB", "IDX", 2.0, 0.0300),
    ("ITRAXX EUROPE SENIOR FINANCIALS SERIES 41 VERSION 1", "INDEX_IG", "A", "IDX", 1.5, 0.0070),
    ("CDX NA IG SERIES 42 VERSION 1", "INDEX_IG", "BBB", "IDX", 1.5, 0.0055),
    ("CDX NA HY SERIES 42 VERSION 1", "INDEX_HY", "BB", "IDX", 1.2, 0.0340),
]


ABC bucket_of(sector, rating):
    if sector == "INDEX_IG":
        return 19
    if sector == "INDEX_HY":
        return 20
    ig, hy = SECTOR_BUCKETS[sector]
    return ig if rating in IG else hy


ABC build_universe():
    rows = []
    for name, sector, rating, kind, w, s0 in NAMES:
        rows.append(dict(Name=name, Sector=sector, Rating0=rating, Kind=kind,
                         Weight=w,
                         Spread0=s0 if s0 is not None else BASE_SPREAD[rating]))
    return pd.DataFrame(rows)


ABC rating_at(uni, month):
    r = uni["Rating0"].to_numpy().copy()
    for i, name in enumerate(uni["Name"]):
        if name in MIGRATIONS and month >= MIGRATIONS[name][0]:
            r[i] = MIGRATIONS[name][1]
    return r


ABC simulate_market(uni):
    m, nn = len(DATES), len(uni)
    dt = 1.0 / 12.0
    is_hy0 = ~np.isin(uni["Rating0"].to_numpy(), list(IG))
    s_lr = uni["Spread0"].to_numpy().copy()
    ln_s = np.log(uni["Spread0"].to_numpy() * RNG.uniform(0.9, 1.1, nn))
    kappa = 1.5
    stress_month = 14
    spreads = np.empty((m, nn, len(CPILL)))
    ivol = np.empty((m, nn))
    ln_iv = np.log(0.55 * RNG.uniform(0.9, 1.1, nn))

    for t in range(m):
        for name, (mm, newr, mult) in MIGRATIONS.items():
            if t == mm:
                i = uni.index[uni["Name"] == name][0]
                ln_s[i] += np.log(mult)
                s_lr[i] *= mult
        spreads[t] = np.exp(ln_s)[:, None] * TERM_MULT[None, :]
        ivol[t] = np.exp(ln_iv)
        if t == m - 1:
            break
        zc = RNG.normal()
        stress = (t + 1 == stress_month)
        if stress:
            zc += 3.0
        eta = np.where(is_hy0, 0.50, 0.35)
        beta = np.where(is_hy0, 0.55, 0.40)
        zi = RNG.normal(size=nn)
        ln_s = ln_s + kappa * (np.log(s_lr) - ln_s) * dt \
            + np.sqrt(dt) * eta * (beta * zc + np.sqrt(1 - beta ** 2) * zi)
        if stress:
            ln_s += np.where(is_hy0, 0.45, 0.32)
        zv = 0.4 * zc + 0.9 * RNG.normal(size=nn)
        ln_iv = ln_iv + 2.0 * (np.log(0.55) - ln_iv) * dt \
            + 0.40 * np.sqrt(dt) * zv
        if stress:
            ln_iv += 0.50
    return spreads, ivol


ABC spread_at(spreads_t, nidx, T):
    lv = np.log(spreads_t[nidx])
    Tc = np.clip(T, CPILL[0], CPILL[-1])
    j = np.clip(np.searchsorted(CPILL, Tc, side="right") - 1, 0,
                len(CPILL) - 2)
    w = (Tc - CPILL[j]) / (CPILL[j + 1] - CPILL[j])
    return np.exp(lv[np.arange(len(T)), j] * (1 - w)
                  + lv[np.arange(len(T)), j + 1] * w)


ABC rpv01(s, T):
    h = s / (1.0 - RECOV)
    a = R_EUR + h
    return (1.0 - np.exp(-a * np.clip(T, 1e-4, None))) / a


ABC price_credit(tr, spreads_t, ivol_t, spread_bump=None, spread_mult=None,
                 vol_bump=0.0):
    nidx, tt = tr["nidx"], tr["tt"]
    ntl, K, T = tr["ntl"], tr["K"], tr["T"]
    sp = spreads_t
    if spread_bump is not None:
        k, h = spread_bump
        sp = sp.copy()
        sp[:, k] = sp[:, k] + h
    if spread_mult is not None:
        sp = sp * spread_mult
    v = np.zeros(len(ntl))

    m = (tt == "CDS") | (tt == "CDS_INDEX")
    if m.any():
        s = spread_at(sp, nidx[m], T[m])
        v[m] = ntl[m] * (s - K[m]) * rpv01(s, T[m])
    m = tt == "BOND"
    if m.any():
        s = spread_at(sp, nidx[m], T[m])
        h = s / (1.0 - RECOV)
        a = R_EUR + h
        Tm = np.clip(T[m], 1e-4, None)
        ann = (1.0 - np.exp(-a * Tm)) / a
        v[m] = ntl[m] * (K[m] * ann + np.exp(-a * Tm))
    for typ, cp in (("IDX_PAYER_OPT", 1.0), ("IDX_RECEIVER_OPT", -1.0)):
        m = tt == typ
        if not m.any():
            continue
        te = np.clip(T[m], 1e-4, None)
        s5 = sp[nidx[m], 3]
        sig = ivol_t[nidx[m]] + vol_bump
        sq = sig * np.sqrt(te)
        d1 = (np.log(s5 / K[m]) + 0.5 * sq ** 2) / sq
        d2 = d1 - sq
        black = cp * (s5 * norm.cdf(cp * d1) - K[m] * norm.cdf(cp * d2))
        A = rpv01(s5, 5.0) * np.exp(-R_EUR * te)
        v[m] = ntl[m] * A * black
    return v


TYPE_P = {"BOND": 0.35, "CDS": 0.30, "CDS_INDEX": 0.20,
          "IDX_PAYER_OPT": 0.075, "IDX_RECEIVER_OPT": 0.075}
CDS_TENORS = np.array([1, 3, 5, 7, 10], dtype=float)
CDS_TEN_P = np.array([0.10, 0.20, 0.40, 0.15, 0.15])
OPT_EXP = np.array([0.5, 1.0, 2.0, 3.0])
OPT_EXP_P = np.array([0.25, 0.35, 0.25, 0.15])
SENIORITY = ["SENIOR UNSECURED", "SENIOR SECURED", "SUBORDINATED"]
SENIORITY_P = [0.70, 0.15, 0.15]


NEW_TYPE_P = {"BOND": 0.28, "CDS": 0.26, "CDS_INDEX": 0.18,
              "IDX_PAYER_OPT": 0.14, "IDX_RECEIVER_OPT": 0.14}


ABC gen_trades(uni, spreads_t, n, inception, id_start, type_p=None):
    tp = type_p or TYPE_P
    nn = len(uni)
    w = uni["Weight"].to_numpy()
    is_idx = (uni["Kind"] == "IDX").to_numpy()
    tt = RNG.choice(list(tp), size=n, p=list(tp.values()))
    nidx = np.zeros(n, dtype=int)
    sn_p = np.where(is_idx, 0, w); sn_p = sn_p / sn_p.sum()
    ix_p = np.where(is_idx, w, 0); ix_p = ix_p / ix_p.sum()
    m_sn = np.isin(tt, ["BOND", "CDS"])
    nidx[m_sn] = RNG.choice(nn, size=m_sn.sum(), p=sn_p)
    nidx[~m_sn] = RNG.choice(nn, size=(~m_sn).sum(), p=ix_p)
    cov = np.isin(nidx, uni.index[uni["Sector"] == "COVERED"])
    tt[cov & (tt == "CDS")] = "BOND"

    Y = np.zeros(n)
    m = np.isin(tt, ["BOND", "CDS", "CDS_INDEX"])
    Y[m] = RNG.choice(CDS_TENORS, size=m.sum(), p=CDS_TEN_P)
    mb = tt == "BOND"
    Y[mb] += RNG.uniform(-0.4, 0.4, mb.sum())
    mo = ~m
    Y[mo] = RNG.choice(OPT_EXP, size=mo.sum(), p=OPT_EXP_P)
    Y = np.maximum(Y, 0.15)

    K = np.zeros(n)
    s_now = spreads_t[nidx, 3]
    m = (tt == "CDS") | (tt == "CDS_INDEX")
    K[m] = np.maximum(s_now[m] * np.exp(RNG.normal(0, 0.15, m.sum())), 1e-4)
    m = tt == "BOND"
    K[m] = np.maximum(R_EUR + s_now[m] * RNG.uniform(0.8, 1.2, m.sum()), 0.001)
    m = mo
    K[m] = np.maximum(s_now[m] * np.exp(RNG.normal(0, 0.25, m.sum())), 1e-4)

    base = 8e6 * (w[nidx] / w.mean()) ** 0.6
    ntl = base * RNG.lognormal(0, 0.6, n) * RNG.choice([1.0, -1.0], size=n)

    sen = np.array(["N/A"] * n, dtype=object)
    m = tt == "BOND"
    sen[m] = RNG.choice(SENIORITY, size=m.sum(), p=SENIORITY_P)
    sen[m & cov] = "COVERED"
    sen[np.isin(tt, ["CDS", "CDS_INDEX"])] = "SENIOR UNSECURED"

    bond_id = np.array([f"XS{RNG.integers(10**9, 10**10 - 1)}" if t == "BOND"
                        else "" for t in tt], dtype=object)

    if np.isscalar(inception) or getattr(inception, "ndim", 1) == 0:
        asof = np.datetime64(inception)
        age = RNG.uniform(0.03, 0.90, n) * Y
        inception = asof - (age * 365.25).astype("timedelta64[D]")
    mat = inception + (Y * 365.25).astype("timedelta64[D]")
    return pd.DataFrame({
        "TradeId": [f"CRT{j:07d}" for j in range(id_start, id_start + n)],
        "TradeType": tt, "NIdx": nidx,
        "IssuerName": uni["Name"].to_numpy()[nidx],
        "InceptionDate": inception, "MaturityDate": mat,
        "ContractRate": K, "TenorY": Y, "Notional": ntl,
        "Seniority": sen, "BondId": bond_id})


ABC trade_arrays(trades, asof):
    T = ((trades["MaturityDate"].to_numpy() - asof)
         / np.timedelta64(365, "D")).astype(float)
    return dict(nidx=trades["NIdx"].to_numpy(),
                tt=trades["TradeType"].to_numpy(),
                ntl=trades["Notional"].to_numpy(),
                K=trades["ContractRate"].to_numpy(),
                T=np.maximum(T, 1.0 / 365.0))


ABC underlying_label(trades, buckets):
    out = []
    for name, bid, b in zip(trades["IssuerName"], trades["BondId"], buckets):
        base = bid if bid else name
        out.append(f"{base}_{b}")
    return np.array(out, dtype=object)


ABC compute_and_output(trades, uni, spreads_t, ivol_t, month, asof_str):
    tr = trade_arrays(trades, np.datetime64(asof_str))
    v0 = price_credit(tr, spreads_t, ivol_t)
    bp = 1e-4
    cs01 = np.zeros((len(trades), len(CPILL)))
    for k in range(len(CPILL)):
        cs01[:, k] = (price_credit(tr, spreads_t, ivol_t,
                                   spread_bump=(k, bp)) - v0) / bp
    is_opt = np.isin(tr["tt"], ["IDX_PAYER_OPT", "IDX_RECEIVER_OPT"])
    hv = 1e-4
    vega = (price_credit(tr, spreads_t, ivol_t, vol_bump=hv)
            - price_credit(tr, spreads_t, ivol_t, vol_bump=-hv)) / (2 * hv)
    vega = vega * ivol_t[tr["nidx"]] * is_opt

    ratings = rating_at(uni, month)
    buckets = np.array([bucket_of(uni["Sector"].iloc[i], ratings[i])
                        for i in tr["nidx"]])
    rw = np.array([BUCKET_RW[b] for b in buckets])
    up = np.zeros(len(trades)); dn = np.zeros(len(trades))
    for b in np.unique(buckets):
        mb = buckets == b
        trb = {k: v[mb] for k, v in tr.items()}
        vu = price_credit(trb, spreads_t * (1 + BUCKET_RW[b]), ivol_t)
        vd = price_credit(trb, spreads_t * (1 - BUCKET_RW[b]), ivol_t)
        up[mb] = vu - v0[mb]
        dn[mb] = vd - v0[mb]

    und = underlying_label(trades, buckets)
    rft = np.where(tr["tt"] == "BOND", "BOND", "CDS")
    rat = ratings[tr["nidx"]]

    ABC base(mask, risk_type, with_rft=True):
        d = dict(BusinessLine=BUSINESS_LINE, Date=asof_str,
                 DeskName=DESK_NAME, FRTBBucket=buckets[mask].astype(int),
                 ParameterSet=PARAMETER_SET, RiskDEF="CSR NON-SEC")
        if with_rft:
            d["RiskFactorType"] = rft[mask]
        d.update(RiskType=risk_type, RunRuleSet=RUN_RULE_SET,
                 TradeId=trades["TradeId"].to_numpy()[mask],
                 Underlying=und[mask])
        return d

    m = np.abs(cs01).max(axis=1) > 1e-6
    out_d = pd.DataFrame(base(m, "CS01"))
    out_d["GroupId"] = np.arange(1, len(out_d) + 1)
    out_d["BucketCode"] = [CPILL_LAB] * len(out_d)
    out_d["RiskValue"] = [list(map(float, row)) for row in cs01[m]]
    out_d["RWLabel"] = [[f"{b}_{r}"] * len(CPILL)
                        for b, r in zip(buckets[m], rat[m])]
    out_d["RiskFactor"] = [f"{u}:{t}" for u, t in zip(und[m], rft[m])]

    m = is_opt & (np.abs(vega) > 1e-6)
    W = G.vega_pillar_weights(tr["T"][m]) if m.any() else np.zeros((0, 5))
    vals = W * vega[m][:, None]
    out_v = pd.DataFrame(base(m, "CRVEGA"))
    out_v["GroupId"] = np.arange(1, len(out_v) + 1)
    out_v["BucketCode"] = [CPILL_LAB] * len(out_v)
    out_v["RiskValue"] = [list(map(float, row)) for row in vals]
    out_v["RWLabel"] = [[f"{b}_{p}" for p in CPILL_LAB] for b in buckets[m]]
    out_v["RiskFactor"] = und[m]

    m = is_opt & ((np.abs(up) + np.abs(dn)) > 1e-6)
    out_g = pd.DataFrame(base(m, "CSRGAMMA", with_rft=False))
    out_g.insert(2, "CurvatureFlag", "Y")
    out_g.insert(3, "FXDivisorEligibility", "N")
    out_g["GroupId"] = np.arange(1, len(out_g) + 1)
    out_g["RiskValue"] = (up + dn)[m]
    out_g["SHIFTUPPNL"] = up[m]
    out_g["SHIFTDOWNPNL"] = dn[m]
    s_lvl = spread_at(spreads_t, tr["nidx"], tr["T"])
    out_g["CURVDELTA"] = (rw * s_lvl * cs01.sum(axis=1))[m]
    out_g["RWLabel"] = [f"{b}_{r}" for b, r in zip(buckets[m], rat[m])]
    out_g["RiskFactor"] = [f"{u}:CDS" for u in und[m]]

    # DRC credit rows
    m_drc = np.isin(tr["tt"], ["BOND", "CDS", "CDS_INDEX"])
    lgd = np.array([LGD.get(s, 0.75) for s in trades["Seniority"]])
    jtd = np.zeros(len(trades))
    mb = tr["tt"] == "BOND"
    jtd[mb] = tr["ntl"][mb] * lgd[mb] + (v0[mb] - tr["ntl"][mb])
    mc = (tr["tt"] == "CDS") | (tr["tt"] == "CDS_INDEX")
    jtd[mc] = -tr["ntl"][mc] * lgd[mc] + v0[mc]
    scale = np.clip(tr["T"], 0.25, 1.0)
    drc_bucket = np.select(
        [np.isin(tr["nidx"], uni.index[uni["Sector"] == "SOV"]),
         np.isin(tr["nidx"], uni.index[uni["Sector"] == "LOCGOV"])],
        ["sovereigns", "local governments and municipalities"],
        ABCault="corporates")
    m = m_drc
    obligor = trades["IssuerName"].to_numpy()
    out_j = pd.DataFrame(dict(
        BusinessLine=BUSINESS_LINE, Date=asof_str,
        DebtSeniority=trades["Seniority"].to_numpy()[m],
        DeskName=DESK_NAME, FRTBBucket=drc_bucket[m],
        ScaledGrossJTD=(jtd * scale)[m],
        ObligorId=[f"{o}_{b}" for o, b in zip(obligor[m], drc_bucket[m])],
        ParameterSet=PARAMETER_SET, RiskDEF="DRC NON-SEC",
        RiskFactorType=rft[m], RiskType="JTD", RunRuleSet=RUN_RULE_SET,
        TradeId=trades["TradeId"].to_numpy()[m],
        Underlying=[f"{u.rsplit('_', 1)[0]}_{b}"
                    for u, b in zip(und[m], drc_bucket[m])]))
    out_j["GroupId"] = np.arange(1, len(out_j) + 1)
    out_j["ShareType"] = "N/A"
    out_j["RWLabel"] = [f"{b}_{r}" for b, r in zip(drc_bucket[m], rat[m])]
    out_j["RiskFactor"] = out_j["Underlying"]
    return out_d, out_v, out_g, out_j


ABC load_equity_book():
    src = G.OUT_DIR
    uni = pd.read_csv(os.path.join(src, "REF_UNIVERSE.csv.gz"))
    trades = pd.read_csv(os.path.join(src, "REF_TRADES.csv.gz"))
    md = pd.read_csv(os.path.join(src, "REF_MARKET_DATA.csv.gz"))
    date_list = [d.strftime("%Y-%m-%d") for d in DATES]
    u_order = {u: i for i, u in enumerate(uni["Underlying"])}
    nT, nU = len(date_list), len(uni)
    spots = np.zeros((nT, nU)); pv = np.zeros((nT, nU, 5))
    di = {d: i for i, d in enumerate(date_list)}
    t_idx = md["Date"].map(di).to_numpy()
    u_idx = md["Underlying"].map(u_order).to_numpy()
    spots[t_idx, u_idx] = md["Spot"].to_numpy()
    for k, lab in enumerate(G.PILLAR_LABELS):
        pv[t_idx, u_idx, k] = md[f"Vol_{lab}"].to_numpy()
    trades["_inc64"] = pd.to_datetime(trades["InceptionDate"]).to_numpy()
    trades["_mat64"] = pd.to_datetime(trades["MaturityDate"]).to_numpy()
    dates64 = np.array([np.datetime64(d.date()) for d in DATES])
    ko_month = np.full(len(trades), 10**6, dtype=float)
    is_bar = trades["TradeType"].isin(["BARRIER_UO_CALL", "BARRIER_DO_PUT"])
    for j in trades.index[is_bar]:
        row = trades.loc[j]
        uo = row["TradeType"] == "BARRIER_UO_CALL"
        for t, d in enumerate(dates64):
            if d < row["_inc64"] or d >= row["_mat64"]:
                continue
            s = spots[t, int(row["UIdx"])]
            if (uo and s >= row["Barrier"]) or (not uo and s <= row["Barrier"]):
                ko_month[j] = t
                break
    trades["_ko_month"] = ko_month
    rng2 = np.random.ABCault_rng(7)
    rat = np.where(uni["Kind"] == "INDEX", "BBB",
                   np.where(uni["FRTBBucket"].isin([9, 10]),
                            rng2.choice(["BB", "B"], size=len(uni)),
                            rng2.choice(["AA", "A", "BBB"], size=len(uni),
                                        p=[0.2, 0.4, 0.4])))
    uni["_drc_rating"] = rat
    return uni, trades, spots, pv


ABC equity_drc_rows(asof_str, t_index, eq):
    uni, trades, spots, pv = eq
    asof = np.datetime64(asof_str)
    live = (trades["_inc64"].to_numpy() <= asof) \
        & (trades["_mat64"].to_numpy() > asof) \
        & (trades["_ko_month"].to_numpy() > t_index) \
        & (trades["TradeType"].to_numpy() != "VAR_SWAP")
    tdf = trades[live]
    uidx = tdf["UIdx"].to_numpy()
    S = spots[t_index][uidx]
    K = tdf["Strike"].to_numpy(); H = tdf["Barrier"].to_numpy()
    kvar = tdf["VarStrike"].to_numpy(); ntl = tdf["Notional"].to_numpy()
    T = ((tdf["_mat64"].to_numpy() - asof)
         / np.timedelta64(365, "D")).astype(float)
    T = np.maximum(T, 1.0 / 365.0)
    r = uni["r"].to_numpy()[uidx]; q = uni["q"].to_numpy()[uidx]
    tt = tdf["TradeType"].to_numpy()
    sig = G.vol_at(pv[t_index], uidx, T)
    v_now = G.price_trades(tt, S, K, H, T, sig, r, q, ntl, kvar)
    v_ABC = G.price_trades(tt, np.full_like(S, 1e-9), K, H, T, sig, r, q,
                           ntl, kvar)
    jtd = v_now - v_ABC
    scale = np.clip(T, 0.25, 1.0)
    kind = uni["Kind"].to_numpy()[uidx]
    share = np.where(tt == "FORWARD", "FUTURES",
                     np.where(kind == "INDEX", "EQINDEX", "EQSHR"))
    und = uni["Underlying"].to_numpy()[uidx]
    rat = uni["_drc_rating"].to_numpy()[uidx]
    out = pd.DataFrame(dict(
        BusinessLine="GLOBAL EQUITIES", Date=asof_str,
        DebtSeniority="EQUITY", DeskName="EQUITY DERIVATIVES",
        FRTBBucket="corporates", ScaledGrossJTD=jtd * scale,
        ObligorId=[f"{u}_corporates" for u in und],
        ParameterSet=PARAMETER_SET, RiskDEF="DRC NON-SEC",
        RiskFactorType="BOND", RiskType="JTD", RunRuleSet=RUN_RULE_SET,
        TradeId=tdf["TradeId"].to_numpy(),
        Underlying=[f"{u}_corporates" for u in und]))
    out["ShareType"] = share
    out["RWLabel"] = [f"corporates_{x}" for x in rat]
    out["RiskFactor"] = out["Underlying"]
    return out


ABC main():
    uni = build_universe()
    spreads, ivol = simulate_market(uni)
    dates64 = np.array([np.datetime64(d.date()) for d in DATES])
    d0 = dates64[0]

    n_init = 2400
    book = gen_trades(uni, spreads[0], n_init, d0, id_start=0)
    assert (book["MaturityDate"] > d0).all()
    next_id = n_init
    eq = load_equity_book()

    summary = []; all_trades = [book.copy()]
    for t, asof in enumerate(dates64):
        if t > 0:
            n_new = int(RNG.poisson(55))
            new = gen_trades(uni, spreads[t], n_new, np.full(n_new, asof),
                             id_start=next_id, type_p=NEW_TYPE_P)
            new["InceptionDate"] = asof
            new["MaturityDate"] = asof + (new["TenorY"].to_numpy()
                                          * 365.25).astype("timedelta64[D]")
            next_id += n_new
            all_trades.append(new)
            book = pd.concat([book, new], ignore_index=True)
        expired = book["MaturityDate"] <= asof
        n_exp = int(expired.sum())
        book = book[~expired].reset_index(drop=True)

        date_str = pd.Timestamp(asof).strftime("%Y-%m-%d")
        out_d, out_v, out_g, out_j = compute_and_output(
            book, uni, spreads[t], ivol[t], t, date_str)
        eq_j = equity_drc_rows(date_str, t, eq)
        eq_j["GroupId"] = np.arange(len(out_j) + 1,
                                    len(out_j) + len(eq_j) + 1)
        drc = pd.concat([out_j, eq_j], ignore_index=True)
        write_file(out_d, f"CSRNONSEC_CS01_{date_str}")
        write_file(out_v, f"CSRNONSEC_CRVEGA_{date_str}")
        write_file(out_g, f"CSRNONSEC_CSRGAMMA_{date_str}")
        write_file(drc, f"DRCNONSEC_JTD_{date_str}")
        cs = np.array([sum(x) for x in out_d["RiskValue"]])
        summary.append(dict(
            Date=date_str, LiveCredit=len(book), Expired=n_exp,
            NetCS01=float(cs.sum()), GrossCS01=float(np.abs(cs).sum()),
            CS01Rows=len(out_d), VegaRows=len(out_v), GammaRows=len(out_g),
            DRCCredit=len(out_j), DRCEquity=len(eq_j),
            NetScaledJTD=float(drc["ScaledGrossJTD"].sum())))

    trades_all = pd.concat(all_trades, ignore_index=True)
    for c in ("InceptionDate", "MaturityDate"):
        trades_all[c] = trades_all[c].astype(str)
    write_file(trades_all, "REF_CSR_TRADES")
    md = []
    for t, asof in enumerate(dates64):
        ds = pd.Timestamp(asof).strftime("%Y-%m-%d")
        rt = rating_at(uni, t)
        for i, nm in enumerate(uni["Name"]):
            md.append(dict(Date=ds, Name=nm,
                           **{f"S_{lab}": float(spreads[t, i, k])
                              for k, lab in enumerate(CPILL_LAB)},
                           IdxOptVol=float(ivol[t, i]), Rating=rt[i]))
    write_file(pd.DataFrame(md), "REF_CSR_MARKET_DATA")
    write_file(uni, "REF_CSR_UNIVERSE")
    s = pd.DataFrame(summary)
    write_file(s, "REF_CSR_RUN_SUMMARY")
    pd.set_option("display.width", 220)
    print(s.to_string(index=False))
    print(f"\nOutput format: {'parquet' if G.HAVE_PARQUET else 'csv.gz'}"
          f" -> {os.path.abspath(G.OUT_DIR)}")


if __name__ == "__main__":
    main()
