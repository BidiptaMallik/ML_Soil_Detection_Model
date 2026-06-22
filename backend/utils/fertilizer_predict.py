import joblib
import numpy as np

model = joblib.load("./models/fertilizer_model.pkl")
crop_encoder = joblib.load("./models/fertilizers_crop_encoder.pkl")
fert_encoder = joblib.load("./models/fertilizer_encoder.pkl")


# ---------------------------
# SAFE CROP ENCODING
# ---------------------------
def safe_crop_encode(crop):
    if crop in crop_encoder.classes_:
        return crop_encoder.transform([crop])[0]

    # fallback to most common class
    return 0


# ---------------------------
# PREDICT FUNCTION
# ---------------------------
def predict_fertilizer(temp, humidity, crop, N, K, P):

    crop_enc = safe_crop_encode(crop)

    input_data = np.array([[
        temp,
        humidity,
        crop_enc,
        N,
        K,
        P
    ]])

    pred = model.predict(input_data)[0]

    return fert_encoder.inverse_transform([pred])[0]