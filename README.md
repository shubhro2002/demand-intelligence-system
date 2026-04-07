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
