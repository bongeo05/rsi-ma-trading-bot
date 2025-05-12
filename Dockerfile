# Dockerfile pentru RSI-MA Trading Bot

# Folosim o imagine oficială Python
FROM python:3.9-slim

# Setăm directorul de lucru
WORKDIR /app

# Copiem fișierele necesare
COPY RSI_MA_Trading_Bot.py .
COPY requirements.txt .

# Instalăm librăriile direct cu versiunile compatibile
RUN pip install --no-cache-dir numpy==1.21.6 pandas==1.3.5 binance-connector==2.0.0

# Sistem de Log pentru Debug
ENV PYTHONUNBUFFERED=1

# Setăm comanda de start
CMD ["python3", "RSI_MA_Trading_Bot.py"]
