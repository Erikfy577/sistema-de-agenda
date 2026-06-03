import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from PIL import Image, ImageTk

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_cadastro(janela_principal):
    cadastro = ttk.Toplevel(master=janela_principal)
    cadastro.title("Cadastro de Paciente - Fila de Espera")
    cadastro.state('zoomed')

    caminho_icone = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icone.ico")
    caminho_fundo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "tela_cadastro.png")

    if os.path.exists(caminho_icone):
        cadastro.iconbitmap(caminho_icone)

    def voltar():
        cadastro.destroy()
        janela_principal.deiconify()
        janela_principal.state('zoomed')

    cadastro.protocol("WM_DELETE_WINDOW", voltar)

    frame_header = tk.Frame(cadastro, bg="#1B365D", height=70)
    frame_header.pack(fill=X, side=TOP, anchor=N)
    frame_header.pack_propagate(False)

    btn_voltar = ttk.Button(frame_header, text="← Menu Principal", command=voltar, bootstyle=LIGHT)
    btn_voltar.pack(side=LEFT, padx=20, pady=18)

    tk.Label(frame_header, text="NOVO CADASTRO DE PACIENTE", font=("Helvetica", 14, "bold"), bg="#1B365D", fg="white").pack(side=RIGHT, padx=20, pady=18)

    frame_fundo = tk.Frame(cadastro, bg="#F8FAFC")
    frame_fundo.pack(fill=BOTH, expand=YES)

    label_imagem_fundo = None
    imagem_original = None

    if os.path.exists(caminho_fundo):
        try:
            imagem_original = Image.open(caminho_fundo)
            label_imagem_fundo = tk.Label(frame_fundo)
            label_imagem_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Erro ao carregar fundo: {e}")

    def redimensionar_fundo(event):
        nonlocal imagem_original, label_imagem_fundo
        if imagem_original and label_imagem_fundo:
            img_redimensionada = imagem_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
            foto_tk = ImageTk.PhotoImage(img_redimensionada)
            label_imagem_fundo.configure(image=foto_tk)
            label_imagem_fundo.image = foto_tk

    frame_fundo.bind('<Configure>', redimensionar_fundo)

    COR_FALSO_VIDRO = "#EBF4F6" 

    card_cadastro = tk.Frame(frame_fundo, bg=COR_FALSO_VIDRO)
    card_cadastro.place(relx=0.74, rely=0.55, anchor=CENTER)

    tk.Label(card_cadastro, text="Informações do Paciente", font=("Helvetica", 18, "bold"), bg=COR_FALSO_VIDRO, fg="#1B365D").pack(pady=(0, 15), anchor=W)

    # NOME
    tk.Label(card_cadastro, text="Nome Completo:", font=("Helvetica", 11, "bold"), bg=COR_FALSO_VIDRO, fg="#555").pack(anchor=W, pady=2)
    entrada_nome = ttk.Entry(card_cadastro, width=38, font=("Helvetica", 11))
    entrada_nome.pack(pady=(0, 15), ipady=5)

    # TELEFONE
    tk.Label(card_cadastro, text="Telefone / WhatsApp:", font=("Helvetica", 11, "bold"), bg=COR_FALSO_VIDRO, fg="#555").pack(anchor=W, pady=2)
    entrada_telefone = ttk.Entry(card_cadastro, width=38, font=("Helvetica", 11))
    entrada_telefone.pack(pady=(0, 15), ipady=5)

    # MÉDICOS ATUALIZADOS
    tk.Label(card_cadastro, text="Profissional / Médico(a):", font=("Helvetica", 11, "bold"), bg=COR_FALSO_VIDRO, fg="#555").pack(anchor=W, pady=2)
    profissionais = ["Dra. Jamile", "Dra. Laurice", "Dr. Gerlando"]
    combo_medico = ttk.Combobox(card_cadastro, values=profissionais, state="readonly", width=36, font=("Helvetica", 11))
    combo_medico.pack(pady=(0, 15))
    combo_medico.set(profissionais[0])

    # NOVO CAMPO: PRIORIDADE
    tk.Label(card_cadastro, text="Prioridade Clínica:", font=("Helvetica", 11, "bold"), bg=COR_FALSO_VIDRO, fg="#555").pack(anchor=W, pady=2)
    prioridades = ["Eletivo", "Prioritário", "Urgente"]
    combo_prioridade = ttk.Combobox(card_cadastro, values=prioridades, state="readonly", width=36, font=("Helvetica", 11))
    combo_prioridade.pack(pady=(0, 25))
    combo_prioridade.set("Eletivo")

    def salvar():
        nome = entrada_nome.get().strip()
        telefone = entrada_telefone.get().strip()
        profissional = combo_medico.get()
        prioridade = combo_prioridade.get()

        if not nome or not telefone:
            return messagebox.showwarning("Aviso", "Por favor, preencha todos os campos antes de salvar.")

        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            # Inserção agora envia a prioridade para o banco
            cursor.execute(
                "INSERT INTO pacientes (nome, telefone, profissional, status, prioridade) VALUES (?, ?, ?, 'Aguardando', ?)", 
                (nome, telefone, profissional, prioridade)
            )
            conexao.commit()
            conexao.close()
            
            messagebox.showinfo("Sucesso", f"Paciente {nome} cadastrado como {prioridade}!")
            entrada_nome.delete(0, tk.END)
            entrada_telefone.delete(0, tk.END)
            combo_prioridade.set("Eletivo") # Reseta a prioridade
            entrada_nome.focus()
            
        except Exception as e: 
            messagebox.showerror("Erro no Banco", f"Não foi possível salvar: {e}")

    estilo_cadastro = ttk.Style()
    estilo_cadastro.configure('BotaoSalvar.TButton', font=('Helvetica', 12, 'bold'))

    btn_salvar = ttk.Button(card_cadastro, text="📥 Salvar na Fila de Espera", bootstyle=DARK, width=32, style='BotaoSalvar.TButton', command=salvar)
    btn_salvar.pack(pady=10)