import tkinter as tk


def abrir_tela_agenda():
    agenda = tk.Toplevel()

    agenda.title("Agenda de Consultas")
    agenda.geometry("500x400")

    titulo = tk.Label(
        agenda,
        text="Agenda de Consultas",
        font=("Arial", 18, "bold")
    )

    titulo.pack(pady=20)

    texto = tk.Label(
        agenda,
        text="Aqui aparecerão os agendamentos"
    )

    texto.pack(pady=10)