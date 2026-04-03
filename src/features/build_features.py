from src.data.preprocess import preprocess_data

def load_data():
    df = preprocess_data()
    return df

def create_time_features(df):
    df = df.copy()
    
    df["year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.month
    df["week"] = df["Date"].dt.isocalendar().week.astype(int)
    df["day_of_week"] = df["Date"].dt.dayofweek
    
    return df

def create_lag_features(df):
    df = df.copy()
    
    df = df.sort_values(["Store", "Date"])
    
    df["lag_1"] = df.groupby("Store")["Weekly_Sales"].shift(1)
    df["lag_7"] = df.groupby("Store")["Weekly_Sales"].shift(7)
    
    return df

def create_rolling_features(df):
    df = df.copy()
    
    df["rolling_mean_4"] = (
        df.groupby("Store")["Weekly_Sales"]
        .transform(lambda x: x.shift(1).rolling(4).mean())
    )
    
    df["rolling_std_4"] = (
        df.groupby("Store")["Weekly_Sales"]
        .transform(lambda x: x.shift(1).rolling(4).std())
    )
    
    return df

def create_promo_features(df):
    df = df.copy()
    
    markdown_cols = ["MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]
    
    df["total_markdown"] = df[markdown_cols].sum(axis=1)
    
    df["has_promo"] = (df["total_markdown"] > 0).astype(int)
    
    return df

def create_interactions(df):
    df = df.copy()
    
    df["holiday_promo"] = df["IsHoliday"] * df["has_promo"]
    
    return df

def build_features():
    df = load_data()
    
    df = create_time_features(df)
    df = create_lag_features(df)
    df = create_rolling_features(df)
    df = create_promo_features(df)
    df = create_interactions(df)
    
    df = df.dropna()
    
    return df