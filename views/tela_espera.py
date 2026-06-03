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

def abrir_tela_espera(janela_principal):
    espera = ttk.Toplevel(master=janela_principal)
    espera.title("Gerenciamento de Fila e Vagas")
    espera.state('zoomed')

    caminho_icone = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icone.ico")
    caminho_fundo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "tela_espera.png")

    if os.path.exists(caminho_icone):
        espera.iconbitmap(caminho_icone)

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

    btn_voltar = ttk.Button(frame_header, text="← Menu Principal", command=voltar, bootstyle=LIGHT)
    btn_voltar.pack(side=LEFT, padx=20, pady=18)

    tk.Label(frame_header, text="GERENCIAMENTO DA FILA DE ESPERA", font=("Helvetica", 14, "bold"), bg="#1B365D", fg="white").pack(side=RIGHT, padx=20, pady=18)

    # -------------------------------------------------------------------------
    # IMAGEM DE FUNDO
    # -------------------------------------------------------------------------
    frame_fundo = tk.Frame(espera, bg="#F8FAFC")
    frame_fundo.pack(fill=BOTH, expand=YES)

    label_imagem_fundo = None
    imagem_original = None

    if os.path.exists(caminho_fundo):
        try:
            imagem_original = Image.open(caminho_fundo)
            label_imagem_fundo = tk.Label(frame_fundo)
            label_imagem_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            pass

    def redimensionar_fundo(event):
        nonlocal imagem_original, label_imagem_fundo
        if imagem_original and label_imagem_fundo:
            img_redimensionada = imagem_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
            foto_tk = ImageTk.PhotoImage(img_redimensionada)
            label_imagem_fundo.configure(image=foto_tk)
            label_imagem_fundo.image = foto_tk

    frame_fundo.bind('<Configure>', redimensionar_fundo)

    # -------------------------------------------------------------------------
    # CARD CENTRAL E FILTRO
    # -------------------------------------------------------------------------
    card_espera = tk.Frame(frame_fundo, bg="white", padx=20, pady=20)
    card_espera.place(relx=0.5, rely=0.53, relwidth=0.9, relheight=0.75, anchor=CENTER)

    frame_topo = tk.Frame(card_espera, bg="white")
    frame_topo.pack(fill=X, pady=(0, 15))

    tk.Label(frame_topo, text="Filtrar por Profissional:", font=("Helvetica", 12, "bold"), bg="white", fg="#555").pack(side=LEFT, padx=5)
    
    profissionais = ["Dra. Jamile", "Dra. Laurice", "Dr. Gerlando"]
    combo_filtro = ttk.Combobox(frame_topo, values=profissionais, state="readonly", font=("Helvetica", 12), width=30)
    combo_filtro.pack(side=LEFT, padx=10)
    combo_filtro.set(profissionais[0])

    # -------------------------------------------------------------------------
    # TABELAS COM CAIXINHAS DE SELEÇÃO (CHECKBOXES)
    # -------------------------------------------------------------------------
    frame_tabelas = tk.Frame(card_espera, bg="white")
    frame_tabelas.pack(fill=BOTH, expand=YES)
    frame_tabelas.columnconfigure(0, weight=1)
    frame_tabelas.columnconfigure(1, weight=1)

    # Nova coluna "Sel" adicionada para a caixinha
    colunas = ("Sel", "ID", "Nome", "Telefone", "Prioridade")

    # Tabela 1
    tk.Label(frame_tabelas, text="Fila de Espera (Rankeada por Prioridade)", font=("Helvetica", 12, "bold"), bg="white", fg="#E67E22").grid(row=0, column=0, pady=5)
    tabela_espera = ttk.Treeview(frame_tabelas, columns=colunas, show="headings", bootstyle=WARNING)
    for col in colunas: tabela_espera.heading(col, text=col)
    tabela_espera.column("Sel", width=40, anchor=CENTER) # Coluna apertadinha só para o quadradinho
    tabela_espera.column("ID", width=50, anchor=CENTER)
    tabela_espera.column("Prioridade", width=100, anchor=CENTER)
    tabela_espera.grid(row=1, column=0, padx=10, sticky="nsew")

    # Tabela 2
    tk.Label(frame_tabelas, text="Lista do Dia (Agendados)", font=("Helvetica", 12, "bold"), bg="white", fg="#27AE60").grid(row=0, column=1, pady=5)
    tabela_agenda = ttk.Treeview(frame_tabelas, columns=colunas, show="headings", bootstyle=SUCCESS)
    for col in colunas: tabela_agenda.heading(col, text=col)
    tabela_agenda.column("Sel", width=40, anchor=CENTER)
    tabela_agenda.column("ID", width=50, anchor=CENTER)
    tabela_agenda.column("Prioridade", width=100, anchor=CENTER)
    tabela_agenda.grid(row=1, column=1, padx=10, sticky="nsew")

    frame_tabelas.rowconfigure(1, weight=1)

    # -------------------------------------------------------------------------
    # LÓGICA DAS CAIXINHAS (CLIQUE PARA MARCAR/DESMARCAR)
    # -------------------------------------------------------------------------
    def alternar_caixinha(event, tabela):
        regiao = tabela.identify("region", event.x, event.y)
        if regiao == "cell":
            coluna = tabela.identify_column(event.x)
            # Se clicou na primeira coluna (#1)
            if coluna == '#1':
                item = tabela.focus()
                if item:
                    valores = list(tabela.item(item, 'values'))
                    # Alterna entre quadrado vazio e quadrado com 'X'
                    if valores[0] == '☐':
                        valores[0] = '☑'
                    else:
                        valores[0] = '☐'
                    tabela.item(item, values=valores)

    # Liga a função de clique nas duas tabelas
    tabela_espera.bind('<ButtonRelease-1>', lambda e: alternar_caixinha(e, tabela_espera))
    tabela_agenda.bind('<ButtonRelease-1>', lambda e: alternar_caixinha(e, tabela_agenda))

    # -------------------------------------------------------------------------
    # LÓGICA DE CARREGAMENTO DE DADOS
    # -------------------------------------------------------------------------
    def carregar_listas(*args):
        medico = combo_filtro.get()
        for item in tabela_espera.get_children(): tabela_espera.delete(item)
        for item in tabela_agenda.get_children(): tabela_agenda.delete(item)
            
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            
            query = """
                SELECT id, nome, telefone, prioridade FROM pacientes 
                WHERE profissional = ? AND status = ? 
                ORDER BY 
                    CASE prioridade 
                        WHEN 'Urgente' THEN 1 
                        WHEN 'Prioritário' THEN 2 
                        ELSE 3 
                    END, 
                    id ASC
            """
            
            cursor.execute(query, (medico, 'Aguardando'))
            # Insere a caixinha vazia '☐' no início de cada linha
            for linha in cursor.fetchall(): 
                tabela_espera.insert("", END, values=('☐', linha[0], linha[1], linha[2], linha[3]))
                
            cursor.execute(query, (medico, 'Agendado'))
            for linha in cursor.fetchall(): 
                tabela_agenda.insert("", END, values=('☐', linha[0], linha[1], linha[2], linha[3]))
            
            conexao.close()
        except Exception as e: 
            print(f"Erro ao carregar listas: {e}")

    combo_filtro.bind("<<ComboboxSelected>>", carregar_listas)

    # -------------------------------------------------------------------------
    # MOVIMENTAÇÃO LENDO AS CAIXINHAS MARCADAS (☑)
    # -------------------------------------------------------------------------
    def mover_pacientes_lote(ids_pacientes, novo_status):
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            placeholders = ','.join('?' * len(ids_pacientes))
            
            cursor.execute(f"UPDATE pacientes SET status = ? WHERE id IN ({placeholders})", [novo_status] + ids_pacientes)
            conexao.commit()
            conexao.close()
            carregar_listas()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar pacientes: {e}")

    def acao_mover_para_agenda():
        # Busca todas as linhas onde a primeira coluna é ☑
        itens_marcados = [item for item in tabela_espera.get_children() if tabela_espera.item(item)['values'][0] == '☑']
        if not itens_marcados:
            return messagebox.showwarning("Aviso", "Marque a caixinha (☑) de um ou mais pacientes na Fila de Espera.")
        
        # O ID agora está na posição 1 (valores[1]), porque a caixinha está na posição 0
        ids_pacientes = [tabela_espera.item(item)['values'][1] for item in itens_marcados]
        mover_pacientes_lote(ids_pacientes, 'Agendado')

    def acao_voltar_para_espera():
        itens_marcados = [item for item in tabela_agenda.get_children() if tabela_agenda.item(item)['values'][0] == '☑']
        if not itens_marcados:
            return messagebox.showwarning("Aviso", "Marque a caixinha (☑) de um ou mais pacientes na Lista do Dia.")
        
        ids_pacientes = [tabela_agenda.item(item)['values'][1] for item in itens_marcados]
        mover_pacientes_lote(ids_pacientes, 'Aguardando')

    def excluir_pacientes_lote():
        marcados_espera = [item for item in tabela_espera.get_children() if tabela_espera.item(item)['values'][0] == '☑']
        marcados_agenda = [item for item in tabela_agenda.get_children() if tabela_agenda.item(item)['values'][0] == '☑']
        
        if not marcados_espera and not marcados_agenda:
            return messagebox.showwarning("Aviso", "Marque as caixinhas dos pacientes que deseja excluir.")

        ids_para_excluir = []
        for item in marcados_espera: ids_para_excluir.append(tabela_espera.item(item)['values'][1])
        for item in marcados_agenda: ids_para_excluir.append(tabela_agenda.item(item)['values'][1])

        total_selecionados = len(ids_para_excluir)
        
        if messagebox.askyesno("Confirmar", f"Deseja deletar permanentemente os {total_selecionados} paciente(s) marcado(s)?"):
            try:
                conexao = sqlite3.connect(obter_caminho_banco())
                cursor = conexao.cursor()
                placeholders = ','.join('?' * len(ids_para_excluir))
                
                cursor.execute(f"DELETE FROM pacientes WHERE id IN ({placeholders})", ids_para_excluir)
                conexao.commit()
                conexao.close()
                carregar_listas()
                messagebox.showinfo("Sucesso", f"{total_selecionados} paciente(s) removido(s) com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

    # -------------------------------------------------------------------------
    # CONTROLES INFERIORES
    # -------------------------------------------------------------------------
    frame_inferior = tk.Frame(card_espera, bg="white")
    frame_inferior.pack(fill=X, pady=(20, 0))

    ttk.Button(frame_inferior, text="Mover para Agenda ➔", bootstyle=SUCCESS, command=acao_mover_para_agenda).pack(side=LEFT, padx=5)
    ttk.Button(frame_inferior, text="⬅ Voltar para Fila", bootstyle=WARNING, command=acao_voltar_para_espera).pack(side=LEFT, padx=5)
    
    ttk.Button(frame_inferior, text="🗑️ Excluir Selecionados", bootstyle=DANGER, command=excluir_pacientes_lote).pack(side=RIGHT, padx=5)

    carregar_listas()