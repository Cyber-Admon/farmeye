import os
import shutil
import hashlib
from pathlib import Path
from PIL import Image

SOURCE_DIR = Path("dataset/PlantVillage")
OUTPUT_DIR = Path("dataset/curated")
IMAGE_SIZE = (640, 640)

ALLOWED_CLASSES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy",
]

def get_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def curate():
    seen_hashes = set()
    total_copied = 0
    total_skipped = 0

    for class_name in ALLOWED_CLASSES:
        source_class_dir = SOURCE_DIR / class_name
        output_class_dir = OUTPUT_DIR / class_name
        output_class_dir.mkdir(parents=True, exist_ok=True)

        if not source_class_dir.exists():
            print(f"[skip] Folder not found: {class_name}")
            continue

        images = list(source_class_dir.glob("*.jpg")) + list(source_class_dir.glob("*.JPG")) + list(source_class_dir.glob("*.png"))

        for img_path in images:
            file_hash = get_hash(img_path)

            if file_hash in seen_hashes:
                total_skipped += 1
                continue

            seen_hashes.add(file_hash)

            try:
                img = Image.open(img_path).convert("RGB")
                img = img.resize(IMAGE_SIZE, Image.LANCZOS)
                out_path = output_class_dir / f"{file_hash}.jpg"
                img.save(out_path, "JPEG", quality=95)
                total_copied += 1
            except Exception as e:
                print(f"[error] {img_path}: {e}")

    print(f"\nDone. Copied: {total_copied} | Duplicates skipped: {total_skipped}")
    print(f"Curated dataset saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    curate()