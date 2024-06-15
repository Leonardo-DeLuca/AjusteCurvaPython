import sys
import os
import math
from fractions import Fraction

# Values and constants
DENOMINADOR = 999999
BOLD = "\033[1m"
ERROR = "\033[91m"
END = "\033[0m"
mensagemInicial = "Olá! Por favor, digite o nome do arquivo que contém a matriz de pontos a ser lida: "
mensagemErro = ERROR + "\nNão foi possível ler o arquivo!\n" + END
mensagemErroInvalida = ERROR + "O arquivo não contém uma matriz válida!\n" + END
mensagemErroFuncao = ERROR + "As funções digitadas são inválidas\n" + END

def imprime(matriz, decimal):
    align = "<"
    maximo = 0
    
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            maximo = max(maximo, len(str(matriz[i][j])))
    
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if decimal:
                print(BOLD + f'{Fraction.from_float(matriz[i][j]).limit_denominator(DENOMINADOR):{align}{maximo}}' + END, end=' ')
            else:
                print(BOLD + f'{matriz[i][j]:{align}{maximo}}' + END, end=' ')
        print()
    print()

def somatorio(i, j, functions, matriz, colunas):
    soma = 0.0
    try:
        for k in range(colunas):
            x = matriz[0][k]
            soma += eval(functions[j]) * eval(functions[i])
        return soma
    except NameError:
        print(mensagemErroFuncao)
        sys.exit()

def calcula_matriz(functions, matriz, colunas):
    matriz_SL = []
    for i in range(len(functions)):
        linha = []
        for j in range(len(functions)):
            linha.append(somatorio(i, j, functions, matriz, colunas))
        matriz_SL.append(linha)
    return matriz_SL

def calcula_b(functions, matriz, colunas):
    vetor_b = []
    try:
        for i in range(len(functions)):
            soma = 0.0
            for k in range(len(matriz[0])):
                x = matriz[0][k]
                soma += matriz[1][k] * eval(functions[i])
            vetor_b.append(soma)
        return vetor_b
    except NameError:
        print(mensagemErroFuncao)
        sys.exit()

def initMatriz(dim):
    return [[0 for _ in range(dim)] for _ in range(dim)]

def termoM(matriz, l, c):
    return matriz[l][c] / float(matriz[c][c])

def linhaMenosLinha(l1, fator, l2):
    return [l1[i] - fator * l2[i] for i in range(len(l1))]

def calcularLU(matrizA):
    dim = len(matrizA)
    tempA = [row[:] for row in matrizA]
    matrizL = initMatriz(dim)
    
    for i in range(dim):
        matrizL[i][i] = 1
    
    for c in range(dim):
        for l in range(c + 1, dim):
            tm = termoM(tempA, l, c)
            tempA[l] = linhaMenosLinha(tempA[l], tm, tempA[c])
            matrizL[l][c] = tm

    return matrizL, tempA

def calcularY(matriz, resolucaoY, vetor_b):
    for k in range(len(matriz)):
        somatorio = sum(matriz[k][i] * resolucaoY[i] for i in range(k))
        resolucaoY.append((vetor_b[k] - somatorio) / matriz[k][k])

def calcularX(matriz, resolucaoX, resolucaoY):
    for k in range(len(matriz)):
        somatorio = sum(matriz[len(matriz) - k - 1][len(matriz) - i - 1] * resolucaoX[i] for i in range(k))
        resolucaoX.append((resolucaoY[len(matriz) - k - 1] - somatorio) / matriz[len(matriz) - k - 1][len(matriz) - k - 1])

# Start of execution
try:
    os.system('clear')
    file_name = input(mensagemInicial).strip()
    if not file_name:
        file_name = 'matriz4.txt'
    
    if not os.path.isfile(file_name):
        print(mensagemErro)
        sys.exit()
    
    print(f"Debug: Tentando abrir o arquivo {file_name}")
    with open(file_name, 'r') as file:
        matriz = [list(map(float, linha.strip().split())) for linha in file]
    print(f"Debug: Arquivo {file_name} lido com sucesso")

    linhas = len(matriz)
    colunas = len(matriz[0])

except FileNotFoundError:
    print(mensagemErro)
    sys.exit()
except ValueError:
    print(mensagemErroInvalida)
    sys.exit()
except Exception as e:
    print(f"{mensagemErro} {str(e)}")
    sys.exit()

print("Este programa leu a seguinte matriz de pontos para x e f(x):")
imprime(matriz, decimal=False)

try:
    opcao = int(input('''Digite qual caso se deseja calcular:
1 - Linear
2 - Hipérbole | linearização por z=1/y |
3 - Exponencial | linearização por z=ln(y) |
'''))
except ValueError:
    print(mensagemErroInvalida)
    sys.exit()

if opcao == 1:
    functions = input("Digite os valores de g(x) usados no ajuste de curva separados por vírgulas: " + BOLD).strip().split(',')
    print(END)
elif opcao == 2:
    for i in range(colunas):
        matriz[1][i] = 1 / matriz[1][i]
    functions = ['1', 'x']
    print("Este programa linearizou os seguintes pontos para x e f(x):")
    imprime(matriz, decimal=False)
elif opcao == 3:
    for i in range(colunas):
        matriz[1][i] = math.log(matriz[1][i])
    functions = ['1', 'x']
    print("Este programa linearizou os seguintes pontos para x e f(x):")
    imprime(matriz, decimal=False)
else:
    print(mensagemErroInvalida)
    sys.exit()

matriz_SL = calcula_matriz(functions, matriz, colunas)
print("A matriz do Sistema Linear de a(alfas) é:")
imprime(matriz_SL, decimal=False)

linhas = len(matriz_SL)

res = calcularLU(matriz_SL)

vetor_b = calcula_b(functions, matriz, colunas)
print("O vetor b relativo ao Sistema Linear é:")
for i in vetor_b:
    print(BOLD + str(i) + END)
print()

resolucaoY = []
calcularY(res[0], resolucaoY, vetor_b)

resolucaoX = []
calcularX(res[1], resolucaoX, resolucaoY)
resolucaoX.reverse()

print("Resolvendo o Sistema Linear temos a curva:", end=' ')
if opcao == 1:
    for i, coef in enumerate(resolucaoX):
        if coef >= 0 and i != 0:
            coef_str = f"+ {coef}"
        else:
            coef_str = str(coef)
        print(BOLD + coef_str + functions[i] + END, end=' ')
    print()
elif opcao == 2:
    print(BOLD + "(" + f"{resolucaoX[0]} {'+ ' if resolucaoX[1] >= 0 else ''}{resolucaoX[1]}x" + ")^-1" + END)
elif opcao == 3:
    print(BOLD + f"{math.exp(resolucaoX[0])} * {math.exp(resolucaoX[1])}^x" + END)
