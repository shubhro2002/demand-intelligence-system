# Demand Intelligence System

An end-to-end **production-style machine learning system** for forecasting retail demand using dynamic feature engineering, asynchronous external data integration, and real-time inference.

---

## Overview

This project goes beyond a typical ML model by implementing a **complete ML system pipeline**, including:

- Historical demand modeling
- Automated lag feature generation
- External data integration (weather)
- Feature engineering pipeline
- REST API for real-time predictions
- Cloud deployment (on Render)

---

## Problem Statement

Forecast **weekly sales for retail stores** based on:

- Historical sales trends
- Store characteristics
- Promotions
- Economic indicators
- Weather conditions

---

## Key Features

### 1. Automated Lag Feature System
- Dynamically retrieves past sales from a feature store (`history.csv`)
- Eliminates need for manual lag inputs
- Ensures training-serving consistency

---

### 2. Asynchronous Weather Integration
- Fetches real-time weather data using OpenWeather API
- Uses `async` calls for non-blocking execution
- Supports multiple store locations

---

### 3. Caching Layer
- Prevents redundant API calls
- Improves latency and efficiency

---

### 4. Feature Engineering Pipeline
- Time-based features (year, month, week, day)
- Store size categorization
- Promotion aggregation (`total_markdown`)
- Rolling statistics & lag features

---

### 5. Model Training
- Model: **XGBoost Regressor**
- Optimized using:
  - Depth tuning
  - Learning rate adjustment
  - Feature selection
- Target transformation using `log1p`

---

### 6. Real-Time Inference API
- Built using **FastAPI**
- Accepts structured JSON input
- Returns predicted weekly sales

---

### 7. Cloud Deployment
- Deployed on Render
- Publicly accessible API endpoint

---
## System Architecture
Request → API (FastAPI)
→ Lag Feature Retrieval (history.csv)
→ Weather Fetch (Async API)
→ Feature Engineering
→ Model Prediction (XGBoost)
→ Response

---

## Installation (Local Setup)

```bash
git clone https://github.com/shubhro2002/demand-intelligence-system.git
cd demand-intelligence-system

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```
---

### Environment Variables

Create a `.env` file (for local use):

```bash
API_KEY=your_openweather_api_key
```
---

### Run Locally

```bash
uvicorn src.api.main:app --reload
```
---

### API Usage

Open Swagger UI:
```bash
http://127.0.0.1:8000/docs
```
### Sample Input

```bash
{
  "Store": 1,
  "Dept": 1,
  "IsHoliday": 0,
  "Size": 150000,
  "Type": "A",
  "CPI": 220,
  "Unemployment": 7.5,
  "Fuel_Price": 3.5,
  "MarkDown1": 0,
  "MarkDown2": 0,
  "MarkDown3": 0,
  "MarkDown4": 0,
  "MarkDown5": 0,
  "Date": "2012-11-23"
}
```
### Sample Output

```bash
{
  "predicted_weekly_sales": 8113.30
}
```
---

## Deployment

The application is deployed on Render:

https://demand-intelligence-system.onrender.com/

Interactive API Docs:

https://demand-intelligence-system.onrender.com/docs