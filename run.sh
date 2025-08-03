#!/bin/bash
# Start FastAPI server
poetry run uvicorn app:app --host 0.0.0.0 --port 7860