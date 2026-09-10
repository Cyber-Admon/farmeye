# FarmEye

GenAI-powered crop disease detection for smallholder farmers growing tomatoes
and peppers. Upload a photo of a plant leaf through any browser and get an
instant diagnosis with plain-language treatment recommendations, no app
install and no specialist hardware required.

**Live demo:** https://farmeye-gray.vercel.app

## About

Smallholder farmers across Nigeria and Sub-Saharan Africa lose a significant
share of their harvests to crop disease every year, largely because
agricultural extension services are severely understaffed (extension
officer-to-farmer ratios as poor as 1:1,172 in some regions) and expert
diagnosis is out of reach during the growing season.

FarmEye addresses this with a lightweight object detection model served
through a web API, paired with a generative AI layer that turns a raw
detection into actionable, farmer-readable advice.

This project was built as a final year Computer Science project at Osun
State University, Osogbo, supervised by Dr. K.O. Jimoh. The accompanying
project report covers the full literature review, methodology, and
evaluation in detail.

## How it works

1. A farmer uploads a photo of a tomato or pepper leaf through the web
   frontend.
2. The backend runs the image through a YOLOv11 Nano model, fine-tuned to
   detect twelve disease and health status classes.
3. If a disease is detected above the confidence threshold, the backend
   calls the OpenAI GPT-4o Mini API to generate a contextual treatment
   recommendation in plain language.
4. The frontend renders the detected bounding boxes on the image and
   displays the diagnosis and recommendation to the farmer.

## Model performance

Evaluated on a held-out validation set of 4,124 images:

| Metric        | Value             |
|---------------|-------------------|
| mAP@0.5        | 99.4%             |
| mAP@0.5:0.95    | 99.2%             |
| Precision       | 99.0%             |
| Recall          | 98.0%             |
| Inference time   | 2.2 ms per image  |
| Model size       | 5.5 MB            |

All twelve classes individually exceed 0.989 mAP@0.5. Real-world testing on
farmer-style outdoor photos surfaced a domain gap versus the lab-style
training images; see the project report (Section 4.6) for details and
planned mitigations.

## Disease classes

- Pepper Bell Bacterial Spot
- Pepper Bell Healthy
- Tomato Bacterial Spot
- Tomato Early Blight
- Tomato Late Blight
- Tomato Leaf Mold
- Tomato Septoria Leaf Spot
- Tomato Spider Mites
- Tomato Target Spot
- Tomato Yellow Leaf Curl Virus
- Tomato Mosaic Virus
- Tomato Healthy

## Tech stack

**Frontend:** React 18, TypeScript
**Backend:** FastAPI, Python, Uvicorn
**Model:** YOLOv11 Nano (Ultralytics), fine-tuned via transfer learning from
COCO weights
**Recommendations:** OpenAI GPT-4o Mini
**Training:** Google Colaboratory, NVIDIA Tesla T4 GPU
**Deployment:** Contabo VPS (Ubuntu 24.04) for the backend, Vercel for the
frontend, ngrok static domain for the public API tunnel

## Project structure

```
farmeye/
├── frontend/               React + TypeScript app
└── backend/
    ├── app/
    │   ├── routes/
    │   │   └── detection.py    API endpoint for image upload and detection
    │   └── services/
    │       ├── detector.py     YOLOv11 inference
    │       └── advisor.py      OpenAI GPT-4o Mini recommendations
    ├── dataset/                 Not committed, see dataset/README.md
    ├── weights/
    │   └── best.pt               Trained model weights
    ├── main.py
    └── .env                     OPENAI_API_KEY, MODEL_PATH
```

## Getting started

### Backend

```
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Create a `.env` file in `backend/` with:

```
OPENAI_API_KEY=your_openai_api_key
MODEL_PATH=weights/best.pt
```

Run the API:

```
uvicorn main:app --reload --port 8004
```

### Frontend

```
cd frontend
npm install
npm run dev
```

Point the frontend at your backend URL (local or the deployed ngrok/VPS
address) in its environment configuration.

### Dataset

The training dataset is not committed to this repository. See
[`backend/dataset/README.md`](backend/dataset/README.md) for the Kaggle
source, the twelve classes used, and the preprocessing steps needed to
reproduce the curated training set.

## Deployment

The production backend runs on a Contabo VPS (Ubuntu 24.04) as a systemd
service (`farmeye.service`) on port 8004, with a static ngrok tunnel
(`farmeye-tunnel.service`) exposing it publicly. The frontend is deployed on
Vercel. Both backend services are systemd-managed so they restart
automatically after a reboot or crash.

## Known limitations

The model was trained entirely on the PlantVillage dataset, which consists
of lab-style images with plain backgrounds. Testing against real-world,
farmer-captured photos revealed a domain gap: outdoor backgrounds, mixed
plant structures, and non-lab lighting reduce detection confidence and can
produce misclassifications. Expanding the training set with field-condition
images is the top priority for improving real-world reliability (see the
project report, Section 5.2, for the full set of recommendations).

## Author

Muraina Babatunde Idris (2022/40956)
Department of Computer Science, Osun State University, Osogbo
Supervised by Dr. K.O. Jimoh