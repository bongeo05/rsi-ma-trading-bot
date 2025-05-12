# Dockerfile pentru RSI-MA Trading Bot

# Folosim o imagine oficială Python 3.9 (versiune compatibilă)
FROM python:3.9-slim

# Setăm directorul de lucru
WORKDIR /app

# Copiem fișierele necesare și instalăm doar pachetele necesare
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiem scriptul după instalarea dependințelor (optimizare pentru cache)
COPY RSI_MA_Trading_Bot.py .

# Sistem de Log pentru Debug
ENV PYTHONUNBUFFERED=1

# Setăm comanda de start
CMD ["python", "RSI_MA_Trading_Bot.py"]
