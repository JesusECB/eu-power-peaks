from prefect import flow, task
from entsoe import EntsoePandasClient
from dotenv import load_dotenv
import pandas as pd
import os
import time
from datetime import datetime
from pathlib import Path

load_dotenv()
client = EntsoePandasClient(api_key=os.getenv("ENTSOE_API_KEY"))

# Países con datos consistentes
COUNTRIES = ["DE", "FR", "ES", "IT", "PL", "SE", "NL", "BE", "AT", "CZ",
             "HU", "SK", "RO", "BG", "FI", "DK", "NO", "CH", "PT", "IE"]

# Últimos 12 meses
TODAY = datetime.utcnow()
DATES = [
    (TODAY.replace(day=1) - pd.DateOffset(months=i)).strftime("%Y-%m-01")
    for i in range(12)
]

@task(retries=3, retry_delay_seconds=30)
def fetch_and_save(country: str, date_str: str):
    start = pd.Timestamp(date_str, tz="Europe/Brussels")
    end = (start + pd.DateOffset(months=1)) - pd.Timedelta(seconds=1)

    try:
        print(f"→ Downloading {country} {start.strftime('%Y-%m')}...")
        data = client.query_load(country, start=start, end=end)
        df = pd.DataFrame(data) if not isinstance(data, pd.DataFrame) else data.copy()

        out_path = Path(f"data/entsoe/{country}/{start.year}")
        out_path.mkdir(parents=True, exist_ok=True)
        fname = out_path / f"{start.month:02}_load.parquet"
        df.to_parquet(fname)
        print(f"✅ Saved: {fname}")
    except Exception as e:
        print(f"❌ Failed for {country} {start.strftime('%Y-%m')}: {e}")
    finally:
        time.sleep(2)

@flow(name="batch-load-pipeline")
def batch_load():
    for country in COUNTRIES:
        for date_str in DATES:
            try:
                fetch_and_save.fn(country, date_str)
            except Exception as e:
                print(f"⚠️ Skipped {country} {date_str} due to fatal error: {e}")

if __name__ == "__main__":
    batch_load()
