import tkinter as tk


def abrir_tela_espera():
    espera = tk.Toplevel()

    espera.title("Lista de Espera")
    espera.geometry("500x400")

    titulo = tk.Label(
        espera,
        text="Lista de Espera",
        font=("Arial", 18, "bold")
    )

    titulo.pack(pady=20)

    texto = tk.Label(
        espera,
        text="Aqui aparecerá a fila de espera"
    )

    texto.pack(pady=10)