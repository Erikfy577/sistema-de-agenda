import tkinter as tk
from views.tela_cadastro import abrir_tela_cadastro
from views.tela_agenda import abrir_tela_agenda
from views.tela_espera import abrir_tela_espera

def iniciar_sistema():
    janela = tk.Tk()
    janela.title("Sistema de Agendamento")
    janela.state('zoomed') # Abre maximizado
    janela.configure(bg="#f0f0f0")

    # Função auxiliar para abrir e esconder a principal
    def abrir_e_esconder(funcao_abrir):
        janela.withdraw() # Esconde a tela principal
        funcao_abrir(janela) # Abre a nova tela passando a principal como 'parent'

    titulo = tk.Label(janela, text="Sistema de Agendamento UBS", font=("Arial", 30, "bold"), bg="#f0f0f0", fg="#333")
    titulo.pack(pady=30)

    tk.Button(janela, text="Cadastrar Paciente", width=25, height=2, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), 
              command=lambda: abrir_e_esconder(abrir_tela_cadastro)).pack(pady=15)
    
    tk.Button(janela, text="Visualizar Agenda", width=25, height=2, bg="#2196F3", fg="white", font=("Arial", 11, "bold"), 
              command=lambda: abrir_e_esconder(abrir_tela_agenda)).pack(pady=15)
    
    tk.Button(janela, text="Gerenciar Fila de Espera", width=25, height=2, bg="#FF9800", fg="white", font=("Arial", 11, "bold"), 
              command=lambda: abrir_e_esconder(abrir_tela_espera)).pack(pady=15)

    janela.mainloop()