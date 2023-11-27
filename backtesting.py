import pandas as pd
from keras.models import load_model
import os

def backtest_trend_strategy(data, model):
    if 'Close' not in data.columns:
        raise KeyError("La columna 'Close' no se encuentra en los datos.")

    prepared_data = data[['Close']]
    predictions = model.predict(prepared_data)
    data['Trend_Prediction'] = (predictions > 0.5).astype(int)

    initial_capital = 10000.0
    positions = pd.DataFrame(index=data.index).fillna(0.0)
    portfolio = pd.DataFrame(index=data.index).fillna(0.0)

    positions['Asset'] = data['Trend_Prediction'] * 1000
    portfolio['positions'] = positions.multiply(data['Close'], axis=0)
    portfolio['total'] = portfolio['positions'] + initial_capital
    portfolio['returns'] = portfolio['total'].pct_change()

    return portfolio

if __name__ == "__main__":
    historical_data = pd.read_csv('historical_data.csv')
    
    model_path = 'mi_modelo_tendencia.h5'
    if not os.path.exists(model_path):
        print(f"El archivo del modelo {model_path} no se encuentra.")
    else:
        trained_model = load_model(model_path)
        backtest_results = backtest_trend_strategy(historical_data, trained_model)
        print(backtest_results)
