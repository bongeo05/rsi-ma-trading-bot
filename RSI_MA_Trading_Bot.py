import os
import time
import pandas as pd
from binance.client import Client
from binance.enums import *

# Conectare la Binance cu variabile de mediu
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
client = Client(api_key, api_secret)

# Setări Bot
symbol = 'ETHUSDT'
interval = '5m'  # Intervalul pentru datele RSI și MA
quantity = 0.01  # Cât ETH să cumpere sau să vândă
rsi_period = 14
ma_short = 50
ma_long = 200

# Functie pentru log (salvează în trading_log.txt)
def log_message(message):
    with open('trading_log.txt', 'a') as log_file:
        log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}: {message}\n')

# Functie pentru a obține date de preț (close prices)
def get_price_data():
    klines = client.get_klines(symbol=symbol, interval=interval, limit=ma_long)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df

# Functie pentru calculul RSI
def calculate_rsi(data):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Functie pentru verificare semnal
def check_signals(df):
    rsi = calculate_rsi(df['close']).iloc[-1]
    ma50 = df['close'].rolling(window=ma_short).mean().iloc[-1]
    ma200 = df['close'].rolling(window=ma_long).mean().iloc[-1]

    log_message(f'RSI: {rsi:.2f}, MA50: {ma50:.2f}, MA200: {ma200:.2f}')

    if rsi < 30 and ma50 > ma200:
        log_message('Semnal de CUMPARARE.')
        # client.order_market_buy(symbol=symbol, quantity=quantity)

    elif rsi > 70 and ma50 < ma200:
        log_message('Semnal de VANZARE.')
        # client.order_market_sell(symbol=symbol, quantity=quantity)

# Bucla principală
def main():
    while True:
        df = get_price_data()
        check_signals(df)
        time.sleep(60)

if __name__ == '__main__':
    main()
