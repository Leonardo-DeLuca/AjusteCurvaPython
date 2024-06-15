import numpy as np
import matplotlib.pyplot as plt

# Dados fornecidos
x = np.array([-3, -2, -1, 1, 4])
y = np.array([-7.4, -5.8, -4.6, -1.3, 2.8])

print(x)

# Tentativa de ajuste linear
coeficientes_linear = np.polyfit(x, y, 1)  # Regressão linear
modelo_linear = np.poly1d(coeficientes_linear)

# Tentativa de ajuste polinomial de grau maior
coeficientes_poly = np.polyfit(x, y, 2)  # Regressão polinomial de grau 2
modelo_poly = np.poly1d(coeficientes_poly)

# Pontos para a linha de ajuste
x_linha = np.linspace(min(x), max(x), 100)
y_linear = modelo_linear(x_linha)
y_poly = modelo_poly(x_linha)

# Plotagem dos dados e das linhas de ajuste
plt.figure(figsize=(10, 5))
plt.scatter(x, y, color='blue', label='Dados reais')
plt.plot(x_linha, y_linear, 'r--', label=f'Linha Linear: {modelo_linear}')
plt.plot(x_linha, y_poly, 'g-', label=f'Curva Polinomial: {modelo_poly}')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Regressão Linear vs. Regressão Polinomial')
plt.legend()
plt.grid(True)
plt.show()
