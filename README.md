# ML Project Lab 🧪

Welcome to the ML Model Deployment Lab!

## 📂 Project Structure
```text
my-ml-project/
├── app/
│   ├── main.py        # โค้ด FastAPI
│   └── model.onnx     # ไฟล์โมเดลที่ทำ Quantization แล้ว
├── tests/
│   └── test_app.py    # ไฟล์ข้อสอบ 
├── Dockerfile         # ใบสั่งต่อกล่อง Docker
├── requirements.txt   # รายชื่อ Library (ต้องมี fastapi, uvicorn, onnxruntime, pytest, httpx)
└── .github/workflows/
    └── main.yml       # ใบสั่งงานหุ่นยนต์ (จากข้อ 3)
```

## 🚀 Setup and Run
1. **Install dependencies:**  
   `pip install -r requirements.txt`
2. **Run API Locally:**  
   `uvicorn app.main:app --reload`
3. **Run Tests:**  
   `PYTHONPATH=. pytest tests/`
4. **Build Docker Image:**  
   `docker build -t my-ml-app .`
5. **Run Docker Container:**  
   `docker run -p 8000:8000 my-ml-app`
