import pandas as pd
from src.features.build_features import build_features

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib

def load_data():
    df = build_features()
    return df

def split_features_target(df):
    X = df.drop(columns=["Weekly_Sales", "Date", "temp_category"])
    y = df["Weekly_Sales"]
    
    return X, y

def encode_features(X):
    X = pd.get_dummies(X, columns=["size_category",  "Type"], drop_first=True)
    return X

def time_split(df):
    split_date = "2012-01-01"
    
    train_df = df[df["Date"] < split_date]
    test_df = df[df["Date"] >= split_date]
    
    return train_df, test_df

def train_model(X_train, y_train):
    model = XGBRegressor(
    n_estimators=700,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
    
    model.fit(X_train, y_train)
    
    return model

def evaluate(model, X_test, y_test):
    preds = model.predict(X_test)
    
    # Reverse log transform
    preds = np.expm1(preds)
    
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    
    print(f"MAE: {mae}")
    print(f"RMSE: {rmse}")
    
    return preds

def feature_importance(model, X):
    importance = pd.Series(model.feature_importances_, index=X.columns)
    importance = importance.sort_values(ascending=False)
    
    print("\nTop Features:")
    print(importance.head(10))

def main():
    df = load_data()
    
    train_df, test_df = time_split(df)
    
    # Remove invalid targets
    train_df = train_df[train_df["Weekly_Sales"] > 0]

    X_train, y_train = split_features_target(train_df)
    X_test, y_test = split_features_target(test_df)
    
    # Encode
    X_train = encode_features(X_train)
    X_test = encode_features(X_test)
    
    # Align columns (important for safety)
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)
    
    # LOG TRANSFORM TARGET
    y_train = np.log1p(y_train.clip(lower=0))
    
    # Train
    model = train_model(X_train, y_train)
    
    # Evaluate
    preds = evaluate(model, X_test, y_test)
    
    # Feature importance
    feature_importance(model, X_train)
    
    # Save model
    joblib.dump(model, "models/xgb_model_v7.pkl")
    
    print("\nModel training complete and saved.")

if __name__ == "__main__":
    main()