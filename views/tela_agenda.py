import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import os

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_agenda(janela_principal):
    agenda = tk.Toplevel()
    agenda.title("Agenda Mensal")
    agenda.state('zoomed')

    def voltar():
        agenda.destroy()
        janela_principal.deiconify()
        janela_principal.state('zoomed')

    agenda.protocol("WM_DELETE_WINDOW", voltar)

    # Botão Voltar
    tk.Button(agenda, text="← Voltar ao Menu", command=voltar, bg="#607D8B", fg="white", font=("Arial", 10, "bold")).pack(anchor="nw", padx=20, pady=10)

    tk.Label(agenda, text="Selecione um dia no Calendário", font=("Arial", 16, "bold")).pack(pady=10)

    calendario = Calendar(agenda, selectmode='day', date_pattern='dd/mm/yyyy', locale='pt_BR')
    calendario.pack(pady=20, fill="both", expand=True, padx=50)

    def buscar_consultas_do_dia():
        data_selecionada = calendario.get_date()
        messagebox.showinfo("Consultas", f"Visualizando agenda para: {data_selecionada}")

    tk.Button(agenda, text="Ver Consultas do Dia", command=buscar_consultas_do_dia, bg="#2196F3", fg="white", font=("Arial", 11, "bold")).pack(pady=20)