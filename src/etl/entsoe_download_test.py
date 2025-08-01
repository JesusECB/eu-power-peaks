from entsoe import EntsoePandasClient
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()


client = EntsoePandasClient(api_key=os.getenv("ENTSOE_API_KEY"))

country_code = 'DE'  # Alemania

start = pd.Timestamp('2024-06-01', tz='Europe/Brussels')
end = pd.Timestamp('2024-06-07', tz='Europe/Brussels')

print("Requesting load data from ENTSO-E...")
load = client.query_load(country_code, start=start, end=end)

# Guardar en disco
os.makedirs("data/raw", exist_ok=True)
load.to_csv("data/raw/load_germany_june_week.csv")

print("Data saved to: data/raw/load_germany_june_week.csv")