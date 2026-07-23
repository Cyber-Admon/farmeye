from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.detector import detect_diseases
from app.services.advisor import get_recommendations

router = APIRouter()


@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG and PNG images are supported")

    image_bytes = await file.read()

    detections = detect_diseases(image_bytes)

    if not detections:
        return {
            "detections": [],
            "recommendations": "No diseases detected. The plant appears healthy.",
        }

    recommendations = await get_recommendations(detections)

    return {
        "detections": detections,
        "recommendations": recommendations,
    }