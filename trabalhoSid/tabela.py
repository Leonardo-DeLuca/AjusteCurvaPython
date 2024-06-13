import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

def is_float(element: any) -> bool:
#If you expect None to be passed:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False  

class App:
        
    def __init__(self, root):
        self.root = root
        self.root.title("Ajuste de Curva")

        self.frame = ttk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.tabela = ttk.Treeview(self.frame, columns=("X", "Y"), show="headings")
        self.tabela.heading("X", text="X", anchor="center")
        self.tabela.heading("Y", text="Y", anchor="center")
        self.tabela.column("X", anchor="center")
        self.tabela.column("Y", anchor="center")
        self.tabela.pack(side="left", fill="y")

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.frameBotoes = ttk.Frame(root)
        self.frameBotoes.pack(side="left", pady=5, padx=5)

        self.botaoAddLinha = ttk.Button(self.frameBotoes, text="Adicionar linha", command=self.addLinha)
        self.botaoAddLinha.grid(row=0, column=0, padx=5)

        self.variavelPrimeiroGrau = tk.IntVar()
        self.variavelSegundoGrau = tk.IntVar()

        self.checkPrimeiroGrau = ttk.Checkbutton(self.frameBotoes, text="Primeiro grau", variable=self.variavelPrimeiroGrau, command=self.onSelectCheckBoxPrimeiroGrau)
        self.checkPrimeiroGrau.grid(row=0, column=1, padx=5)

        self.checkSegundoGrau = ttk.Checkbutton(self.frameBotoes, text="Segundo grau", variable=self.variavelSegundoGrau, command=self.onSelectCheckBoxSegundoGrau)
        self.checkSegundoGrau.grid(row=0, column=2, padx=5)

        self.botaoAddLinha = ttk.Button(self.frameBotoes, text="Executar", command=self.executar)
        self.botaoAddLinha.grid(row=0, column=3, padx=5)

        self.tabela.bind('<Double-1>', self.editarCelula)

    def addLinha(self):
        self.tabela.insert('', 'end', values=(0, 0))

    def editarCelula(self, event):
        try:
            item = self.tabela.selection()[0]
            column = self.tabela.identify_column(event.x)
            editorCelula = self.criaEditorCelula(event, item, column)
            editorCelula.focus()
        except:
            messagebox.showerror("Erro", "Não há célula aqui.") 

    def criaEditorCelula(self, event, item, column):
        x, y, width, height = self.tabela.bbox(item, column)
        column_index = int(column.replace('#', ''))
        value = self.tabela.item(item, 'values')[column_index - 1]

        editorCelula = tk.Entry(self.root)
        editorCelula.place(x=x + self.frame.winfo_x(), y=y + self.frame.winfo_y(), width=width, height=height)
        editorCelula.insert(0, value)

        def salvar(event):
            novoValor = editorCelula.get()
            if is_float(novoValor):
                values = list(self.tabela.item(item, 'values'))
                values[column_index - 1] = novoValor
                self.tabela.item(item, values=values)
            else:
                messagebox.showerror("Erro de entrada", "Por favor, insira um número válido.")
            editorCelula.destroy()

        editorCelula.bind('<Return>', salvar)
        editorCelula.bind('<FocusOut>', lambda e: editorCelula.destroy())
        
        return editorCelula

    def onSelectCheckBoxPrimeiroGrau(self):
        if self.variavelPrimeiroGrau.get() == 1:
            self.variavelSegundoGrau.set(0)
            
    def onSelectCheckBoxSegundoGrau(self):
        if self.variavelSegundoGrau.get() == 1:
            self.variavelPrimeiroGrau.set(0)

    def executar(self):
        linhas = self.tabela.get_children()
        valores = {'X': [], 'Y': []}

        for linha in linhas:
            values = self.tabela.item(linha, 'values')
            valores['X'].append(values[0])
            valores['Y'].append(values[1])

        xs = np.array(valores["X"])
        x = xs.astype(float)
        ys = np.array(valores["Y"])
        y = ys.astype(float)
        print(x)

        print(valores)
        if self.variavelPrimeiroGrau.get() == 1:
            # Tentativa de ajuste linear
            coeficientes_linear = np.polyfit(x, y, 1)  # Regressão linear
            modelo_linear = np.poly1d(coeficientes_linear)
            # Pontos para a linha de ajuste
            x_linha = np.linspace(min(x), max(x), 100)
            y_linear = modelo_linear(x_linha)
            # Plotagem dos dados e das linhas de ajuste
            plt.figure(figsize=(10, 5))
            plt.scatter(x, y, color='blue', label='Dados reais')
            plt.plot(x_linha, y_linear, 'r--', label=f'Linha Linear: {modelo_linear}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Regressão Linear')
            plt.legend()
            plt.grid(True)
            plt.show()
        elif self.variavelSegundoGrau.get() == 1:
            # Tentativa de ajuste polinomial de grau maior
            coeficientes_poly = np.polyfit(x, y, 2)  # Regressão polinomial de grau 2
            modelo_poly = np.poly1d(coeficientes_poly)
            # Pontos para a linha de ajuste
            x_linha = np.linspace(min(x), max(x), 100)
            y_poly = modelo_poly(x_linha)
            # Plotagem dos dados e das linhas de ajuste
            plt.figure(figsize=(10, 5))
            plt.scatter(x, y, color='blue', label='Dados reais')
            plt.plot(x_linha, y_poly, 'g-', label=f'Curva Polinomial: {modelo_poly}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Regressão Polinomial')
            plt.legend()
            plt.grid(True)
            plt.show()
        else:
            messagebox.showerror("Erro box", "Nenhuma box selecionada!")

            

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
