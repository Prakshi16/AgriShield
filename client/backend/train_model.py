import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os

# ---------------------
# Paths
# ---------------------
dataset_dir = "C:/Users/Lenovo/Desktop/dataset"   # <-- path to PlantVillage dataset
model_path = "model/disease_model.h5"
os.makedirs("model", exist_ok=True)

# ---------------------
# Parameters
# ---------------------
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 10

# ---------------------
# Data Generators
# ---------------------
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_ds = datagen.flow_from_directory(
    dataset_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_ds = datagen.flow_from_directory(
    dataset_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# ---------------------
# Build Model
# ---------------------
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(train_ds.num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# ---------------------
# Train Model
# ---------------------
history = model.fit(train_ds,
                    validation_data=val_ds,
                    epochs=EPOCHS)

# ---------------------
# Save Model
# ---------------------
model.save(model_path)

print(f"✅ Model trained and saved at {model_path}")
