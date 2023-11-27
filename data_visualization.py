import matplotlib.pyplot as plt
import pandas as pd

def visualize_data(real_data, trend_predictions, period_option):
    plt.figure(figsize=(15, 7))

    # Determinar el rango de fechas para visualizar según la opción seleccionada
    if period_option == 'dia':
        # Muestra los últimos 30 días
        displayed_data = real_data.last('30D')
    elif period_option == 'semana':
        # Muestra las últimas 8 semanas
        displayed_data = real_data.last('8W')
    elif period_option == 'mes':
        # Muestra los últimos 6 meses
        displayed_data = real_data.last('6M')

    # Graficar los datos reales
    plt.plot(displayed_data.index, displayed_data['Close'], color='red', label='Datos Reales')

    # Marcar la tendencia predicha
    if trend_predictions[-1] == 1:
        plt.axhline(y=displayed_data['Close'].mean(), color='blue', linestyle='-', label='Tendencia Alcista')
    else:
        plt.axhline(y=displayed_data['Close'].mean(), color='green', linestyle='-', label='Tendencia Bajista')

    # Configurar la visualización
    plt.title('Predicción de Tendencia del Mercado')
    plt.xlabel('Fecha')
    plt.ylabel('Precio de Cierre')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
