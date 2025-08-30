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
    password="password",# your DB password
    database="cropdb"   # your DB name
)

cursor = db.cursor()

# Make sure you have a table like:
# CREATE TABLE predictions (
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   filename VARCHAR(255),
#   prediction VARCHAR(100),
#   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

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
    class_names = ["Apple___healthy", "Apple___scab", "Tomato___mosaic_virus"]  # <-- replace with your dataset classes
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
