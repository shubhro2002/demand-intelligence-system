import pandas as pd
import numpy as np
import joblib
from src.data.fetch_weather import get_weather
from src.config.store_locations import STORE_LOCATIONS

# -------------------------------
# Load Model
# -------------------------------
model = joblib.load("models/xgb_model_v7.pkl")

# -------------------------------
# Load History (Mini Feature Store)
# -------------------------------
history_df = pd.read_csv("data/processed/history.csv")
history_df["Date"] = pd.to_datetime(history_df["Date"])


# -------------------------------
# Lag Retrieval Function
# -------------------------------
def get_lag_features(store, dept, date):
    df = history_df.copy()
    
    df = df[
        (df["Store"] == store) &
        (df["Dept"] == dept) &
        (df["Date"] < date)
    ].sort_values("Date", ascending=False)
    
    # Handle edge cases
    lag_1 = df.iloc[0]["Weekly_Sales"] if len(df) > 0 else 0
    lag_2 = df.iloc[1]["Weekly_Sales"] if len(df) > 1 else lag_1
    lag_3 = df.iloc[2]["Weekly_Sales"] if len(df) > 2 else lag_2
    
    return lag_1, lag_2, lag_3


# -------------------------------
# Preprocessing
# -------------------------------
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


# -------------------------------
# Prediction Function
# -------------------------------
async def predict(data: dict):
    date = pd.to_datetime(data["Date"])
    
    # -------------------------------
    # AUTO FETCH LAG FEATURES
    # -------------------------------
    lag_1, lag_2, lag_3 = get_lag_features(
        data["Store"],
        data["Dept"],
        date
    )
    
    data["lag_1"] = lag_1
    data["lag_2"] = lag_2
    data["lag_3"] = lag_3
    
    # -------------------------------
    # FETCH WEATHER (ASYNC)
    # -------------------------------
    location = STORE_LOCATIONS.get(data["Store"], STORE_LOCATIONS[1])
    
    weather_data = await get_weather(location["lat"], location["lon"], str(date))
    
    data["Temperature"] = weather_data["Temperature"]    
    # -------------------------------
    # PREPROCESS + PREDICT
    # -------------------------------
    df = preprocess_input(data)
    
    model_features = model.get_booster().feature_names
    df = df.reindex(columns=model_features, fill_value=0)
    
    pred = model.predict(df)
    pred = np.expm1(pred)
    
    return float(pred[0])