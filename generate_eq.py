#!/usr/bin/env python3
"""
Synthetic FRTB SA equity portfolio generator
=============================================
Produces per-(RiskClass_RiskType, Date) files with trade-level FRTB SA
sensitivities (EQDELTA, EQVEGA, EQGAMMA/curvature) for 24 monthly dates.

Design
------
Market model
  * ~200 equity underlyings (indices + single names), G7-weighted materiality.
  * Spots: correlated monthly GBM (global factor + region factor + idio).
  * Vols: per-name short-vol follows a mean-reverting log-OU process,
    negatively correlated with the spot return (leverage effect).
    Pillar term structure {0.5,1,3,5,10}Y blends short vol into a long-run
    level (flat smile; term structure only).

Portfolio
  * ~8,500 seasoned trades at t0 + ~220 new trades/month; trades expire on
    maturity; barrier trades can knock out on monthly observations.
  * Types: FORWARD, EURO_CALL, EURO_PUT, STRADDLE, DIGITAL_CALL, DIGITAL_PUT,
    BARRIER_UO_CALL, BARRIER_DO_PUT, VAR_SWAP.
  * Closed-form pricing (Black-Scholes; Reiner-Rubinstein for barriers;
    simplified implied-variance mark for var swaps).
  * Per-underlying delta-hedge forwards are booked at inception so the book
    carries little net delta but material gamma and vega.

Sensitivity conventions (documented inference, not client-confirmed):
  * EQDELTA  RiskValue = (V(1.01*S) - V(S)) / 0.01          (MAR21.19 style)
  * EQVEGA   RiskValue = sigma * dV/dsigma, central FD,      (MAR21.26 style)
             allocated to tenor pillars by linear interpolation in remaining
             maturity.
  * EQGAMMA  SHIFTUPPNL   = V(S*(1+RW)) - V(S)
             SHIFTDOWNPNL = V(S*(1-RW)) - V(S)
             CURVDELTA    = RW * delta_sensitivity
             with RW = CRR2 equity spot risk weight of the FRTB bucket.

Output: parquet if pyarrow is importable, else csv.gz (list columns
serialised as JSON; convert_to_parquet.py restores them).
"""
from __future__ import annotations

import json
import os
import numpy as np
import pandas as pd
from scipy.stats import norm

RNG = np.random.default_rng(20260712)

OUT_DIR = os.environ.get("FRTB_OUT", "output")
DATES = pd.date_range("2024-07-31", periods=24, freq="ME")
PILLARS = np.array([0.5, 1.0, 3.0, 5.0, 10.0])
PILLAR_LABELS = ["0.5Y", "1Y", "3Y", "5Y", "10Y"]

BUSINESS_LINE = "GLOBAL EQUITIES"
DESK_NAME = "EQUITY DERIVATIVES"
PARAMETER_SET = "CRR_ECB_EUR"
RUN_RULE_SET = "CRR2_ECB"

# CRR2 equity spot risk weights by FRTB bucket (used for curvature shocks)
BUCKET_RW = {1: 0.55, 2: 0.60, 3: 0.45, 4: 0.55,
             5: 0.30, 6: 0.35, 7: 0.40, 8: 0.50,
             9: 0.70, 10: 0.50}

RATES = {"USD": 0.040, "EUR": 0.025, "JPY": 0.005, "GBP": 0.0425,
         "CAD": 0.035, "BRL": 0.105, "INR": 0.065, "KRW": 0.030}

# ---------------------------------------------------------------------------
# 1. Underlying universe (~200 names)
# ---------------------------------------------------------------------------

def build_universe() -> pd.DataFrame:
    rows = []

    def add(uid, kind, region, ccy, bucket, s0, vol, weight):
        rows.append(dict(Underlying=uid, Kind=kind, Region=region, Ccy=ccy,
                         FRTBBucket=bucket, S0=s0, VolLR=vol, Weight=weight))

    # --- indices (advanced-economy; mapped into buckets 5-8 as a
    #     simplification since the spec caps buckets at 10) ---
    idx = [("SPX", "US", "USD", 8, 5500, 0.16, 10.0),
           ("NDX", "US", "USD", 8, 19500, 0.20, 8.0),
           ("RTY", "US", "USD", 6, 2200, 0.22, 4.0),
           ("SX5E", "EU", "EUR", 5, 4900, 0.17, 7.0),
           ("DAX", "EU", "EUR", 6, 18200, 0.17, 5.0),
           ("CAC", "EU", "EUR", 5, 7600, 0.17, 3.5),
           ("FTSE", "UK", "GBP", 7, 8200, 0.14, 4.0),
           ("FTSEMIB", "EU", "EUR", 8, 33500, 0.19, 2.0),
           ("NKY", "JP", "JPY", 6, 39000, 0.19, 6.0),
           ("TPX", "JP", "JPY", 5, 2750, 0.17, 3.0),
           ("SPTSX", "CA", "CAD", 7, 22000, 0.14, 2.5),
           ("SMI", "EU", "EUR", 5, 12000, 0.14, 2.0)]
    for u, rg, c, b, s, v, w in idx:
        add(u, "INDEX", rg, c, b, s, v, w)

    # --- advanced-economy large-cap single names, bucket by sector ---
    # bucket 5: consumer/health/utilities, 6: telecom/industrials,
    # bucket 7: materials/energy, 8: financials/tech
    us_names = [
        ("AAPL", 8, 210, 0.24, 6.0), ("MSFT", 8, 440, 0.22, 6.0),
        ("NVDA", 8, 130, 0.42, 6.0), ("AMZN", 5, 190, 0.28, 4.5),
        ("GOOGL", 8, 175, 0.26, 4.0), ("META", 8, 500, 0.32, 3.5),
        ("TSLA", 5, 250, 0.52, 3.5), ("BRK", 8, 420, 0.16, 2.0),
        ("JPM", 8, 200, 0.22, 2.5), ("BAC", 8, 40, 0.24, 1.5),
        ("GS", 8, 460, 0.24, 1.2), ("MS", 8, 100, 0.25, 1.0),
        ("XOM", 7, 115, 0.22, 2.0), ("CVX", 7, 155, 0.21, 1.5),
        ("UNH", 5, 500, 0.22, 1.5), ("JNJ", 5, 150, 0.15, 1.3),
        ("PFE", 5, 28, 0.24, 0.9), ("MRK", 5, 128, 0.20, 1.0),
        ("LLY", 5, 800, 0.28, 1.8), ("ABBV", 5, 170, 0.20, 1.0),
        ("PG", 5, 165, 0.14, 1.2), ("KO", 5, 62, 0.14, 1.0),
        ("PEP", 5, 170, 0.15, 0.9), ("WMT", 5, 68, 0.16, 1.3),
        ("COST", 5, 850, 0.19, 1.1), ("HD", 5, 340, 0.20, 1.0),
        ("MCD", 5, 260, 0.15, 0.8), ("NKE", 5, 95, 0.26, 0.7),
        ("DIS", 5, 100, 0.24, 0.8), ("NFLX", 5, 650, 0.32, 1.2),
        ("CRM", 8, 260, 0.30, 0.9), ("ORCL", 8, 140, 0.26, 1.0),
        ("ADBE", 8, 520, 0.28, 0.8), ("INTC", 8, 31, 0.34, 0.7),
        ("AMD", 8, 160, 0.44, 1.4), ("QCOM", 8, 190, 0.30, 0.8),
        ("AVGO", 8, 1650, 0.32, 1.4), ("TXN", 8, 195, 0.24, 0.6),
        ("MU", 8, 130, 0.42, 0.8), ("IBM", 8, 175, 0.20, 0.6),
        ("CSCO", 6, 47, 0.20, 0.6), ("VZ", 6, 41, 0.16, 0.6),
        ("T", 6, 18, 0.18, 0.5), ("TMUS", 6, 180, 0.18, 0.6),
        ("BA", 6, 180, 0.32, 0.8), ("CAT", 6, 330, 0.24, 0.8),
        ("DE", 6, 380, 0.24, 0.6), ("GE", 6, 160, 0.26, 0.7),
        ("HON", 6, 210, 0.18, 0.6), ("UPS", 6, 135, 0.22, 0.5),
        ("FDX", 6, 260, 0.26, 0.5), ("UNP", 6, 240, 0.20, 0.5),
        ("LMT", 6, 460, 0.16, 0.5), ("RTX", 6, 105, 0.18, 0.5),
        ("FCX", 7, 48, 0.36, 0.5), ("NEM", 7, 45, 0.32, 0.4),
        ("COP", 7, 110, 0.26, 0.7), ("SLB", 7, 45, 0.30, 0.4),
        ("OXY", 7, 60, 0.30, 0.4), ("DOW", 7, 52, 0.24, 0.3),
        ("V", 8, 275, 0.18, 1.5), ("MA", 8, 460, 0.19, 1.3),
        ("AXP", 8, 240, 0.22, 0.7), ("BLK", 8, 820, 0.22, 0.7),
        ("C", 8, 64, 0.26, 0.8), ("WFC", 8, 60, 0.24, 0.8),
        ("SCHW", 8, 72, 0.28, 0.5), ("SPGI", 8, 460, 0.20, 0.5),
    ]
    for t, b, s, v, w in us_names:
        add(f"{t}.US", "SINGLE", "US", "USD", b, s, v, w)

    jp_names = [("7203", 6, 2900, 0.24, 1.5), ("6758", 5, 13500, 0.26, 1.2),
                ("8306", 8, 1650, 0.28, 1.0), ("9984", 8, 9200, 0.38, 1.2),
                ("6861", 6, 65000, 0.28, 0.8), ("9432", 6, 150, 0.18, 0.6),
                ("8035", 8, 34000, 0.40, 1.0), ("4063", 7, 6100, 0.24, 0.5),
                ("6501", 6, 3600, 0.28, 0.6), ("7974", 5, 8200, 0.28, 0.7),
                ("9983", 5, 41000, 0.28, 0.5), ("8058", 7, 3200, 0.24, 0.5),
                ("8031", 7, 3400, 0.24, 0.4), ("4502", 5, 4100, 0.18, 0.4),
                ("6902", 6, 2300, 0.26, 0.4), ("6367", 6, 22000, 0.24, 0.4),
                ("8766", 8, 5400, 0.20, 0.4), ("8316", 8, 10500, 0.26, 0.5)]
    for t, b, s, v, w in jp_names:
        add(f"{t}.JP", "SINGLE", "JP", "JPY", b, s, v, w)

    eu_names = [("SAP", 8, 185, 0.22, 1.2), ("ASML", 8, 900, 0.34, 1.5),
                ("SIE", 6, 175, 0.22, 0.8), ("ALV", 8, 265, 0.18, 0.7),
                ("DTE", 6, 23, 0.16, 0.6), ("BAS", 7, 46, 0.24, 0.4),
                ("BMW", 5, 92, 0.24, 0.4), ("MBG", 5, 65, 0.24, 0.4),
                ("VOW3", 5, 105, 0.28, 0.4), ("BAYN", 5, 27, 0.32, 0.3),
                ("MC", 5, 720, 0.26, 1.0), ("OR", 5, 420, 0.20, 0.6),
                ("TTE", 7, 62, 0.20, 0.7), ("SAN", 5, 92, 0.18, 0.5),
                ("AIR", 6, 145, 0.24, 0.6), ("BNP", 8, 63, 0.24, 0.5),
                ("SU", 6, 225, 0.24, 0.5), ("EL", 6, 190, 0.28, 0.3),
                ("ISP", 8, 3.6, 0.24, 0.4), ("ENI", 7, 14.5, 0.20, 0.3),
                ("UCG", 8, 36, 0.28, 0.4), ("ENEL", 5, 6.6, 0.18, 0.4),
                ("STLAM", 5, 19, 0.32, 0.3), ("NESN", 5, 92, 0.14, 0.8),
                ("NOVN", 5, 96, 0.16, 0.7), ("ROG", 5, 250, 0.18, 0.6)]
    for t, b, s, v, w in eu_names:
        add(f"{t}.EU", "SINGLE", "EU", "EUR", b, s, v, w)

    uk_names = [("SHEL", 7, 28, 0.20, 0.8), ("AZN", 5, 122, 0.18, 0.7),
                ("HSBA", 8, 6.8, 0.20, 0.7), ("ULVR", 5, 44, 0.16, 0.5),
                ("BP", 7, 4.7, 0.22, 0.5), ("GSK", 5, 15.5, 0.18, 0.4),
                ("RIO", 7, 52, 0.26, 0.5), ("GLEN", 7, 4.5, 0.30, 0.4),
                ("BARC", 8, 2.2, 0.28, 0.4), ("LLOY", 8, 0.58, 0.24, 0.3),
                ("VOD", 6, 0.70, 0.22, 0.3), ("BT.A", 6, 1.4, 0.24, 0.2),
                ("REL", 5, 36, 0.16, 0.3), ("DGE", 5, 25, 0.18, 0.3)]
    for t, b, s, v, w in uk_names:
        add(f"{t}.UK", "SINGLE", "UK", "GBP", b, s, v, w)

    ca_names = [("RY", 8, 145, 0.16, 0.5), ("TD", 8, 78, 0.18, 0.4),
                ("SHOP", 8, 88, 0.44, 0.5), ("ENB", 7, 48, 0.16, 0.3),
                ("CNQ", 7, 48, 0.24, 0.3), ("BNS", 8, 64, 0.18, 0.3),
                ("CP", 6, 110, 0.20, 0.3), ("CNR", 6, 165, 0.18, 0.3)]
    for t, b, s, v, w in ca_names:
        add(f"{t}.CA", "SINGLE", "CA", "CAD", b, s, v, w)

    # --- emerging-market large caps (buckets 1-4) ---
    em_names = [("VALE3.BR", "EM", "BRL", 3, 62, 0.32, 0.4),
                ("PETR4.BR", "EM", "BRL", 3, 38, 0.34, 0.4),
                ("ITUB4.BR", "EM", "BRL", 2, 32, 0.28, 0.3),
                ("RELIANCE.IN", "EM", "INR", 3, 2950, 0.24, 0.5),
                ("TCS.IN", "EM", "INR", 4, 3900, 0.22, 0.4),
                ("INFY.IN", "EM", "INR", 4, 1550, 0.24, 0.3),
                ("HDFCB.IN", "EM", "INR", 2, 1650, 0.22, 0.4),
                ("005930.KR", "EM", "KRW", 4, 78000, 0.28, 0.6),
                ("000660.KR", "EM", "KRW", 4, 210000, 0.40, 0.4),
                ("051910.KR", "EM", "KRW", 3, 350000, 0.30, 0.2),
                ("BBRI.ID", "EM", "IDR_PROXY", 2, 4600, 0.28, 0.2),
                ("MTN.ZA", "EM", "ZAR_PROXY", 1, 95, 0.32, 0.2)]
    for t, rg, c, b, s, v, w in em_names:
        add(t, "SINGLE", rg, c if c in RATES else "USD", b, s, v, w)

    # --- small caps (bucket 9 EM / 10 advanced), synthetic tickers ---
    n_small_adv = 200 - len(rows) - 12
    for i in range(n_small_adv):
        region = RNG.choice(["US", "EU", "JP", "UK", "CA"],
                            p=[0.5, 0.2, 0.15, 0.1, 0.05])
        ccy = {"US": "USD", "EU": "EUR", "JP": "JPY",
               "UK": "GBP", "CA": "CAD"}[region]
        add(f"SC{i:03d}.{region}", "SINGLE", region, ccy, 10,
            float(RNG.uniform(8, 120)), float(RNG.uniform(0.30, 0.55)),
            float(RNG.uniform(0.05, 0.20)))
    for i in range(12):
        add(f"EMSC{i:02d}", "SINGLE", "EM", "USD", 9,
            float(RNG.uniform(5, 60)), float(RNG.uniform(0.35, 0.60)),
            float(RNG.uniform(0.04, 0.12)))

    df = pd.DataFrame(rows)
    assert len(df) == 200, f"universe size {len(df)}"
    df["q"] = RNG.uniform(0.0, 0.035, len(df))          # dividend yield
    df["r"] = df["Ccy"].map(RATES).fillna(0.05)
    df["Sector"] = assign_equity_sectors(df)
    return df



# GICS-style sector classification (descriptive metadata; FRTB buckets
# follow CRR sector groups and are assigned independently)
EQ_SECTOR_MAP = {
    # US
    "AAPL": "Information Technology", "MSFT": "Information Technology",
    "NVDA": "Information Technology", "AMZN": "Consumer Discretionary",
    "GOOGL": "Communication Services", "META": "Communication Services",
    "TSLA": "Consumer Discretionary", "BRK": "Financials",
    "JPM": "Financials", "BAC": "Financials", "GS": "Financials",
    "MS": "Financials", "XOM": "Energy", "CVX": "Energy",
    "UNH": "Health Care", "JNJ": "Health Care", "PFE": "Health Care",
    "MRK": "Health Care", "LLY": "Health Care", "ABBV": "Health Care",
    "PG": "Consumer Staples", "KO": "Consumer Staples",
    "PEP": "Consumer Staples", "WMT": "Consumer Staples",
    "COST": "Consumer Staples", "HD": "Consumer Discretionary",
    "MCD": "Consumer Discretionary", "NKE": "Consumer Discretionary",
    "DIS": "Communication Services", "NFLX": "Communication Services",
    "CRM": "Information Technology", "ORCL": "Information Technology",
    "ADBE": "Information Technology", "INTC": "Information Technology",
    "AMD": "Information Technology", "QCOM": "Information Technology",
    "AVGO": "Information Technology", "TXN": "Information Technology",
    "MU": "Information Technology", "IBM": "Information Technology",
    "CSCO": "Information Technology", "VZ": "Communication Services",
    "T": "Communication Services", "TMUS": "Communication Services",
    "BA": "Industrials", "CAT": "Industrials", "DE": "Industrials",
    "GE": "Industrials", "HON": "Industrials", "UPS": "Industrials",
    "FDX": "Industrials", "UNP": "Industrials", "LMT": "Industrials",
    "RTX": "Industrials", "FCX": "Materials", "NEM": "Materials",
    "COP": "Energy", "SLB": "Energy", "OXY": "Energy", "DOW": "Materials",
    "V": "Financials", "MA": "Financials", "AXP": "Financials",
    "BLK": "Financials", "C": "Financials", "WFC": "Financials",
    "SCHW": "Financials", "SPGI": "Financials",
    # JP
    "7203": "Consumer Discretionary", "6758": "Consumer Discretionary",
    "8306": "Financials", "9984": "Communication Services",
    "6861": "Information Technology", "9432": "Communication Services",
    "8035": "Information Technology", "4063": "Materials",
    "6501": "Industrials", "7974": "Communication Services",
    "9983": "Consumer Discretionary", "8058": "Industrials",
    "8031": "Industrials", "4502": "Health Care",
    "6902": "Consumer Discretionary", "6367": "Industrials",
    "8766": "Financials", "8316": "Financials",
    # EU
    "SAP": "Information Technology", "ASML": "Information Technology",
    "SIE": "Industrials", "ALV": "Financials",
    "DTE": "Communication Services", "BAS": "Materials",
    "BMW": "Consumer Discretionary", "MBG": "Consumer Discretionary",
    "VOW3": "Consumer Discretionary", "BAYN": "Health Care",
    "MC": "Consumer Discretionary", "OR": "Consumer Staples",
    "TTE": "Energy", "SAN": "Health Care", "AIR": "Industrials",
    "BNP": "Financials", "SU": "Industrials", "EL": "Health Care",
    "ISP": "Financials", "ENI": "Energy", "UCG": "Financials",
    "ENEL": "Utilities", "STLAM": "Consumer Discretionary",
    "NESN": "Consumer Staples", "NOVN": "Health Care", "ROG": "Health Care",
    # UK
    "SHEL": "Energy", "AZN": "Health Care", "HSBA": "Financials",
    "ULVR": "Consumer Staples", "BP": "Energy", "GSK": "Health Care",
    "RIO": "Materials", "GLEN": "Materials", "BARC": "Financials",
    "LLOY": "Financials", "VOD": "Communication Services",
    "BT.A": "Communication Services", "REL": "Industrials",
    "DGE": "Consumer Staples",
    # CA
    "RY": "Financials", "TD": "Financials",
    "SHOP": "Information Technology", "ENB": "Energy", "CNQ": "Energy",
    "BNS": "Financials", "CP": "Industrials", "CNR": "Industrials",
    # EM
    "VALE3.BR": "Materials", "PETR4.BR": "Energy", "ITUB4.BR": "Financials",
    "RELIANCE.IN": "Energy", "TCS.IN": "Information Technology",
    "INFY.IN": "Information Technology", "HDFCB.IN": "Financials",
    "005930.KR": "Information Technology",
    "000660.KR": "Information Technology", "051910.KR": "Materials",
    "BBRI.ID": "Financials", "MTN.ZA": "Communication Services",
}
GICS_SECTORS = ["Information Technology", "Communication Services",
                "Consumer Discretionary", "Consumer Staples", "Health Care",
                "Financials", "Energy", "Materials", "Industrials",
                "Utilities", "Real Estate"]


def assign_equity_sectors(uni: pd.DataFrame) -> pd.Series:
    """Named tickers via EQ_SECTOR_MAP (ticker = id before the region dot);
    indices -> 'Index'; synthetic small caps -> seeded random sector."""
    rng = np.random.default_rng(11)
    out = []
    for u, kind in zip(uni["Underlying"], uni["Kind"]):
        if kind == "INDEX":
            out.append("Index")
            continue
        key = u if u in EQ_SECTOR_MAP else u.split(".")[0]
        if key in EQ_SECTOR_MAP:
            out.append(EQ_SECTOR_MAP[key])
        else:
            out.append(str(rng.choice(GICS_SECTORS)))
    return pd.Series(out, index=uni.index)


# ---------------------------------------------------------------------------
# 2. Market simulation: spots + vol term structures, monthly
# ---------------------------------------------------------------------------

def simulate_market(uni: pd.DataFrame):
    n, m = len(uni), len(DATES)
    dt = 1.0 / 12.0
    is_index = (uni["Kind"] == "INDEX").to_numpy()
    regions = uni["Region"].to_numpy()
    region_list = ["US", "EU", "JP", "UK", "CA", "EM"]
    reg_idx = np.array([region_list.index(r) for r in regions])

    # factor loadings
    beta_g = np.where(is_index, 0.95, RNG.uniform(0.6, 1.1, n))
    beta_r = np.where(is_index, 0.6, RNG.uniform(0.4, 0.9, n))
    total_vol = uni["VolLR"].to_numpy().copy()

    sig_g, sig_r = 0.11, 0.07                     # annualised factor vols
    sys_var = (beta_g * sig_g) ** 2 + (beta_r * sig_r) ** 2
    idio_vol = np.sqrt(np.maximum(total_vol ** 2 - sys_var, 0.02 ** 2))

    spots = np.empty((m, n))
    short_vol = np.empty((m, n))
    # log short-vol OU, correlated with own return
    ln_vol = np.log(total_vol * RNG.uniform(0.85, 1.15, n))
    kappa, eta, rho_sv = 3.0, 0.9, -0.55
    S = uni["S0"].to_numpy().copy()
    drift = uni["r"].to_numpy() - uni["q"].to_numpy()

    # engineered stress in month 14 (2025-09): global equity selloff,
    # vol spike -> gives the movement-explain agent a regime event
    stress_month = 14

    for t in range(m):
        spots[t] = S
        short_vol[t] = np.exp(ln_vol)
        if t == m - 1:
            break
        zg = RNG.normal()
        zr = RNG.normal(size=len(region_list))
        zi = RNG.normal(size=n)
        if t + 1 == stress_month:
            zg -= 2.8                              # ~ -8% global factor shock
        ret = (drift - 0.5 * total_vol ** 2) * dt + np.sqrt(dt) * (
            beta_g * sig_g * zg + beta_r * sig_r * zr[reg_idx]
            + idio_vol * zi)
        S = S * np.exp(ret)
        z_std = (ret - ret.mean()) / (ret.std() + 1e-12)
        zv = rho_sv * z_std + np.sqrt(1 - rho_sv ** 2) * RNG.normal(size=n)
        ln_vol = ln_vol + kappa * (np.log(total_vol) - ln_vol) * dt \
            + eta * np.sqrt(dt) * zv
        if t + 1 == stress_month:
            ln_vol += 0.35                         # vol spike on the selloff

    # pillar vols: blend short vol into long-run level with tenor
    w = (PILLARS / (PILLARS + 2.0))[None, None, :]          # (1,1,5)
    ln_lr = np.log(total_vol)[None, :, None]
    ln_sh = np.log(short_vol)[:, :, None]
    pillar_vol = np.exp((1 - w) * ln_sh + w * ln_lr)         # (m,n,5)
    return spots, pillar_vol


def vol_at(pillar_vol_t: np.ndarray, uidx: np.ndarray, T: np.ndarray):
    """Interpolate log pillar vols linearly in tenor, flat extrapolation."""
    lv = np.log(pillar_vol_t[uidx])                          # (k,5)
    Tc = np.clip(T, PILLARS[0], PILLARS[-1])
    j = np.searchsorted(PILLARS, Tc, side="right") - 1
    j = np.clip(j, 0, len(PILLARS) - 2)
    w = (Tc - PILLARS[j]) / (PILLARS[j + 1] - PILLARS[j])
    out = np.exp(lv[np.arange(len(T)), j] * (1 - w)
                 + lv[np.arange(len(T)), j + 1] * w)
    return out


# ---------------------------------------------------------------------------
# 3. Pricing (vectorised, closed form)
# ---------------------------------------------------------------------------

def _d1d2(S, K, T, sig, r, q):
    sq = sig * np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sig ** 2) * T) / sq
    return d1, d1 - sq


def bs_price(S, K, T, sig, r, q, cp):
    d1, d2 = _d1d2(S, K, T, sig, r, q)
    return np.where(np.asarray(cp) > 0,
                 S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2),
                 K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1))


def digital_price(S, K, T, sig, r, q, cp):
    _, d2 = _d1d2(S, K, T, sig, r, q)
    return np.where(cp > 0, np.exp(-r * T) * norm.cdf(d2),
                    np.exp(-r * T) * norm.cdf(-d2))


def barrier_uo_call(S, K, H, T, sig, r, q):
    """Up-and-out call, H > K, no rebate (Reiner-Rubinstein).
    Returns 0 where S >= H (knocked out at observation)."""
    sq = sig * np.sqrt(T)
    lam = (r - q + 0.5 * sig ** 2) / sig ** 2
    x1 = np.log(S / K) / sq + lam * sq
    x2 = np.log(S / H) / sq + lam * sq
    y1 = np.log(H ** 2 / (S * K)) / sq + lam * sq
    y2 = np.log(H / S) / sq + lam * sq
    hs = (H / S)
    # Haug (eta=-1, phi=+1), K < H:  c_uo = A - B + C - D
    A = S * np.exp(-q * T) * norm.cdf(x1) - K * np.exp(-r * T) * norm.cdf(x1 - sq)
    B = S * np.exp(-q * T) * norm.cdf(x2) - K * np.exp(-r * T) * norm.cdf(x2 - sq)
    C = S * np.exp(-q * T) * hs ** (2 * lam) * norm.cdf(-y1) \
        - K * np.exp(-r * T) * hs ** (2 * lam - 2) * norm.cdf(-y1 + sq)
    D = S * np.exp(-q * T) * hs ** (2 * lam) * norm.cdf(-y2) \
        - K * np.exp(-r * T) * hs ** (2 * lam - 2) * norm.cdf(-y2 + sq)
    v = A - B + C - D
    return np.where(S >= H, 0.0, np.maximum(v, 0.0))


def barrier_do_put(S, K, H, T, sig, r, q):
    """Down-and-out put, H < K, no rebate: P_do = P_vanilla - P_down_and_in."""
    sq = sig * np.sqrt(T)
    lam = (r - q + 0.5 * sig ** 2) / sig ** 2
    x1 = np.log(S / K) / sq + lam * sq
    x2 = np.log(S / H) / sq + lam * sq
    y1 = np.log(H ** 2 / (S * K)) / sq + lam * sq
    y2 = np.log(H / S) / sq + lam * sq
    hs = H / S
    # down-and-in put (H < K), Haug 2007 (eta=1, phi=-1):
    A = -S * np.exp(-q * T) * norm.cdf(-x1) + K * np.exp(-r * T) * norm.cdf(-x1 + sq)
    B = -S * np.exp(-q * T) * norm.cdf(-x2) + K * np.exp(-r * T) * norm.cdf(-x2 + sq)
    C = -S * np.exp(-q * T) * hs ** (2 * lam) * norm.cdf(y1) \
        + K * np.exp(-r * T) * hs ** (2 * lam - 2) * norm.cdf(y1 - sq)
    D = -S * np.exp(-q * T) * hs ** (2 * lam) * norm.cdf(y2) \
        + K * np.exp(-r * T) * hs ** (2 * lam - 2) * norm.cdf(y2 - sq)
    p_di = B - C + D
    p_van = bs_price(S, K, T, sig, r, q, np.full_like(S, -1.0))
    v = p_van - p_di
    return np.where(S <= H, 0.0, np.maximum(v, 0.0))


def price_trades(tt, S, K, H, T, sig, r, q, ntl, kvar):
    """Dispatch by trade type. All args are aligned numpy arrays.
    Returns value in trade currency units (notional applied)."""
    v = np.zeros_like(S)
    m = tt == "FORWARD"
    if m.any():
        v[m] = ntl[m] * (S[m] * np.exp(-q[m] * T[m]) - K[m] * np.exp(-r[m] * T[m]))
    m = tt == "EURO_CALL"
    if m.any():
        v[m] = ntl[m] * bs_price(S[m], K[m], T[m], sig[m], r[m], q[m], 1)
    m = tt == "EURO_PUT"
    if m.any():
        v[m] = ntl[m] * bs_price(S[m], K[m], T[m], sig[m], r[m], q[m], -1)
    m = tt == "STRADDLE"
    if m.any():
        v[m] = ntl[m] * (bs_price(S[m], K[m], T[m], sig[m], r[m], q[m], 1)
                         + bs_price(S[m], K[m], T[m], sig[m], r[m], q[m], -1))
    m = tt == "DIGITAL_CALL"
    if m.any():
        v[m] = ntl[m] * K[m] * digital_price(S[m], K[m], T[m], sig[m], r[m], q[m], 1)
    m = tt == "DIGITAL_PUT"
    if m.any():
        v[m] = ntl[m] * K[m] * digital_price(S[m], K[m], T[m], sig[m], r[m], q[m], -1)
    m = tt == "BARRIER_UO_CALL"
    if m.any():
        v[m] = ntl[m] * barrier_uo_call(S[m], K[m], H[m], T[m], sig[m], r[m], q[m])
    m = tt == "BARRIER_DO_PUT"
    if m.any():
        v[m] = ntl[m] * barrier_do_put(S[m], K[m], H[m], T[m], sig[m], r[m], q[m])
    m = tt == "VAR_SWAP"
    if m.any():
        # simplified mark on remaining implied variance vs strike (realised
        # leg ignored); ntl = variance notional (per variance point)
        v[m] = ntl[m] * np.exp(-r[m] * T[m]) * (sig[m] ** 2 - kvar[m] ** 2) * 1e4
    return v


# ---------------------------------------------------------------------------
# 4. Portfolio generation
# ---------------------------------------------------------------------------

TYPE_P = {"FORWARD": 0.10, "EURO_CALL": 0.19, "EURO_PUT": 0.19,
          "STRADDLE": 0.17, "DIGITAL_CALL": 0.045, "DIGITAL_PUT": 0.045,
          "BARRIER_UO_CALL": 0.08, "BARRIER_DO_PUT": 0.08, "VAR_SWAP": 0.10}
TENORS = np.array([0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0])
TENOR_P = np.array([0.14, 0.20, 0.24, 0.16, 0.10, 0.08, 0.04, 0.04])


def gen_trades(uni, n, inception_dates, spot_ref, id_start, spot_jitter=0.0):
    """Generate n trades with given inception dates (np datetime64 array).
    spot_ref: per-underlying spot array (len = #underlyings) used as the
    inception spot reference; spot_jitter adds lognormal noise for
    seasoned trades whose true inception spot pre-dates the simulation."""
    k = len(uni)
    w = uni["Weight"].to_numpy()
    p_u = w / w.sum()
    uidx = RNG.choice(k, size=n, p=p_u)
    ttypes = RNG.choice(list(TYPE_P), size=n, p=list(TYPE_P.values()))
    tenor = RNG.choice(TENORS, size=n, p=TENOR_P)
    if np.isscalar(inception_dates) or getattr(inception_dates, "ndim", 1) == 0:
        # seasoned book: age drawn conditional on trade alive at `asof`
        asof = np.datetime64(inception_dates)
        age = RNG.uniform(0.03, 0.90, n) * tenor
        inception_dates = asof - (age * 365.25).astype("timedelta64[D]")
    s_inc = spot_ref[uidx]
    if spot_jitter > 0:
        s_inc = s_inc * np.exp(RNG.normal(0.0, spot_jitter, n))
    # moneyness: lognormal around ATM, wider for longer tenors
    mny = np.exp(RNG.normal(0.0, 0.10 + 0.04 * np.sqrt(tenor)))
    K = s_inc * mny
    K[ttypes == "STRADDLE"] = (s_inc * np.exp(RNG.normal(0, 0.03, n)))[ttypes == "STRADDLE"]
    H = np.full(n, np.nan)
    m = ttypes == "BARRIER_UO_CALL"
    H[m] = np.maximum(s_inc[m], K[m]) * RNG.uniform(1.15, 1.45, m.sum())
    m = ttypes == "BARRIER_DO_PUT"
    H[m] = np.minimum(s_inc[m], K[m]) * RNG.uniform(0.60, 0.85, m.sum())
    kvar = np.full(n, np.nan)
    m = ttypes == "VAR_SWAP"
    kvar[m] = uni["VolLR"].to_numpy()[uidx[m]] * RNG.uniform(0.9, 1.1, m.sum())

    # notionals: materiality-weighted, signed (long/short ~50/50);
    # expressed in units (shares/contracts); scaled so big names dominate
    base = 2.0e6 * (w[uidx] / w.mean()) ** 0.7 / s_inc
    ntl = base * RNG.lognormal(0.0, 0.6, n) * RNG.choice([1.0, -1.0], size=n)
    m = ttypes == "VAR_SWAP"
    ntl[m] = np.sign(ntl[m]) * np.abs(ntl[m]) * s_inc[m] * 2e-4  # var units

    mat = inception_dates + (tenor * 365.25).astype("timedelta64[D]")
    return pd.DataFrame({
        "TradeId": [f"EQT{j:07d}" for j in range(id_start, id_start + n)],
        "TradeType": ttypes, "UIdx": uidx,
        "Underlying": uni["Underlying"].to_numpy()[uidx],
        "InceptionDate": inception_dates, "MaturityDate": mat,
        "Strike": K, "Barrier": H, "VarStrike": kvar, "Notional": ntl,
        "Alive": True,
    })


def add_hedge_forwards(trades, uni, spots_t, pillar_vol_t, asof, id_start,
                       hedge_ratio=0.85):
    """Book delta-hedge forwards per underlying against the delta of the
    trades passed in (valued as of `asof`)."""
    d = compute_greeks(trades, uni, spots_t, pillar_vol_t, asof)
    agg = d.groupby("UIdx")["DeltaShares"].sum()
    rows = []
    j = id_start
    for uidx, dshares in agg.items():
        if abs(dshares) * spots_t[uidx] < 5e5:      # skip immaterial
            continue
        tenor = float(RNG.choice([0.5, 1.0, 2.0]))
        rows.append(dict(
            TradeId=f"EQT{j:07d}", TradeType="FORWARD", UIdx=int(uidx),
            Underlying=uni["Underlying"].iloc[int(uidx)],
            InceptionDate=asof,
            MaturityDate=asof + np.timedelta64(int(tenor * 365.25), "D"),
            Strike=spots_t[uidx], Barrier=np.nan, VarStrike=np.nan,
            Notional=-hedge_ratio * dshares, Alive=True))
        j += 1
    return pd.DataFrame(rows), j


# ---------------------------------------------------------------------------
# 5. Greeks / FRTB sensitivities
# ---------------------------------------------------------------------------

def _arrays(trades, uni, spots_t, asof):
    uidx = trades["UIdx"].to_numpy()
    S = spots_t[uidx]
    K = trades["Strike"].to_numpy()
    H = trades["Barrier"].to_numpy()
    kvar = trades["VarStrike"].to_numpy()
    ntl = trades["Notional"].to_numpy()
    T = (trades["MaturityDate"].to_numpy() - asof) / np.timedelta64(365, "D")
    T = np.maximum(T.astype(float), 1.0 / 365.0)
    r = uni["r"].to_numpy()[uidx]
    q = uni["q"].to_numpy()[uidx]
    tt = trades["TradeType"].to_numpy()
    return tt, uidx, S, K, H, T, r, q, ntl, kvar


def compute_greeks(trades, uni, spots_t, pillar_vol_t, asof):
    """FRTB-convention sensitivities per trade."""
    tt, uidx, S, K, H, T, r, q, ntl, kvar = _arrays(trades, uni, spots_t, asof)
    sig = vol_at(pillar_vol_t, uidx, T)

    def V(Sx, sx):
        return price_trades(tt, Sx, K, H, T, sx, r, q, ntl, kvar)

    v0 = V(S, sig)
    # FRTB delta: (V(1.01 S) - V(S)) / 0.01
    delta_sens = (V(1.01 * S, sig) - v0) / 0.01
    hs = 1e-4
    delta_shares = (V(S * (1 + hs), sig) - V(S * (1 - hs), sig)) / (2 * hs * S)
    hv = 1e-4
    vega_raw = (V(S, sig + hv) - V(S, sig - hv)) / (2 * hv)
    vega_sens = vega_raw * sig                       # FRTB: vega * sigma
    # curvature shocks at bucket RW
    rw = np.array([BUCKET_RW[b] for b in
                   uni["FRTBBucket"].to_numpy()[uidx]])
    up = V(S * (1 + rw), sig) - v0
    dn = V(S * (1 - rw), sig) - v0

    return pd.DataFrame({
        "TradeId": trades["TradeId"].to_numpy(), "UIdx": uidx,
        "TradeType": tt, "T": T, "Value": v0,
        "DeltaSens": delta_sens, "DeltaShares": delta_shares,  # dV/dS in shares
        "VegaSens": vega_sens, "ShiftUpPnl": up, "ShiftDownPnl": dn,
        "RW": rw,
    })


def vega_pillar_weights(T):
    """Linear allocation of vega to adjacent pillars; flat outside."""
    W = np.zeros((len(T), len(PILLARS)))
    Tc = np.clip(T, PILLARS[0], PILLARS[-1])
    j = np.clip(np.searchsorted(PILLARS, Tc, side="right") - 1, 0,
                len(PILLARS) - 2)
    w = (Tc - PILLARS[j]) / (PILLARS[j + 1] - PILLARS[j])
    W[np.arange(len(T)), j] = 1 - w
    W[np.arange(len(T)), j + 1] = w
    return W


# ---------------------------------------------------------------------------
# 6. Output writers
# ---------------------------------------------------------------------------

try:
    import pyarrow  # noqa: F401
    HAVE_PARQUET = True
except ImportError:
    HAVE_PARQUET = False


def write_file(df: pd.DataFrame, name: str):
    os.makedirs(OUT_DIR, exist_ok=True)
    if HAVE_PARQUET:
        df.to_parquet(os.path.join(OUT_DIR, name + ".parquet"), index=False)
    else:
        d = df.copy()
        for c in d.columns:
            if len(d) and isinstance(d[c].iloc[0], (list, np.ndarray)):
                d[c] = d[c].map(lambda x: json.dumps(list(np.asarray(x).tolist())))
        d.to_csv(os.path.join(OUT_DIR, name + ".csv.gz"), index=False,
                 compression="gzip")


def build_outputs(g: pd.DataFrame, uni: pd.DataFrame, date_str: str):
    buckets = uni["FRTBBucket"].to_numpy()[g["UIdx"].to_numpy()]
    und = uni["Underlying"].to_numpy()[g["UIdx"].to_numpy()]
    common = dict(BusinessLine=BUSINESS_LINE, Date=date_str,
                  DeskName=DESK_NAME, ParameterSet=PARAMETER_SET,
                  RiskClass="EQUITY", RiskFactorType="SPOT",
                  RunRuleSet=RUN_RULE_SET)

    # ---- EQDELTA ----
    m = np.abs(g["DeltaSens"].to_numpy()) > 1e-8
    d = g[m]
    bd = buckets[m]
    ud = und[m]
    _ = common  # kept for readability of shared fields
    delta = pd.DataFrame({
            "BusinessLine": BUSINESS_LINE, "Date": date_str,
            "DeskName": DESK_NAME, "FRTBBucket": bd.astype(int),
            "ParameterSet": PARAMETER_SET, "RiskClass": "EQUITY",
            "RiskFactorType": "SPOT", "RiskType": "EQDELTA",
            "RunRuleSet": RUN_RULE_SET,
            "TradeId": d["TradeId"].to_numpy(), "Underlying": ud,
        })
    delta["GroupID"] = np.arange(1, len(delta) + 1)
    delta["BucketCode"] = [["SINGLE"]] * len(delta)
    delta["RiskValue"] = [[float(x)] for x in d["DeltaSens"]]
    delta["RWLabel"] = [[f"{b}_SPOT"] for b in bd]
    delta["RiskFactor"] = [f"{u}:SPOT" for u in ud]

    # ---- EQVEGA ----
    m = np.abs(g["VegaSens"].to_numpy()) > 1e-8
    v = g[m]
    bv, uv = buckets[m], und[m]
    W = vega_pillar_weights(v["T"].to_numpy())
    vals = W * v["VegaSens"].to_numpy()[:, None]
    vega = pd.DataFrame({
        "BusinessLine": BUSINESS_LINE, "Date": date_str,
        "DeskName": DESK_NAME, "FRTBBucket": bv.astype(int),
        "ParameterSet": PARAMETER_SET, "RiskClass": "EQUITY",
        "RiskFactorType": "SPOT", "RiskType": "EQVEGA",
        "RunRuleSet": RUN_RULE_SET,
        "TradeId": v["TradeId"].to_numpy(), "Underlying": uv,
    })
    vega["GroupID"] = np.arange(1, len(vega) + 1)
    vega["BucketCode"] = [PILLAR_LABELS] * len(vega)
    vega["RiskValue"] = [list(map(float, row)) for row in vals]
    vega["RWLabel"] = [[f"{b}_{p}_SPOT" for p in PILLAR_LABELS] for b in bv]
    vega["RiskFactor"] = uv

    # ---- EQGAMMA (curvature) ----
    opt = ~np.isin(g["TradeType"].to_numpy(), ["FORWARD", "VAR_SWAP"])
    m = opt & (np.abs(g["ShiftUpPnl"].to_numpy())
               + np.abs(g["ShiftDownPnl"].to_numpy()) > 1e-8)
    c = g[m]
    bc, uc = buckets[m], und[m]
    gamma = pd.DataFrame({
        "BusinessLine": BUSINESS_LINE, "Date": date_str,
        "CurvatureFlag": "Y", "DeskName": DESK_NAME,
        "FRTBBucket": bc.astype(int), "ParameterSet": PARAMETER_SET,
        "RiskClass": "EQUITY", "RiskFactorType": "SPOT",
        "RiskType": "EQGAMMA", "RunRuleSet": RUN_RULE_SET,
        "TradeId": c["TradeId"].to_numpy(), "Underlying": uc,
    })
    gamma["GroupID"] = np.arange(1, len(gamma) + 1)
    gamma["BucketCode"] = "SINGLE"
    gamma["RiskValue"] = (c["ShiftUpPnl"] + c["ShiftDownPnl"]).astype(float).to_numpy()  # convexity proxy
    gamma["SHIFTUPPNL"] = c["ShiftUpPnl"].to_numpy()
    gamma["SHIFTDOWNPNL"] = c["ShiftDownPnl"].to_numpy()
    gamma["CURVDELTA"] = (c["RW"] * c["DeltaSens"]).to_numpy()
    gamma["RWLabel"] = [f"{b}_SPOT" for b in bc]
    gamma["RiskFactor"] = uc
    return delta, vega, gamma


# ---------------------------------------------------------------------------
# 7. Main loop
# ---------------------------------------------------------------------------

def main():
    uni = build_universe()
    spots, pillar_vol = simulate_market(uni)
    dates64 = np.array([np.datetime64(d.date()) for d in DATES])
    d0 = dates64[0]

    # --- seasoned initial book: inception in the 2y before t0, alive at t0
    n_init = 10800
    book = gen_trades(uni, n_init, d0, spot_ref=uni["S0"].to_numpy(),
                      id_start=0, spot_jitter=0.12)
    assert (book["MaturityDate"] > d0).all()
    next_id = n_init

    # inception delta hedges for the initial book, booked as of t0
    hf, next_id = add_hedge_forwards(book, uni, spots[0], pillar_vol[0],
                                     d0, next_id)
    book = pd.concat([book, hf], ignore_index=True)

    summary = []
    all_trades = [book.copy()]
    for t, asof in enumerate(dates64):
        # ---- monthly new business (from month 1 onward) ----
        if t > 0:
            n_new = int(RNG.poisson(520))
            new = gen_trades(uni, n_new, np.full(n_new, asof),
                             spot_ref=spots[t], id_start=next_id)
            next_id += n_new
            hf, next_id = add_hedge_forwards(new, uni, spots[t],
                                             pillar_vol[t], asof, next_id)
            new = pd.concat([new, hf], ignore_index=True)
            all_trades.append(new)
            book = pd.concat([book, new], ignore_index=True)

        # ---- lifecycle: expiries and barrier knockouts ----
        expired = book["MaturityDate"] <= asof
        S_now = spots[t][book["UIdx"].to_numpy()]
        ko = (((book["TradeType"] == "BARRIER_UO_CALL")
               & (S_now >= book["Barrier"].to_numpy()))
              | ((book["TradeType"] == "BARRIER_DO_PUT")
                 & (S_now <= book["Barrier"].to_numpy())))
        n_exp, n_ko = int(expired.sum()), int((ko & ~expired).sum())
        book = book[~(expired | ko)].reset_index(drop=True)

        # ---- sensitivities and outputs ----
        g = compute_greeks(book, uni, spots[t], pillar_vol[t], asof)
        date_str = pd.Timestamp(asof).strftime("%Y-%m-%d")
        delta, vega, gamma = build_outputs(g, uni, date_str)
        write_file(delta, f"EQUITY_EQDELTA_{date_str}")
        write_file(vega, f"EQUITY_EQVEGA_{date_str}")
        write_file(gamma, f"EQUITY_EQGAMMA_{date_str}")

        summary.append(dict(
            Date=date_str, LiveTrades=len(book), Expired=n_exp,
            KnockedOut=n_ko,
            NetDelta=float(g["DeltaSens"].sum()),
            GrossDelta=float(g["DeltaSens"].abs().sum()),
            NetVega=float(g["VegaSens"].sum()),
            GrossVega=float(g["VegaSens"].abs().sum()),
            DeltaRows=len(delta), VegaRows=len(vega), GammaRows=len(gamma)))

    # ---- reference extras: trade store + market data ----
    trades_all = pd.concat(all_trades, ignore_index=True)
    trades_all["InceptionDate"] = trades_all["InceptionDate"].astype(str)
    trades_all["MaturityDate"] = trades_all["MaturityDate"].astype(str)
    write_file(trades_all.drop(columns=["Alive"]), "REF_TRADES")
    md = []
    for t, asof in enumerate(dates64):
        for i, u in enumerate(uni["Underlying"]):
            md.append(dict(Date=pd.Timestamp(asof).strftime("%Y-%m-%d"),
                           Underlying=u, Sector=uni["Sector"].iloc[i],
                           Spot=float(spots[t, i]),
                           **{f"Vol_{lab}": float(pillar_vol[t, i, j])
                              for j, lab in enumerate(PILLAR_LABELS)}))
    write_file(pd.DataFrame(md), "REF_MARKET_DATA")
    write_file(uni, "REF_UNIVERSE")

    s = pd.DataFrame(summary)
    write_file(s, "REF_RUN_SUMMARY")
    pd.set_option("display.width", 200)
    print(s.to_string(index=False))
    print(f"\nOutput format: {'parquet' if HAVE_PARQUET else 'csv.gz'}"
          f" -> {os.path.abspath(OUT_DIR)}")


if __name__ == "__main__":
    main()
