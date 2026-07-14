#!/usr/bin/env python3
"""Convert the csv.gz outputs to parquet (list columns restored).

Usage:  python convert_to_parquet.py [input_dir] [output_dir]
Requires: pandas, pyarrow.
"""
import glob
import json
import os
import sys

import pandas as pd

LIST_COLS = {"BucketCode", "RiskValue", "RWLavel"}


def main(src="output", dst="output_parquet"):
    os.makedirs(dst, exist_ok=True)
    files = sorted(glob.glob(os.path.join(src, "*.csv.gz")))
    if not files:
        sys.exit(f"no csv.gz files under {src}")
    for f in files:
        df = pd.read_csv(f)
        def _maybe_json(x):
            if isinstance(x, str) and x.startswith("["):
                return json.loads(x)
            return x
        for c in LIST_COLS & set(df.columns):
            df[c] = df[c].map(_maybe_json)
        name = os.path.basename(f).replace(".csv.gz", ".parquet")
        df.to_parquet(os.path.join(dst, name), index=False)
        print(name, len(df))


if __name__ == "__main__":
    main(*sys.argv[1:3])
