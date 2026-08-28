#!/usr/bin/env bash
# Start DRACO-4 Backend API

echo "Starting DRACO-4 Backend API..."
echo "Environment: Production"
echo "Python Version: $(python --version)"

# Install dependencies
pip install -q fastapi uvicorn pydantic pyyaml

# Start server
echo "Starting FastAPI server on http://0.0.0.0:8000"
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
