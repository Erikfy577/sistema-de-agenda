import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import os
from PIL import Image, ImageTk
from views.tela_cadastro import abrir_tela_cadastro
from views.tela_agenda import abrir_tela_agenda
from views.tela_espera import abrir_tela_espera

def abrir_tela_principal():
    # Inicializa a janela principal com o tema Bootstrap
    janela = ttk.Window(themename="flatly")
    janela.title("Sistema de Agendamento UBS")
    janela.state('zoomed')

    diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_icone = os.path.join(diretorio_raiz, "assets", "icone.ico")
    
    # Atualizado para a nova imagem
    caminho_fundo = os.path.join(diretorio_raiz, "assets", "tela_principal.png")

    if os.path.exists(caminho_icone):
        janela.iconbitmap(caminho_icone)

    def abrir_e_esconder(funcao_abrir):
        janela.withdraw()
        funcao_abrir(janela)

    # --- PLANO DE FUNDO COM PILLOW ---
    label_fundo = None
    imagem_original = None

    if os.path.exists(caminho_fundo):
        try:
            imagem_original = Image.open(caminho_fundo)
            label_fundo = tk.Label(janela)
            label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Erro no fundo: {e}")

    def redimensionar_fundo(event):
        nonlocal imagem_original, label_fundo
        
        # CORREÇÃO DO BUG: Garante que o redimensionamento só usa as medidas da janela principal
        # e ignora eventos gerados por frames ou botões internos durante a abertura
        if event.widget == janela and imagem_original and label_fundo:
            largura = event.width
            altura = event.height
            
            # Previne erros se a janela inicializar minimizada ou pequena demais
            if largura > 100 and altura > 100:
                img_redimensionada = imagem_original.resize((largura, altura), Image.Resampling.LANCZOS)
                foto_tk = ImageTk.PhotoImage(img_redimensionada)
                label_fundo.configure(image=foto_tk)
                label_fundo.image = foto_tk

    janela.bind('<Configure>', redimensionar_fundo)

    # --- CARD CENTRAL GIGANTE ---
    card_central = ttk.Frame(janela, padding=60, bootstyle=LIGHT)
    card_central.place(relx=0.5, rely=0.5, anchor=CENTER)

    ttk.Label(
        card_central, 
        text="SISTEMA DE AGENDAMENTO UBS", 
        font=("Helvetica", 24, "bold"), 
        bootstyle=PRIMARY
    ).pack(pady=(0, 40))

    # Configuração correta de estilo para fontes no ttkbootstrap
    estilo = ttk.Style()
    estilo.configure('Grande.TButton', font=('Helvetica', 13, 'bold'))

    # --- BOTÕES USANDO O ESTILO DA FASE BETA ---
    ttk.Button(
        card_central, text="➕ Cadastrar Paciente", bootstyle=SUCCESS, width=35,
        style='Grande.TButton', command=lambda: abrir_e_esconder(abrir_tela_cadastro)
    ).pack(pady=15)

    ttk.Button(
        card_central, text="🗓️ Visualizar Agenda", bootstyle=INFO, width=35,
        style='Grande.TButton', command=lambda: abrir_e_esconder(abrir_tela_agenda)
    ).pack(pady=15)

    ttk.Button(
        card_central, text="⏳ Gerenciar Fila de Espera", bootstyle=WARNING, width=35,
        style='Grande.TButton', command=lambda: abrir_e_esconder(abrir_tela_espera)
    ).pack(pady=15)

    ttk.Label(card_central, text="Fase Beta - Gestão Unificada", font=("Helvetica", 11), bootstyle=SECONDARY).pack(pady=(30, 0))

    janela.mainloop()