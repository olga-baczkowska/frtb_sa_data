# Equity derivatives pricing library

- Python 3.12, numpy, scipy, pytest. Run: `make test`
- Units: rates, vols, yields as decimals (0.20)
- T in years via `pricing/dates.year_fraction()`
- Model specs: `docs/model-spec/`
- Market data: only through `src/marketdata/api.py`
- Test data: synthetic only, in `tests/data/`
- Ask before changing `src/pricing/api.py` signatures
