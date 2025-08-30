from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import os
import pymysql
from datetime import datetime
from tensorflow.keras.preprocessing import image

# -------------------------
# Flask setup
# -------------------------
app = Flask(__name__)
CORS(app)  # allow frontend (React) to call backend

# -------------------------
# Load trained model
# -------------------------
MODEL_PATH = "model/disease_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# (You must use the same image size used in training)
IMG_SIZE = 128  

# Database setup 

db = pymysql.connect(
    host="localhost",   # or your DB host
    user="root",        # your DB username
    password="ShiroBeCutefr!!",# your DB password
    database="cropdb"   # your DB name
)

cursor = db.cursor()



# Helper: preprocess image

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# API Routes

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save temporarily
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

    # Preprocess & predict
    img_array = preprocess_image(file_path)
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]

    # Map prediction to class name
    class_names = ["Pepper__bell___Bacterial_spot",
                    "Pepper__bell___healthy",
                    "Potato___Early_blight",
                    "Potato___healthy",
                    "Potato___Late_blight",
                    "Tomato__Target_Spot",
                    "Tomato__Tomato_mosaic_virus",
                    "Tomato__Tomato_YellowLeaf__Curl_Virus",
                    "Tomato_Bacterial_spot",
                    "Tomato_Early_blight"
                    "Tomato_healthy"
                    "Tomato_Late_blight"
                    "Tomato_Leaf_Mold",
                    "Tomato_Septoria_leaf_spot",
                    "Tomato_Spider_mites_Two_spotted_spider_mite"

                    ]  # <-- replace with your dataset classes
    result = class_names[predicted_class]

    # Store in DB
    cursor.execute("INSERT INTO predictions (filename, prediction) VALUES (%s, %s)", (file.filename, result))
    db.commit()

    return jsonify({"filename": file.filename, "prediction": result})

@app.route("/history", methods=["GET"])
def history():
    cursor.execute("SELECT id, filename, prediction, created_at FROM predictions ORDER BY created_at DESC LIMIT 20")
    rows = cursor.fetchall()
    history = [
        {"id": r[0], "filename": r[1], "prediction": r[2], "created_at": str(r[3])}
        for r in rows
    ]
    return jsonify(history)

# Run server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
