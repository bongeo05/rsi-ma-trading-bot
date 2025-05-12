# Dockerfile pentru RSI-MA Trading Bot

# Folosim o imagine oficială Python 3.9 (versiune compatibilă)
FROM python:3.9-slim

# Setăm directorul de lucru
WORKDIR /app

# Copiem fișierele necesare
COPY requirements.txt .
COPY RSI_MA_Trading_Bot.py .

# Instalăm librăriile corecte și stabile
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Sistem de Log pentru Debug (loguri în timp real)
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# Setăm comanda de start
CMD ["python", "RSI_MA_Trading_Bot.py"]
