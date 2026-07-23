import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

os.environ["KAGGLE_USERNAME"] = os.getenv("KAGGLE_USERNAME")
os.environ["KAGGLE_KEY"] = os.getenv("KAGGLE_KEY")

import kaggle

kaggle.api.authenticate()

kaggle.api.dataset_create_new(
    folder="dataset/annotated",
    dir_mode="zip",
    convert_to_csv=False,
)

print("Dataset uploaded to Kaggle.")