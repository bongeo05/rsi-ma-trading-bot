# Dockerfile pentru RSI-MA Trading Bot

# Imaginea de bază
FROM python:3.9-slim

# Setează directorul de lucru
WORKDIR /app

# Copiază fișierele necesare
COPY requirements.txt .
COPY RSI_MA_Trading_Bot.py .

# Instalează dependințele
RUN pip install --no-cache-dir -r requirements.txt

# Rulează scriptul botului
CMD ["python", "RSI_MA_Trading_Bot.py"]
