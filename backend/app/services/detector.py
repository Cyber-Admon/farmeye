import os
import io
from PIL import Image

MODEL_PATH = os.getenv("MODEL_PATH", "weights/best.pt")
print(f"[detector] Looking for model at: {os.path.abspath(MODEL_PATH)}")
USE_DUMMY = not os.path.exists(MODEL_PATH)

model = None

if not USE_DUMMY:
    try:
        from ultralytics import YOLO
        model = YOLO(MODEL_PATH)
        print(f"[detector] Model loaded from {MODEL_PATH}")
    except Exception as e:
        print(f"[detector] Failed to load model: {e}. Falling back to dummy.")
        USE_DUMMY = True
else:
    print("[detector] No weights found. Running in dummy mode.")


def detect_diseases(image_bytes: bytes) -> list[dict]:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_width, img_height = image.size

    if USE_DUMMY:
        return _dummy_detections(img_width, img_height)

    results = model(image, conf=0.15, iou=0.45)
    detections = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append({
                "class_name": result.names[int(box.cls)],
                "confidence": round(float(box.conf), 4),
                "bbox": {
                    "x1": round(x1),
                    "y1": round(y1),
                    "x2": round(x2),
                    "y2": round(y2),
                },
                "image_width": img_width,
                "image_height": img_height,
            })

    return detections


def _dummy_detections(img_width: int, img_height: int) -> list[dict]:
    return [
        {
            "class_name": "Tomato_Leaf_Early_Blight",
            "confidence": 0.91,
            "bbox": {"x1": 50, "y1": 60, "x2": 220, "y2": 200},
            "image_width": img_width,
            "image_height": img_height,
        },
        {
            "class_name": "Tomato_Leaf_Late_Blight",
            "confidence": 0.78,
            "bbox": {"x1": 280, "y1": 100, "x2": 450, "y2": 300},
            "image_width": img_width,
            "image_height": img_height,
        },
    ]