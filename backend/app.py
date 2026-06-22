from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import shutil
import os
import joblib
import numpy as np
import traceback
from fastapi.middleware.cors import CORSMiddleware
from utils.soil_predict import predict_soil
from utils.crop_predict import predict_crop
from utils.fertilizer_predict import predict_fertilizer
from services.weather_service import get_weather

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ml-soil-detection-model-2-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

crop_scaler = joblib.load("models/crop_scaler.pkl")

@app.get("/")
def home():
    return {"message": "Smart Agriculture API Running"}

@app.post("/predict")
async def predict(
    city: str = Form(...),
    N: int = Form(...),
    P: int = Form(...),
    K: int = Form(...),
    ph: float = Form(...),
    file: UploadFile = File(...)
):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("✅ File saved:", file_path)

        soil_type = predict_soil(file_path)
        print("✅ Soil type:", soil_type)

        temperature, humidity, rainfall = get_weather(city)
        print("✅ Weather:", temperature, humidity, rainfall)

        recommended_crop = predict_crop(N, P, K, temperature, humidity, ph, rainfall)
        print("✅ Crop:", recommended_crop)

        fertilizer = predict_fertilizer(temperature, humidity, recommended_crop, N, K, P)
        print("✅ Fertilizer:", fertilizer)

        return {
            "soil_type": soil_type,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "recommended_crop": recommended_crop,
            "fertilizer": fertilizer
        }

    except Exception as e:
        print("❌ ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))