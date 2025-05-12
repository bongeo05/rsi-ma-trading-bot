import os
import time
import pandas as pd
import requests
from binance.client import Client
from binance.enums import *

# Conectare la Binance cu variabile de mediu
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
client = Client(api_key, api_secret)

# Setări Bot
symbol = 'ETHUSDC'  # Am schimbat la ETHUSDC pentru compatibilitate
interval = '5m'  # Intervalul pentru datele RSI și MA
quantity = 0.01  # Cât ETH să cumpere sau să vândă
rsi_period = 14
ma_short = 50
ma_long = 200

# Setări Telegram
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

# Funcție pentru trimitere mesaje Telegram
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    payload = {'chat_id': telegram_chat_id, 'text': message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        log_error(f"Eroare Telegram: {str(e)}")

# Funcție pentru loguri (salvează în trading_log.txt și error_log.txt)
def log_message(message):
    print(message)
    with open('trading_log.txt', 'a') as log_file:
        log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}: {message}\n')
    send_telegram_message(message)

# Funcție pentru log erori
def log_error(message):
    print(f"EROARE: {message}")
    with open('error_log.txt', 'a') as error_file:
        error_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}: {message}\n')

# Funcție pentru a obține date de preț (close prices)
def get_price_data():
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=ma_long)
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time','quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])
        df['close'] = df['close'].astype(float)
        return df
    except Exception as e:
        log_error(f"EROARE API: {str(e)}")
        time.sleep(5)
        return get_price_data()

# Funcție pentru calculul RSI
def calculate_rsi(data):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Funcție pentru verificare semnal și execuție tranzacții
def check_signals(df):
    try:
        rsi = calculate_rsi(df['close']).iloc[-1]
        ma50 = df['close'].rolling(window=ma_short).mean().iloc[-1]
        ma200 = df['close'].rolling(window=ma_long).mean().iloc[-1]

        log_message(f'RSI: {rsi:.2f}, MA50: {ma50:.2f}, MA200: {ma200:.2f}, Price: {df["close"].iloc[-1]:.2f}')

        if rsi < 25 and ma50 > ma200:
            log_message('🚀 Semnal de CUMPARARE.')
            try:
                response = client.order_market_buy(symbol=symbol, quantity=quantity)
                log_message(f'✅ Tranzacție de CUMPĂRARE executată: {response}')
            except Exception as e:
                log_error(f"EROARE LA CUMPĂRARE: {str(e)}")

        elif rsi > 75 and ma50 < ma200:
            log_message('⚠️ Semnal de VANZARE.')
            try:
                response = client.order_market_sell(symbol=symbol, quantity=quantity)
                log_message(f'✅ Tranzacție de VÂNZARE executată: {response}')
            except Exception as e:
                log_error(f"EROARE LA VÂNZARE: {str(e)}")

    except Exception as e:
        log_error(f"EROARE LA SEMNAL: {str(e)}")

# Bucla principală
def main():
    log_message("🚀 Botul a pornit și monitorizează piața...")
    while True:
        df = get_price_data()
        check_signals(df)
        time.sleep(10)

if __name__ == '__main__':
    main()
