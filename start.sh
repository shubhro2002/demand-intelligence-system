#!/bin/bash

echo "Starting FastAPI app..."

uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-10000}