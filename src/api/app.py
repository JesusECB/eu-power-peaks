from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Power Demand Prediction API")

# Load model
MODEL_PATH = "models/lgbm_model.pkl"
model = joblib.load(MODEL_PATH)

# Input schema
class InputData(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    temperature: float
    is_weekend: int
    is_holiday: int

@app.get("/")
def root():
    return {"message": "⚡ Ready to predict power demand"}

@app.post("/predict")
def predict(data: InputData):
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)[0]
    return {"predicted_load_MW": round(prediction, 2)}
