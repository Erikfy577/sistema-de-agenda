import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import webbrowser  # Nativo do Python para abrir o navegador
from urllib.parse import quote  # Para formatar o texto para o padrão de links

def obter_caminho_banco():
    dir_views = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_views)
    return os.path.join(dir_raiz, "database", "banco.db")

def abrir_tela_espera(janela_principal):
    espera = tk.Toplevel()
    espera.title("Gerenciamento de Fila e Vagas")
    espera.state('zoomed')

    def voltar():
        espera.destroy()
        janela_principal.deiconify()
        janela_principal.state('zoomed')

    espera.protocol("WM_DELETE_WINDOW", voltar)

    # Botão Voltar
    tk.Button(espera, text="← Voltar ao Menu", command=voltar, bg="#607D8B", fg="white", font=("Arial", 10, "bold")).pack(anchor="nw", padx=20, pady=10)

    frame_topo = tk.Frame(espera)
    frame_topo.pack(pady=10)

    tk.Label(frame_topo, text="Filtrar por Profissional:", font=("Arial", 12)).pack(side="left", padx=5)
    profissionais = ["Dra. Laurice", "Thiago", "Jamile", "Gerlando"]
    combo_filtro = ttk.Combobox(frame_topo, values=profissionais, state="readonly", font=("Arial", 12))
    combo_filtro.pack(side="left", padx=5)
    combo_filtro.set(profissionais[0])

    frame_tabelas = tk.Frame(espera)
    frame_tabelas.pack(fill="both", expand=True, padx=10, pady=10)

    # Tabelas de Fila e Agenda
    tk.Label(frame_tabelas, text="Fila de Espera", fg="#FF9800", font=("Arial", 11, "bold")).grid(row=0, column=0)
    tabela_espera = ttk.Treeview(frame_tabelas, columns=("ID", "Nome", "Telefone"), show="headings", height=15)
    for col in ("ID", "Nome", "Telefone"): 
        tabela_espera.heading(col, text=col)
    tabela_espera.grid(row=1, column=0, padx=10, sticky="nsew")

    tk.Label(frame_tabelas, text="Lista do Dia (Agendados)", fg="#4CAF50", font=("Arial", 11, "bold")).grid(row=0, column=1)
    tabela_agenda = ttk.Treeview(frame_tabelas, columns=("ID", "Nome", "Telefone"), show="headings", height=15)
    for col in ("ID", "Nome", "Telefone"): 
        tabela_agenda.heading(col, text=col)
    tabela_agenda.grid(row=1, column=1, padx=10, sticky="nsew")

    def carregar_listas(*args):
        medico = combo_filtro.get()
        for item in tabela_espera.get_children(): tabela_espera.delete(item)
        for item in tabela_agenda.get_children(): tabela_agenda.delete(item)
            
        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            
            cursor.execute("SELECT id, nome, telefone FROM pacientes WHERE profissional = ? AND status = 'Aguardando' ORDER BY id ASC", (medico,))
            for linha in cursor.fetchall(): tabela_espera.insert("", "end", values=linha)
                
            cursor.execute("SELECT id, nome, telefone FROM pacientes WHERE profissional = ? AND status = 'Agendado' ORDER BY id ASC", (medico,))
            for linha in cursor.fetchall(): tabela_agenda.insert("", "end", values=linha)
            conexao.close()
        except Exception as e: 
            print(f"Erro ao carregar listas: {e}")

    combo_filtro.bind("<<ComboboxSelected>>", carregar_listas)

    def preencher_vagas():
        medico = combo_filtro.get()
        try:
            vagas = int(entrada_vagas.get())
        except ValueError:
            return messagebox.showwarning("Aviso", "Digite um número válido de vagas.")

        try:
            conexao = sqlite3.connect(obter_caminho_banco())
            cursor = conexao.cursor()
            cursor.execute("SELECT id FROM pacientes WHERE profissional = ? AND status = 'Aguardando' ORDER BY id ASC LIMIT ?", (medico, vagas))
            selecionados = cursor.fetchall()
            
            if not selecionados:
                conexao.close()
                return messagebox.showinfo("Aviso", f"Não há pacientes na fila de espera para {medico}.")
            
            ids = [str(p[0]) for p in selecionados]
            cursor.execute(f"UPDATE pacientes SET status = 'Agendado' WHERE id IN ({','.join('?'*len(ids))})", ids)
            conexao.commit()
            conexao.close()
            
            messagebox.showinfo("Sucesso", f"{len(ids)} pacientes movidos para a agenda do dia!")
            carregar_listas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar vagas: {e}")

    def excluir_paciente():
        sel_espera = tabela_espera.selection()
        sel_agenda = tabela_agenda.selection()

        if not sel_espera and not sel_agenda:
            messagebox.showwarning("Aviso", "Selecione um paciente em qualquer uma das tabelas para excluir.")
            return

        item_selecionado = sel_espera[0] if sel_espera else sel_agenda[0]
        tabela_alvo = tabela_espera if sel_espera else tabela_agenda
        
        valores = tabela_alvo.item(item_selecionado)['values']
        paciente_id = valores[0]
        nome_paciente = valores[1]

        if messagebox.askyesno("Confirmar", f"Deseja deletar permanentemente o paciente {nome_paciente}?"):
            try:
                conexao = sqlite3.connect(obter_caminho_banco())
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
                conexao.commit()
                conexao.close()
                messagebox.showinfo("Sucesso", "Paciente removido.")
                carregar_listas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

    # --- NOVA INTEGRAÇÃO: API WEB DO WHATSAPP ---
    def chamar_no_whatsapp():
        sel_espera = tabela_espera.selection()
        sel_agenda = tabela_agenda.selection()

        if not sel_espera and not sel_agenda:
            messagebox.showwarning("Aviso", "Selecione um paciente em uma das tabelas para notificar.")
            return

        # Pega os dados do paciente selecionado (seja da fila ou já agendado)
        item_selecionado = sel_espera[0] if sel_espera else sel_agenda[0]
        tabela_alvo = tabela_espera if sel_espera else tabela_agenda
        valores = tabela_alvo.item(item_selecionado)['values']
        
        nome_paciente = valores[1]
        telefone = str(valores[2]).replace(" ", "").replace("-", "").replace("(", "").replace(")", "") # Limpa o número
        medico = combo_filtro.get()

        # Garante o código do país (55 para Brasil) no início do número
        if not telefone.startswith("55"):
            telefone = f"55{telefone}"

        # Monta a mensagem estruturada (O asterisco * deixa o texto em negrito no WhatsApp)
        mensagem = f"Olá, *{nome_paciente}*! 🏥\n\nInformamos que sua consulta com o profissional *{medico}* foi agendada.\n\nPor favor, compareça à unidade portando o seu Cartão SUS e Documento com foto."
        mensagem_codificada = quote(mensagem) # Trata os espaços e quebras de linha para o formato URL

        # Endpoint da API oficial do WhatsApp (Click to Chat)
        url_whatsapp = f"https://wa.me/{telefone}?text={mensagem_codificada}"
        if len(telefone) < 12:
         return messagebox.showwarning("Aviso", "Número de telefone inválido.")
        
        # Executa a chamada abrindo o navegador/aplicativo
        webbrowser.open(url_whatsapp)


    # Controles de Vagas e Exclusão
    frame_inferior = tk.Frame(espera)
    frame_inferior.pack(pady=20)
    
    tk.Label(frame_inferior, text="Vagas:").pack(side="left", padx=5)
    entrada_vagas = tk.Entry(frame_inferior, width=5)
    entrada_vagas.pack(side="left", padx=5)
    entrada_vagas.insert(0, "5")
    
    tk.Button(frame_inferior, text="Gerar Lista do Dia", command=preencher_vagas, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    
    # --- NOVO BOTÃO DO WHATSAPP ---
    tk.Button(frame_inferior, text="💬 Chamar no WhatsApp (API)", command=chamar_no_whatsapp, bg="#25D366", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    
    tk.Button(frame_inferior, text="Excluir Selecionado", command=excluir_paciente, bg="#F44336", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)

    carregar_listas()