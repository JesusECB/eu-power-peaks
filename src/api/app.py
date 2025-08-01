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

# app.py
FEATURES = ["hour", "temperature", "is_weekend", "is_holiday"]

@app.post("/predict")
def predict(input_data: InputData):
    data = input_data.dict()
    df = pd.DataFrame([data])

    # Filtra solo las columnas necesarias
    df = df[FEATURES]

    prediction = model.predict(df)[0]
    return {"prediction": prediction}
