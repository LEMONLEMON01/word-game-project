# syntax=docker/dockerfile:1

from python:3.12-slim
workdir /app
copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt

copy . .

expose 8000

cmd ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]