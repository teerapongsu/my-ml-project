from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np
import os
import io
from PIL import Image

app = FastAPI(title="ML Model API")

# Update path to match uploaded resnet50.onnx
MODEL_PATH = os.path.join(os.path.dirname(__file__), "resnet50.onnx")

session = None
try:
    if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 0:
        session = ort.InferenceSession(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print("Model file not found or empty. Running in mock mode.")
except Exception as e:
    print(f"Error loading model: {e}. Running in mock mode.")

class PredictionResponse(BaseModel):
    prediction_class: int
    confidence: float

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    # ResNet-50 requires [1, 3, 224, 224] input
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize((224, 224))
    img_data = np.array(img).astype('float32')
    
    # Normalize
    mean = np.array([0.485, 0.456, 0.406]).astype('float32')
    std = np.array([0.229, 0.224, 0.225]).astype('float32')
    img_data = (img_data / 255.0 - mean) / std
    
    # Transpose HWC to CHW and add batch dimension
    img_data = np.transpose(img_data, (2, 0, 1))
    img_data = np.expand_dims(img_data, axis=0)
    return img_datas

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML Model API"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    
    if session is None:
        return {"prediction_class": 0, "confidence": 0.99}
    
    try:
        input_data = preprocess_image(image_bytes)
        input_name = session.get_inputs()[0].name
        
        # Run inference
        result = session.run(None, {input_name: input_data})
        output = result[0][0] # Output is [1, 1000]
        
        # Apply softmax to get confidence
        exp_preds = np.exp(output - np.max(output))
        softmax_preds = exp_preds / np.sum(exp_preds)
        
        pred_class = np.argmax(softmax_preds)
        confidence = softmax_preds[pred_class]
        
        return {"prediction_class": int(pred_class), "confidence": float(confidence)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
