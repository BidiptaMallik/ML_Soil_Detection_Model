from fastapi import FastAPI, UploadFile, File,Form
import shutil
import os
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from utils.soil_predict import predict_soil
from utils.crop_predict import predict_crop
from utils.fertilizer_predict import predict_fertilizer
from services.weather_service import get_weather

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# LOAD SCALER
# =========================
crop_scaler = joblib.load("models/crop_scaler.pkl")


@app.get("/")
def home():
    return {"message": "Smart Agriculture API Running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/predict")
async def predict(
    city: str = Form(...),
    N: int = Form(...),
    P: int = Form(...),
    K: int = Form(...),
    ph: float = Form(...),
    file: UploadFile = File(...)
):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    soil_type = predict_soil(file_path)

    temperature, humidity, rainfall = get_weather(city)

    # ✅ CLEAN CALL (NO SCALING HERE)
    recommended_crop = predict_crop(
        N, P, K,
        temperature,
        humidity,
        ph,
        rainfall
    )

    fertilizer = predict_fertilizer(
        temperature,
        humidity,
        recommended_crop,
        N,
        K,
        P
    )

    return {
        "soil_type": soil_type,
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "recommended_crop": recommended_crop,
        "fertilizer": fertilizer
    }