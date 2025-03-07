import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Função para executar um script Python
def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
        messagebox.showinfo("Sucesso", f"'{script_name}' foi executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao executar {script_name}: {e}")

# Criar a janela principal da aplicação
root = tk.Tk()
root.title("Interface de Execução de Scripts")
root.geometry("300x250")  # Tamanho da janela

# Adicionar os botões para executar os scripts
button_analyze = tk.Button(root, text="Analizar", command=lambda: run_script('analyze_games.py'))
button_analyze.pack(pady=10)

button_fetch = tk.Button(root, text="Carregar Jogos", command=lambda: run_script('fetch_games.py'))
button_fetch.pack(pady=10)

button_visualize = tk.Button(root, text="Gerar Relatório", command=lambda: run_script('visualize.py'))
button_visualize.pack(pady=10)

button_config = tk.Button(root, text="Executar config.py", command=lambda: run_script('config.py'))
button_config.pack(pady=10)

# Iniciar a interface gráfica
root.mainloop()
