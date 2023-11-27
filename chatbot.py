import openai

class TradingChatbot:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def consulta(self, mensaje, contexto="", modelo="gpt-4-1106-preview", temp=0.7, tokens=300):
        prompt_completo = self._construir_prompt(mensaje, contexto)
        response = self.client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt_completo}],
            temperature=temp,
            max_tokens=tokens
        )
        return response.choices[0].message.content  

    def _construir_prompt(self, mensaje, contexto):
        mensaje_sistema = "Estás hablando con un asistente de trading avanzado."
        return f"{mensaje_sistema}\n{contexto}\nUsuario: {mensaje}\nChatbot:"
