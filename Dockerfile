# Dockerfile pentru RSI-MA Trading Bot

# Folosim o imagine oficială Python 3.9 (versiune compatibilă)
FROM python:3.9-slim

# Setăm directorul de lucru
WORKDIR /app

# Copiem fișierele necesare
COPY RSI_MA_Trading_Bot.py .
COPY requirements.txt .

# Instalăm librăriile corecte și stabile
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir numpy==1.21.6 pandas==1.3.5 python-binance==1.0.16

# Sistem de Log pentru Debug
ENV PYTHONUNBUFFERED=1

# Setăm comanda de start
CMD ["python3", "RSI_MA_Trading_Bot.py"]
