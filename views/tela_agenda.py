import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import os
import webbrowser
from urllib.parse import quote
from PIL import Image, ImageTk

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_agenda(janela_principal):
    agenda = ttk.Toplevel(master=janela_principal)
    agenda.title("Agenda Mensal e Sincronização")
    agenda.state('zoomed')

    caminho_icone = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icone.ico")
    caminho_fundo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "tela_agenda.png")

    if os.path.exists(caminho_icone): agenda.iconbitmap(caminho_icone)

    def voltar():
        agenda.destroy()
        janela_principal.deiconify()
        janela_principal.state('zoomed')

    agenda.protocol("WM_DELETE_WINDOW", voltar)

    # -------------------------------------------------------------------------
    # BARRA SUPERIOR
    # -------------------------------------------------------------------------
    frame_header = tk.Frame(agenda, bg="#1B365D", height=70)
    frame_header.pack(fill=X, side=TOP, anchor=N)
    frame_header.pack_propagate(False)
    ttk.Button(frame_header, text="← Menu Principal", command=voltar, bootstyle=LIGHT).pack(side=LEFT, padx=20, pady=18)
    tk.Label(frame_header, text="CENTRAL DE AGENDAMENTOS E NOTIFICAÇÃO", font=("Helvetica", 14, "bold"), bg="#1B365D", fg="white").pack(side=RIGHT, padx=20, pady=18)

    # -------------------------------------------------------------------------
    # FUNDO
    # -------------------------------------------------------------------------
    frame_fundo = tk.Frame(agenda, bg="#F8FAFC")
    frame_fundo.pack(fill=BOTH, expand=YES)
    label_imagem_fundo = tk.Label(frame_fundo)
    imagem_original = Image.open(caminho_fundo) if os.path.exists(caminho_fundo) else None
    if imagem_original: label_imagem_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    def redimensionar_fundo(event):
        if event.widget == agenda and imagem_original:
            img_redimensionada = imagem_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
            foto_tk = ImageTk.PhotoImage(img_redimensionada)
            label_imagem_fundo.configure(image=foto_tk)
            label_imagem_fundo.image = foto_tk

    agenda.bind('<Configure>', redimensionar_fundo)

    # -------------------------------------------------------------------------
    # CARD CENTRAL
    # -------------------------------------------------------------------------
    card_agenda = tk.Frame(frame_fundo, bg="white", padx=20, pady=20)
    card_agenda.place(relx=0.5, rely=0.53, relwidth=0.9, relheight=0.8, anchor=CENTER)

    # -------------------------------------------------------------------------
    # COLUNA ESQUERDA (Filtros e Calendário)
    # -------------------------------------------------------------------------
    col_esquerda = tk.Frame(card_agenda, bg="white")
    col_esquerda.pack(side=LEFT, fill=BOTH, padx=10, expand=False)

    tk.Label(col_esquerda, text="1. Filtrar Profissional", font=("Helvetica", 12, "bold"), bg="white", fg="#1B365D").pack(anchor=W, pady=5)
    profissionais = ["Dra. Jamile", "Dra. Laurice", "Dr. Gerlando"]
    combo_filtro = ttk.Combobox(col_esquerda, values=profissionais, state="readonly", font=("Helvetica", 12))
    combo_filtro.pack(fill=X, pady=(0, 20))
    combo_filtro.set(profissionais[0])

    tk.Label(col_esquerda, text="2. Selecione a Data", font=("Helvetica", 12, "bold"), bg="white", fg="#1B365D").pack(anchor=W, pady=5)
    calendario = Calendar(col_esquerda, selectmode='day', date_pattern='dd/mm/yyyy', locale='pt_BR', background="#2C3E50", foreground="white", selectbackground="#18BC9C")
    calendario.pack(pady=10, fill=BOTH, expand=YES)

    # -------------------------------------------------------------------------
    # COLUNA DIREITA (Tabela e Controles)
    # -------------------------------------------------------------------------
    col_direita = tk.Frame(card_agenda, bg="white")
    col_direita.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10)

    tk.Label(col_direita, text="3. Pacientes Agendados", font=("Helvetica", 12, "bold"), bg="white", fg="#1B365D").pack(anchor=W, pady=5)
    colunas = ("ID", "Nome", "Telefone", "Prioridade")
    tabela_dia = ttk.Treeview(col_direita, columns=colunas, show="headings", bootstyle=INFO)
    for col in colunas: 
        tabela_dia.heading(col, text=col)
        tabela_dia.column(col, anchor=CENTER)
    tabela_dia.column("ID", width=50)
    tabela_dia.pack(fill=BOTH, expand=YES, pady=5)

    # -------------------------------------------------------------------------
    # CONTROLES DE API (WhatsApp e Google Calendar)
    # -------------------------------------------------------------------------
    frame_controles = ttk.Labelframe(col_direita, text=" 4. Configurar Envio (API) ", padding=15, bootstyle=PRIMARY)
    frame_controles.pack(fill=X, pady=15)
    
    ttk.Label(frame_controles, text="Período da Consulta:").grid(row=0, column=0, padx=5, sticky=W)
    combo_periodo = ttk.Combobox(frame_controles, values=["Manhã", "Tarde", "Noite"], state="readonly", width=30)
    combo_periodo.grid(row=0, column=1, padx=5, sticky=W)
    combo_periodo.set("Manhã")

    def acao_api_whatsapp():
        selecao = tabela_dia.selection()
        if not selecao: 
            return messagebox.showwarning("Aviso", "Selecione um paciente.")
        
        item = tabela_dia.item(selecao[0])['values']
        tel = "".join(filter(str.isdigit, str(item[2])))
        if not tel.startswith("55"): tel = f"55{tel}"
        
        msg = f"Olá, *{item[1]}*! 🏥\n\nConfirmamos sua consulta com *{combo_filtro.get()}*.\n\n🗓️ *Data:* {calendario.get_date()}\n🕒 *Período:* {combo_periodo.get()}\n\nCompareça portando Cartão SUS e documento."
        webbrowser.open(f"https://api.whatsapp.com/send?phone={tel}&text={quote(msg)}")

    def acao_api_google():
        selecao = tabela_dia.selection()
        if not selecao: 
            return messagebox.showwarning("Aviso", "Selecione um paciente para sincronizar.")
        
        item = tabela_dia.item(selecao[0])['values']
        data_br = calendario.get_date()
        dia, mes, ano = data_br.split('/')
        data_google = f"{ano}{mes}{dia}"
        
        profissional = combo_filtro.get()
        titulo = quote(f"Consulta: {item[1]} ({profissional})")
        detalhes = quote(f"Paciente: {item[1]}\nTelefone: {item[2]}\nProfissional: {profissional}\nPeríodo: {combo_periodo.get()}")
        
        
        hora_inicio = "080000"
        hora_fim = "090000"
        if combo_periodo.get() == "Tarde":
            hora_inicio = "130000"
            hora_fim = "140000"
        elif combo_periodo.get() == "Noite":
            hora_inicio = "170000"
            hora_fim = "180000"
        
        
        url_google = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titulo}&dates={data_google}T{hora_inicio}/{data_google}T{hora_fim}&details={detalhes}"
        webbrowser.open(url_google)

    btn_frame = ttk.Frame(frame_controles)
    btn_frame.grid(row=1, column=0, columnspan=2, pady=15, sticky=W)
    ttk.Button(btn_frame, text="💬 Enviar WhatsApp", command=acao_api_whatsapp, bootstyle=SUCCESS, width=20).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="🗓️ Sincronizar Google", command=acao_api_google, bootstyle=INFO, width=20).pack(side=LEFT, padx=5)

    # -------------------------------------------------------------------------
    # CARREGAMENTO DE DADOS
    # -------------------------------------------------------------------------
    def atualizar_tabela(*args):
        for item in tabela_dia.get_children(): tabela_dia.delete(item)
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            
            
            query = """
                SELECT id, nome, telefone, prioridade FROM pacientes 
                WHERE status = 'Agendado' AND profissional = ? AND data_consulta = ?
                ORDER BY CASE prioridade WHEN 'Urgente' THEN 1 WHEN 'Prioritário' THEN 2 ELSE 3 END, id ASC
            """
            cursor.execute(query, (combo_filtro.get(), calendario.get_date()))
            for linha in cursor.fetchall(): 
                tabela_dia.insert("", END, values=linha)
            
            conexao.close()
        except Exception as e: 
            print(f"Erro ao atualizar tabela: {e}")

    
    calendario.bind("<<CalendarSelected>>", atualizar_tabela)
    combo_filtro.bind("<<ComboboxSelected>>", atualizar_tabela)
    atualizar_tabela()