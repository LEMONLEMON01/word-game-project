# syntax=docker/dockerfile:1

from python:3.12-slim
workdir /word-game-project
copy requirements.txt .
run pip install -r requirements.txt

copy . .

expose 8000

cmd ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]