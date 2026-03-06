from fastapi.testclient import TestClient
from app.main import app
import io
from PIL import Image

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the ML Model API"}

def test_predict():
    # Create a dummy image
    image = Image.new('RGB', (224, 224), color = 'red')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    # Test file upload endpoint
    response = client.post("/predict", files={"file": ("test.jpg", img_byte_arr, "image/jpeg")})
    assert response.status_code == 200
    result = response.json()
    assert "prediction_class" in result
    assert "confidence" in result
    assert isinstance(result["prediction_class"], int)
    assert isinstance(result["confidence"], float)
