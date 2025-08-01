import pandas as pd
from pathlib import Path
import os

RAW_DIR = Path("data/entsoe")
OUT_DIR = Path("data/features")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_all_files():
    all_dfs = []
    for country_dir in RAW_DIR.glob("*"):
        for year_dir in country_dir.glob("*"):
            for file in year_dir.glob("*_load.parquet"):
                try:
                    df = pd.read_parquet(file)
                    df = df.rename(columns={df.columns[0]: "load_mw"})
                    df["timestamp"] = df.index
                    df["country"] = country_dir.name
                    all_dfs.append(df)
                except Exception as e:
                    print(f"❌ Error with {file}: {e}")
    return pd.concat(all_dfs)

def clean_and_engineer(df: pd.DataFrame):
    df = df.reset_index(drop=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.set_index("timestamp")
    df = df.sort_index()

    df = df[~df.index.duplicated()]
    df = df.asfreq("h")
    df["load_mw"] = df["load_mw"].interpolate(limit_direction="both")

    df["hour"] = df.index.hour
    df["dayofweek"] = df.index.dayofweek
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["weekend"] = df["dayofweek"] >= 5

    return df

if __name__ == "__main__":
    print("🚀 Loading all parquet files...")
    df = load_all_files()
    print("✅ Merging and cleaning data...")

    df_clean = clean_and_engineer(df)

    out_path = OUT_DIR / "all_countries_features.parquet"
    df_clean.to_parquet(out_path)
    print(f"📦 Saved engineered dataset to {out_path}")
