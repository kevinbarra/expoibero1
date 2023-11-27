import shap
import matplotlib.pyplot as plt

def explain_model(model, X_train):
    """
    Utiliza SHAP para explicar las decisiones del modelo y visualiza los resultados.
    """
    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_train)

    # Visualización de los valores de SHAP
    shap.summary_plot(shap_values, X_train, plot_type="bar")

    # También puedes visualizar la importancia de las características para una sola predicción
    # Por ejemplo, para la primera muestra:
    # shap.force_plot(explainer.expected_value, shap_values[0, :], X_train.iloc[0, :])

    return shap_values

# Ejemplo de uso
# Suponiendo que 'model' es tu modelo entrenado y 'X_train' los datos de entrenamiento
# explain_model(model, X_train)
