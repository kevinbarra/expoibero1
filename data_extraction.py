import yfinance as yf
from datetime import datetime, timedelta

def extract_historical_data(ticker, period_option):
    """
    Extrae datos históricos del ticker especificado para realizar predicciones para el día, la semana o el mes siguiente.
    """
    # Definir la cantidad de días a extraer según la opción seleccionada
    days_to_extract = {
        "dia": 365,    # Un año de datos para predecir el siguiente día
        "semana": 2 * 365,  # Dos años de datos para predecir la siguiente semana
        "mes": 3 * 365   # Cinco años de datos para predecir el siguiente mes
    }

    # Calcula la fecha de inicio basada en la cantidad de días a extraer
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_to_extract.get(period_option, 365))

    # Formatear fechas para yfinance
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    # Descargar datos del ticker desde la fecha de inicio hasta hoy
    data = yf.download(ticker, start=start_str, end=end_str, interval='1d')
    return data
