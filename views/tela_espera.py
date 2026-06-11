import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import os
from PIL import Image, ImageTk

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_espera(janela_principal):
    espera = ttk.Toplevel(master=janela_principal)
    espera.title("Gerenciamento de Fila e Vagas")
    espera.state('zoomed')

    caminho_icone = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icone.ico")
    caminho_fundo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "tela_espera.png")

    if os.path.exists(caminho_icone): espera.iconbitmap(caminho_icone)

    def voltar():
        espera.destroy()
        janela_principal.deiconify()
        janela_principal.state('zoomed')

    espera.protocol("WM_DELETE_WINDOW", voltar)

    # -------------------------------------------------------------------------
    # BARRA SUPERIOR
    # -------------------------------------------------------------------------
    frame_header = tk.Frame(espera, bg="#1B365D", height=70)
    frame_header.pack(fill=X, side=TOP, anchor=N)
    frame_header.pack_propagate(False)
    ttk.Button(frame_header, text="← Menu Principal", command=voltar, bootstyle=LIGHT).pack(side=LEFT, padx=20, pady=18)
    tk.Label(frame_header, text="GERENCIAMENTO DA FILA DE ESPERA", font=("Helvetica", 14, "bold"), bg="#1B365D", fg="white").pack(side=RIGHT, padx=20, pady=18)

    # -------------------------------------------------------------------------
    # FUNDO
    # -------------------------------------------------------------------------
    frame_fundo = tk.Frame(espera, bg="#F8FAFC")
    frame_fundo.pack(fill=BOTH, expand=YES)
    label_imagem_fundo = tk.Label(frame_fundo)
    imagem_original = Image.open(caminho_fundo) if os.path.exists(caminho_fundo) else None
    if imagem_original: label_imagem_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    def redimensionar_fundo(event):
        if imagem_original and label_imagem_fundo:
            img_redimensionada = imagem_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
            foto_tk = ImageTk.PhotoImage(img_redimensionada)
            label_imagem_fundo.configure(image=foto_tk)
            label_imagem_fundo.image = foto_tk

    frame_fundo.bind('<Configure>', redimensionar_fundo)

    # -------------------------------------------------------------------------
    # CARD CENTRAL (Aumentado para 0.88 para evitar cortes)
    # -------------------------------------------------------------------------
    card_espera = tk.Frame(frame_fundo, bg="white", padx=20, pady=20)
    card_espera.place(relx=0.5, rely=0.53, relwidth=0.9, relheight=0.88, anchor=CENTER)

    # CRIANDO E EMPACOTANDO OS CONTAINERS NA ORDEM CORRETA (Isso resolve o bug visual)
    frame_topo = tk.Frame(card_espera, bg="white")
    frame_topo.pack(side=TOP, fill=X, pady=(0, 15))

    frame_inferior = tk.Frame(card_espera, bg="white")
    frame_inferior.pack(side=BOTTOM, fill=X, pady=(10, 0)) # Garante o espaço dos botões no fundo

    frame_tabelas = tk.Frame(card_espera, bg="white")
    frame_tabelas.pack(side=TOP, fill=BOTH, expand=YES) # Ocupa apenas o espaço que sobrou no meio

    # -------------------------------------------------------------------------
    # 1. PREENCHENDO O TOPO (Filtro e Calendário)
    # -------------------------------------------------------------------------
    tk.Label(frame_topo, text="Profissional:", font=("Helvetica", 12, "bold"), bg="white", fg="#555").pack(side=LEFT, padx=5)
    combo_filtro = ttk.Combobox(frame_topo, values=["Dra. Jamile", "Dra. Laurice", "Dr. Gerlando"], state="readonly", font=("Helvetica", 12), width=20)
    combo_filtro.pack(side=LEFT, padx=10)
    combo_filtro.set("Dra. Jamile")

    tk.Label(frame_topo, text="Data do Agendamento:", font=("Helvetica", 12, "bold"), bg="white", fg="#555").pack(side=LEFT, padx=(30, 5))
    calendario = Calendar(frame_topo, selectmode='day', date_pattern='dd/mm/yyyy', locale='pt_BR')
    calendario.pack(side=LEFT, padx=10)

    # -------------------------------------------------------------------------
    # 2. PREENCHENDO AS TABELAS
    # -------------------------------------------------------------------------
    frame_tabelas.columnconfigure(0, weight=1)
    frame_tabelas.columnconfigure(1, weight=1)

    colunas = ("Sel", "ID", "Nome", "Telefone", "Prioridade")

    tk.Label(frame_tabelas, text="Fila de Espera (Aguardando Data)", font=("Helvetica", 12, "bold"), bg="white", fg="#E67E22").grid(row=0, column=0, pady=5)
    tabela_espera = ttk.Treeview(frame_tabelas, columns=colunas, show="headings", bootstyle=WARNING)
    for col in colunas: tabela_espera.heading(col, text=col)
    tabela_espera.column("Sel", width=40, anchor=CENTER); tabela_espera.column("ID", width=50, anchor=CENTER)
    tabela_espera.grid(row=1, column=0, padx=10, sticky="nsew")

    tk.Label(frame_tabelas, text="Lista do Dia (Agendados)", font=("Helvetica", 12, "bold"), bg="white", fg="#27AE60").grid(row=0, column=1, pady=5)
    tabela_agenda = ttk.Treeview(frame_tabelas, columns=colunas, show="headings", bootstyle=SUCCESS)
    for col in colunas: tabela_agenda.heading(col, text=col)
    tabela_agenda.column("Sel", width=40, anchor=CENTER); tabela_agenda.column("ID", width=50, anchor=CENTER)
    tabela_agenda.grid(row=1, column=1, padx=10, sticky="nsew")
    frame_tabelas.rowconfigure(1, weight=1)

    # CAIXINHAS
    def alternar_caixinha(event, tabela):
        if tabela.identify("region", event.x, event.y) == "cell" and tabela.identify_column(event.x) == '#1':
            item = tabela.focus()
            if item:
                valores = list(tabela.item(item, 'values'))
                valores[0] = '☑' if valores[0] == '☐' else '☐'
                tabela.item(item, values=valores)

    tabela_espera.bind('<ButtonRelease-1>', lambda e: alternar_caixinha(e, tabela_espera))
    tabela_agenda.bind('<ButtonRelease-1>', lambda e: alternar_caixinha(e, tabela_agenda))

    # LÓGICA DE DADOS
    def carregar_listas(*args):
        medico, data_sel = combo_filtro.get(), calendario.get_date()
        for item in tabela_espera.get_children(): tabela_espera.delete(item)
        for item in tabela_agenda.get_children(): tabela_agenda.delete(item)
            
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            query_base = """
                SELECT id, nome, telefone, prioridade FROM pacientes WHERE profissional = ? AND status = ? {data_filtro}
                ORDER BY CASE prioridade WHEN 'Urgente' THEN 1 WHEN 'Prioritário' THEN 2 ELSE 3 END, id ASC
            """
            
            cursor.execute(query_base.format(data_filtro=""), (medico, 'Aguardando'))
            for linha in cursor.fetchall(): tabela_espera.insert("", END, values=('☐',) + linha)
                
            cursor.execute(query_base.format(data_filtro="AND data_consulta = ?"), (medico, 'Agendado', data_sel))
            for linha in cursor.fetchall(): tabela_agenda.insert("", END, values=('☐',) + linha)
            conexao.close()
        except Exception as e: print(f"Erro: {e}")

    combo_filtro.bind("<<ComboboxSelected>>", carregar_listas)
    calendario.bind("<<CalendarSelected>>", carregar_listas)

    # MOVIMENTAÇÃO
    def mover_pacientes_lote(ids, novo_status, data=None):
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            placeholders = ','.join('?' * len(ids))
            cursor.execute(f"UPDATE pacientes SET status = ?, data_consulta = ? WHERE id IN ({placeholders})", [novo_status, data] + ids)
            conexao.commit()
            conexao.close()
            carregar_listas()
        except Exception as e: messagebox.showerror("Erro", f"Falha: {e}")

    def acao_mover_para_agenda():
        itens = [item for item in tabela_espera.get_children() if tabela_espera.item(item)['values'][0] == '☑']
        if not itens: return messagebox.showwarning("Aviso", "Marque na Fila de Espera.")
        mover_pacientes_lote([tabela_espera.item(i)['values'][1] for i in itens], 'Agendado', calendario.get_date())

    def acao_voltar_para_espera():
        itens = [item for item in tabela_agenda.get_children() if tabela_agenda.item(item)['values'][0] == '☑']
        if not itens: return messagebox.showwarning("Aviso", "Marque na Lista do Dia.")
        mover_pacientes_lote([tabela_agenda.item(i)['values'][1] for i in itens], 'Aguardando', None)

    def excluir_pacientes_lote():
        marcados = [tabela_espera.item(i)['values'][1] for i in tabela_espera.get_children() if tabela_espera.item(i)['values'][0] == '☑']
        marcados += [tabela_agenda.item(i)['values'][1] for i in tabela_agenda.get_children() if tabela_agenda.item(i)['values'][0] == '☑']
        if not marcados: return messagebox.showwarning("Aviso", "Marque para excluir.")
        if messagebox.askyesno("Confirmar", f"Deletar {len(marcados)} paciente(s)?"):
            try:
                conexao = sqlite3.connect(obter_caminho_banco())
                conexao.cursor().execute(f"DELETE FROM pacientes WHERE id IN ({','.join('?'*len(marcados))})", marcados)
                conexao.commit(); conexao.close(); carregar_listas()
            except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")

    # -------------------------------------------------------------------------
    # 3. PREENCHENDO O INFERIOR (Botões corrigidos e com mais respiro)
    # -------------------------------------------------------------------------
    ttk.Button(frame_inferior, text="Mover para Agenda ➔", bootstyle=SUCCESS, command=acao_mover_para_agenda).pack(side=LEFT, padx=5, ipady=3)
    ttk.Button(frame_inferior, text="⬅ Voltar para Fila", bootstyle=WARNING, command=acao_voltar_para_espera).pack(side=LEFT, padx=5, ipady=3)
    ttk.Button(frame_inferior, text="🗑️ Excluir Selecionados", bootstyle=DANGER, command=excluir_pacientes_lote).pack(side=RIGHT, padx=5, ipady=3)

    carregar_listas()