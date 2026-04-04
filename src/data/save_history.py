from src.features.build_features import build_features

df = build_features()

history = df[["Store", "Dept", "Date", "Weekly_Sales"]].copy()
history.to_csv("data/processed/history.csv", index=False)