import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = Path("data/raw")


def load_csv(file_name: str) -> pd.DataFrame:
    file_path = DATA_DIR / file_name
    
    if not file_path.exists():
        raise FileNotFoundError(f"{file_name} not found in {DATA_DIR}")
    
    df = pd.read_csv(file_path)
    logger.info(f"{file_name} loaded successfully with shape {df.shape}")
    
    return df


def load_all_data():
    data = {
        "train": load_csv("train.csv"),
        "test": load_csv("test.csv"),
        "features": load_csv("features.csv"),
        "stores": load_csv("stores.csv")
    }
    return data


def validate_train(df):
    required_cols = ["Store", "Date", "Weekly_Sales"]
    missing = [col for col in required_cols if col not in df.columns]
    
    if missing:
        raise ValueError(f"Train missing columns: {missing}")
    
    logger.info("Train data validation passed")


def main():
    logger.info("🔄 Loading all datasets...")
    data = load_all_data()
    
    logger.info("🔍 Validating train dataset...")
    validate_train(data["train"])
    
    for name, df in data.items():
        logger.info(f"{name} shape: {df.shape}")
    
    logger.info("✅ Data ingestion complete")


if __name__ == "__main__":
    main()