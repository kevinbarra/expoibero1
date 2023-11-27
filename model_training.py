from sklearn.model_selection import train_test_split
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import yfinance as yf
from datetime import datetime

# Función para descargar datos
def download_data(ticker, start_date='2022-01-01'):
    end_date = datetime.now().strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    return data['Close']

# Preparar datos para el modelo de tendencia
def prepare_data_for_trend(data, n_steps):
    X, y = [], []
    for i in range(n_steps, len(data) - 1):
        X.append(data[i-n_steps:i])
        y.append(1 if data[i] < data[i + 1] else 0)
    return np.array(X), np.array(y)

# Predecir la tendencia
def predict_trend(data, n_steps=30):
    model = load_model('mi_modelo_tendencia.h5')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))

    X, _ = prepare_data_for_trend(scaled_data, n_steps)
    if len(X) == 0:
        return np.array([])

    X = X.reshape(X.shape[0], X.shape[1], 1)
    predictions = model.predict(X)
    predicted_trends = (predictions > 0.5).astype(int)
    return predicted_trends

# Entrenar el modelo para la tendencia
def train_model_for_trend(ticker, n_steps=30):
    data = download_data(ticker)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))

    X, y = prepare_data_for_trend(scaled_data, n_steps)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {test_accuracy:.4f}, Test Loss: {test_loss:.4f}")

    model.save('mi_modelo_tendencia.h5')

# Llamada a la función de entrenamiento
if __name__ == "__main__":
    train_model_for_trend('USDMXN=X')
