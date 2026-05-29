import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_cadastro(janela_principal):
    cadastro = ttk.Toplevel(master=janela_principal)
    cadastro.title("Cadastro de Paciente - Fila de Espera")
    cadastro.state('zoomed')

    # Configuração de ícone (Fase Beta)
    caminho_icone = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icone.ico")
    if os.path.exists(caminho_icone):
        cadastro.iconbitmap(caminho_icone)

    def voltar():
        cadastro.destroy()
        janela_principal.deiconify()
        janela_principal.state('zoomed')

    cadastro.protocol("WM_DELETE_WINDOW", voltar)

    # -------------------------------------------------------------------------
    # BARRA SUPERIOR: Mantendo a identidade visual Azul e-SUS PEC
    # -------------------------------------------------------------------------
    frame_header = tk.Frame(cadastro, bg="#1B365D", height=70)
    frame_header.pack(fill=X, side=TOP, anchor=N)
    frame_header.pack_propagate(False)

    btn_voltar = ttk.Button(frame_header, text="← Menu Principal", command=voltar, bootstyle=LIGHT)
    btn_voltar.pack(side=LEFT, padx=20, pady=18)

    label_titulo = tk.Label(
        frame_header, 
        text="NOVO CADASTRO DE PACIENTE", 
        font=("Helvetica", 14, "bold"), 
        bg="#1B365D", 
        fg="white"
    )
    label_titulo.pack(side=RIGHT, padx=20, pady=18)

    # -------------------------------------------------------------------------
    # ÁREA DE CONTEÚDO (Fundo limpo e painel centralizado)
    # -------------------------------------------------------------------------
    frame_fundo = tk.Frame(cadastro, bg="#F8FAFC")
    frame_fundo.pack(fill=BOTH, expand=YES)

    # Card Centralizado para o Formulário
    card_cadastro = ttk.Frame(frame_fundo, padding=40, bootstyle=LIGHT)
    card_cadastro.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Título interno do Formulário
    ttk.Label(
        card_cadastro, 
        text="Informações do Paciente", 
        font=("Helvetica", 16, "bold"), 
        bootstyle=PRIMARY
    ).pack(pady=(0, 25), anchor=W)

    # --- CAMPO: NOME ---
    ttk.Label(card_cadastro, text="Nome Completo:", font=("Helvetica", 11)).pack(anchor=W, pady=2)
    entrada_nome = ttk.Entry(card_cadastro, width=45, font=("Helvetica", 11))
    entrada_nome.pack(pady=(0, 15), ipady=4) # ipady dá uma altura interna confortável para digitação

    # --- CAMPO: TELEFONE ---
    ttk.Label(card_cadastro, text="Telefone / WhatsApp:", font=("Helvetica", 11)).pack(anchor=W, pady=2)
    entrada_telefone = ttk.Entry(card_cadastro, width=45, font=("Helvetica", 11))
    entrada_telefone.pack(pady=(0, 15), ipady=4)

    # --- CAMPO: PROFISSIONAL ---
    ttk.Label(card_cadastro, text="Profissional / Médico(a):", font=("Helvetica", 11)).pack(anchor=W, pady=2)
    profissionais = ["Dra. Laurice", "Thiago", "Jamile", "Gerlando"]
    combo = ttk.Combobox(card_cadastro, values=profissionais, state="readonly", width=43, font=("Helvetica", 11))
    combo.pack(pady=(0, 25))
    combo.set(profissionais[0])

    # Lógica de persistência no Banco de Dados
    def salvar():
        nome = entrada_nome.get().strip()
        telefone = entrada_telefone.get().strip()
        profissional = combo.get()

        # Validação simples de campos vazios para evitar lixo no banco
        if not nome or not telefone:
            return messagebox.showwarning("Aviso", "Por favor, preencha todos os campos antes de salvar.")

        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            
            # Adicionado explicitamente o status 'Aguardando' padrão na inserção
            cursor.execute(
                "INSERT INTO pacientes (nome, telefone, profissional, status) VALUES (?, ?, ?, 'Aguardando')", 
                (nome, telefone, profissional)
            )
            
            conexao.commit()
            conexao.close()
            
            messagebox.showinfo("Sucesso", f"Paciente {nome} adicionado à Fila de Espera!")
            
            # Limpa os campos para o próximo cadastro
            entrada_nome.delete(0, tk.END)
            entrada_telefone.delete(0, tk.END)
            entrada_nome.focus() # Devolve o cursor para o campo nome
            
        except Exception as e: 
            messagebox.showerror("Erro no Banco", f"Não foi possível salvar: {e}")

# Configuração correta de estilo para a fonte do botão de salvar
    estilo_cadastro = ttk.Style()
    estilo_cadastro.configure('BotaoSalvar.TButton', font=('Helvetica', 12, 'bold'))

    # --- BOTÃO SALVAR (Versão blindada usando Style) ---
    btn_salvar = ttk.Button(
        card_cadastro, 
        text="📥 Salvar na Fila de Espera", 
        bootstyle=SUCCESS, 
        width=35,
        style='BotaoSalvar.TButton',  # <-- Usa o estilo em vez do parâmetro font
        command=salvar
    )
    btn_salvar.pack(pady=10)