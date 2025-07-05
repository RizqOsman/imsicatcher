#!/bin/bash

# Inisialisasi DB (jika perlu)
echo "Menjalankan server FastAPI..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000