import pandas as pd
import numpy as np
import joblib

from datetime import datetime

# Load model
model = joblib.load("models/xgb_model_v7.pkl")


def preprocess_input(data):
    df = pd.DataFrame([data])
    
    # Date features
    df["Date"] = pd.to_datetime(df["Date"])
    df["year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.month
    df["week"] = df["Date"].dt.isocalendar().week.astype(int)
    df["day_of_week"] = df["Date"].dt.dayofweek
    
    # Size bucket
    def size_bucket(size):
        if size < 100000:
            return "small"
        elif size < 180000:
            return "medium"
        else:
            return "large"
    
    df["size_category"] = df["Size"].apply(size_bucket)
    
    # Promo features
    markdown_cols = ["MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]
    df["total_markdown"] = df[markdown_cols].sum(axis=1)
    df["has_promo"] = (df["total_markdown"] > 0).astype(int)
    
    # Dummy encoding
    df = pd.get_dummies(df, columns=["Type", "size_category"], drop_first=True)
    
    # Drop unused
    df = df.drop(columns=["Date"])
    
    return df


def predict(data: dict):
    df = preprocess_input(data)
    
    # Align columns (IMPORTANT)
    model_features = model.get_booster().feature_names
    df = df.reindex(columns=model_features, fill_value=0)
    
    pred = model.predict(df)
    
    # Reverse log transform
    pred = np.expm1(pred)
    
    return float(pred[0])