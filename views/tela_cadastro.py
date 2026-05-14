import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_cadastro(janela_principal):
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro de Paciente")
    cadastro.state('zoomed')

    # Função para voltar
    def voltar():
        cadastro.destroy() # Fecha a tela de cadastro
        janela_principal.deiconify() # Mostra a principal de volta
        janela_principal.state('zoomed')

    cadastro.protocol("WM_DELETE_WINDOW", voltar) # Caso feche no 'X'

    tk.Button(cadastro, text="← Voltar ao Menu", command=voltar, bg="#607D8B", fg="white").pack(anchor="nw", padx=10, pady=10)

    # ... (Restante do seu código de labels e entradas) ...
    tk.Label(cadastro, text="Nome do Paciente:").pack(pady=5)
    entrada_nome = tk.Entry(cadastro, width=40); entrada_nome.pack(pady=5)
    
    tk.Label(cadastro, text="Telefone:").pack(pady=5)
    entrada_telefone = tk.Entry(cadastro, width=40); entrada_telefone.pack(pady=5)

    profissionais = ["Dra. Laurice", "Thiago", "Jamile", "Gerlando"]
    combo = ttk.Combobox(cadastro, values=profissionais, state="readonly", width=37)
    combo.pack(pady=5); combo.set(profissionais[0])

    def salvar():
        # ... seu código de salvar ...
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO pacientes (nome, telefone, profissional) VALUES (?, ?, ?)", 
                           (entrada_nome.get(), entrada_telefone.get(), combo.get()))
            conexao.commit(); conexao.close()
            messagebox.showinfo("Sucesso", "Cadastrado!")
            entrada_nome.delete(0, tk.END); entrada_telefone.delete(0, tk.END)
        except Exception as e: messagebox.showerror("Erro", str(e))

    tk.Button(cadastro, text="Salvar na Fila", command=salvar, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=20)