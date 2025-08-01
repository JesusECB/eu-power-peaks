import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
from pathlib import Path
import numpy as np

DATA_PATH = Path("data/features/all_countries_features.parquet")
MODEL_PATH = Path("models/lgbm_model.pkl")

print("📥 Loading data...")
df = pd.read_parquet(DATA_PATH)

# Focus on one country for now, e.g., Germany
df = df[df["country"] == "DE"]

# Drop rows with NaNs just in case
df = df.dropna()

# Define target and features
TARGET = "load_mw"
FEATURES = ["hour", "dayofweek", "month", "weekend"]

X = df[FEATURES]
y = df[TARGET]

print("✂️ Splitting train/test...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

print("🧠 Training LightGBM model...")
model = lgb.LGBMRegressor(n_estimators=500, learning_rate=0.05)
model.fit(X_train, y_train)

print("📊 Evaluating...")
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
print(f"✅ RMSE: {rmse:.2f}")
print(f"✅ MAE: {mae:.2f}")

print(f"💾 Saving model to {MODEL_PATH}")
joblib.dump(model, MODEL_PATH)
