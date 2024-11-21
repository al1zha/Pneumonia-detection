# Backend: FastAPI
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
from PIL import Image
import os
import shutil
import tempfile

app = FastAPI()

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the tflite model
model_path = "main.tflite"
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']
output_shape = output_details[0]['shape']
input_dtype = input_details[0]['dtype']
output_dtype = output_details[0]['dtype']

# Define class names
class_names = ['Covid', 'Viral Pneumonia', 'Normal']

@app.get("/")
async def main():
    return HTMLResponse(content=open("static/index.html").read())

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Create a temporary directory to save the image
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Save the uploaded image in the temporary directory
            temp_image_path = os.path.join(tmpdirname, file.filename)
            with open(temp_image_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            # Open the saved image
            image = Image.open(temp_image_path)

            # Ensure image has 3 channels (RGB)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Resize the image to match the model input
            image = image.resize((input_shape[1], input_shape[2]))
            image = np.array(image, dtype=np.float32)
            image /= 255.0
            image = np.expand_dims(image, axis=0)

            # Set the input tensor
            interpreter.set_tensor(input_details[0]['index'], image.astype(input_dtype))
            interpreter.invoke()

            # Get the output tensor
            predictions = interpreter.get_tensor(output_details[0]['index'])
            predicted_class_index = np.argmax(predictions, axis=1)
            predicted_class_name = class_names[predicted_class_index[0]]

            # Return prediction result
            response = {
                "prediction": predicted_class_name,
                "probabilities": predictions.tolist(),
                "image_url": ""  # Image is not saved permanently
            }

            return JSONResponse(response)

    except Exception as e:
        return JSONResponse({"error": str(e)})