import onnxruntime as rt
import numpy as np
from PIL import Image

session = rt.InferenceSession("./models/soil_model.onnx")

class_names = {
    0: "Alluvial_Soil",
    1: "Arid_Soil",
    2: "Black_Soil",
    3: "Laterite_Soil",
    4: "Mountain_Soil",
    5: "Red_Soil",
    6: "Yellow_Soil"
}

def predict_soil(img_path):
    img = Image.open(img_path).resize((256, 256))
    img_array = np.array(img).astype(np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    input_name = session.get_inputs()[0].name
    prediction = session.run(None, {input_name: img_array})
    predicted_class = np.argmax(prediction[0])
    return class_names[predicted_class]