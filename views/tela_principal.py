import tkinter as tk
from views.tela_cadastro import abrir_tela_cadastro
from views.tela_cadastro import abrir_tela_cadastro
from views.tela_agenda import abrir_tela_agenda
from views.tela_espera import abrir_tela_espera

def iniciar_sistema():
    janela = tk.Tk()

    # Configurações da janela
    janela.title("Sistema de Agendamento")
    janela.geometry("700x500")
    janela.configure(bg="#f0f0f0")

    # Título
    titulo = tk.Label(
        janela,
        text="Sistema de Agendamento UBS",
        font=("Arial", 30, "bold"),
        bg="#f0f0f0",
        fg="#333"
    )

    titulo.pack(pady=30)

    # Texto de boas-vindas
    subtitulo = tk.Label(
        janela,
        text="Gerencie consultas e lista de espera",
        font=("Arial", 12),
        bg="#f0f0f0",
        fg="#666"
    )

    subtitulo.pack(pady=10)

    # Botão cadastrar
    
    botao_cadastro = tk.Button(
    janela,
    text="Cadastrar Paciente",
    width=25,
    height=2,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 11, "bold"),
    command=abrir_tela_cadastro
)

    botao_cadastro.pack(pady=15)

    # Botão visualizar agenda
    botao_agenda = tk.Button(
        janela,
        text="Visualizar Agenda",
        width=25,
        height=2,
        bg="#2196F3",
        fg="white",
        font=("Arial", 11, "bold"),
        command=abrir_tela_agenda
        
    )

    botao_agenda.pack(pady=15)

    # Botão lista de espera
    botao_espera = tk.Button(
        janela,
        text="Lista de Espera",
        width=25,
        height=2,
        bg="#FFAA00",
        fg="white",
        font=("Arial", 11, "bold")
    )

    botao_espera.pack(pady=15)

    janela.mainloop()