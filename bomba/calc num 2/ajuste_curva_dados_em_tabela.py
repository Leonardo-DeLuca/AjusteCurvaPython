import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Definindo as funções de ajuste
def linear(x, a, b):
    return a * x + b

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def exponential(x, a, b):
    return a * np.exp(b * x)

def logarithmic(x, a, b):
    return a * np.log(x) + b

# Função para calcular o erro quadrático médio
def mse(f, x, y, params):
    return np.mean((y - f(x, *params))**2)

# Função principal da aplicação
def identify_best_fit(data):
    data = pd.read_csv('data.csv', dtype=str)
    # Substitui vírgulas por pontos e converte para float
    data['x'] = data['x'].str.replace(',', '.').astype(float)
    data['y'] = data['y'].astype(float) 
    x = data['x'].values
    y = data['y'].values
    
    # Ajuste das funções
    params_linear, _ = curve_fit(linear, x, y)
    params_quadratic, _ = curve_fit(quadratic, x, y)
    params_exponential, _ = curve_fit(exponential, x, y)
    params_logarithmic, _ = curve_fit(logarithmic, x, y)

    # Calcular o erro quadrático médio para cada função
    mse_linear = mse(linear, x, y, params_linear)
    mse_quadratic = mse(quadratic, x, y, params_quadratic)
    mse_exponential = mse(exponential, x, y, params_exponential)
    mse_logarithmic = mse(logarithmic, x, y, params_logarithmic)

    # Identificar a melhor função
    errors = {
        'Linear': mse_linear,
        'Quadratic': mse_quadratic,
        'Exponential': mse_exponential,
        'Logarithmic': mse_logarithmic
    }

    best_fit = min(errors, key=errors.get)
    
    print(f"A melhor função de ajuste é: {best_fit}")
    
    # Plotando os dados e a função ajustada
    plt.scatter(x, y, label='Dados')
    x_fit = np.linspace(min(x), max(x), 100)

    if best_fit == 'Linear':
        y_fit = linear(x_fit, *params_linear)
    elif best_fit == 'Quadratic':
        y_fit = quadratic(x_fit, *params_quadratic)
    elif best_fit == 'Exponential':
        y_fit = exponential(x_fit, *params_exponential)
    elif best_fit == 'Logarithmic':
        y_fit = logarithmic(x_fit, *params_logarithmic)

    plt.plot(x_fit, y_fit, label=f'Ajuste {best_fit}')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Ajuste de Curva')
    plt.show()

    return best_fit, params_linear, params_quadratic, params_exponential, params_logarithmic

# Exemplo de uso
# Supondo que temos um arquivo CSV com duas colunas: 'x' e 'y'
data = pd.read_csv('data.csv')
identify_best_fit(data)
