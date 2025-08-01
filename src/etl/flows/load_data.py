from prefect import flow, task
from entsoe import EntsoePandasClient
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

@task
def fetch_load_data(country_code: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    client = EntsoePandasClient(api_key=os.getenv("ENTSOE_API_KEY"))
    data = client.query_load(country_code, start=start, end=end)
    return data

@task
def save_to_parquet(data: pd.Series, output_path: str):
    df = data.copy()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path)
    print(f"Saved to {output_path}")

@flow
def load_pipeline(country_code: str, start_date: str, end_date: str):
    start = pd.Timestamp(start_date, tz='Europe/Brussels')
    end = pd.Timestamp(end_date, tz='Europe/Brussels')

    series = fetch_load_data(country_code, start, end)
    filename = f"data/entsoe/{country_code}/{start.year}/{start.month:02}_load.parquet"
    save_to_parquet(series, filename)

# Test run
if __name__ == "__main__":
    load_pipeline("DE", "2024-06-01", "2024-06-07")
