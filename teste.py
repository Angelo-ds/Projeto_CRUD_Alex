import tkinter as tk
from tkinter import ttk

# Janela principal
janela = tk.Tk()
janela.title("Exemplo de Combobox")

# Criação do Combobox
opcoes = ["Python", "Java", "C++", "JavaScript"]
combo = ttk.Combobox(janela, values=opcoes)

# Define um valor inicial
combo.set("Selecione uma linguagem")

# Posiciona na tela
combo.pack(padx=10, pady=10)

# Função para capturar o valor selecionado
def mostrar_escolha():
    escolha = combo.get()
    print(f"Você escolheu: {escolha}")

# Botão para mostrar a escolha
botao = tk.Button(janela, text="Confirmar", command=mostrar_escolha)
botao.pack(pady=10)

# Executa a interface
janela.mainloop()
