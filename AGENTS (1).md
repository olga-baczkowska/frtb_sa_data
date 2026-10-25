# FRTB SA capital engine

- Python 3.12, numpy, pytest. Run: `make test`
- Sensitivities per MAR21.19: s_k = ΔV(+1bp) / 0.0001, reporting ccy EUR
- Methodology and golden cases: `docs/methodology/`
- Rule texts: `docs/reg/` (MAR21 extracts)
- Parameters: `params/*.yaml` (signed off)
- Test data: synthetic only, in `tests/data/`
- Ask before changing `src/frtb/api.py` signatures
