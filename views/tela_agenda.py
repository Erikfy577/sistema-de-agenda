import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import os
import webbrowser
from urllib.parse import quote

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_agenda(janela_principal):
    agenda = ttk.Toplevel(master=janela_principal)
    agenda.title("Agenda Mensal e Sincronização")
    agenda.state('zoomed')

    # Configuração de ícone
    caminho_icone = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icone.ico")
    if os.path.exists(caminho_icone):
        agenda.iconbitmap(caminho_icone)

    def voltar():
        agenda.destroy()
        janela_principal.deiconify()
        janela_principal.state('zoomed')

    agenda.protocol("WM_DELETE_WINDOW", voltar)

    # -------------------------------------------------------------------------
    # BARRA SUPERIOR
    # -------------------------------------------------------------------------
    frame_header = ttk.Frame(agenda, bootstyle=PRIMARY, padding=15)
    frame_header.pack(fill=X, side=TOP, anchor=N)

    # Título interno usando estilo INVERSE para herdar o fundo escuro automaticamente
    label_titulo = ttk.Label(
        frame_header, 
        text="CENTRAL DE AGENDAMENTOS E NOTIFICAÇÃO", 
        font=("Helvetica", 14, "bold"), 
        bootstyle=(INVERSE, PRIMARY)
    )

    # Botão Voltar ajustado para o estilo padrão de alto contraste sobre o Dark
    btn_voltar = ttk.Button(frame_header, text="← Menu Principal", command=voltar, bootstyle=INFO)
    
    # Renderização limpa em um único fluxo do pack
    btn_voltar.pack(side=LEFT, padx=10)
    label_titulo.pack(side=RIGHT, padx=10)

    # -------------------------------------------------------------------------
    # CORPO DA TELA
    # -------------------------------------------------------------------------
    container = ttk.Frame(agenda, padding=20)
    container.pack(fill=BOTH, expand=YES)

    # --- COLUNA ESQUERDA (Calendário) ---
    col_esquerda = ttk.Frame(container)
    col_esquerda.pack(side=LEFT, fill=BOTH, padx=10)

    ttk.Label(col_esquerda, text="1. Selecione a Data", font=("Helvetica", 12, "bold")).pack(anchor=W, pady=5)
    
    calendario = Calendar(col_esquerda, selectmode='day', date_pattern='dd/mm/yyyy', locale='pt_BR',
                         background="#2C3E50", foreground="white", selectbackground="#18BC9C")
    calendario.pack(pady=10, fill=BOTH, expand=YES)

    # --- COLUNA DIREITA (Tabela e Botões) ---
    col_direita = ttk.Frame(container)
    col_direita.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10)

    ttk.Label(col_direita, text="2. Pacientes Agendados", font=("Helvetica", 12, "bold"), bootstyle=PRIMARY).pack(anchor=W, pady=5)

    # Tabela com estilo do Bootstrap
    colunas = ("ID", "Nome", "Telefone", "Profissional")
    tabela_dia = ttk.Treeview(col_direita, columns=colunas, show="headings", bootstyle=INFO)
    for col in colunas:
        tabela_dia.heading(col, text=col)
        tabela_dia.column(col, anchor=CENTER)
    tabela_dia.column("ID", width=50)
    tabela_dia.pack(fill=BOTH, expand=YES, pady=5)

    # --- ÁREA DE CONTROLES (Período e APIs) ---
    frame_controles = ttk.Labelframe(col_direita, text=" 3. Configurar Envio (API) ", padding=15, bootstyle=PRIMARY)
    frame_controles.pack(fill=X, pady=15)

    ttk.Label(frame_controles, text="Período da Consulta:").grid(row=0, column=0, padx=5, sticky=W)
    periodos = ["Manhã (07:00 às 10:00)", "Tarde (13:00 às 16:00)", "Noite (17:00 às 19:00)"]
    combo_periodo = ttk.Combobox(frame_controles, values=periodos, state="readonly", width=30)
    combo_periodo.grid(row=0, column=1, padx=5, sticky=W)
    combo_periodo.set(periodos[0])

    def formatar_telefone(tel):
        return "".join(filter(str.isdigit, str(tel)))

    def acao_api_whatsapp():
        selecao = tabela_dia.selection()
        if not selecao:
            return messagebox.showwarning("Aviso", "Selecione um paciente na lista acima.")
        
        item = tabela_dia.item(selecao[0])['values']
        data_sel = calendario.get_date()
        periodo_sel = combo_periodo.get()
        telefone = formatar_telefone(item[2])
        if not telefone.startswith("55"): telefone = f"55{telefone}"

        msg = (f"Olá, *{item[1]}*! 🏥\n\nConfirmamos sua consulta com o profissional *{item[3]}*.\n\n"
               f"🗓️ *Data:* {data_sel}\n"
               f"🕒 *Período:* {periodo_sel}\n\n"
               f"Por favor, compareça à UBS portando Cartão SUS e documento com foto.")
        
        webbrowser.open(f"https://api.whatsapp.com/send?phone={telefone}&text={quote(msg)}")

    def acao_api_google():
        selecao = tabela_dia.selection()
        if not selecao:
            return messagebox.showwarning("Aviso", "Selecione um paciente.")
        
        item = tabela_dia.item(selecao[0])['values']
        data_br = calendario.get_date()
        dia, mes, ano = data_br.split('/')
        data_google = f"{ano}{mes}{dia}"
        
        titulo = quote(f"Consulta: {item[1]} ({item[3]})")
        detalhes = quote(f"Paciente: {item[1]}\nTelefone: {item[2]}\nProfissional: {item[3]}\nPeríodo: {combo_periodo.get()}")
        
        url_google = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titulo}&dates={data_google}T100000Z/{data_google}T110000Z&details={detalhes}"
        webbrowser.open(url_google)

    btn_frame = ttk.Frame(frame_controles)
    btn_frame.grid(row=1, column=0, columnspan=2, pady=15, sticky=W)

    ttk.Button(btn_frame, text="💬 Enviar WhatsApp", command=acao_api_whatsapp, bootstyle=SUCCESS, width=20).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="🗓️ Sincronizar Google", command=acao_api_google, bootstyle=INFO, width=20).pack(side=LEFT, padx=5)

    def atualizar_tabela(*args):
        for item in tabela_dia.get_children(): tabela_dia.delete(item)
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, telefone, profissional FROM pacientes WHERE status = 'Agendado'")
            for linha in cursor.fetchall():
                tabela_dia.insert("", END, values=linha)
            conexao.close()
        except Exception as e: print(e)

    calendario.bind("<<CalendarSelected>>", atualizar_tabela)
    atualizar_tabela()