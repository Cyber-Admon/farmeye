import os
import time
from roboflow import Roboflow
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.getenv("ROBOFLOW_API_KEY")
WORKSPACE = "abdulmaliks-workspace-jii8q"
PROJECT = "farmeye-javot"
CURATED_DIR = Path("dataset/curated")

rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT)

for class_dir in sorted(CURATED_DIR.iterdir()):
    if not class_dir.is_dir():
        continue

    images = list(class_dir.glob("*.jpg"))
    print(f"\nUploading {len(images)} images for class: {class_dir.name}")

    for i, img_path in enumerate(images):
        success = False
        attempts = 0

        while not success and attempts < 3:
            try:
                project.upload(
                    image_path=str(img_path),
                    annotation_path=None,
                    split="train",
                    tag_names=[class_dir.name],
                    batch_name=class_dir.name,
                )
                success = True
                if i % 50 == 0:
                    print(f"  [{i}/{len(images)}] uploaded")
            except Exception as e:
                attempts += 1
                print(f"  [retry {attempts}] {img_path.name}: {e}")
                time.sleep(3)

        time.sleep(0.3)

print("\nUpload complete.")