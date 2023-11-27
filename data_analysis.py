import pandas as pd

def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

def calculate_rsi(data, window):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(data, window):
    sma = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    return sma + (std * 2), sma - (std * 2)

def analyze_data(data, window_sma=15, window_ema=20, window_rsi=14, window_bollinger=20):
    if 'Close' not in data.columns:
        raise ValueError("La columna 'Close' no se encuentra en los datos.")

    data['SMA'] = data['Close'].rolling(window=window_sma).mean()
    data['EMA'] = calculate_ema(data['Close'], window_ema)
    data['RSI'] = calculate_rsi(data['Close'], window_rsi)
    data['Bollinger_Upper'], data['Bollinger_Lower'] = calculate_bollinger_bands(data['Close'], window_bollinger)
    data['Volatility'] = data['Close'].rolling(window=window_sma).std()

    return data
