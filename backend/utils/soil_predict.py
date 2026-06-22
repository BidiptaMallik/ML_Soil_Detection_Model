import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image


model = tf.keras.models.load_model("./models/soil_model.keras")

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

    img = image.load_img(img_path, target_size=(256, 256))

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)

    img_array = img_array / 255.0

    prediction = model.predict(img_array)

    predicted_class = np.argmax(prediction)

    return class_names[predicted_class]