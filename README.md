This project is a **COVID-19 Chest X-ray Classifier** built using FastAPI, TensorFlow Lite, and a pretrained TFLite model for classifying chest X-rays into one of three categories: COVID-19, Viral Pneumonia, or Normal. The backend API accepts an image upload, processes the image, and uses the TFLite model to predict the class of the X-ray.

**Key Features:**

1. **Image Upload and Processing**:
- Users can upload chest X-ray images via the /predict/ endpoint.
- The image is preprocessed to ensure it matches the model's input size and format.
2. **TensorFlow Lite Model Inference**:
- The system uses a TensorFlow Lite model (main.tflite) to make predictions.
- The model takes the preprocessed image, performs inference, and returns the predicted class (COVID-19, Viral Pneumonia, or Normal).
3. **Class Prediction and Probabilities**:
- The API returns the predicted class and the associated probabilities for each class.
- The results are provided in a JSON response for easy integration with frontend applications.
4. **CORS Support**:
   1. The application allows Cross-Origin Resource Sharing (CORS), enabling it to communicate with frontend applications hosted on different domains.
4. **Static File Support**:
- The FastAPI application serves static files (like HTML, CSS, and JavaScript) to provide a frontend interface for interacting with the API.

**Endpoints:**

- **GET /**: Serves the static HTML page as the frontend interface.
- **POST /predict/**: Accepts an image file and returns the class prediction along with the prediction probabilities.

**Model Inference Process:**

1. **Image Upload**: The user uploads an image file (X-ray image).
1. **Image Preprocessing**:
   1. The image is converted to RGB format (if necessary) and resized to match the model's expected input shape.
   1. The pixel values are normalized to a range of [0, 1].
1. **Model Inference**: The processed image is fed into the TensorFlow Lite model for prediction.
1. **Response**: The API returns a JSON object containing the predicted class and the probabilities of each class.

**Stack:**

- **Backend**: FastAPI for API handling.
- **Model Inference**: TensorFlow Lite for performing inference with a pre-trained model.
- **Static Files**: Used for serving a frontend interface.
- **CORS Middleware**: Enabled to allow cross-origin requests.

This API provides an efficient solution for chest X-ray classification, enabling easy integration with medical imaging systems or web applications for automated diagnosis.
