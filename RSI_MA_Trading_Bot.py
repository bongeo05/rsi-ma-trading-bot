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
simulated_trading = True  # Activare Simulated Trading
usdc_balance = 1000.0  # Sold virtual inițial
eth_balance = 0.2
initial_usdc_balance = usdc_balance

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
    global usdc_balance, eth_balance
    try:
        rsi = calculate_rsi(df['close']).iloc[-1]
        ma50 = df['close'].rolling(window=ma_short).mean().iloc[-1]
        ma200 = df['close'].rolling(window=ma_long).mean().iloc[-1]

        log_message(f'RSI: {rsi:.2f}, MA50: {ma50:.2f}, MA200: {ma200:.2f}, Price: {df["close"].iloc[-1]:.2f}')

        price = df['close'].iloc[-1]

        if rsi < 25 and ma50 > ma200:
            log_message('🚀 Semnal de CUMPARARE.')
            if simulated_trading:
                if usdc_balance >= price * quantity:
                    usdc_balance -= price * quantity
                    eth_balance += quantity
                    log_message(f'Simulated BUY: +{quantity} ETH -{price * quantity} USDC')
            else:
                client.order_market_buy(symbol=symbol, quantity=quantity)

        elif rsi > 75 and ma50 < ma200:
            log_message('⚠️ Semnal de VANZARE.')
            if simulated_trading:
                if eth_balance >= quantity:
                    eth_balance -= quantity
                    usdc_balance += price * quantity
                    log_message(f'Simulated SELL: -{quantity} ETH +{price * quantity} USDC')
            else:
                client.order_market_sell(symbol=symbol, quantity=quantity)

    except Exception as e:
        log_error(f"EROARE LA SEMNAL: {str(e)}")

# Funcție pentru afișare raport final
def final_report():
    profit_usdc = usdc_balance - initial_usdc_balance
    log_message("📊 RAPORT FINAL - Simulated Trading")
    log_message(f"💰 Sold inițial: {initial_usdc_balance} USDC")
    log_message(f"💰 Sold final: {usdc_balance} USDC")
    log_message(f"💰 Profit/Pierdere: {profit_usdc} USDC")

# Bucla principală
def main():
    log_message("🚀 Botul a pornit și monitorizează piața... (Simulated Trading: " + str(simulated_trading) + ")")
    try:
        while True:
            df = get_price_data()
            check_signals(df)
            log_message(f'💰 USDC: {usdc_balance:.2f}, ETH: {eth_balance:.4f}')
            time.sleep(10)
    except KeyboardInterrupt:
        final_report()
        log_message("✅ Botul a fost oprit corect.")

if __name__ == '__main__':
    main()
