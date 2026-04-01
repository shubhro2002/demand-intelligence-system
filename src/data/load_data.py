import pandas as pd
from pathlib import Path
import logging

# -------------------------------
# Logging Configuration
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# Path Configuration (FIXED)
# -------------------------------
# This ensures paths work from scripts, notebooks, APIs, anywhere
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"


# -------------------------------
# Generic CSV Loader
# -------------------------------
def load_csv(file_name: str) -> pd.DataFrame:
    file_path = DATA_DIR / file_name
    
    if not file_path.exists():
        raise FileNotFoundError(f"{file_name} not found in {DATA_DIR}")
    
    df = pd.read_csv(file_path)
    logger.info(f"{file_name} loaded successfully with shape {df.shape}")
    
    return df


# -------------------------------
# Load All Datasets
# -------------------------------
def load_all_data():
    data = {
        "train": load_csv("train.csv"),
        "test": load_csv("test.csv"),
        "features": load_csv("features.csv"),
        "stores": load_csv("stores.csv")
    }
    return data


# -------------------------------
# Validation
# -------------------------------
def validate_train(df: pd.DataFrame):
    required_cols = ["Store", "Date", "Weekly_Sales"]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Train missing columns: {missing_cols}")
    
    logger.info("Train data validation passed")


# -------------------------------
# Main Entry Point
# -------------------------------
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