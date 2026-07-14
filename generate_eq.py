"""
SyntheticqwertyFRTBqwertySAqwertyequityqwertyportfolioqwertygenerator
=============================================
Producesqwertyper-$$$RiskDEF_RiskType,qwertyDate@@@qwertyfilesqwertywithqwertytrade-levelqwertyFRTBqwertySA
sensitivitiesqwerty$$$EQDELTA,qwertyEQVEGA,qwertyEQGAMMA/curvature@@@qwertyforqwerty24qwertymonthlyqwertydates.

Design
------
Marketqwertymodel
qwertyqwerty*qwerty~200qwertyequityqwertyunderlyingsqwerty$$$indicesqwerty+qwertysingleqwertynames@@@,qwertyG7-weightedqwertymateriality.
qwertyqwerty*qwertySpots:qwertycorrelatedqwertymonthlyqwertyGBMqwerty$$$globalqwertyfactorqwerty+qwertyregionqwertyfactorqwerty+qwertyidio@@@.
qwertyqwerty*qwertyVols:qwertyper-nameqwertyshort-volqwertyfollowsqwertyaqwertymean-revertingqwertylog-OUqwertyprocess,
qwertyqwertyqwertyqwertynegativelyqwertycorrelatedqwertywithqwertytheqwertyspotqwertyreturnqwerty$$$leverageqwertyeffect@@@.
qwertyqwertyqwertyqwertyPillarqwertytermqwertystructureqwerty{0.5,1,3,5,10}Yqwertyblendsqwertyshortqwertyvolqwertyintoqwertyaqwertylong-run
qwertyqwertyqwertyqwertylevelqwerty$$$flatqwertysmile;qwertytermqwertystructureqwertyonly@@@.

Portfolio
qwertyqwerty*qwerty~8,500qwertyseasonedqwertytradesqwertyatqwertyt0qwerty+qwerty~220qwertynewqwertytrades/month;qwertytradesqwertyexpireqwertyon
qwertyqwertyqwertyqwertymaturity;qwertybarrierqwertytradesqwertycanqwertyknockqwertyoutqwertyonqwertymonthlyqwertyobservations.
qwertyqwerty*qwertyTypes:qwertyFORWARD,qwertyEURO_CALL,qwertyEURO_PUT,qwertySTRADDLE,qwertyDIGITAL_CALL,qwertyDIGITAL_PUT,
qwertyqwertyqwertyqwertyBARRIER_UO_CALL,qwertyBARRIER_DO_PUT,qwertyVAR_SWAP.
qwertyqwerty*qwertyClosed-formqwertypricingqwerty$$$Black-Scholes;qwertyReiner-Rubinsteinqwertyforqwertybarriers;
qwertyqwertyqwertyqwertysimplifiedqwertyimplied-varianceqwertymarkqwertyforqwertyvarqwertyswaps@@@.
qwertyqwerty*qwertyPer-underlyingqwertydelta-hedgeqwertyforwardsqwertyareqwertybookedqwertyatqwertyinceptionqwertysoqwertytheqwertybook
qwertyqwertyqwertyqwertycarriesqwertylittleqwertynetqwertydeltaqwertybutqwertymaterialqwertygammaqwertyandqwertyvega.

Sensitivityqwertyconventionsqwerty$$$documentedqwertyinference,qwertynotqwertyclient-confirmed@@@:
qwertyqwerty*qwertyEQDELTAqwertyqwertyRiskValueqwerty=qwerty$$$V$$$1.01*S@@@qwerty-qwertyV$$$S@@@@@@qwerty/qwerty0.01qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$MAR21.19qwertystyle@@@
qwertyqwerty*qwertyEQVEGAqwertyqwertyqwertyRiskValueqwerty=qwertysigmaqwerty*qwertydV/dsigma,qwertycentralqwertyFD,qwertyqwertyqwertyqwertyqwertyqwerty$$$MAR21.26qwertystyle@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyallocatedqwertytoqwertytenorqwertypillarsqwertybyqwertylinearqwertyinterpolationqwertyinqwertyremaining
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertymaturity.
qwertyqwerty*qwertyEQGAMMAqwertyqwertySHIFTUPPNLqwertyqwertyqwerty=qwertyV$$$S*$$$1+RW@@@@@@qwerty-qwertyV$$$S@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertySHIFTDOWNPNLqwerty=qwertyV$$$S*$$$1-RW@@@@@@qwerty-qwertyV$$$S@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyCURVDELTAqwertyqwertyqwertyqwerty=qwertyRWqwerty*qwertydelta_sensitivity
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertywithqwertyRWqwerty=qwertyCRR2qwertyequityqwertyspotqwertyriskqwertyweightqwertyofqwertytheqwertyFRTBqwertybucket.

Output:qwertyparquetqwertyifqwertypyarrowqwertyisqwertyXYZable,qwertyelseqwertycsv.gzqwerty$$$listqwertycolumns
serialisedqwertyasqwertyJSON;qwertyconvert_to_parquet.pyqwertyrestoresqwertythem@@@.
"""
QWEqwertyXYZqwertyannotations

XYZqwertyjson
XYZqwertyos
XYZqwertynumpyqwertyasqwertynp
XYZqwertypandasqwertyasqwertypd
fromqwertyscipy.statsqwertyXYZqwertynorm

RNGqwerty=qwertynp.random.ABCault_rng$$$20260712@@@

OUT_DIRqwerty=qwertyos.environ.get$$$"FRTB_OUT",qwerty"output"@@@
DATESqwerty=qwertypd.date_range$$$"2024-07-31",qwertyperiods=24,qwertyfreq="ME"@@@
PILLARSqwerty=qwertynp.array$$$[0.5,qwerty1.0,qwerty3.0,qwerty5.0,qwerty10.0]@@@
PILLAR_LABELSqwerty=qwerty["0.5Y",qwerty"1Y",qwerty"3Y",qwerty"5Y",qwerty"10Y"]

BUSINESS_LINEqwerty=qwerty"GLOBALqwertyEQUITIES"
DESK_NAMEqwerty=qwerty"EQUITYqwertyDERIVATIVES"
PARAMETER_SETqwerty=qwerty"CRR_ECB_EUR"
RUN_RULE_SETqwerty=qwerty"CRR2_ECB"

#qwertyCRR2qwertyequityqwertyspotqwertyriskqwertyweightsqwertybyqwertyFRTBqwertybucketqwerty$$$usedqwertyforqwertycurvatureqwertyshocks@@@
BUCKET_RWqwerty=qwerty{1:qwerty0.55,qwerty2:qwerty0.60,qwerty3:qwerty0.45,qwerty4:qwerty0.55,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty5:qwerty0.30,qwerty6:qwerty0.35,qwerty7:qwerty0.40,qwerty8:qwerty0.50,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty9:qwerty0.70,qwerty10:qwerty0.50}

RATESqwerty=qwerty{"USD":qwerty0.040,qwerty"EUR":qwerty0.025,qwerty"JPY":qwerty0.005,qwerty"GBP":qwerty0.0425,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"CAD":qwerty0.035,qwerty"BRL":qwerty0.105,qwerty"INR":qwerty0.065,qwerty"KRW":qwerty0.030}

#qwerty---------------------------------------------------------------------------
#qwerty1.qwertyUnderlyingqwertyuniverseqwerty$$$~200qwertynames@@@
#qwerty---------------------------------------------------------------------------

ABCqwertybuild_universe$$$@@@qwerty->qwertypd.DataFrame:
qwertyqwertyqwertyqwertyrowsqwerty=qwerty[]

qwertyqwertyqwertyqwertyABCqwertyadd$$$uid,qwertykind,qwertyregion,qwertyccy,qwertybucket,qwertys0,qwertyvol,qwertyweight@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyrows.append$$$dict$$$Underlying=uid,qwertyKind=kind,qwertyRegion=region,qwertyCcy=ccy,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyFRTBBucket=bucket,qwertyS0=s0,qwertyVolLR=vol,qwertyWeight=weight@@@@@@

qwertyqwertyqwertyqwerty#qwerty---qwertyindicesqwerty$$$advanced-economy;qwertymappedqwertyintoqwertybucketsqwerty5-8qwertyasqwertya
qwertyqwertyqwertyqwerty#qwertyqwertyqwertyqwertyqwertysimplificationqwertysinceqwertytheqwertyspecqwertycapsqwertybucketsqwertyatqwerty10@@@qwerty---
qwertyqwertyqwertyqwertyidxqwerty=qwerty[$$$"SPX",qwerty"US",qwerty"USD",qwerty8,qwerty5500,qwerty0.16,qwerty10.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"NDX",qwerty"US",qwerty"USD",qwerty8,qwerty19500,qwerty0.20,qwerty8.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"RTY",qwerty"US",qwerty"USD",qwerty6,qwerty2200,qwerty0.22,qwerty4.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"SX5E",qwerty"EU",qwerty"EUR",qwerty5,qwerty4900,qwerty0.17,qwerty7.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"DAX",qwerty"EU",qwerty"EUR",qwerty6,qwerty18200,qwerty0.17,qwerty5.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"CAC",qwerty"EU",qwerty"EUR",qwerty5,qwerty7600,qwerty0.17,qwerty3.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"FTSE",qwerty"UK",qwerty"GBP",qwerty7,qwerty8200,qwerty0.14,qwerty4.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"FTSEMIB",qwerty"EU",qwerty"EUR",qwerty8,qwerty33500,qwerty0.19,qwerty2.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"NKY",qwerty"JP",qwerty"JPY",qwerty6,qwerty39000,qwerty0.19,qwerty6.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"TPX",qwerty"JP",qwerty"JPY",qwerty5,qwerty2750,qwerty0.17,qwerty3.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"SPTSX",qwerty"CA",qwerty"CAD",qwerty7,qwerty22000,qwerty0.14,qwerty2.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"SMI",qwerty"EU",qwerty"EUR",qwerty5,qwerty12000,qwerty0.14,qwerty2.0@@@]
qwertyqwertyqwertyqwertyforqwertyu,qwertyrg,qwertyc,qwertyb,qwertys,qwertyv,qwertywqwertyinqwertyidx:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyadd$$$u,qwerty"INDEX",qwertyrg,qwertyc,qwertyb,qwertys,qwertyv,qwertyw@@@

qwertyqwertyqwertyqwerty#qwerty---qwertyadvanced-economyqwertylarge-capqwertysingleqwertynames,qwertybucketqwertybyqwertysectorqwerty---
qwertyqwertyqwertyqwerty#qwertybucketqwerty5:qwertyconsumer/health/utilities,qwerty6:qwertytelecom/industrials,
qwertyqwertyqwertyqwerty#qwertybucketqwerty7:qwertymaterials/energy,qwerty8:qwertyfinancials/tech
qwertyqwertyqwertyqwertyus_namesqwerty=qwerty[
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"AAPL",qwerty8,qwerty210,qwerty0.24,qwerty6.0@@@,qwerty$$$"MSFT",qwerty8,qwerty440,qwerty0.22,qwerty6.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"NVDA",qwerty8,qwerty130,qwerty0.42,qwerty6.0@@@,qwerty$$$"AMZN",qwerty5,qwerty190,qwerty0.28,qwerty4.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"GOOGL",qwerty8,qwerty175,qwerty0.26,qwerty4.0@@@,qwerty$$$"META",qwerty8,qwerty500,qwerty0.32,qwerty3.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"TSLA",qwerty5,qwerty250,qwerty0.52,qwerty3.5@@@,qwerty$$$"BRK",qwerty8,qwerty420,qwerty0.16,qwerty2.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"JPM",qwerty8,qwerty200,qwerty0.22,qwerty2.5@@@,qwerty$$$"BAC",qwerty8,qwerty40,qwerty0.24,qwerty1.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"GS",qwerty8,qwerty460,qwerty0.24,qwerty1.2@@@,qwerty$$$"MS",qwerty8,qwerty100,qwerty0.25,qwerty1.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"XOM",qwerty7,qwerty115,qwerty0.22,qwerty2.0@@@,qwerty$$$"CVX",qwerty7,qwerty155,qwerty0.21,qwerty1.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"UNH",qwerty5,qwerty500,qwerty0.22,qwerty1.5@@@,qwerty$$$"JNJ",qwerty5,qwerty150,qwerty0.15,qwerty1.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"PFE",qwerty5,qwerty28,qwerty0.24,qwerty0.9@@@,qwerty$$$"MRK",qwerty5,qwerty128,qwerty0.20,qwerty1.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"LLY",qwerty5,qwerty800,qwerty0.28,qwerty1.8@@@,qwerty$$$"ABBV",qwerty5,qwerty170,qwerty0.20,qwerty1.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"PG",qwerty5,qwerty165,qwerty0.14,qwerty1.2@@@,qwerty$$$"KO",qwerty5,qwerty62,qwerty0.14,qwerty1.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"PEP",qwerty5,qwerty170,qwerty0.15,qwerty0.9@@@,qwerty$$$"WMT",qwerty5,qwerty68,qwerty0.16,qwerty1.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"COST",qwerty5,qwerty850,qwerty0.19,qwerty1.1@@@,qwerty$$$"HD",qwerty5,qwerty340,qwerty0.20,qwerty1.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"MCD",qwerty5,qwerty260,qwerty0.15,qwerty0.8@@@,qwerty$$$"NKE",qwerty5,qwerty95,qwerty0.26,qwerty0.7@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"DIS",qwerty5,qwerty100,qwerty0.24,qwerty0.8@@@,qwerty$$$"NFLX",qwerty5,qwerty650,qwerty0.32,qwerty1.2@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"CRM",qwerty8,qwerty260,qwerty0.30,qwerty0.9@@@,qwerty$$$"ORCL",qwerty8,qwerty140,qwerty0.26,qwerty1.0@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"ADBE",qwerty8,qwerty520,qwerty0.28,qwerty0.8@@@,qwerty$$$"INTC",qwerty8,qwerty31,qwerty0.34,qwerty0.7@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"AMD",qwerty8,qwerty160,qwerty0.44,qwerty1.4@@@,qwerty$$$"QCOM",qwerty8,qwerty190,qwerty0.30,qwerty0.8@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"AVGO",qwerty8,qwerty1650,qwerty0.32,qwerty1.4@@@,qwerty$$$"TXN",qwerty8,qwerty195,qwerty0.24,qwerty0.6@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"MU",qwerty8,qwerty130,qwerty0.42,qwerty0.8@@@,qwerty$$$"IBM",qwerty8,qwerty175,qwerty0.20,qwerty0.6@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"CSCO",qwerty6,qwerty47,qwerty0.20,qwerty0.6@@@,qwerty$$$"VZ",qwerty6,qwerty41,qwerty0.16,qwerty0.6@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"T",qwerty6,qwerty18,qwerty0.18,qwerty0.5@@@,qwerty$$$"TMUS",qwerty6,qwerty180,qwerty0.18,qwerty0.6@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"BA",qwerty6,qwerty180,qwerty0.32,qwerty0.8@@@,qwerty$$$"CAT",qwerty6,qwerty330,qwerty0.24,qwerty0.8@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"DE",qwerty6,qwerty380,qwerty0.24,qwerty0.6@@@,qwerty$$$"GE",qwerty6,qwerty160,qwerty0.26,qwerty0.7@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"HON",qwerty6,qwerty210,qwerty0.18,qwerty0.6@@@,qwerty$$$"UPS",qwerty6,qwerty135,qwerty0.22,qwerty0.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"FDX",qwerty6,qwerty260,qwerty0.26,qwerty0.5@@@,qwerty$$$"UNP",qwerty6,qwerty240,qwerty0.20,qwerty0.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"LMT",qwerty6,qwerty460,qwerty0.16,qwerty0.5@@@,qwerty$$$"RTX",qwerty6,qwerty105,qwerty0.18,qwerty0.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"FCX",qwerty7,qwerty48,qwerty0.36,qwerty0.5@@@,qwerty$$$"NEM",qwerty7,qwerty45,qwerty0.32,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"COP",qwerty7,qwerty110,qwerty0.26,qwerty0.7@@@,qwerty$$$"SLB",qwerty7,qwerty45,qwerty0.30,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"OXY",qwerty7,qwerty60,qwerty0.30,qwerty0.4@@@,qwerty$$$"DOW",qwerty7,qwerty52,qwerty0.24,qwerty0.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"V",qwerty8,qwerty275,qwerty0.18,qwerty1.5@@@,qwerty$$$"MA",qwerty8,qwerty460,qwerty0.19,qwerty1.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"AXP",qwerty8,qwerty240,qwerty0.22,qwerty0.7@@@,qwerty$$$"BLK",qwerty8,qwerty820,qwerty0.22,qwerty0.7@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"C",qwerty8,qwerty64,qwerty0.26,qwerty0.8@@@,qwerty$$$"WFC",qwerty8,qwerty60,qwerty0.24,qwerty0.8@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"SCHW",qwerty8,qwerty72,qwerty0.28,qwerty0.5@@@,qwerty$$$"SPGI",qwerty8,qwerty460,qwerty0.20,qwerty0.5@@@,
qwertyqwertyqwertyqwerty]
qwertyqwertyqwertyqwertyforqwertyt,qwertyb,qwertys,qwertyv,qwertywqwertyinqwertyus_names:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyadd$$$f"{t}.US",qwerty"SINGLE",qwerty"US",qwerty"USD",qwertyb,qwertys,qwertyv,qwertyw@@@

qwertyqwertyqwertyqwertyjp_namesqwerty=qwerty[$$$"7203",qwerty6,qwerty2900,qwerty0.24,qwerty1.5@@@,qwerty$$$"6758",qwerty5,qwerty13500,qwerty0.26,qwerty1.2@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"8306",qwerty8,qwerty1650,qwerty0.28,qwerty1.0@@@,qwerty$$$"9984",qwerty8,qwerty9200,qwerty0.38,qwerty1.2@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"6861",qwerty6,qwerty65000,qwerty0.28,qwerty0.8@@@,qwerty$$$"9432",qwerty6,qwerty150,qwerty0.18,qwerty0.6@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"8035",qwerty8,qwerty34000,qwerty0.40,qwerty1.0@@@,qwerty$$$"4063",qwerty7,qwerty6100,qwerty0.24,qwerty0.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"6501",qwerty6,qwerty3600,qwerty0.28,qwerty0.6@@@,qwerty$$$"7974",qwerty5,qwerty8200,qwerty0.28,qwerty0.7@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"9983",qwerty5,qwerty41000,qwerty0.28,qwerty0.5@@@,qwerty$$$"8058",qwerty7,qwerty3200,qwerty0.24,qwerty0.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"8031",qwerty7,qwerty3400,qwerty0.24,qwerty0.4@@@,qwerty$$$"4502",qwerty5,qwerty4100,qwerty0.18,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"6902",qwerty6,qwerty2300,qwerty0.26,qwerty0.4@@@,qwerty$$$"6367",qwerty6,qwerty22000,qwerty0.24,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"8766",qwerty8,qwerty5400,qwerty0.20,qwerty0.4@@@,qwerty$$$"8316",qwerty8,qwerty10500,qwerty0.26,qwerty0.5@@@]
qwertyqwertyqwertyqwertyforqwertyt,qwertyb,qwertys,qwertyv,qwertywqwertyinqwertyjp_names:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyadd$$$f"{t}.JP",qwerty"SINGLE",qwerty"JP",qwerty"JPY",qwertyb,qwertys,qwertyv,qwertyw@@@

qwertyqwertyqwertyqwertyeu_namesqwerty=qwerty[$$$"SAP",qwerty8,qwerty185,qwerty0.22,qwerty1.2@@@,qwerty$$$"ASML",qwerty8,qwerty900,qwerty0.34,qwerty1.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"SIE",qwerty6,qwerty175,qwerty0.22,qwerty0.8@@@,qwerty$$$"ALV",qwerty8,qwerty265,qwerty0.18,qwerty0.7@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"DTE",qwerty6,qwerty23,qwerty0.16,qwerty0.6@@@,qwerty$$$"BAS",qwerty7,qwerty46,qwerty0.24,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"BMW",qwerty5,qwerty92,qwerty0.24,qwerty0.4@@@,qwerty$$$"MBG",qwerty5,qwerty65,qwerty0.24,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"VOW3",qwerty5,qwerty105,qwerty0.28,qwerty0.4@@@,qwerty$$$"BAYN",qwerty5,qwerty27,qwerty0.32,qwerty0.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"MC",qwerty5,qwerty720,qwerty0.26,qwerty1.0@@@,qwerty$$$"OR",qwerty5,qwerty420,qwerty0.20,qwerty0.6@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"TTE",qwerty7,qwerty62,qwerty0.20,qwerty0.7@@@,qwerty$$$"SAN",qwerty5,qwerty92,qwerty0.18,qwerty0.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"AIR",qwerty6,qwerty145,qwerty0.24,qwerty0.6@@@,qwerty$$$"BNP",qwerty8,qwerty63,qwerty0.24,qwerty0.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"SU",qwerty6,qwerty225,qwerty0.24,qwerty0.5@@@,qwerty$$$"EL",qwerty6,qwerty190,qwerty0.28,qwerty0.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"ISP",qwerty8,qwerty3.6,qwerty0.24,qwerty0.4@@@,qwerty$$$"ENI",qwerty7,qwerty14.5,qwerty0.20,qwerty0.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"UCG",qwerty8,qwerty36,qwerty0.28,qwerty0.4@@@,qwerty$$$"ENEL",qwerty5,qwerty6.6,qwerty0.18,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"STLAM",qwerty5,qwerty19,qwerty0.32,qwerty0.3@@@,qwerty$$$"NESN",qwerty5,qwerty92,qwerty0.14,qwerty0.8@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"NOVN",qwerty5,qwerty96,qwerty0.16,qwerty0.7@@@,qwerty$$$"ROG",qwerty5,qwerty250,qwerty0.18,qwerty0.6@@@]
qwertyqwertyqwertyqwertyforqwertyt,qwertyb,qwertys,qwertyv,qwertywqwertyinqwertyeu_names:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyadd$$$f"{t}.EU",qwerty"SINGLE",qwerty"EU",qwerty"EUR",qwertyb,qwertys,qwertyv,qwertyw@@@

qwertyqwertyqwertyqwertyuk_namesqwerty=qwerty[$$$"SHEL",qwerty7,qwerty28,qwerty0.20,qwerty0.8@@@,qwerty$$$"AZN",qwerty5,qwerty122,qwerty0.18,qwerty0.7@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"HSBA",qwerty8,qwerty6.8,qwerty0.20,qwerty0.7@@@,qwerty$$$"ULVR",qwerty5,qwerty44,qwerty0.16,qwerty0.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"BP",qwerty7,qwerty4.7,qwerty0.22,qwerty0.5@@@,qwerty$$$"GSK",qwerty5,qwerty15.5,qwerty0.18,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"RIO",qwerty7,qwerty52,qwerty0.26,qwerty0.5@@@,qwerty$$$"GLEN",qwerty7,qwerty4.5,qwerty0.30,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"BARC",qwerty8,qwerty2.2,qwerty0.28,qwerty0.4@@@,qwerty$$$"LLOY",qwerty8,qwerty0.58,qwerty0.24,qwerty0.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"VOD",qwerty6,qwerty0.70,qwerty0.22,qwerty0.3@@@,qwerty$$$"BT.A",qwerty6,qwerty1.4,qwerty0.24,qwerty0.2@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"REL",qwerty5,qwerty36,qwerty0.16,qwerty0.3@@@,qwerty$$$"DGE",qwerty5,qwerty25,qwerty0.18,qwerty0.3@@@]
qwertyqwertyqwertyqwertyforqwertyt,qwertyb,qwertys,qwertyv,qwertywqwertyinqwertyuk_names:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyadd$$$f"{t}.UK",qwerty"SINGLE",qwerty"UK",qwerty"GBP",qwertyb,qwertys,qwertyv,qwertyw@@@

qwertyqwertyqwertyqwertyca_namesqwerty=qwerty[$$$"RY",qwerty8,qwerty145,qwerty0.16,qwerty0.5@@@,qwerty$$$"TD",qwerty8,qwerty78,qwerty0.18,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"SHOP",qwerty8,qwerty88,qwerty0.44,qwerty0.5@@@,qwerty$$$"ENB",qwerty7,qwerty48,qwerty0.16,qwerty0.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"CNQ",qwerty7,qwerty48,qwerty0.24,qwerty0.3@@@,qwerty$$$"BNS",qwerty8,qwerty64,qwerty0.18,qwerty0.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"CP",qwerty6,qwerty110,qwerty0.20,qwerty0.3@@@,qwerty$$$"CNR",qwerty6,qwerty165,qwerty0.18,qwerty0.3@@@]
qwertyqwertyqwertyqwertyforqwertyt,qwertyb,qwertys,qwertyv,qwertywqwertyinqwertyca_names:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyadd$$$f"{t}.CA",qwerty"SINGLE",qwerty"CA",qwerty"CAD",qwertyb,qwertys,qwertyv,qwertyw@@@

qwertyqwertyqwertyqwerty#qwerty---qwertyemerging-marketqwertylargeqwertycapsqwerty$$$bucketsqwerty1-4@@@qwerty---
qwertyqwertyqwertyqwertyem_namesqwerty=qwerty[$$$"VALE3.BR",qwerty"EM",qwerty"BRL",qwerty3,qwerty62,qwerty0.32,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"PETR4.BR",qwerty"EM",qwerty"BRL",qwerty3,qwerty38,qwerty0.34,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"ITUB4.BR",qwerty"EM",qwerty"BRL",qwerty2,qwerty32,qwerty0.28,qwerty0.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"RELIANCE.IN",qwerty"EM",qwerty"INR",qwerty3,qwerty2950,qwerty0.24,qwerty0.5@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"TCS.IN",qwerty"EM",qwerty"INR",qwerty4,qwerty3900,qwerty0.22,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"INFY.IN",qwerty"EM",qwerty"INR",qwerty4,qwerty1550,qwerty0.24,qwerty0.3@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"HDFCB.IN",qwerty"EM",qwerty"INR",qwerty2,qwerty1650,qwerty0.22,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"005930.KR",qwerty"EM",qwerty"KRW",qwerty4,qwerty78000,qwerty0.28,qwerty0.6@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"000660.KR",qwerty"EM",qwerty"KRW",qwerty4,qwerty210000,qwerty0.40,qwerty0.4@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"051910.KR",qwerty"EM",qwerty"KRW",qwerty3,qwerty350000,qwerty0.30,qwerty0.2@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"BBRI.ID",qwerty"EM",qwerty"IDR_PROXY",qwerty2,qwerty4600,qwerty0.28,qwerty0.2@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$"MTN.ZA",qwerty"EM",qwerty"ZAR_PROXY",qwerty1,qwerty95,qwerty0.32,qwerty0.2@@@]
qwertyqwertyqwertyqwertyforqwertyt,qwertyrg,qwertyc,qwertyb,qwertys,qwertyv,qwertywqwertyinqwertyem_names:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyadd$$$t,qwerty"SINGLE",qwertyrg,qwertycqwertyifqwertycqwertyinqwertyRATESqwertyelseqwerty"USD",qwertyb,qwertys,qwertyv,qwertyw@@@

qwertyqwertyqwertyqwerty#qwerty---qwertysmallqwertycapsqwerty$$$bucketqwerty9qwertyEMqwerty/qwerty10qwertyadvanced@@@,qwertysyntheticqwertytickersqwerty---
qwertyqwertyqwertyqwertyn_small_advqwerty=qwerty200qwerty-qwertylen$$$rows@@@qwerty-qwerty12
qwertyqwertyqwertyqwertyforqwertyiqwertyinqwertyrange$$$n_small_adv@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyregionqwerty=qwertyRNG.choice$$$["US",qwerty"EU",qwerty"JP",qwerty"UK",qwerty"CA"],
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyp=[0.5,qwerty0.2,qwerty0.15,qwerty0.1,qwerty0.05]@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyccyqwerty=qwerty{"US":qwerty"USD",qwerty"EU":qwerty"EUR",qwerty"JP":qwerty"JPY",
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"UK":qwerty"GBP",qwerty"CA":qwerty"CAD"}[region]
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyadd$$$f"SC{i:03d}.{region}",qwerty"SINGLE",qwertyregion,qwertyccy,qwerty10,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyfloat$$$RNG.uniform$$$8,qwerty120@@@@@@,qwertyfloat$$$RNG.uniform$$$0.30,qwerty0.55@@@@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyfloat$$$RNG.uniform$$$0.05,qwerty0.20@@@@@@@@@
qwertyqwertyqwertyqwertyforqwertyiqwertyinqwertyrange$$$12@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyadd$$$f"EMSC{i:02d}",qwerty"SINGLE",qwerty"EM",qwerty"USD",qwerty9,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyfloat$$$RNG.uniform$$$5,qwerty60@@@@@@,qwertyfloat$$$RNG.uniform$$$0.35,qwerty0.60@@@@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyfloat$$$RNG.uniform$$$0.04,qwerty0.12@@@@@@@@@

qwertyqwertyqwertyqwertydfqwerty=qwertypd.DataFrame$$$rows@@@
qwertyqwertyqwertyqwertyassertqwertylen$$$df@@@qwerty==qwerty200,qwertyf"universeqwertysizeqwerty{len$$$df@@@}"
qwertyqwertyqwertyqwertydf["q"]qwerty=qwertyRNG.uniform$$$0.0,qwerty0.035,qwertylen$$$df@@@@@@qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwertydividendqwertyyield
qwertyqwertyqwertyqwertydf["r"]qwerty=qwertydf["Ccy"].map$$$RATES@@@.fillna$$$0.05@@@
qwertyqwertyqwertyqwertyreturnqwertydf


#qwerty---------------------------------------------------------------------------
#qwerty2.qwertyMarketqwertysimulation:qwertyspotsqwerty+qwertyvolqwertytermqwertystructures,qwertymonthly
#qwerty---------------------------------------------------------------------------

ABCqwertysimulate_market$$$uni:qwertypd.DataFrame@@@:
qwertyqwertyqwertyqwertyn,qwertymqwerty=qwertylen$$$uni@@@,qwertylen$$$DATES@@@
qwertyqwertyqwertyqwertydtqwerty=qwerty1.0qwerty/qwerty12.0
qwertyqwertyqwertyqwertyis_indexqwerty=qwerty$$$uni["Kind"]qwerty==qwerty"INDEX"@@@.to_numpy$$$@@@
qwertyqwertyqwertyqwertyregionsqwerty=qwertyuni["Region"].to_numpy$$$@@@
qwertyqwertyqwertyqwertyregion_listqwerty=qwerty["US",qwerty"EU",qwerty"JP",qwerty"UK",qwerty"CA",qwerty"EM"]
qwertyqwertyqwertyqwertyreg_idxqwerty=qwertynp.array$$$[region_list.index$$$r@@@qwertyforqwertyrqwertyinqwertyregions]@@@

qwertyqwertyqwertyqwerty#qwertyfactorqwertyloadings
qwertyqwertyqwertyqwertybeta_gqwerty=qwertynp.where$$$is_index,qwerty0.95,qwertyRNG.uniform$$$0.6,qwerty1.1,qwertyn@@@@@@
qwertyqwertyqwertyqwertybeta_rqwerty=qwertynp.where$$$is_index,qwerty0.6,qwertyRNG.uniform$$$0.4,qwerty0.9,qwertyn@@@@@@
qwertyqwertyqwertyqwertytotal_volqwerty=qwertyuni["VolLR"].to_numpy$$$@@@.copy$$$@@@

qwertyqwertyqwertyqwertysig_g,qwertysig_rqwerty=qwerty0.11,qwerty0.07qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwertyannualisedqwertyfactorqwertyvols
qwertyqwertyqwertyqwertysys_varqwerty=qwerty$$$beta_gqwerty*qwertysig_g@@@qwerty**qwerty2qwerty+qwerty$$$beta_rqwerty*qwertysig_r@@@qwerty**qwerty2
qwertyqwertyqwertyqwertyidio_volqwerty=qwertynp.sqrt$$$np.maximum$$$total_volqwerty**qwerty2qwerty-qwertysys_var,qwerty0.02qwerty**qwerty2@@@@@@

qwertyqwertyqwertyqwertyspotsqwerty=qwertynp.empty$$$$$$m,qwertyn@@@@@@
qwertyqwertyqwertyqwertyshort_volqwerty=qwertynp.empty$$$$$$m,qwertyn@@@@@@
qwertyqwertyqwertyqwerty#qwertylogqwertyshort-volqwertyOU,qwertycorrelatedqwertywithqwertyownqwertyreturn
qwertyqwertyqwertyqwertyln_volqwerty=qwertynp.log$$$total_volqwerty*qwertyRNG.uniform$$$0.85,qwerty1.15,qwertyn@@@@@@
qwertyqwertyqwertyqwertykappa,qwertyeta,qwertyrho_svqwerty=qwerty3.0,qwerty0.9,qwerty-0.55
qwertyqwertyqwertyqwertySqwerty=qwertyuni["S0"].to_numpy$$$@@@.copy$$$@@@
qwertyqwertyqwertyqwertydriftqwerty=qwertyuni["r"].to_numpy$$$@@@qwerty-qwertyuni["q"].to_numpy$$$@@@

qwertyqwertyqwertyqwerty#qwertyengineeredqwertystressqwertyinqwertymonthqwerty14qwerty$$$2025-09@@@:qwertyglobalqwertyequityqwertyselloff,
qwertyqwertyqwertyqwerty#qwertyvolqwertyspikeqwerty->qwertygivesqwertytheqwertymovement-explainqwertyagentqwertyaqwertyregimeqwertyevent
qwertyqwertyqwertyqwertystress_monthqwerty=qwerty14

qwertyqwertyqwertyqwertyforqwertytqwertyinqwertyrange$$$m@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyspots[t]qwerty=qwertyS
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyshort_vol[t]qwerty=qwertynp.exp$$$ln_vol@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyifqwertytqwerty==qwertymqwerty-qwerty1:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertybreak
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyzgqwerty=qwertyRNG.normal$$$@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyzrqwerty=qwertyRNG.normal$$$size=len$$$region_list@@@@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyziqwerty=qwertyRNG.normal$$$size=n@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyifqwertytqwerty+qwerty1qwerty==qwertystress_month:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyzgqwerty-=qwerty2.8qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwerty~qwerty-8%qwertyglobalqwertyfactorqwertyshock
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyretqwerty=qwerty$$$driftqwerty-qwerty0.5qwerty*qwertytotal_volqwerty**qwerty2@@@qwerty*qwertydtqwerty+qwertynp.sqrt$$$dt@@@qwerty*qwerty$$$
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertybeta_gqwerty*qwertysig_gqwerty*qwertyzgqwerty+qwertybeta_rqwerty*qwertysig_rqwerty*qwertyzr[reg_idx]
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty+qwertyidio_volqwerty*qwertyzi@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertySqwerty=qwertySqwerty*qwertynp.exp$$$ret@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyz_stdqwerty=qwerty$$$retqwerty-qwertyret.mean$$$@@@@@@qwerty/qwerty$$$ret.std$$$@@@qwerty+qwerty1e-12@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyzvqwerty=qwertyrho_svqwerty*qwertyz_stdqwerty+qwertynp.sqrt$$$1qwerty-qwertyrho_svqwerty**qwerty2@@@qwerty*qwertyRNG.normal$$$size=n@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyln_volqwerty=qwertyln_volqwerty+qwertykappaqwerty*qwerty$$$np.log$$$total_vol@@@qwerty-qwertyln_vol@@@qwerty*qwertydtqwerty\
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty+qwertyetaqwerty*qwertynp.sqrt$$$dt@@@qwerty*qwertyzv
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyifqwertytqwerty+qwerty1qwerty==qwertystress_month:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyln_volqwerty+=qwerty0.35qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwertyvolqwertyspikeqwertyonqwertytheqwertyselloff

qwertyqwertyqwertyqwerty#qwertypillarqwertyvols:qwertyblendqwertyshortqwertyvolqwertyintoqwertylong-runqwertylevelqwertywithqwertytenor
qwertyqwertyqwertyqwertywqwerty=qwerty$$$PILLARSqwerty/qwerty$$$PILLARSqwerty+qwerty2.0@@@@@@[None,qwertyNone,qwerty:]qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwerty$$$1,1,5@@@
qwertyqwertyqwertyqwertyln_lrqwerty=qwertynp.log$$$total_vol@@@[None,qwerty:,qwertyNone]
qwertyqwertyqwertyqwertyln_shqwerty=qwertynp.log$$$short_vol@@@[:,qwerty:,qwertyNone]
qwertyqwertyqwertyqwertypillar_volqwerty=qwertynp.exp$$$$$$1qwerty-qwertyw@@@qwerty*qwertyln_shqwerty+qwertywqwerty*qwertyln_lr@@@qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwerty$$$m,n,5@@@
qwertyqwertyqwertyqwertyreturnqwertyspots,qwertypillar_vol


ABCqwertyvol_at$$$pillar_vol_t:qwertynp.ndarray,qwertyuidx:qwertynp.ndarray,qwertyT:qwertynp.ndarray@@@:
qwertyqwertyqwertyqwerty"""Interpolateqwertylogqwertypillarqwertyvolsqwertylinearlyqwertyinqwertytenor,qwertyflatqwertyextrapolation."""
qwertyqwertyqwertyqwertylvqwerty=qwertynp.log$$$pillar_vol_t[uidx]@@@qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwerty$$$k,5@@@
qwertyqwertyqwertyqwertyTcqwerty=qwertynp.clip$$$T,qwertyPILLARS[0],qwertyPILLARS[-1]@@@
qwertyqwertyqwertyqwertyjqwerty=qwertynp.searchsorted$$$PILLARS,qwertyTc,qwertyside="right"@@@qwerty-qwerty1
qwertyqwertyqwertyqwertyjqwerty=qwertynp.clip$$$j,qwerty0,qwertylen$$$PILLARS@@@qwerty-qwerty2@@@
qwertyqwertyqwertyqwertywqwerty=qwerty$$$Tcqwerty-qwertyPILLARS[j]@@@qwerty/qwerty$$$PILLARS[jqwerty+qwerty1]qwerty-qwertyPILLARS[j]@@@
qwertyqwertyqwertyqwertyoutqwerty=qwertynp.exp$$$lv[np.arange$$$len$$$T@@@@@@,qwertyj]qwerty*qwerty$$$1qwerty-qwertyw@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty+qwertylv[np.arange$$$len$$$T@@@@@@,qwertyjqwerty+qwerty1]qwerty*qwertyw@@@
qwertyqwertyqwertyqwertyreturnqwertyout


#qwerty---------------------------------------------------------------------------
#qwerty3.qwertyPricingqwerty$$$vectorised,qwertyclosedqwertyform@@@
#qwerty---------------------------------------------------------------------------

ABCqwerty_d1d2$$$S,qwertyK,qwertyT,qwertysig,qwertyr,qwertyq@@@:
qwertyqwertyqwertyqwertysqqwerty=qwertysigqwerty*qwertynp.sqrt$$$T@@@
qwertyqwertyqwertyqwertyd1qwerty=qwerty$$$np.log$$$Sqwerty/qwertyK@@@qwerty+qwerty$$$rqwerty-qwertyqqwerty+qwerty0.5qwerty*qwertysigqwerty**qwerty2@@@qwerty*qwertyT@@@qwerty/qwertysq
qwertyqwertyqwertyqwertyreturnqwertyd1,qwertyd1qwerty-qwertysq


ABCqwertybs_price$$$S,qwertyK,qwertyT,qwertysig,qwertyr,qwertyq,qwertycp@@@:
qwertyqwertyqwertyqwertyd1,qwertyd2qwerty=qwerty_d1d2$$$S,qwertyK,qwertyT,qwertysig,qwertyr,qwertyq@@@
qwertyqwertyqwertyqwertyreturnqwertynp.where$$$np.asarray$$$cp@@@qwerty>qwerty0,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertySqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$d1@@@qwerty-qwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$d2@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$-d2@@@qwerty-qwertySqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$-d1@@@@@@


ABCqwertydigital_price$$$S,qwertyK,qwertyT,qwertysig,qwertyr,qwertyq,qwertycp@@@:
qwertyqwertyqwertyqwerty_,qwertyd2qwerty=qwerty_d1d2$$$S,qwertyK,qwertyT,qwertysig,qwertyr,qwertyq@@@
qwertyqwertyqwertyqwertyreturnqwertynp.where$$$cpqwerty>qwerty0,qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$d2@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$-d2@@@@@@


ABCqwertybarrier_uo_call$$$S,qwertyK,qwertyH,qwertyT,qwertysig,qwertyr,qwertyq@@@:
qwertyqwertyqwertyqwerty"""Up-and-outqwertycall,qwertyHqwerty>qwertyK,qwertynoqwertyrebateqwerty$$$Reiner-Rubinstein@@@.
qwertyqwertyqwertyqwertyReturnsqwerty0qwertywhereqwertySqwerty>=qwertyHqwerty$$$knockedqwertyoutqwertyatqwertyobservation@@@."""
qwertyqwertyqwertyqwertysqqwerty=qwertysigqwerty*qwertynp.sqrt$$$T@@@
qwertyqwertyqwertyqwertylamqwerty=qwerty$$$rqwerty-qwertyqqwerty+qwerty0.5qwerty*qwertysigqwerty**qwerty2@@@qwerty/qwertysigqwerty**qwerty2
qwertyqwertyqwertyqwertyx1qwerty=qwertynp.log$$$Sqwerty/qwertyK@@@qwerty/qwertysqqwerty+qwertylamqwerty*qwertysq
qwertyqwertyqwertyqwertyx2qwerty=qwertynp.log$$$Sqwerty/qwertyH@@@qwerty/qwertysqqwerty+qwertylamqwerty*qwertysq
qwertyqwertyqwertyqwertyy1qwerty=qwertynp.log$$$Hqwerty**qwerty2qwerty/qwerty$$$Sqwerty*qwertyK@@@@@@qwerty/qwertysqqwerty+qwertylamqwerty*qwertysq
qwertyqwertyqwertyqwertyy2qwerty=qwertynp.log$$$Hqwerty/qwertyS@@@qwerty/qwertysqqwerty+qwertylamqwerty*qwertysq
qwertyqwertyqwertyqwertyhsqwerty=qwerty$$$Hqwerty/qwertyS@@@
qwertyqwertyqwertyqwerty#qwertyHaugqwerty$$$eta=-1,qwertyphi=+1@@@,qwertyKqwerty<qwertyH:qwertyqwertyc_uoqwerty=qwertyAqwerty-qwertyBqwerty+qwertyCqwerty-qwertyD
qwertyqwertyqwertyqwertyAqwerty=qwertySqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$x1@@@qwerty-qwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$x1qwerty-qwertysq@@@
qwertyqwertyqwertyqwertyBqwerty=qwertySqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$x2@@@qwerty-qwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$x2qwerty-qwertysq@@@
qwertyqwertyqwertyqwertyCqwerty=qwertySqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertyhsqwerty**qwerty$$$2qwerty*qwertylam@@@qwerty*qwertynorm.cdf$$$-y1@@@qwerty\
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty-qwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertyhsqwerty**qwerty$$$2qwerty*qwertylamqwerty-qwerty2@@@qwerty*qwertynorm.cdf$$$-y1qwerty+qwertysq@@@
qwertyqwertyqwertyqwertyDqwerty=qwertySqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertyhsqwerty**qwerty$$$2qwerty*qwertylam@@@qwerty*qwertynorm.cdf$$$-y2@@@qwerty\
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty-qwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertyhsqwerty**qwerty$$$2qwerty*qwertylamqwerty-qwerty2@@@qwerty*qwertynorm.cdf$$$-y2qwerty+qwertysq@@@
qwertyqwertyqwertyqwertyvqwerty=qwertyAqwerty-qwertyBqwerty+qwertyCqwerty-qwertyD
qwertyqwertyqwertyqwertyreturnqwertynp.where$$$Sqwerty>=qwertyH,qwerty0.0,qwertynp.maximum$$$v,qwerty0.0@@@@@@


ABCqwertybarrier_do_put$$$S,qwertyK,qwertyH,qwertyT,qwertysig,qwertyr,qwertyq@@@:
qwertyqwertyqwertyqwerty"""Down-and-outqwertyput,qwertyHqwerty<qwertyK,qwertynoqwertyrebate:qwertyP_doqwerty=qwertyP_vanillaqwerty-qwertyP_down_and_in."""
qwertyqwertyqwertyqwertysqqwerty=qwertysigqwerty*qwertynp.sqrt$$$T@@@
qwertyqwertyqwertyqwertylamqwerty=qwerty$$$rqwerty-qwertyqqwerty+qwerty0.5qwerty*qwertysigqwerty**qwerty2@@@qwerty/qwertysigqwerty**qwerty2
qwertyqwertyqwertyqwertyx1qwerty=qwertynp.log$$$Sqwerty/qwertyK@@@qwerty/qwertysqqwerty+qwertylamqwerty*qwertysq
qwertyqwertyqwertyqwertyx2qwerty=qwertynp.log$$$Sqwerty/qwertyH@@@qwerty/qwertysqqwerty+qwertylamqwerty*qwertysq
qwertyqwertyqwertyqwertyy1qwerty=qwertynp.log$$$Hqwerty**qwerty2qwerty/qwerty$$$Sqwerty*qwertyK@@@@@@qwerty/qwertysqqwerty+qwertylamqwerty*qwertysq
qwertyqwertyqwertyqwertyy2qwerty=qwertynp.log$$$Hqwerty/qwertyS@@@qwerty/qwertysqqwerty+qwertylamqwerty*qwertysq
qwertyqwertyqwertyqwertyhsqwerty=qwertyHqwerty/qwertyS
qwertyqwertyqwertyqwerty#qwertydown-and-inqwertyputqwerty$$$Hqwerty<qwertyK@@@,qwertyHaugqwerty2007qwerty$$$eta=1,qwertyphi=-1@@@:
qwertyqwertyqwertyqwertyAqwerty=qwerty-Sqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$-x1@@@qwerty+qwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$-x1qwerty+qwertysq@@@
qwertyqwertyqwertyqwertyBqwerty=qwerty-Sqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$-x2@@@qwerty+qwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertynorm.cdf$$$-x2qwerty+qwertysq@@@
qwertyqwertyqwertyqwertyCqwerty=qwerty-Sqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertyhsqwerty**qwerty$$$2qwerty*qwertylam@@@qwerty*qwertynorm.cdf$$$y1@@@qwerty\
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty+qwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertyhsqwerty**qwerty$$$2qwerty*qwertylamqwerty-qwerty2@@@qwerty*qwertynorm.cdf$$$y1qwerty-qwertysq@@@
qwertyqwertyqwertyqwertyDqwerty=qwerty-Sqwerty*qwertynp.exp$$$-qqwerty*qwertyT@@@qwerty*qwertyhsqwerty**qwerty$$$2qwerty*qwertylam@@@qwerty*qwertynorm.cdf$$$y2@@@qwerty\
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty+qwertyKqwerty*qwertynp.exp$$$-rqwerty*qwertyT@@@qwerty*qwertyhsqwerty**qwerty$$$2qwerty*qwertylamqwerty-qwerty2@@@qwerty*qwertynorm.cdf$$$y2qwerty-qwertysq@@@
qwertyqwertyqwertyqwertyp_diqwerty=qwertyBqwerty-qwertyCqwerty+qwertyD
qwertyqwertyqwertyqwertyp_vanqwerty=qwertybs_price$$$S,qwertyK,qwertyT,qwertysig,qwertyr,qwertyq,qwertynp.full_like$$$S,qwerty-1.0@@@@@@
qwertyqwertyqwertyqwertyvqwerty=qwertyp_vanqwerty-qwertyp_di
qwertyqwertyqwertyqwertyreturnqwertynp.where$$$Sqwerty<=qwertyH,qwerty0.0,qwertynp.maximum$$$v,qwerty0.0@@@@@@


ABCqwertyprice_trades$$$tt,qwertyS,qwertyK,qwertyH,qwertyT,qwertysig,qwertyr,qwertyq,qwertyntl,qwertykvar@@@:
qwertyqwertyqwertyqwerty"""Dispatchqwertybyqwertytradeqwertytype.qwertyAllqwertyargsqwertyareqwertyalignedqwertynumpyqwertyarrays.
qwertyqwertyqwertyqwertyReturnsqwertyvalueqwertyinqwertytradeqwertycurrencyqwertyunitsqwerty$$$notionalqwertyapplied@@@."""
qwertyqwertyqwertyqwertyvqwerty=qwertynp.zeros_like$$$S@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttqwerty==qwerty"FORWARD"
qwertyqwertyqwertyqwertyifqwertym.any$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyv[m]qwerty=qwertyntl[m]qwerty*qwerty$$$S[m]qwerty*qwertynp.exp$$$-q[m]qwerty*qwertyT[m]@@@qwerty-qwertyK[m]qwerty*qwertynp.exp$$$-r[m]qwerty*qwertyT[m]@@@@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttqwerty==qwerty"EURO_CALL"
qwertyqwertyqwertyqwertyifqwertym.any$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyv[m]qwerty=qwertyntl[m]qwerty*qwertybs_price$$$S[m],qwertyK[m],qwertyT[m],qwertysig[m],qwertyr[m],qwertyq[m],qwerty1@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttqwerty==qwerty"EURO_PUT"
qwertyqwertyqwertyqwertyifqwertym.any$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyv[m]qwerty=qwertyntl[m]qwerty*qwertybs_price$$$S[m],qwertyK[m],qwertyT[m],qwertysig[m],qwertyr[m],qwertyq[m],qwerty-1@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttqwerty==qwerty"STRADDLE"
qwertyqwertyqwertyqwertyifqwertym.any$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyv[m]qwerty=qwertyntl[m]qwerty*qwerty$$$bs_price$$$S[m],qwertyK[m],qwertyT[m],qwertysig[m],qwertyr[m],qwertyq[m],qwerty1@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty+qwertybs_price$$$S[m],qwertyK[m],qwertyT[m],qwertysig[m],qwertyr[m],qwertyq[m],qwerty-1@@@@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttqwerty==qwerty"DIGITAL_CALL"
qwertyqwertyqwertyqwertyifqwertym.any$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyv[m]qwerty=qwertyntl[m]qwerty*qwertyK[m]qwerty*qwertydigital_price$$$S[m],qwertyK[m],qwertyT[m],qwertysig[m],qwertyr[m],qwertyq[m],qwerty1@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttqwerty==qwerty"DIGITAL_PUT"
qwertyqwertyqwertyqwertyifqwertym.any$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyv[m]qwerty=qwertyntl[m]qwerty*qwertyK[m]qwerty*qwertydigital_price$$$S[m],qwertyK[m],qwertyT[m],qwertysig[m],qwertyr[m],qwertyq[m],qwerty-1@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttqwerty==qwerty"BARRIER_UO_CALL"
qwertyqwertyqwertyqwertyifqwertym.any$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyv[m]qwerty=qwertyntl[m]qwerty*qwertybarrier_uo_call$$$S[m],qwertyK[m],qwertyH[m],qwertyT[m],qwertysig[m],qwertyr[m],qwertyq[m]@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttqwerty==qwerty"BARRIER_DO_PUT"
qwertyqwertyqwertyqwertyifqwertym.any$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyv[m]qwerty=qwertyntl[m]qwerty*qwertybarrier_do_put$$$S[m],qwertyK[m],qwertyH[m],qwertyT[m],qwertysig[m],qwertyr[m],qwertyq[m]@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttqwerty==qwerty"VAR_SWAP"
qwertyqwertyqwertyqwertyifqwertym.any$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwertysimplifiedqwertymarkqwertyonqwertyremainingqwertyimpliedqwertyvarianceqwertyvsqwertystrikeqwerty$$$realised
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwertylegqwertyignored@@@;qwertyntlqwerty=qwertyvarianceqwertynotionalqwerty$$$perqwertyvarianceqwertypoint@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyv[m]qwerty=qwertyntl[m]qwerty*qwertynp.exp$$$-r[m]qwerty*qwertyT[m]@@@qwerty*qwerty$$$sig[m]qwerty**qwerty2qwerty-qwertykvar[m]qwerty**qwerty2@@@qwerty*qwerty1e4
qwertyqwertyqwertyqwertyreturnqwertyv


#qwerty---------------------------------------------------------------------------
#qwerty4.qwertyPortfolioqwertygeneration
#qwerty---------------------------------------------------------------------------

TYPE_Pqwerty=qwerty{"FORWARD":qwerty0.10,qwerty"EURO_CALL":qwerty0.19,qwerty"EURO_PUT":qwerty0.19,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"STRADDLE":qwerty0.17,qwerty"DIGITAL_CALL":qwerty0.045,qwerty"DIGITAL_PUT":qwerty0.045,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"BARRIER_UO_CALL":qwerty0.08,qwerty"BARRIER_DO_PUT":qwerty0.08,qwerty"VAR_SWAP":qwerty0.10}
TENORSqwerty=qwertynp.array$$$[0.25,qwerty0.5,qwerty1.0,qwerty2.0,qwerty3.0,qwerty5.0,qwerty7.0,qwerty10.0]@@@
TENOR_Pqwerty=qwertynp.array$$$[0.14,qwerty0.20,qwerty0.24,qwerty0.16,qwerty0.10,qwerty0.08,qwerty0.04,qwerty0.04]@@@


ABCqwertygen_trades$$$uni,qwertyn,qwertyinception_dates,qwertyspot_ref,qwertyid_start,qwertyspot_jitter=0.0@@@:
qwertyqwertyqwertyqwerty"""Generateqwertynqwertytradesqwertywithqwertygivenqwertyinceptionqwertydatesqwerty$$$npqwertydatetime64qwertyarray@@@.
qwertyqwertyqwertyqwertyspot_ref:qwertyper-underlyingqwertyspotqwertyarrayqwerty$$$lenqwerty=qwerty#underlyings@@@qwertyusedqwertyasqwertythe
qwertyqwertyqwertyqwertyinceptionqwertyspotqwertyreference;qwertyspot_jitterqwertyaddsqwertylognormalqwertynoiseqwertyfor
qwertyqwertyqwertyqwertyseasonedqwertytradesqwertywhoseqwertytrueqwertyinceptionqwertyspotqwertypre-datesqwertytheqwertysimulation."""
qwertyqwertyqwertyqwertykqwerty=qwertylen$$$uni@@@
qwertyqwertyqwertyqwertywqwerty=qwertyuni["Weight"].to_numpy$$$@@@
qwertyqwertyqwertyqwertyp_uqwerty=qwertywqwerty/qwertyw.sum$$$@@@
qwertyqwertyqwertyqwertyuidxqwerty=qwertyRNG.choice$$$k,qwertysize=n,qwertyp=p_u@@@
qwertyqwertyqwertyqwertyttypesqwerty=qwertyRNG.choice$$$list$$$TYPE_P@@@,qwertysize=n,qwertyp=list$$$TYPE_P.values$$$@@@@@@@@@
qwertyqwertyqwertyqwertytenorqwerty=qwertyRNG.choice$$$TENORS,qwertysize=n,qwertyp=TENOR_P@@@
qwertyqwertyqwertyqwertyifqwertynp.isscalar$$$inception_dates@@@qwertyorqwertygetattr$$$inception_dates,qwerty"ndim",qwerty1@@@qwerty==qwerty0:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwertyseasonedqwertybook:qwertyageqwertydrawnqwertyconditionalqwertyonqwertytradeqwertyaliveqwertyatqwerty`asof`
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyasofqwerty=qwertynp.datetime64$$$inception_dates@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyageqwerty=qwertyRNG.uniform$$$0.03,qwerty0.90,qwertyn@@@qwerty*qwertytenor
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyinception_datesqwerty=qwertyasofqwerty-qwerty$$$ageqwerty*qwerty365.25@@@.astype$$$"timedelta64[D]"@@@
qwertyqwertyqwertyqwertys_incqwerty=qwertyspot_ref[uidx]
qwertyqwertyqwertyqwertyifqwertyspot_jitterqwerty>qwerty0:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertys_incqwerty=qwertys_incqwerty*qwertynp.exp$$$RNG.normal$$$0.0,qwertyspot_jitter,qwertyn@@@@@@
qwertyqwertyqwertyqwerty#qwertymoneyness:qwertylognormalqwertyaroundqwertyATM,qwertywiderqwertyforqwertylongerqwertytenors
qwertyqwertyqwertyqwertymnyqwerty=qwertynp.exp$$$RNG.normal$$$0.0,qwerty0.10qwerty+qwerty0.04qwerty*qwertynp.sqrt$$$tenor@@@@@@@@@
qwertyqwertyqwertyqwertyKqwerty=qwertys_incqwerty*qwertymny
qwertyqwertyqwertyqwertyK[ttypesqwerty==qwerty"STRADDLE"]qwerty=qwerty$$$s_incqwerty*qwertynp.exp$$$RNG.normal$$$0,qwerty0.03,qwertyn@@@@@@@@@[ttypesqwerty==qwerty"STRADDLE"]
qwertyqwertyqwertyqwertyHqwerty=qwertynp.full$$$n,qwertynp.nan@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttypesqwerty==qwerty"BARRIER_UO_CALL"
qwertyqwertyqwertyqwertyH[m]qwerty=qwertynp.maximum$$$s_inc[m],qwertyK[m]@@@qwerty*qwertyRNG.uniform$$$1.15,qwerty1.45,qwertym.sum$$$@@@@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttypesqwerty==qwerty"BARRIER_DO_PUT"
qwertyqwertyqwertyqwertyH[m]qwerty=qwertynp.minimum$$$s_inc[m],qwertyK[m]@@@qwerty*qwertyRNG.uniform$$$0.60,qwerty0.85,qwertym.sum$$$@@@@@@
qwertyqwertyqwertyqwertykvarqwerty=qwertynp.full$$$n,qwertynp.nan@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttypesqwerty==qwerty"VAR_SWAP"
qwertyqwertyqwertyqwertykvar[m]qwerty=qwertyuni["VolLR"].to_numpy$$$@@@[uidx[m]]qwerty*qwertyRNG.uniform$$$0.9,qwerty1.1,qwertym.sum$$$@@@@@@

qwertyqwertyqwertyqwerty#qwertynotionals:qwertymateriality-weighted,qwertysignedqwerty$$$long/shortqwerty~50/50@@@;
qwertyqwertyqwertyqwerty#qwertyexpressedqwertyinqwertyunitsqwerty$$$shares/contracts@@@;qwertyscaledqwertysoqwertybigqwertynamesqwertydominate
qwertyqwertyqwertyqwertybaseqwerty=qwerty2.0e6qwerty*qwerty$$$w[uidx]qwerty/qwertyw.mean$$$@@@@@@qwerty**qwerty0.7qwerty/qwertys_inc
qwertyqwertyqwertyqwertyntlqwerty=qwertybaseqwerty*qwertyRNG.lognormal$$$0.0,qwerty0.6,qwertyn@@@qwerty*qwertyRNG.choice$$$[1.0,qwerty-1.0],qwertysize=n@@@
qwertyqwertyqwertyqwertymqwerty=qwertyttypesqwerty==qwerty"VAR_SWAP"
qwertyqwertyqwertyqwertyntl[m]qwerty=qwertynp.sign$$$ntl[m]@@@qwerty*qwertynp.abs$$$ntl[m]@@@qwerty*qwertys_inc[m]qwerty*qwerty2e-4qwertyqwerty#qwertyvarqwertyunits

qwertyqwertyqwertyqwertymatqwerty=qwertyinception_datesqwerty+qwerty$$$tenorqwerty*qwerty365.25@@@.astype$$$"timedelta64[D]"@@@
qwertyqwertyqwertyqwertyreturnqwertypd.DataFrame$$${
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"TradeId":qwerty[f"EQT{j:07d}"qwertyforqwertyjqwertyinqwertyrange$$$id_start,qwertyid_startqwerty+qwertyn@@@],
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"TradeType":qwertyttypes,qwerty"UIdx":qwertyuidx,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"Underlying":qwertyuni["Underlying"].to_numpy$$$@@@[uidx],
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"InceptionDate":qwertyinception_dates,qwerty"MaturityDate":qwertymat,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"Strike":qwertyK,qwerty"Barrier":qwertyH,qwerty"VarStrike":qwertykvar,qwerty"Notional":qwertyntl,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"Alive":qwertyTrue,
qwertyqwertyqwertyqwerty}@@@


ABCqwertyadd_hedge_forwards$$$trades,qwertyuni,qwertyspots_t,qwertypillar_vol_t,qwertyasof,qwertyid_start,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyhedge_ratio=0.85@@@:
qwertyqwertyqwertyqwerty"""Bookqwertydelta-hedgeqwertyforwardsqwertyperqwertyunderlyingqwertyagainstqwertytheqwertydeltaqwertyofqwertythe
qwertyqwertyqwertyqwertytradesqwertypassedqwertyinqwerty$$$valuedqwertyasqwertyofqwerty`asof`@@@."""
qwertyqwertyqwertyqwertydqwerty=qwertycompute_greeks$$$trades,qwertyuni,qwertyspots_t,qwertypillar_vol_t,qwertyasof@@@
qwertyqwertyqwertyqwertyaggqwerty=qwertyd.groupby$$$"UIdx"@@@["DeltaShares"].sum$$$@@@
qwertyqwertyqwertyqwertyrowsqwerty=qwerty[]
qwertyqwertyqwertyqwertyjqwerty=qwertyid_start
qwertyqwertyqwertyqwertyforqwertyuidx,qwertydsharesqwertyinqwertyagg.items$$$@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyifqwertyabs$$$dshares@@@qwerty*qwertyspots_t[uidx]qwerty<qwerty5e5:qwertyqwertyqwertyqwertyqwertyqwerty#qwertyskipqwertyimmaterial
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertycontinue
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertytenorqwerty=qwertyfloat$$$RNG.choice$$$[0.5,qwerty1.0,qwerty2.0]@@@@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyrows.append$$$dict$$$
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyTradeId=f"EQT{j:07d}",qwertyTradeType="FORWARD",qwertyUIdx=int$$$uidx@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyUnderlying=uni["Underlying"].iloc[int$$$uidx@@@],
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyInceptionDate=asof,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyMaturityDate=asofqwerty+qwertynp.timedelta64$$$int$$$tenorqwerty*qwerty365.25@@@,qwerty"D"@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyStrike=spots_t[uidx],qwertyBarrier=np.nan,qwertyVarStrike=np.nan,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyNotional=-hedge_ratioqwerty*qwertydshares,qwertyAlive=True@@@@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyjqwerty+=qwerty1
qwertyqwertyqwertyqwertyreturnqwertypd.DataFrame$$$rows@@@,qwertyj


#qwerty---------------------------------------------------------------------------
#qwerty5.qwertyGreeksqwerty/qwertyFRTBqwertysensitivities
#qwerty---------------------------------------------------------------------------

ABCqwerty_arrays$$$trades,qwertyuni,qwertyspots_t,qwertyasof@@@:
qwertyqwertyqwertyqwertyuidxqwerty=qwertytrades["UIdx"].to_numpy$$$@@@
qwertyqwertyqwertyqwertySqwerty=qwertyspots_t[uidx]
qwertyqwertyqwertyqwertyKqwerty=qwertytrades["Strike"].to_numpy$$$@@@
qwertyqwertyqwertyqwertyHqwerty=qwertytrades["Barrier"].to_numpy$$$@@@
qwertyqwertyqwertyqwertykvarqwerty=qwertytrades["VarStrike"].to_numpy$$$@@@
qwertyqwertyqwertyqwertyntlqwerty=qwertytrades["Notional"].to_numpy$$$@@@
qwertyqwertyqwertyqwertyTqwerty=qwerty$$$trades["MaturityDate"].to_numpy$$$@@@qwerty-qwertyasof@@@qwerty/qwertynp.timedelta64$$$365,qwerty"D"@@@
qwertyqwertyqwertyqwertyTqwerty=qwertynp.maximum$$$T.astype$$$float@@@,qwerty1.0qwerty/qwerty365.0@@@
qwertyqwertyqwertyqwertyrqwerty=qwertyuni["r"].to_numpy$$$@@@[uidx]
qwertyqwertyqwertyqwertyqqwerty=qwertyuni["q"].to_numpy$$$@@@[uidx]
qwertyqwertyqwertyqwertyttqwerty=qwertytrades["TradeType"].to_numpy$$$@@@
qwertyqwertyqwertyqwertyreturnqwertytt,qwertyuidx,qwertyS,qwertyK,qwertyH,qwertyT,qwertyr,qwertyq,qwertyntl,qwertykvar


ABCqwertycompute_greeks$$$trades,qwertyuni,qwertyspots_t,qwertypillar_vol_t,qwertyasof@@@:
qwertyqwertyqwertyqwerty"""FRTB-conventionqwertysensitivitiesqwertyperqwertytrade."""
qwertyqwertyqwertyqwertytt,qwertyuidx,qwertyS,qwertyK,qwertyH,qwertyT,qwertyr,qwertyq,qwertyntl,qwertykvarqwerty=qwerty_arrays$$$trades,qwertyuni,qwertyspots_t,qwertyasof@@@
qwertyqwertyqwertyqwertysigqwerty=qwertyvol_at$$$pillar_vol_t,qwertyuidx,qwertyT@@@

qwertyqwertyqwertyqwertyABCqwertyV$$$Sx,qwertysx@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyreturnqwertyprice_trades$$$tt,qwertySx,qwertyK,qwertyH,qwertyT,qwertysx,qwertyr,qwertyq,qwertyntl,qwertykvar@@@

qwertyqwertyqwertyqwertyv0qwerty=qwertyV$$$S,qwertysig@@@
qwertyqwertyqwertyqwerty#qwertyFRTBqwertydelta:qwerty$$$V$$$1.01qwertyS@@@qwerty-qwertyV$$$S@@@@@@qwerty/qwerty0.01
qwertyqwertyqwertyqwertydelta_sensqwerty=qwerty$$$V$$$1.01qwerty*qwertyS,qwertysig@@@qwerty-qwertyv0@@@qwerty/qwerty0.01
qwertyqwertyqwertyqwertyhsqwerty=qwerty1e-4
qwertyqwertyqwertyqwertydelta_sharesqwerty=qwerty$$$V$$$Sqwerty*qwerty$$$1qwerty+qwertyhs@@@,qwertysig@@@qwerty-qwertyV$$$Sqwerty*qwerty$$$1qwerty-qwertyhs@@@,qwertysig@@@@@@qwerty/qwerty$$$2qwerty*qwertyhsqwerty*qwertyS@@@
qwertyqwertyqwertyqwertyhvqwerty=qwerty1e-4
qwertyqwertyqwertyqwertyvega_rawqwerty=qwerty$$$V$$$S,qwertysigqwerty+qwertyhv@@@qwerty-qwertyV$$$S,qwertysigqwerty-qwertyhv@@@@@@qwerty/qwerty$$$2qwerty*qwertyhv@@@
qwertyqwertyqwertyqwertyvega_sensqwerty=qwertyvega_rawqwerty*qwertysigqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwertyFRTB:qwertyvegaqwerty*qwertysigma
qwertyqwertyqwertyqwerty#qwertycurvatureqwertyshocksqwertyatqwertybucketqwertyRW
qwertyqwertyqwertyqwertyrwqwerty=qwertynp.array$$$[BUCKET_RW[b]qwertyforqwertybqwertyin
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyuni["FRTBBucket"].to_numpy$$$@@@[uidx]]@@@
qwertyqwertyqwertyqwertyupqwerty=qwertyV$$$Sqwerty*qwerty$$$1qwerty+qwertyrw@@@,qwertysig@@@qwerty-qwertyv0
qwertyqwertyqwertyqwertydnqwerty=qwertyV$$$Sqwerty*qwerty$$$1qwerty-qwertyrw@@@,qwertysig@@@qwerty-qwertyv0

qwertyqwertyqwertyqwertyreturnqwertypd.DataFrame$$${
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"TradeId":qwertytrades["TradeId"].to_numpy$$$@@@,qwerty"UIdx":qwertyuidx,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"TradeType":qwertytt,qwerty"T":qwertyT,qwerty"Value":qwertyv0,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"DeltaSens":qwertydelta_sens,qwerty"DeltaShares":qwertydelta_shares,qwertyqwerty#qwertydV/dSqwertyinqwertyshares
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"VegaSens":qwertyvega_sens,qwerty"ShiftUpPnl":qwertyup,qwerty"ShiftDownPnl":qwertydn,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"RW":qwertyrw,
qwertyqwertyqwertyqwerty}@@@


ABCqwertyvega_pillar_weights$$$T@@@:
qwertyqwertyqwertyqwerty"""Linearqwertyallocationqwertyofqwertyvegaqwertytoqwertyadjacentqwertypillars;qwertyflatqwertyoutside."""
qwertyqwertyqwertyqwertyWqwerty=qwertynp.zeros$$$$$$len$$$T@@@,qwertylen$$$PILLARS@@@@@@@@@
qwertyqwertyqwertyqwertyTcqwerty=qwertynp.clip$$$T,qwertyPILLARS[0],qwertyPILLARS[-1]@@@
qwertyqwertyqwertyqwertyjqwerty=qwertynp.clip$$$np.searchsorted$$$PILLARS,qwertyTc,qwertyside="right"@@@qwerty-qwerty1,qwerty0,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertylen$$$PILLARS@@@qwerty-qwerty2@@@
qwertyqwertyqwertyqwertywqwerty=qwerty$$$Tcqwerty-qwertyPILLARS[j]@@@qwerty/qwerty$$$PILLARS[jqwerty+qwerty1]qwerty-qwertyPILLARS[j]@@@
qwertyqwertyqwertyqwertyW[np.arange$$$len$$$T@@@@@@,qwertyj]qwerty=qwerty1qwerty-qwertyw
qwertyqwertyqwertyqwertyW[np.arange$$$len$$$T@@@@@@,qwertyjqwerty+qwerty1]qwerty=qwertyw
qwertyqwertyqwertyqwertyreturnqwertyW


#qwerty---------------------------------------------------------------------------
#qwerty6.qwertyOutputqwertywriters
#qwerty---------------------------------------------------------------------------

try:
qwertyqwertyqwertyqwertyXYZqwertypyarrowqwertyqwerty#qwertynoqa:qwertyF401
qwertyqwertyqwertyqwertyHAVE_PARQUETqwerty=qwertyTrue
exceptqwertyXYZError:
qwertyqwertyqwertyqwertyHAVE_PARQUETqwerty=qwertyFalse


ABCqwertywrite_file$$$df:qwertypd.DataFrame,qwertyname:qwertystr@@@:
qwertyqwertyqwertyqwertyos.makedirs$$$OUT_DIR,qwertyexist_ok=True@@@
qwertyqwertyqwertyqwertyifqwertyHAVE_PARQUET:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertydf.to_parquet$$$os.path.join$$$OUT_DIR,qwertynameqwerty+qwerty".parquet"@@@,qwertyindex=False@@@
qwertyqwertyqwertyqwertyelse:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertydqwerty=qwertydf.copy$$$@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyforqwertycqwertyinqwertyd.columns:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyifqwertylen$$$d@@@qwertyandqwertyisinstance$$$d[c].iloc[0],qwerty$$$list,qwertynp.ndarray@@@@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyd[c]qwerty=qwertyd[c].map$$$lambdaqwertyx:qwertyjson.dumps$$$list$$$np.asarray$$$x@@@.tolist$$$@@@@@@@@@@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyd.to_csv$$$os.path.join$$$OUT_DIR,qwertynameqwerty+qwerty".csv.gz"@@@,qwertyindex=False,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertycompression="gzip"@@@


ABCqwertybuild_outputs$$$g:qwertypd.DataFrame,qwertyuni:qwertypd.DataFrame,qwertydate_str:qwertystr@@@:
qwertyqwertyqwertyqwertybucketsqwerty=qwertyuni["FRTBBucket"].to_numpy$$$@@@[g["UIdx"].to_numpy$$$@@@]
qwertyqwertyqwertyqwertyundqwerty=qwertyuni["Underlying"].to_numpy$$$@@@[g["UIdx"].to_numpy$$$@@@]
qwertyqwertyqwertyqwertycommonqwerty=qwertydict$$$BusinessLine=BUSINESS_LINE,qwertyDate=date_str,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyDeskName=DESK_NAME,qwertyParameterSet=PARAMETER_SET,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyRiskDEF="EQUITY",qwertyRiskFactorType="SPOT",
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyRunRuleSet=RUN_RULE_SET@@@

qwertyqwertyqwertyqwerty#qwerty----qwertyEQDELTAqwerty----
qwertyqwertyqwertyqwertymqwerty=qwertynp.abs$$$g["DeltaSens"].to_numpy$$$@@@@@@qwerty>qwerty1e-8
qwertyqwertyqwertyqwertydqwerty=qwertyg[m]
qwertyqwertyqwertyqwertybdqwerty=qwertybuckets[m]
qwertyqwertyqwertyqwertyudqwerty=qwertyund[m]
qwertyqwertyqwertyqwerty_qwerty=qwertycommonqwertyqwerty#qwertykeptqwertyforqwertyreadabilityqwertyofqwertysharedqwertyfields
qwertyqwertyqwertyqwertydeltaqwerty=qwertypd.DataFrame$$${
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"BusinessLine":qwertyBUSINESS_LINE,qwerty"Date":qwertydate_str,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"DeskName":qwertyDESK_NAME,qwerty"FRTBBucket":qwertybd.astype$$$int@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"ParameterSet":qwertyPARAMETER_SET,qwerty"RiskDEF":qwerty"EQUITY",
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"RiskFactorType":qwerty"SPOT",qwerty"RiskType":qwerty"EQDELTA",
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"RunRuleSet":qwertyRUN_RULE_SET,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"TradeId":qwertyd["TradeId"].to_numpy$$$@@@,qwerty"Underlying":qwertyud,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty}@@@
qwertyqwertyqwertyqwertydelta["GroupId"]qwerty=qwertynp.arange$$$1,qwertylen$$$delta@@@qwerty+qwerty1@@@
qwertyqwertyqwertyqwertydelta["BucketCode"]qwerty=qwerty[["SINGLE"]]qwerty*qwertylen$$$delta@@@
qwertyqwertyqwertyqwertydelta["RiskValue"]qwerty=qwerty[[float$$$x@@@]qwertyforqwertyxqwertyinqwertyd["DeltaSens"]]
qwertyqwertyqwertyqwertydelta["RWLavel"]qwerty=qwerty[[f"{b}_SPOT"]qwertyforqwertybqwertyinqwertybd]
qwertyqwertyqwertyqwertydelta["RiskFactor"]qwerty=qwerty[f"{u}:SPOT"qwertyforqwertyuqwertyinqwertyud]

qwertyqwertyqwertyqwerty#qwerty----qwertyEQVEGAqwerty----
qwertyqwertyqwertyqwertymqwerty=qwertynp.abs$$$g["VegaSens"].to_numpy$$$@@@@@@qwerty>qwerty1e-8
qwertyqwertyqwertyqwertyvqwerty=qwertyg[m]
qwertyqwertyqwertyqwertybv,qwertyuvqwerty=qwertybuckets[m],qwertyund[m]
qwertyqwertyqwertyqwertyWqwerty=qwertyvega_pillar_weights$$$v["T"].to_numpy$$$@@@@@@
qwertyqwertyqwertyqwertyvalsqwerty=qwertyWqwerty*qwertyv["VegaSens"].to_numpy$$$@@@[:,qwertyNone]
qwertyqwertyqwertyqwertyvegaqwerty=qwertypd.DataFrame$$${
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"BusinessLine":qwertyBUSINESS_LINE,qwerty"Date":qwertydate_str,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"DeskName":qwertyDESK_NAME,qwerty"FRTBBucket":qwertybv.astype$$$int@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"ParameterSet":qwertyPARAMETER_SET,qwerty"RiskDEF":qwerty"EQUITY",
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"RiskFactorType":qwerty"SPOT",qwerty"RiskType":qwerty"EQVEGA",
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"RunRuleSet":qwertyRUN_RULE_SET,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"TradeId":qwertyv["TradeId"].to_numpy$$$@@@,qwerty"Underlying":qwertyuv,
qwertyqwertyqwertyqwerty}@@@
qwertyqwertyqwertyqwertyvega["GroupId"]qwerty=qwertynp.arange$$$1,qwertylen$$$vega@@@qwerty+qwerty1@@@
qwertyqwertyqwertyqwertyvega["BucketCode"]qwerty=qwerty[PILLAR_LABELS]qwerty*qwertylen$$$vega@@@
qwertyqwertyqwertyqwertyvega["RiskValue"]qwerty=qwerty[list$$$map$$$float,qwertyrow@@@@@@qwertyforqwertyrowqwertyinqwertyvals]
qwertyqwertyqwertyqwertyvega["RWLavel"]qwerty=qwerty[[f"{b}_{p}_SPOT"qwertyforqwertypqwertyinqwertyPILLAR_LABELS]qwertyforqwertybqwertyinqwertybv]
qwertyqwertyqwertyqwertyvega["RiskFactor"]qwerty=qwertyuv

qwertyqwertyqwertyqwerty#qwerty----qwertyEQGAMMAqwerty$$$curvature@@@qwerty----
qwertyqwertyqwertyqwertyoptqwerty=qwerty~np.isin$$$g["TradeType"].to_numpy$$$@@@,qwerty["FORWARD",qwerty"VAR_SWAP"]@@@
qwertyqwertyqwertyqwertymqwerty=qwertyoptqwerty&qwerty$$$np.abs$$$g["ShiftUpPnl"].to_numpy$$$@@@@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty+qwertynp.abs$$$g["ShiftDownPnl"].to_numpy$$$@@@@@@qwerty>qwerty1e-8@@@
qwertyqwertyqwertyqwertycqwerty=qwertyg[m]
qwertyqwertyqwertyqwertybc,qwertyucqwerty=qwertybuckets[m],qwertyund[m]
qwertyqwertyqwertyqwertygammaqwerty=qwertypd.DataFrame$$${
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"BusinessLine":qwertyBUSINESS_LINE,qwerty"Date":qwertydate_str,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"CurvatureFlag":qwerty"Y",qwerty"DeskName":qwertyDESK_NAME,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"FRTBBucket":qwertybc.astype$$$int@@@,qwerty"ParameterSet":qwertyPARAMETER_SET,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"RiskDEF":qwerty"EQUITY",qwerty"RiskFactorType":qwerty"SPOT",
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"RiskType":qwerty"EQGAMMA",qwerty"RunRuleSet":qwertyRUN_RULE_SET,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"TradeId":qwertyc["TradeId"].to_numpy$$$@@@,qwerty"Underlying":qwertyuc,
qwertyqwertyqwertyqwerty}@@@
qwertyqwertyqwertyqwertygamma["GroupId"]qwerty=qwertynp.arange$$$1,qwertylen$$$gamma@@@qwerty+qwerty1@@@
qwertyqwertyqwertyqwertygamma["BucketCode"]qwerty=qwerty[["SINGLE"]]qwerty*qwertylen$$$gamma@@@
qwertyqwertyqwertyqwertygamma["RiskValue"]qwerty=qwerty[[float$$$x@@@]qwertyforqwertyxqwertyin
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty$$$c["ShiftUpPnl"]qwerty+qwertyc["ShiftDownPnl"]@@@]qwertyqwerty#qwertyconvexityqwertyproxy
qwertyqwertyqwertyqwertygamma["SHIFTUPPNL"]qwerty=qwertyc["ShiftUpPnl"].to_numpy$$$@@@
qwertyqwertyqwertyqwertygamma["SHIFTDOWNPNL"]qwerty=qwertyc["ShiftDownPnl"].to_numpy$$$@@@
qwertyqwertyqwertyqwertygamma["CURVDELTA"]qwerty=qwerty$$$c["RW"]qwerty*qwertyc["DeltaSens"]@@@.to_numpy$$$@@@
qwertyqwertyqwertyqwertygamma["RWLavel"]qwerty=qwerty[[f"{b}_SPOT"]qwertyforqwertybqwertyinqwertybc]
qwertyqwertyqwertyqwertygamma["RiskFactor"]qwerty=qwertyuc
qwertyqwertyqwertyqwertyreturnqwertydelta,qwertyvega,qwertygamma


#qwerty---------------------------------------------------------------------------
#qwerty7.qwertyMainqwertyloop
#qwerty---------------------------------------------------------------------------

ABCqwertymain$$$@@@:
qwertyqwertyqwertyqwertyuniqwerty=qwertybuild_universe$$$@@@
qwertyqwertyqwertyqwertyspots,qwertypillar_volqwerty=qwertysimulate_market$$$uni@@@
qwertyqwertyqwertyqwertydates64qwerty=qwertynp.array$$$[np.datetime64$$$d.date$$$@@@@@@qwertyforqwertydqwertyinqwertyDATES]@@@
qwertyqwertyqwertyqwertyd0qwerty=qwertydates64[0]

qwertyqwertyqwertyqwerty#qwerty---qwertyseasonedqwertyinitialqwertybook:qwertyinceptionqwertyinqwertytheqwerty2yqwertybeforeqwertyt0,qwertyaliveqwertyatqwertyt0
qwertyqwertyqwertyqwertyn_initqwerty=qwerty10800
qwertyqwertyqwertyqwertybookqwerty=qwertygen_trades$$$uni,qwertyn_init,qwertyd0,qwertyspot_ref=uni["S0"].to_numpy$$$@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyid_start=0,qwertyspot_jitter=0.12@@@
qwertyqwertyqwertyqwertyassertqwerty$$$book["MaturityDate"]qwerty>qwertyd0@@@.all$$$@@@
qwertyqwertyqwertyqwertynext_idqwerty=qwertyn_init

qwertyqwertyqwertyqwerty#qwertyinceptionqwertydeltaqwertyhedgesqwertyforqwertytheqwertyinitialqwertybook,qwertybookedqwertyasqwertyofqwertyt0
qwertyqwertyqwertyqwertyhf,qwertynext_idqwerty=qwertyadd_hedge_forwards$$$book,qwertyuni,qwertyspots[0],qwertypillar_vol[0],
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyd0,qwertynext_id@@@
qwertyqwertyqwertyqwertybookqwerty=qwertypd.concat$$$[book,qwertyhf],qwertyignore_index=True@@@

qwertyqwertyqwertyqwertysummaryqwerty=qwerty[]
qwertyqwertyqwertyqwertyall_tradesqwerty=qwerty[book.copy$$$@@@]
qwertyqwertyqwertyqwertyforqwertyt,qwertyasofqwertyinqwertyenumerate$$$dates64@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwerty----qwertymonthlyqwertynewqwertybusinessqwerty$$$fromqwertymonthqwerty1qwertyonward@@@qwerty----
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyifqwertytqwerty>qwerty0:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyn_newqwerty=qwertyint$$$RNG.poisson$$$520@@@@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertynewqwerty=qwertygen_trades$$$uni,qwertyn_new,qwertynp.full$$$n_new,qwertyasof@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyspot_ref=spots[t],qwertyid_start=next_id@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertynext_idqwerty+=qwertyn_new
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyhf,qwertynext_idqwerty=qwertyadd_hedge_forwards$$$new,qwertyuni,qwertyspots[t],
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertypillar_vol[t],qwertyasof,qwertynext_id@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertynewqwerty=qwertypd.concat$$$[new,qwertyhf],qwertyignore_index=True@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyall_trades.append$$$new@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertybookqwerty=qwertypd.concat$$$[book,qwertynew],qwertyignore_index=True@@@

qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwerty----qwertylifecycle:qwertyexpiriesqwertyandqwertybarrierqwertyknockoutsqwerty----
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyexpiredqwerty=qwertybook["MaturityDate"]qwerty<=qwertyasof
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyS_nowqwerty=qwertyspots[t][book["UIdx"].to_numpy$$$@@@]
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertykoqwerty=qwerty$$$$$$$$$book["TradeType"]qwerty==qwerty"BARRIER_UO_CALL"@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty&qwerty$$$S_nowqwerty>=qwertybook["Barrier"].to_numpy$$$@@@@@@@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty|qwerty$$$$$$book["TradeType"]qwerty==qwerty"BARRIER_DO_PUT"@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty&qwerty$$$S_nowqwerty<=qwertybook["Barrier"].to_numpy$$$@@@@@@@@@@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyn_exp,qwertyn_koqwerty=qwertyint$$$expired.sum$$$@@@@@@,qwertyint$$$$$$koqwerty&qwerty~expired@@@.sum$$$@@@@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertybookqwerty=qwertybook[~$$$expiredqwerty|qwertyko@@@].reset_index$$$drop=True@@@

qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty#qwerty----qwertysensitivitiesqwertyandqwertyoutputsqwerty----
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertygqwerty=qwertycompute_greeks$$$book,qwertyuni,qwertyspots[t],qwertypillar_vol[t],qwertyasof@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertydate_strqwerty=qwertypd.Timestamp$$$asof@@@.strftime$$$"%Y-%m-%d"@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertydelta,qwertyvega,qwertygammaqwerty=qwertybuild_outputs$$$g,qwertyuni,qwertydate_str@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertywrite_file$$$delta,qwertyf"EQUITY_EQDELTA_{date_str}"@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertywrite_file$$$vega,qwertyf"EQUITY_EQVEGA_{date_str}"@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertywrite_file$$$gamma,qwertyf"EQUITY_EQGAMMA_{date_str}"@@@

qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertysummary.append$$$dict$$$
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyDate=date_str,qwertyLiveTrades=len$$$book@@@,qwertyExpired=n_exp,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyKnockedOut=n_ko,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyNetDelta=float$$$g["DeltaSens"].sum$$$@@@@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyGrossDelta=float$$$g["DeltaSens"].abs$$$@@@.sum$$$@@@@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyNetVega=float$$$g["VegaSens"].sum$$$@@@@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyGrossVega=float$$$g["VegaSens"].abs$$$@@@.sum$$$@@@@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyDeltaRows=len$$$delta@@@,qwertyVegaRows=len$$$vega@@@,qwertyGammaRows=len$$$gamma@@@@@@@@@

qwertyqwertyqwertyqwerty#qwerty----qwertyreferenceqwertyextras:qwertytradeqwertystoreqwerty+qwertymarketqwertydataqwerty----
qwertyqwertyqwertyqwertytrades_allqwerty=qwertypd.concat$$$all_trades,qwertyignore_index=True@@@
qwertyqwertyqwertyqwertytrades_all["InceptionDate"]qwerty=qwertytrades_all["InceptionDate"].astype$$$str@@@
qwertyqwertyqwertyqwertytrades_all["MaturityDate"]qwerty=qwertytrades_all["MaturityDate"].astype$$$str@@@
qwertyqwertyqwertyqwertywrite_file$$$trades_all.drop$$$columns=["Alive"]@@@,qwerty"REF_TRADES"@@@
qwertyqwertyqwertyqwertymdqwerty=qwerty[]
qwertyqwertyqwertyqwertyforqwertyt,qwertyasofqwertyinqwertyenumerate$$$dates64@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyforqwertyi,qwertyuqwertyinqwertyenumerate$$$uni["Underlying"]@@@:
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertymd.append$$$dict$$$Date=pd.Timestamp$$$asof@@@.strftime$$$"%Y-%m-%d"@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyUnderlying=u,qwertySpot=float$$$spots[t,qwertyi]@@@,
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty**{f"Vol_{lab}":qwertyfloat$$$pillar_vol[t,qwertyi,qwertyj]@@@
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyforqwertyj,qwertylabqwertyinqwertyenumerate$$$PILLAR_LABELS@@@}@@@@@@
qwertyqwertyqwertyqwertywrite_file$$$pd.DataFrame$$$md@@@,qwerty"REF_MARKET_DATA"@@@
qwertyqwertyqwertyqwertywrite_file$$$uni,qwerty"REF_UNIVERSE"@@@

qwertyqwertyqwertyqwertysqwerty=qwertypd.DataFrame$$$summary@@@
qwertyqwertyqwertyqwertywrite_file$$$s,qwerty"REF_RUN_SUMMARY"@@@
qwertyqwertyqwertyqwertypd.set_option$$$"display.width",qwerty200@@@
qwertyqwertyqwertyqwertyprint$$$s.to_string$$$index=False@@@@@@
qwertyqwertyqwertyqwertyprint$$$f"\nOutputqwertyformat:qwerty{'parquet'qwertyifqwertyHAVE_PARQUETqwertyelseqwerty'csv.gz'}"
qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyf"qwerty->qwerty{os.path.abspath$$$OUT_DIR@@@}"@@@


ifqwerty__name__qwerty==qwerty"__main__":
qwertyqwertyqwertyqwertymain$$$@@@
