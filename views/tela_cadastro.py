import tkinter as tk


def abrir_tela_cadastro():
    cadastro = tk.Toplevel()

    cadastro.title("Cadastro de Paciente")
    cadastro.geometry("400x300")

    titulo = tk.Label(
        cadastro,
        text="Tela de Cadastro",
        font=("Arial", 18, "bold")
    )

    titulo.pack(pady=20)

    nome = tk.Label(
        cadastro,
        text="Aqui ficará o formulário futuramente"
    )

    nome.pack(pady=10)