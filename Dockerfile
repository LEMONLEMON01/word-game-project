FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM python:3.12-slim
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./static

# Create a simple startup script to debug
RUN echo '#!/bin/bash\n\
echo "Starting Connections Game API..."\n\
echo "Current directory:" && pwd\n\
echo "Contents:" && ls -la\n\
echo "Static files:" && ls -la static/ || echo "No static directory"\n\
uvicorn main:app --host 0.0.0.0 --port 8000 --access-log\n\
' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000
CMD ["/app/start.sh"]