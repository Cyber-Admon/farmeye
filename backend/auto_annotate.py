import os
from pathlib import Path
from PIL import Image

CURATED_DIR = Path("dataset/curated")
OUTPUT_DIR = Path("dataset/annotated")

CLASS_NAMES = [
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

CLASS_MAP = {name: i for i, name in enumerate(CLASS_NAMES)}


def generate_annotations():
    images_out = OUTPUT_DIR / "images"
    labels_out = OUTPUT_DIR / "labels"
    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    total = 0

    for class_name, class_id in CLASS_MAP.items():
        class_dir = CURATED_DIR / class_name
        if not class_dir.exists():
            print(f"[skip] {class_name}")
            continue

        images = list(class_dir.glob("*.jpg"))
        print(f"[{class_id}] {class_name} — {len(images)} images")

        for img_path in images:
            try:
                img = Image.open(img_path)
                w, h = img.size

                # Full image bounding box in YOLO format (cx, cy, w, h normalized)
                annotation = f"{class_id} 0.5 0.5 1.0 1.0\n"

                stem = img_path.stem
                label_path = labels_out / f"{stem}.txt"
                img_out_path = images_out / f"{stem}.jpg"

                label_path.write_text(annotation)
                img.save(img_out_path, "JPEG", quality=95)

                total += 1
            except Exception as e:
                print(f"[error] {img_path}: {e}")

    # Write data.yaml for YOLO training
    yaml_content = f"""train: ../dataset/annotated/images
val: ../dataset/annotated/images

nc: {len(CLASS_NAMES)}
names: {CLASS_NAMES}
"""
    (OUTPUT_DIR / "data.yaml").write_text(yaml_content)
    print(f"\nDone. {total} images annotated.")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_annotations()