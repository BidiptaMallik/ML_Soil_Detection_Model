import joblib
import numpy as np

crop_model = joblib.load("./models/crop_model.pkl")
crop_encoder = joblib.load("./models/crop_label_encoder.pkl")
crop_scaler = joblib.load("./models/crop_scaler.pkl")   # ✅ ADD THIS


def predict_crop(N, P, K, temperature, humidity, ph, rainfall):

    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

    # ✅ SCALE HERE (VERY IMPORTANT)
    features = crop_scaler.transform(features)

    prediction = crop_model.predict(features)

    return crop_encoder.inverse_transform(prediction)[0]