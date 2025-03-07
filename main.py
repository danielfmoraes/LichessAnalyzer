import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

# Função para executar um script Python em uma thread separada
def run_script(script_name):
    def execute():
        status_label.config(text=f"Executando {script_name}...", fg="blue")
        try:
            subprocess.run(['python', script_name], check=True)
            status_label.config(text=f"'{script_name}' executado com sucesso!", fg="green")
            messagebox.showinfo("Sucesso", f"'{script_name}' foi executado com sucesso!")
        except subprocess.CalledProcessError as e:
            status_label.config(text=f"Erro ao executar {script_name}", fg="red")
            messagebox.showerror("Erro", f"Ocorreu um erro ao executar {script_name}: {e}")

    threading.Thread(target=execute, daemon=True).start()

# Criar a janela principal
root = tk.Tk()
root.title("Interface de Execução de Scripts")
root.geometry("300x250")  # Tamanho da janela

# Adicionar um rótulo de status
status_label = tk.Label(root, text="Aguardando ação...", fg="black")
status_label.pack(pady=10)

# Botões para executar os scripts
button_fetch = tk.Button(root, text="Carregar Jogos", command=lambda: run_script('fetch_games.py'))
button_fetch.pack(pady=10)

button_analyze = tk.Button(root, text="Analisar Partidas", command=lambda: run_script('analyze_games.py'))
button_analyze.pack(pady=10)

button_visualize = tk.Button(root, text="Gerar Relatório", command=lambda: run_script('visualize.py'))
button_visualize.pack(pady=10)

# Iniciar a interface gráfica
root.mainloop()
