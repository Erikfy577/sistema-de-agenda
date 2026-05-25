import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
import os
import webbrowser  # Biblioteca nativa para abrir o navegador
from urllib.parse import quote  # Para formatar o texto padrão URL

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_agenda(janela_principal):
    agenda = tk.Toplevel()
    agenda.title("Agenda Mensal")
    agenda.state('zoomed')

    def voltar():
        agenda.destroy()
        janela_principal.deiconify()
        janela_principal.state('zoomed')

    agenda.protocol("WM_DELETE_WINDOW", voltar)

    # Botão Voltar
    tk.Button(agenda, text="← Voltar ao Menu", command=voltar, bg="#607D8B", fg="white", font=("Arial", 10, "bold")).pack(anchor="nw", padx=20, pady=10)

    # Frame principal dividido em 2 colunas
    frame_conteudo = tk.Frame(agenda)
    frame_conteudo.pack(fill="both", expand=True, padx=20, pady=10)

    # LADO ESQUERDO: Calendário
    frame_esquerdo = tk.Frame(frame_conteudo)
    frame_esquerdo.pack(side="left", fill="both", expand=True, padx=10)

    tk.Label(frame_esquerdo, text="Selecione o Dia da Consulta", font=("Arial", 14, "bold")).pack(pady=5)
    calendario = Calendar(frame_esquerdo, selectmode='day', date_pattern='dd/mm/yyyy', locale='pt_BR')
    calendario.pack(pady=10, fill="both", expand=True)

    # LADO DIREITO: Pacientes do Dia Selecionado
    frame_direito = tk.Frame(frame_conteudo)
    frame_direito.pack(side="right", fill="both", expand=True, padx=10)

    tk.Label(frame_direito, text="Pacientes Agendados no Dia", font=("Arial", 14, "bold"), fg="#4CAF50").pack(pady=5)
    
    tabela_dia = ttk.Treeview(frame_direito, columns=("ID", "Nome", "Telefone", "Médico"), show="headings", height=12)
    for col in ("ID", "Nome", "Telefone", "Médico"): 
        tabela_dia.heading(col, text=col)
    tabela_dia.column("ID", width=40)
    tabela_dia.pack(fill="both", expand=True, pady=5)

    # Função para buscar os agendados no banco local
    def atualizar_lista_do_dia(*args):
        data_sel = calendario.get_date()
        for item in tabela_dia.get_children(): 
            tabela_dia.delete(item)
            
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            
            # Como seu sistema atual move para 'Agendado' sem salvar uma data fixa,
            # vamos listar todos os 'Agendados' para teste. No futuro, você pode filtrar por data.
            cursor.execute("SELECT id, nome, telefone, profissional FROM pacientes WHERE status = 'Agendado' ORDER BY id ASC")
            
            for linha in cursor.fetchall(): 
                tabela_dia.insert("", "end", values=linha)
            conexao.close()
        except Exception as e: 
            print(e)

    # Atualiza a lista sempre que mudar a data selecionada no calendário
    calendario.bind("<<CalendarSelected>>", atualizar_lista_do_dia)

    # INTEGRAÇÃO COM A API DO GOOGLE AGENDA (Via Requisição Web)
    def enviar_para_google_agenda():
        selecionado = tabela_dia.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um paciente na tabela ao lado para enviar à agenda!")
            return
            
        item = tabela_dia.item(selecionado[0])
        valores = item['values']
        
        nome_paciente = valores[1]
        telefone = valores[2]
        medico = valores[3]
        data_consulta = calendario.get_date() # Pega a data do calendário (ex: 25/05/2026)
        
        # Converte a data do formato BR (dd/mm/aaaa) para o formato que a API do Google exige (aaaammdd)
        dia, mes, ano = data_consulta.split('/')
        data_formatada = f"{ano}{mes}{dia}"
        
        # Monta os textos da requisição
        titulo_evento = quote(f"Consulta UBS: {nome_paciente}")
        detalhes = quote(f"Paciente: {nome_paciente}\nTelefone: {telefone}\nProfissional: {medico}\nAgendado pelo Sistema Desktop UBS.")
        
        # URL da API Web do Google Agenda (Cria um evento direto na nuvem)
        url_api = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titulo_evento}&dates={data_formatada}T100000Z/{data_formatada}T103000Z&details={detalhes}&sf=true&output=xml"
        
        # Abre o navegador executando a chamada da API
        webbrowser.open(url_api)

    # Botão de Integração
    tk.Button(agenda, text="🗓️ Sincronizar Paciente com Google Agenda (API)", command=enviar_para_google_agenda, bg="#4285F4", fg="white", font=("Arial", 11, "bold")).pack(pady=15)

    # Carrega os dados assim que abrir a tela
    atualizar_lista_do_dia()