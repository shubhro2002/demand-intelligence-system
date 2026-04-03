import pandas as pd
from src.data.load_data import load_all_data

def load_and_merge():
    data = load_all_data()
    
    train = data["train"]
    features = data["features"]
    stores = data["stores"]
    
    train["Date"] = pd.to_datetime(train["Date"])
    features["Date"] = pd.to_datetime(features["Date"])
    
    df = train.merge(features.drop(columns=["IsHoliday"]), on=["Store", "Date"], how="left")
    df = df.merge(stores, on="Store", how="left")
    
    return df

def create_size_bucket(df):
    def bucket(size):
        if size < 100000:
            return "small"
        elif size < 180000:
            return "medium"
        else:
            return "large"
    
    df["size_category"] = df["Size"].apply(bucket)
    return df

def basic_cleaning(df):
    df = df.copy()
    
    # Ensure correct types
    df["IsHoliday"] = df["IsHoliday"].astype(int)
    
    return df

def preprocess_data():
    df = load_and_merge()
    
    # Handle missing values
    markdown_cols = ["MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]
    df[markdown_cols] = df[markdown_cols].fillna(0)
    
    df = df.sort_values(["Store", "Date"])
    
    df[["CPI", "Unemployment", "Temperature", "Fuel_Price"]] = (
        df.groupby("Store")[["CPI", "Unemployment", "Temperature", "Fuel_Price"]]
          .ffill()
    )
    
    df = df.fillna(0)
    
    # Feature creation
    df = create_size_bucket(df)
    
    # Cleanup
    df = basic_cleaning(df)
    
    return df