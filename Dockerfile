# Dockerfile pentru RSI-MA Trading Bot

# Folosim o imagine oficială Python
FROM python:3.9-slim

# Setăm directorul de lucru
WORKDIR /app

# Copiem fișierele necesare
COPY RSI_MA_Trading_Bot.py .
COPY requirements.txt .

# Instalăm librăriile direct
RUN pip install --no-cache-dir -r requirements.txt

# Setăm comanda de start
CMD ["python3", "RSI_MA_Trading_Bot.py"]
