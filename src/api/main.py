from fastapi import FastAPI
from src.api.schema import PredictionRequest
from src.api.predict import predict

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Demand Prediction API is running"}


@app.post("/predict")
async def get_prediction(request: PredictionRequest):
    result = await predict(request.dict())
    return {"predicted_weekly_sales": result}