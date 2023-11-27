import os
from dotenv import load_dotenv
from chatbot import TradingChatbot
import data_extraction
import data_analysis
import model_training
import data_visualization

load_dotenv()

class TradingApplication:
    def __init__(self, api_key):
        self.chatbot = TradingChatbot(api_key)

    def run(self):
        while True:
            print("\nMenú de Opciones:")
            print("1. Escribe tu pregunta sobre trading")
            print("2. Realiza el análisis del dólar-peso")
            print("3. Salir")
            opcion = input("Elige una opción: ")

            if opcion == '1':
                self.ask_trading_question()
            elif opcion == '2':
                self.analyze_usdmxn()
            elif opcion == '3':
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Por favor, intenta de nuevo.")

    def ask_trading_question(self):
        user_input = input("\nEscribe tu pregunta sobre trading: ")
        contexto = self.get_trading_context()
        response = self.chatbot.consulta(user_input, contexto)
        print("\nChatbot:", response)

    def analyze_usdmxn(self):
        period_option = input("\nElige el periodo de análisis (dia, semana, mes): ")
        data = data_extraction.extract_historical_data('USDMXN=X', period_option)
        analyzed_data = data_analysis.analyze_data(data)

        if len(analyzed_data) >= 30:  # Asegurarse de tener al menos 30 días de datos
            trend_predictions = model_training.predict_trend(analyzed_data)

            if len(trend_predictions) > 0:
                # Determinar si la tendencia es alcista o bajista
                trend = "alcista" if trend_predictions[-1] == 1 else "bajista"

            # Aquí se agrega el period_option como argumento adicional
                visualization = data_visualization.visualize_data(analyzed_data, trend_predictions, period_option)
                justification_prompt = f"El modelo ha predicho una tendencia {trend} para el mercado USD/MXN en el período seleccionado ({period_option}). ¿Conectate a internet e investiga en bing  3 posibles puntos de por que la tendencia es asi utiliza un lenguaje seguro y que no genere desconfianza, se breve, ya soy conciente de la volatilidad el mercado no es necesario que lo recuerdes ?"
                interpretation = self.chatbot.consulta(justification_prompt, "")

                print(f"\nTendencia del mercado: {trend}")
                print(f"Justificación del Chatbot: {interpretation}")
            else:
                print("No se pudieron realizar predicciones precisas para el período seleccionado.")
        else:
            print("No hay suficientes datos históricos para realizar predicciones para el período seleccionado.")

    def get_trading_context(self):
        return "Contexto de Trading: [Información relevante aquí]"

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    app = TradingApplication(api_key)
    app.run()
