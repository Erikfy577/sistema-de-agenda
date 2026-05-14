import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_espera(janela_principal):
    espera = tk.Toplevel()
    espera.title("Gerenciamento de Fila e Vagas")
    espera.state('zoomed')

    def voltar():
        espera.destroy()
        janela_principal.deiconify()
        janela_principal.state('zoomed')

    espera.protocol("WM_DELETE_WINDOW", voltar)

    # Botão Voltar
    tk.Button(espera, text="← Voltar ao Menu", command=voltar, bg="#607D8B", fg="white", font=("Arial", 10, "bold")).pack(anchor="nw", padx=20, pady=10)

    frame_topo = tk.Frame(espera)
    frame_topo.pack(pady=10)

    tk.Label(frame_topo, text="Filtrar por Profissional:", font=("Arial", 12)).pack(side="left", padx=5)
    profissionais = ["Dra. Laurice", "Thiago", "Jamile", "Gerlando"]
    combo_filtro = ttk.Combobox(frame_topo, values=profissionais, state="readonly", font=("Arial", 12))
    combo_filtro.pack(side="left", padx=5)
    combo_filtro.set(profissionais[0])

    frame_tabelas = tk.Frame(espera)
    frame_tabelas.pack(fill="both", expand=True, padx=10, pady=10)

    # Tabelas de Fila e Agenda
    tk.Label(frame_tabelas, text="Fila de Espera", fg="#FF9800", font=("Arial", 11, "bold")).grid(row=0, column=0)
    tabela_espera = ttk.Treeview(frame_tabelas, columns=("ID", "Nome", "Telefone"), show="headings", height=15)
    for col in ("ID", "Nome", "Telefone"): tabela_espera.heading(col, text=col)
    tabela_espera.grid(row=1, column=0, padx=10, sticky="nsew")

    tk.Label(frame_tabelas, text="Lista do Dia (Agendados)", fg="#4CAF50", font=("Arial", 11, "bold")).grid(row=0, column=1)
    tabela_agenda = ttk.Treeview(frame_tabelas, columns=("ID", "Nome", "Telefone"), show="headings", height=15)
    for col in ("ID", "Nome", "Telefone"): tabela_agenda.heading(col, text=col)
    tabela_agenda.grid(row=1, column=1, padx=10, sticky="nsew")

    def carregar_listas(*args):
        medico = combo_filtro.get()
        for item in tabela_espera.get_children(): tabela_espera.delete(item)
        for item in tabela_agenda.get_children(): tabela_agenda.delete(item)
            
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, telefone FROM pacientes WHERE profissional = ? AND status = 'Aguardando' ORDER BY id ASC", (medico,))
            for linha in cursor.fetchall(): tabela_espera.insert("", "end", values=linha)
                
            cursor.execute("SELECT id, nome, telefone FROM pacientes WHERE profissional = ? AND status = 'Agendado' ORDER BY id ASC", (medico,))
            for linha in cursor.fetchall(): tabela_agenda.insert("", "end", values=linha)
            conexao.close()
        except Exception as e: print(e)

    combo_filtro.bind("<<ComboboxSelected>>", carregar_listas)

    # Controles de Vagas e Exclusão
    frame_inferior = tk.Frame(espera)
    frame_inferior.pack(pady=20)
    
    tk.Label(frame_inferior, text="Vagas:").pack(side="left", padx=5)
    entrada_vagas = tk.Entry(frame_inferior, width=5)
    entrada_vagas.pack(side="left", padx=5)
    entrada_vagas.insert(0, "5")
    
    tk.Button(frame_inferior, text="Gerar Lista do Dia", command=lambda: carregar_listas(), bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    
    def excluir_paciente():
        # Lógica de exclusão aqui
        pass

    tk.Button(frame_inferior, text="Excluir Selecionado", command=excluir_paciente, bg="#F44336", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)

    carregar_listas()