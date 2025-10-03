import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import threading
import logging
from datetime import datetime, timedelta
from processador_documentos import ProcessadorDocumentos

# Configurar sistema de logs centralizado
def setup_logging():
    """Configura sistema de logs com rotatividade de 20 dias"""
    # Criar diretório de logs
    os.makedirs("logs", exist_ok=True)
    
    # Limpar logs antigos (mais de 20 dias)
    cleanup_old_logs()
    
    # Configurar logging
    log_filename = f"logs/integra_evidencias_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8')
        ],
        force=True
    )
    
    return logging.getLogger('IntegraEvidencias')

def cleanup_old_logs():
    """Remove logs com mais de 20 dias"""
    try:
        cutoff_date = datetime.now() - timedelta(days=20)
        logs_dir = "logs"
        
        if os.path.exists(logs_dir):
            for filename in os.listdir(logs_dir):
                if filename.endswith('.log'):
                    file_path = os.path.join(logs_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    
                    if file_time < cutoff_date:
                        os.remove(file_path)
    except Exception:
        pass  # Ignora erros na limpeza

# Configurar logs no início
app_logger = setup_logging()

# Configurar tema moderno (será alterado dinamicamente)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GeradorEvidenciasTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Variáveis de controle
        self.tema_escuro = True
        self.arquivo_gerado = None
        
        # Diretórios base (carregados de config.py)
        from config import BASE_TEST_DIR, BASE_QA_DIR, BASE_TEMPLATES_DIR
        self.base_test = BASE_TEST_DIR
        self.base_qa = BASE_QA_DIR
        self.base_templates = BASE_TEMPLATES_DIR
        
        self.criar_interface()
    
    def get_root(self):
        return self.parent_frame.winfo_toplevel()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent_frame, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cabeçalho compacto
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=60)
        header_frame.pack(fill="x", pady=(5, 5))
        header_frame.pack_propagate(False)
        
        # Status e título em linha
        status_titulo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_titulo_frame.pack(fill="both", expand=True)
        
        # Frame do indicador de status (esquerda)
        status_frame = ctk.CTkFrame(status_titulo_frame, fg_color="transparent")
        status_frame.pack(side="left", padx=(5, 10))
        
        # Indicador de status
        self.status_indicator = ctk.CTkLabel(status_frame, text="●", font=ctk.CTkFont(size=20), 
                                           text_color="#FFA500", width=30)
        self.status_indicator.pack()
        
        # Texto explicativo
        status_text = ctk.CTkLabel(status_frame, text="Status Conexão\ndiretórios", 
                                  font=ctk.CTkFont(size=8), justify="center")
        status_text.pack()
        
        # Título e subtítulo (centro)
        titulo_frame = ctk.CTkFrame(status_titulo_frame, fg_color="transparent")
        titulo_frame.pack(side="left", expand=True, fill="both")
        
        titulo = ctk.CTkLabel(titulo_frame, text="🔧 Gerador de Evidências", 
                             font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=(5, 0))
        
        subtitulo = ctk.CTkLabel(titulo_frame, text="Sistema automatizado para documentos",
                                font=ctk.CTkFont(size=11))
        subtitulo.pack()
        
        # Frame de configurações
        config_frame = ctk.CTkFrame(main_frame, corner_radius=8)
        config_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        # Grid de configurações (2 colunas)
        grid_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=10)
        
        # Coluna 1
        col1_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        col1_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Ambiente
        ctk.CTkLabel(col1_frame, text="📋 Ambiente:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 2))
        
        ambiente_frame = ctk.CTkFrame(col1_frame, fg_color="transparent")
        ambiente_frame.pack(fill="x", pady=(0, 8))
        
        self.versao_var = ctk.StringVar()
        self.versao_combo = ctk.CTkComboBox(ambiente_frame, values=["TEST", "QA"], 
                                           variable=self.versao_var, command=self.on_versao_change,
                                           font=ctk.CTkFont(size=11), height=30)
        self.versao_combo.pack(side="left", fill="x", expand=True)
        
        self.btn_navegar_ambiente = ctk.CTkButton(ambiente_frame, text="📁", 
                                                 command=self.navegar_ambiente, width=30, height=30,
                                                 font=ctk.CTkFont(size=10))
        
        self.critica_ambiente = ctk.CTkLabel(col1_frame, text="", 
                                           font=ctk.CTkFont(size=9), text_color="#FF0000")
        self.critica_ambiente.pack(anchor="w")
        
        # Template
        ctk.CTkLabel(col1_frame, text="📄 Template:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(5, 2))
        
        template_frame = ctk.CTkFrame(col1_frame, fg_color="transparent")
        template_frame.pack(fill="x", pady=(0, 8))
        
        self.template_var = ctk.StringVar()
        self.template_combo = ctk.CTkComboBox(template_frame, variable=self.template_var,
                                             font=ctk.CTkFont(size=11), height=30)
        self.template_combo.pack(side="left", fill="x", expand=True)
        
        self.btn_navegar_template = ctk.CTkButton(template_frame, text="📁", 
                                                 command=self.navegar_template, width=30, height=30,
                                                 font=ctk.CTkFont(size=10))
        
        self.critica_template = ctk.CTkLabel(col1_frame, text="", 
                                           font=ctk.CTkFont(size=9), text_color="#FF0000")
        self.critica_template.pack(anchor="w")
        
        # Coluna 2
        col2_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        col2_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Pasta
        ctk.CTkLabel(col2_frame, text="📁 Pasta:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 2))
        
        self.pasta_var = ctk.StringVar()
        self.pasta_combo = ctk.CTkComboBox(col2_frame, variable=self.pasta_var,
                                          font=ctk.CTkFont(size=11), height=30)
        self.pasta_combo.pack(fill="x", pady=(0, 8))
        
        # Configurações em linha
        config_inline_frame = ctk.CTkFrame(col2_frame, fg_color="transparent")
        config_inline_frame.pack(fill="x", pady=(5, 0))
        
        # Largura
        largura_frame = ctk.CTkFrame(config_inline_frame, fg_color="transparent")
        largura_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(largura_frame, text="🖼️ Largura:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w")
        
        self.largura_var = ctk.StringVar(value="6.0")
        largura_entry = ctk.CTkEntry(largura_frame, textvariable=self.largura_var, 
                                    font=ctk.CTkFont(size=11), height=30, width=60)
        largura_entry.pack(fill="x")
        
        # Qualidade
        qualidade_frame = ctk.CTkFrame(config_inline_frame, fg_color="transparent")
        qualidade_frame.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(qualidade_frame, text="📊 Qualidade:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w")
        
        self.qualidade_var = ctk.StringVar(value="Alta")
        qualidade_combo = ctk.CTkComboBox(qualidade_frame, values=["Alta", "Média", "Baixa"],
                                         variable=self.qualidade_var, font=ctk.CTkFont(size=11), height=30)
        qualidade_combo.pack(fill="x")
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=5)
        
        # Centralizar botões
        btn_center_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        btn_center_frame.pack(expand=True)
        
        gerar_btn = ctk.CTkButton(btn_center_frame, text="🚀 Gerar Documento", 
                                 command=self.gerar_documento, height=35, width=150,
                                 font=ctk.CTkFont(size=12, weight="bold"))
        gerar_btn.pack(side="left", padx=3)
        
        templates_btn = ctk.CTkButton(btn_center_frame, text="📁 Templates", 
                                     command=self.gerenciar_templates, height=35, width=120,
                                     font=ctk.CTkFont(size=12, weight="bold"), fg_color="orange", hover_color="darkorange")
        templates_btn.pack(side="left", padx=3)
        
        # Área de progresso compacta
        self.progress_frame = ctk.CTkFrame(main_frame, corner_radius=8, height=70)
        self.progress_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.progress_frame.pack_propagate(False)
        
        ctk.CTkLabel(self.progress_frame, text="🚀 Progresso", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(8, 2))
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Aguardando...", 
                                          font=ctk.CTkFont(size=10))
        self.progress_label.pack(pady=(0, 3))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=250, height=12, 
                                              progress_color="#008000")
        self.progress_bar.pack(pady=(0, 8))
        self.progress_bar.set(0)
        
        # Animação de entrada
        self.animate_entrance()
        
        # Inicializar dados
        self.get_root().after(100, self.inicializar_dados)
        
        # Verificar status dos diretórios
        self.get_root().after(200, self.verificar_status_diretorios)
    
    def on_versao_change(self, choice):
        if choice == "TEST":
            self.carregar_pastas(self.base_test)
            self.log(f"🔄 Ambiente selecionado: {choice} - Carregando pastas...")
        elif choice == "QA":
            self.carregar_pastas(self.base_qa)
            self.log(f"🔄 Ambiente selecionado: {choice} - Carregando pastas...")
    
    def carregar_pastas(self, base_dir):
        try:
            if os.path.exists(base_dir):
                pastas = [d for d in os.listdir(base_dir) 
                         if os.path.isdir(os.path.join(base_dir, d))]
                self.pasta_combo.configure(values=pastas)
                self.pasta_var.set('')
                self.log(f"✅ Carregadas {len(pastas)} pastas disponíveis")
            else:
                self.pasta_combo.configure(values=[])
                self.log(f"❌ Diretório não encontrado: {base_dir}")
        except Exception as e:
            self.log(f"❌ Erro ao carregar pastas: {str(e)}")
    
    def animate_entrance(self):
        """Animação de entrada da interface"""
        self.get_root().attributes('-alpha', 0.8)
        self.get_root().after(100, lambda: self.get_root().attributes('-alpha', 1.0))
    
    def verificar_status_diretorios(self):
        """Verifica se todos os diretórios estão acessíveis com animação"""
        def check():
            import time
            # Animação de carregamento
            for i in range(3):
                dots = "." * (i + 1)
                self.get_root().after(0, lambda d=dots: None)  # Placeholder para status
                time.sleep(0.3)
            
            # Verificar cada diretório individualmente
            test_ok = os.path.exists(self.base_test) and os.path.isdir(self.base_test)
            qa_ok = os.path.exists(self.base_qa) and os.path.isdir(self.base_qa)
            templates_ok = os.path.exists(self.base_templates) and os.path.isdir(self.base_templates)
            
            status_list = [test_ok, qa_ok, templates_ok]
            
            # Atualizar indicador geral
            self.get_root().after(0, lambda: self.update_status_indicator(status_list, test_ok, qa_ok, templates_ok))
        
        import threading
        threading.Thread(target=check, daemon=True).start()
    
    def update_status_indicator(self, status_list, test_ok, qa_ok, templates_ok):
        """Atualiza indicador de status"""
        if all(status_list):
            self.status_indicator.configure(text_color="#008000")
        elif any(status_list):
            self.status_indicator.configure(text_color="#FFA500")
        else:
            self.status_indicator.configure(text_color="#FF0000")
        
        # Controlar estado dos campos
        self.controlar_campos_por_status(test_ok, qa_ok, templates_ok)
        
        # Animação de ativação se tudo OK
        if all(status_list):
            self.animate_activation()
    
    def animate_activation(self):
        """Animação quando interface é ativada"""
        # Efeito de destaque nos campos ativados
        for widget in [self.versao_combo, self.pasta_combo, self.template_combo]:
            try:
                self.get_root().after(100, lambda: None)  # Placeholder para animação
            except:
                pass
    
    def controlar_campos_por_status(self, test_ok, qa_ok, templates_ok):
        """Controla estado dos campos baseado no status dos diretórios"""
        # Controlar campo ambiente
        if not test_ok and not qa_ok:
            self.versao_combo.configure(state="disabled")
            self.critica_ambiente.configure(text="Sem conexão com diretório")
            self.btn_navegar_ambiente.pack(side="right", padx=(10, 0))
        else:
            self.versao_combo.configure(state="normal")
            self.critica_ambiente.configure(text="")
            self.btn_navegar_ambiente.pack_forget()
            # Atualizar valores disponíveis
            valores_disponiveis = []
            if test_ok:
                valores_disponiveis.append("TEST")
            if qa_ok:
                valores_disponiveis.append("QA")
            self.versao_combo.configure(values=valores_disponiveis)
        
        # Controlar campo template
        if not templates_ok:
            self.template_combo.configure(state="disabled")
            self.critica_template.configure(text="Sem conexão com diretório")
            self.btn_navegar_template.pack(side="right", padx=(10, 0))
        else:
            self.template_combo.configure(state="normal")
            self.critica_template.configure(text="")
            self.btn_navegar_template.pack_forget()
    
    def navegar_ambiente(self):
        """Permite navegar manualmente para selecionar diretório de ambiente"""
        diretorio = filedialog.askdirectory(title="Selecionar Diretório de Ambiente (TEST ou QA)")
        if diretorio:
            # Determinar se é TEST ou QA baseado no caminho
            if "Test" in diretorio or "TEST" in diretorio:
                self.base_test = diretorio
                self.versao_combo.configure(values=["TEST"], state="normal")
                self.versao_var.set("TEST")
                self.carregar_pastas(self.base_test)
            elif "Qa" in diretorio or "QA" in diretorio:
                self.base_qa = diretorio
                self.versao_combo.configure(values=["QA"], state="normal")
                self.versao_var.set("QA")
                self.carregar_pastas(self.base_qa)
            else:
                # Permitir usar qualquer diretório como TEST
                self.base_test = diretorio
                self.versao_combo.configure(values=["TEST"], state="normal")
                self.versao_var.set("TEST")
                self.carregar_pastas(self.base_test)
            
            self.critica_ambiente.configure(text="")
            self.btn_navegar_ambiente.pack_forget()
            self.verificar_status_diretorios()
    
    def navegar_template(self):
        """Permite navegar manualmente para selecionar diretório de templates"""
        diretorio = filedialog.askdirectory(title="Selecionar Diretório de Templates")
        if diretorio:
            self.base_templates = diretorio
            self.template_combo.configure(state="normal")
            self.carregar_templates()
            self.critica_template.configure(text="")
            self.btn_navegar_template.pack_forget()
            self.verificar_status_diretorios()
    
    def inicializar_dados(self):
        self.carregar_templates()
        self.log("🚀 Sistema inicializado! Interface moderna carregada.")
    
    def carregar_templates(self):
        try:
            if os.path.exists(self.base_templates):
                templates = [f for f in os.listdir(self.base_templates) 
                           if f.endswith('.docx')]
                self.template_combo.configure(values=templates)
                if templates:
                    self.template_var.set(templates[0])
                self.log(f"✅ Carregados {len(templates)} templates disponíveis")
            else:
                self.template_combo.configure(values=[])
                self.log(f"❌ Diretório de templates não encontrado")
        except Exception as e:
            self.log(f"❌ Erro ao carregar templates: {str(e)}")
    
    def mostrar_progresso(self, texto="Processando..."):
        self.progress_label.configure(text=texto)
        self.progress_bar.set(0)
        self.get_root().update()
    
    def ocultar_progresso(self):
        self.progress_label.configure(text="Aguardando...")
        self.progress_bar.set(0)
        self.get_root().update()
    
    def atualizar_progresso(self, valor, texto, status=""):
        self.progress_bar.set(valor)
        if status:
            self.progress_label.configure(text=f"{texto} - {status}")
        else:
            self.progress_label.configure(text=texto)
        self.get_root().update()
    
    def gerenciar_templates(self):
        # Janela de gerenciamento de templates
        template_window = ctk.CTkToplevel(self.get_root())
        template_window.title("📁 Gerenciar Templates")
        template_window.geometry("600x400")
        template_window.transient(self.get_root())
        
        # Lista de templates
        ctk.CTkLabel(template_window, text="Templates Disponíveis", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))
        
        # Frame para lista
        list_frame = ctk.CTkFrame(template_window)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Usar Listbox ao invés de Textbox para seleção
        import tkinter as tk
        self.template_listbox = tk.Listbox(list_frame, height=12, font=("Segoe UI", 10),
                                          selectmode=tk.SINGLE, bg="#212121", fg="white",
                                          selectbackground="#1f538d", relief="flat")
        self.template_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar para o listbox
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.template_listbox.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 10))
        self.template_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(template_window, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="➕ Adicionar", command=self.adicionar_template, width=120).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Remover", command=self.remover_template, width=120, fg_color="red").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔄 Atualizar", command=self.atualizar_lista_templates, width=120).pack(side="left", padx=5)
        
        self.atualizar_lista_templates()
    
    def adicionar_template(self):
        arquivo = filedialog.askopenfilename(
            title="Selecionar Template",
            filetypes=[("Documentos Word", "*.docx")]
        )
        if arquivo:
            import shutil
            nome_arquivo = os.path.basename(arquivo)
            destino = os.path.join(self.base_templates, nome_arquivo)
            try:
                shutil.copy2(arquivo, destino)
                self.log(f"✅ Template adicionado: {nome_arquivo}")
                self.atualizar_lista_templates()
                self.carregar_templates()
            except Exception as e:
                self.log(f"❌ Erro ao adicionar template: {str(e)}")
    
    def remover_template(self):
        # Obter template selecionado
        selection = self.template_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um template para remover.")
            return
        
        # Obter nome do template selecionado
        selected_index = selection[0]
        selected_text = self.template_listbox.get(selected_index)
        # Extrair nome do arquivo (remover numeração)
        template_name = selected_text.split(". ", 1)[1] if ". " in selected_text else selected_text
        
        resposta = messagebox.askyesno("Confirmar", f"Remover template '{template_name}'?")
        if resposta:
            try:
                os.remove(os.path.join(self.base_templates, template_name))
                self.log(f"🗑️ Template removido: {template_name}")
                self.atualizar_lista_templates()
                self.carregar_templates()
            except Exception as e:
                self.log(f"❌ Erro ao remover template: {str(e)}")
                messagebox.showerror("Erro", f"Erro ao remover template: {str(e)}")
    
    def atualizar_lista_templates(self):
        if hasattr(self, 'template_listbox'):
            self.template_listbox.delete(0, "end")
            try:
                templates = [f for f in os.listdir(self.base_templates) if f.endswith('.docx')]
                for i, template in enumerate(templates, 1):
                    self.template_listbox.insert("end", f"{i}. {template}")
            except Exception as e:
                self.template_listbox.insert("end", f"Erro ao listar templates: {str(e)}")
    
    def gerar_documento(self):
        if not self.versao_var.get():
            messagebox.showerror("Erro", "Selecione um ambiente (TEST ou QA)")
            return
        
        if not self.pasta_var.get():
            messagebox.showerror("Erro", "Selecione uma pasta")
            return
        
        if not self.template_var.get():
            messagebox.showerror("Erro", "Selecione um template")
            return
        
        # Construir caminhos completos
        base_dir = self.base_test if self.versao_var.get() == "TEST" else self.base_qa
        diretorio_selecionado = os.path.join(base_dir, self.pasta_var.get())
        template_selecionado = os.path.join(self.base_templates, self.template_var.get())
        
        try:
            largura = float(self.largura_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Largura deve ser um número válido")
            return
        
        # Gerar nome padrão do arquivo
        from datetime import datetime
        data_atual = datetime.now().strftime("%d%m%Y")
        nome_padrao = f"RELEASE NOTE - PROJETO AILOS - VERSÃO V00XC001RXXX - {data_atual}.docx"
        
        # Selecionar local para salvar com nome padrão
        arquivo_saida = filedialog.asksaveasfilename(
            title="Salvar documento como",
            initialfile=nome_padrao,
            defaultextension=".docx",
            filetypes=[("Documentos Word", "*.docx")]
        )
        
        if not arquivo_saida:
            return
        
        self.arquivo_gerado = arquivo_saida
        
        # Executar geração em thread separada
        thread = threading.Thread(target=self.processar_documento, 
                                 args=(template_selecionado, diretorio_selecionado, arquivo_saida, largura))
        thread.daemon = True
        thread.start()
    
    def processar_documento(self, template_selecionado, diretorio_selecionado, arquivo_saida, largura):
        try:
            self.mostrar_progresso("Iniciando processamento...")
            self.log("🔄 Iniciando geração do documento...")
            
            # Contar imagens para progresso
            total_imagens = 0
            for root, dirs, files in os.walk(diretorio_selecionado):
                total_imagens += len([f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            
            self.atualizar_progresso(0.1, "Analisando diretório", f"Encontradas {total_imagens} imagens")
            
            processador = ProcessadorDocumentos(template_selecionado, largura)
            
            # Configurar qualidade baseada na seleção
            qualidade = self.qualidade_var.get()
            if "Média" in qualidade:
                processador.qualidade_imagem = 0.7
            elif "Baixa" in qualidade:
                processador.qualidade_imagem = 0.5
            else:
                processador.qualidade_imagem = 1.0
            
            self.atualizar_progresso(0.2, "Carregando template", "Preparando documento")
            
            sucesso = processador.processar_diretorio(diretorio_selecionado, arquivo_saida)
            
            self.atualizar_progresso(1.0, "Documento gerado com sucesso!", "Processo concluído")
            
            if sucesso:
                self.log("✅ Documento gerado com sucesso!")
                self.get_root().after(100, self.mostrar_opcoes_pos_geracao)
            else:
                self.log("❌ Erro na geração do documento")
                self.get_root().after(100, lambda: messagebox.showerror("Erro", "Falha na geração do documento"))
                
        except Exception as e:
            self.log(f"❌ Erro: {str(e)}")
            self.get_root().after(100, lambda: messagebox.showerror("Erro", f"Erro na geração: {str(e)}"))
        finally:
            self.get_root().after(3000, self.ocultar_progresso)
    
    def mostrar_opcoes_pos_geracao(self):
        resposta = messagebox.askyesnocancel(
            "Documento Gerado", 
            f"Documento gerado com sucesso!\n\n{self.arquivo_gerado}\n\nDeseja:",
            **{"detail": "Sim = Abrir no Word | Não = Abrir pasta | Cancelar = Fechar"}
        )
        
        if resposta is True:  # Sim - Abrir no Word
            try:
                os.startfile(self.arquivo_gerado)
                self.log("📄 Documento aberto no Word")
            except Exception as e:
                self.log(f"❌ Erro ao abrir documento: {str(e)}")
        elif resposta is False:  # Não - Abrir pasta
            try:
                pasta = os.path.dirname(self.arquivo_gerado)
                os.startfile(pasta)
                self.log("📁 Pasta de destino aberta")
            except Exception as e:
                self.log(f"❌ Erro ao abrir pasta: {str(e)}")
    
    def log(self, mensagem):
        app_logger.info(f"[Gerador] {mensagem}")
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

class SistemaAbas:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🔧 IntegraEvidências")
        self.root.geometry("1100x900")
        
        # Variáveis de controle
        self.tema_escuro = True
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cabeçalho com título e controle de tema
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 0))
        
        # Frame do título e autor
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", expand=True)
        
        # Título principal
        titulo = ctk.CTkLabel(title_frame, text="🔧 IntegraEvidências", 
                             font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack()
        
        # Informações do autor
        autor = ctk.CTkLabel(title_frame, text="Desenvolvido por Alessandro Luiz Mariano da Silva Melo", 
                            font=ctk.CTkFont(size=9), text_color="gray")
        autor.pack()
        
        email = ctk.CTkLabel(title_frame, text="1986.alessandro@gmail.com", 
                            font=ctk.CTkFont(size=9), text_color="gray")
        email.pack()
        
        # Switch de tema
        tema_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        tema_frame.pack(side="right", padx=(0, 10))
        
        ctk.CTkLabel(tema_frame, text="🌙", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 5))
        self.tema_switch = ctk.CTkSwitch(tema_frame, text="", command=self.alternar_tema, width=40)
        self.tema_switch.select()  # Inicia em dark
        self.tema_switch.pack(side="left")
        ctk.CTkLabel(tema_frame, text="☀️", font=ctk.CTkFont(size=14)).pack(side="left", padx=(5, 0))
        
        # Sistema de abas
        self.tabview = ctk.CTkTabview(main_frame, width=1050, height=820)
        self.tabview.pack(fill="both", expand=True, padx=5, pady=(5, 5))
        
        # Aba 1: Gerador de Evidências
        self.tab_evidencias = self.tabview.add("📋 Gerador de Evidências")
        self.gerador_evidencias = GeradorEvidenciasTab(self.tab_evidencias)
        
        # Aba 2: Upload Nexus
        self.tab_upload = self.tabview.add("📤 Upload Nexus")
        self.upload_nexus = UploadNexusTab(self.tab_upload)
        
        # Aba 3: Confluence
        self.tab_confluence = self.tabview.add("📝 Confluence")
        self.confluence_system = ConfluenceTab(self.tab_confluence)
    
    def alternar_tema(self):
        self.tema_escuro = not self.tema_escuro
        modo = "dark" if self.tema_escuro else "light"
        ctk.set_appearance_mode(modo)
    
    def executar(self):
        self.root.mainloop()

class UploadNexusTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Importar módulos do sistema de upload
        import sys
        sys.path.append(r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\Sistemas\SISTEMA-UPLOAD-EVIDENCIAS-NEXUS")
        
        try:
            from nexus_client import NexusClient
            from file_manager import FileManager
            from logger import app_logger
            
            # Suprimir logs durante inicialização
            import logging
            logging.getLogger().setLevel(logging.ERROR)
            
            self.nexus_client = NexusClient()
            self.file_manager = FileManager()
            self.app_logger = app_logger
            
            # Restaurar nível de log
            logging.getLogger().setLevel(logging.INFO)
            
            # Controle de navegação
            self.current_environment = None
            self.current_folder = None
            self.in_folder_view = False
            
            self.criar_interface()
            self.check_connection()
            
        except ImportError as e:
            self.criar_interface_erro(str(e))
    
    def get_root(self):
        return self.parent_frame.winfo_toplevel()
    
    def criar_interface_erro(self, erro):
        """Interface de erro quando módulos não estão disponíveis"""
        main_frame = ctk.CTkFrame(self.parent_frame, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="❌ Erro ao carregar sistema", 
                    font=ctk.CTkFont(size=18, weight="bold"), text_color="red").pack(pady=50)
        
        ctk.CTkLabel(main_frame, text=f"Erro: {erro}", 
                    font=ctk.CTkFont(size=12)).pack(pady=10)
        
        ctk.CTkLabel(main_frame, text="Verifique se o diretório do sistema existe:", 
                    font=ctk.CTkFont(size=11)).pack(pady=5)
        
        ctk.CTkLabel(main_frame, text="C:\\Users\\alessandro.melo\\OneDrive - Stefanini\\Ailos\\Sistemas\\SISTEMA-UPLOAD-EVIDENCIAS-NEXUS", 
                    font=ctk.CTkFont(size=10), text_color="gray").pack(pady=5)
    
    def criar_interface(self):
        """Cria interface compacta do sistema de upload"""
        main_frame = ctk.CTkFrame(self.parent_frame, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cabeçalho compacto
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=60)
        header_frame.pack(fill="x", pady=(5, 5))
        header_frame.pack_propagate(False)
        
        # Título e subtítulo centralizados
        titulo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        titulo_frame.pack(expand=True, fill="both")
        
        titulo = ctk.CTkLabel(titulo_frame, text="📤 Upload Evidências Nexus", 
                             font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=(5, 0))
        
        self.status_label = ctk.CTkLabel(titulo_frame, text="Verificando conexão...", 
                                        font=ctk.CTkFont(size=11), text_color="orange")
        self.status_label.pack()
        
        # Frame de configurações
        config_frame = ctk.CTkFrame(main_frame, corner_radius=8)
        config_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        # Grid de configurações (2 colunas)
        grid_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=10)
        
        # Coluna 1
        col1_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        col1_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Ambiente
        ctk.CTkLabel(col1_frame, text="📋 Ambiente:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 2))
        
        self.ambiente_var = ctk.StringVar()
        self.ambiente_combo = ctk.CTkComboBox(col1_frame, values=["TEST", "QA"], 
                                             variable=self.ambiente_var, command=self.on_ambiente_change,
                                             font=ctk.CTkFont(size=11), height=30, state="disabled")
        self.ambiente_combo.pack(fill="x", pady=(0, 8))
        
        # Versão
        ctk.CTkLabel(col1_frame, text="🔢 Versão:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(5, 2))
        
        self.versao_var = ctk.StringVar()
        self.versao_entry = ctk.CTkEntry(col1_frame, textvariable=self.versao_var, 
                                        font=ctk.CTkFont(size=11), height=30, state="disabled",
                                        placeholder_text="Ex: V000C001R000")
        self.versao_entry.pack(fill="x", pady=(0, 8))
        
        # Coluna 2
        col2_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        col2_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Arquivo PDF
        ctk.CTkLabel(col2_frame, text="📄 Arquivo PDF:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 2))
        
        self.arquivo_var = ctk.StringVar()
        self.arquivo_combo = ctk.CTkComboBox(col2_frame, variable=self.arquivo_var,
                                            font=ctk.CTkFont(size=11), height=30, state="disabled")
        self.arquivo_combo.pack(fill="x", pady=(0, 8))
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=5)
        
        # Centralizar botões
        btn_center_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        btn_center_frame.pack(expand=True)
        
        self.enviar_button = ctk.CTkButton(btn_center_frame, text="📤 Enviar Arquivo", 
                                          command=self.enviar_arquivo, height=35, width=150,
                                          font=ctk.CTkFont(size=12, weight="bold"), state="disabled")
        self.enviar_button.pack(side="left", padx=3)
        
        self.back_button = ctk.CTkButton(btn_center_frame, text="← Voltar", 
                                        command=self.go_back, height=35, width=80,
                                        font=ctk.CTkFont(size=12), state="disabled")
        self.back_button.pack(side="left", padx=3)
        
        refresh_button = ctk.CTkButton(btn_center_frame, text="🔄 Atualizar", 
                                      command=self.refresh_directory, height=35, width=100,
                                      font=ctk.CTkFont(size=12), fg_color="orange", hover_color="darkorange")
        refresh_button.pack(side="left", padx=3)
        
        # Área de progresso compacta
        self.progress_frame = ctk.CTkFrame(main_frame, corner_radius=8, height=50)
        self.progress_frame.pack(fill="x", padx=10, pady=(5, 5))
        self.progress_frame.pack_propagate(False)
        
        ctk.CTkLabel(self.progress_frame, text="📊 Status", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(8, 2))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=250, height=12, 
                                              progress_color="#008000")
        self.progress_bar.pack(pady=(0, 8))
        
        # Lista do Nexus
        nexus_frame = ctk.CTkFrame(main_frame, corner_radius=8)
        nexus_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        self.nexus_label = ctk.CTkLabel(nexus_frame, text="Selecione um ambiente", 
                                       font=ctk.CTkFont(size=12, weight="bold"))
        self.nexus_label.pack(pady=(10, 5))
        
        # Lista com scrollbar
        list_frame = ctk.CTkFrame(nexus_frame, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.nexus_textbox = ctk.CTkTextbox(list_frame, height=200, font=ctk.CTkFont(size=10))
        self.nexus_textbox.pack(fill="both", expand=True)
        self.nexus_textbox.bind("<Double-Button-1>", self.on_double_click)
        
        # Bind para validação
        self.versao_var.trace("w", lambda *args: self.validate_form())
        
        # Animação de entrada
        self.animate_entrance()
    
    def animate_entrance(self):
        """Animação de entrada da interface"""
        # Fade in effect simulado
        self.get_root().attributes('-alpha', 0.8)
        self.get_root().after(100, lambda: self.get_root().attributes('-alpha', 1.0))
    
    def check_connection(self):
        """Verifica conexão com o Nexus em thread separada"""
        def check():
            import time
            # Animação de carregamento
            for i in range(3):
                dots = "." * (i + 1)
                self.get_root().after(0, lambda d=dots: self.status_label.configure(text=f"Verificando conexão{d}"))
                time.sleep(0.5)
            
            try:
                if self.nexus_client.test_connection():
                    self.get_root().after(0, lambda: [
                        self.status_label.configure(text="✓ Conectado ao Nexus Repository Manager", text_color="green"),
                        self.enable_interface()
                    ])
                else:
                    self.get_root().after(0, lambda: [
                        self.status_label.configure(text="✗ Erro de conexão com o Nexus", text_color="red")
                    ])
            except Exception as e:
                self.get_root().after(0, lambda: [
                    self.status_label.configure(text="✗ Erro de conexão com o Nexus", text_color="red")
                ])
        
        import threading
        threading.Thread(target=check, daemon=True).start()
    
    def enable_interface(self):
        """Habilita a interface após conexão bem-sucedida"""
        self.ambiente_combo.configure(state="readonly")
        self.versao_entry.configure(state="normal")
        self.arquivo_combo.configure(state="readonly")
        # Animação de ativação
        self.animate_activation()
    
    def animate_activation(self):
        """Animação quando interface é ativada"""
        # Efeito de destaque nos campos ativados
        original_colors = {}
        for widget in [self.ambiente_combo, self.versao_entry, self.arquivo_combo]:
            try:
                # Simular destaque mudando cor temporariamente
                self.get_root().after(100, lambda: None)  # Placeholder para animação
            except:
                pass
    
    def on_ambiente_change(self, choice=None):
        """Atualiza combo de arquivos e lista do Nexus quando ambiente muda"""
        ambiente = self.ambiente_var.get()
        if not ambiente:
            return
        
        # Preencher versão automaticamente
        if ambiente == "TEST":
            self.versao_var.set("V004C001RXXX")
        elif ambiente == "QA":
            self.versao_var.set("V002C001RXXX")
        
        # Carregar arquivos
        try:
            files = self.file_manager.list_pdf_files(ambiente)
            filenames = [os.path.basename(f) for f in files]
            
            if filenames:
                self.arquivo_combo.configure(values=filenames)
            else:
                self.arquivo_combo.configure(values=[])
        except:
            self.arquivo_combo.configure(values=[])
        
        # Atualizar lista do Nexus
        self.current_environment = ambiente
        self.load_environment_folders(ambiente)
        self.validate_form()
    
    def validate_form(self):
        """Valida formulário"""
        ambiente = self.ambiente_var.get()
        versao = self.versao_var.get().strip()
        arquivo = self.arquivo_var.get()
        
        if ambiente and versao and arquivo:
            self.enviar_button.configure(state="normal")
        else:
            self.enviar_button.configure(state="disabled")
    
    def enviar_arquivo(self):
        """Envia arquivo para o Nexus"""
        ambiente = self.ambiente_var.get()
        versao = self.versao_var.get().strip()
        arquivo_nome = self.arquivo_var.get()
        
        if not all([ambiente, versao, arquivo_nome]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return
        
        # Obter caminho completo do arquivo
        try:
            files = self.file_manager.list_pdf_files(ambiente)
            arquivo_path = None
            for file_path in files:
                if os.path.basename(file_path) == arquivo_nome:
                    arquivo_path = file_path
                    break
            
            if not arquivo_path:
                messagebox.showerror("Erro", "Arquivo não encontrado.")
                return
        except:
            messagebox.showerror("Erro", "Erro ao localizar arquivo.")
            return
        
        def upload():
            self.get_root().after(0, lambda: self.progress_bar.start())
            self.get_root().after(0, lambda: self.enviar_button.configure(state="disabled", text="Enviando..."))
            
            try:
                # Validar estrutura
                dir_result = self.nexus_client.create_directory_structure(ambiente, versao)
                
                if dir_result["success"]:
                    result = self.nexus_client.upload_file(arquivo_path, ambiente, versao)
                else:
                    result = dir_result
                
                self.get_root().after(0, lambda: self.progress_bar.stop())
                self.get_root().after(0, lambda: self.enviar_button.configure(state="normal", text="📤 Enviar Arquivo"))
                
                if result["success"]:
                    self.get_root().after(0, lambda: messagebox.showinfo("Sucesso", result["message"]))
                    self.get_root().after(0, lambda: self.versao_var.set(""))
                    self.get_root().after(0, lambda: self.arquivo_var.set(""))
                    self.get_root().after(0, self.validate_form)
                    self.get_root().after(0, self.refresh_directory)
                else:
                    self.get_root().after(0, lambda: messagebox.showerror("Erro", result["error"]))
            except Exception as e:
                self.get_root().after(0, lambda: self.progress_bar.stop())
                self.get_root().after(0, lambda: self.enviar_button.configure(state="normal", text="📤 Enviar Arquivo"))
                self.get_root().after(0, lambda: messagebox.showerror("Erro", f"Erro no upload: {str(e)}"))
        
        import threading
        threading.Thread(target=upload, daemon=True).start()
    
    def load_environment_folders(self, ambiente):
        """Carrega pastas do ambiente"""
        def load_folders():
            try:
                result = self.nexus_client.list_folders_by_environment(ambiente)
                self.get_root().after(0, lambda: self.update_nexus_list(result, f"Pastas do ambiente {ambiente}"))
            except Exception as e:
                self.get_root().after(0, lambda: self.update_nexus_list({"success": False, "error": str(e)}, f"Erro ao carregar {ambiente}"))
        
        self.current_folder = None
        self.in_folder_view = False
        self.back_button.configure(state="disabled")
        
        import threading
        threading.Thread(target=load_folders, daemon=True).start()
    
    def update_nexus_list(self, result, label_text):
        """Atualiza lista do Nexus"""
        self.nexus_label.configure(text=label_text)
        self.nexus_textbox.delete("1.0", "end")
        
        if result["success"]:
            items = result.get("folders", []) or result.get("files", [])
            if items:
                for item in items:
                    self.nexus_textbox.insert("end", f"{item}\n")
            else:
                self.nexus_textbox.insert("end", "Nenhum item encontrado")
        else:
            self.nexus_textbox.insert("end", "Erro ao carregar itens")
    
    def refresh_directory(self):
        """Atualiza diretório"""
        if not self.current_environment:
            return
        
        if self.in_folder_view and self.current_folder:
            self.load_folder_contents(self.current_environment, self.current_folder)
        else:
            self.load_environment_folders(self.current_environment)
    
    def load_folder_contents(self, ambiente, folder):
        """Carrega conteúdo de uma pasta"""
        def load_files():
            try:
                result = self.nexus_client.list_files_in_folder(ambiente, folder)
                self.get_root().after(0, lambda: self.update_folder_contents(result, folder))
            except Exception as e:
                self.get_root().after(0, lambda: self.update_nexus_list({"success": False, "error": str(e)}, f"Erro na pasta {folder}"))
        
        self.in_folder_view = True
        import threading
        threading.Thread(target=load_files, daemon=True).start()
    
    def update_folder_contents(self, result, folder_name):
        """Atualiza com arquivos da pasta"""
        label_text = f"Arquivos na pasta {folder_name}"
        self.update_nexus_list(result, label_text)
    
    def on_double_click(self, event=None):
        """Navega para dentro de uma pasta"""
        if not self.current_environment:
            return
        
        try:
            # Obter linha atual do cursor
            current_pos = self.nexus_textbox.index("insert")
            line_start = current_pos.split('.')[0] + '.0'
            line_end = current_pos.split('.')[0] + '.end'
            selected_line = self.nexus_textbox.get(line_start, line_end).strip()
            
            if selected_line and selected_line.startswith("📁 "):
                folder_name = selected_line[2:]  # Remove o ícone
                self.current_folder = folder_name
                self.load_folder_contents(self.current_environment, folder_name)
                self.back_button.configure(state="normal")
        except Exception as e:
            pass  # Ignora erros de navegação
    
    def go_back(self):
        """Volta para lista de pastas"""
        if self.current_environment and self.in_folder_view:
            self.current_folder = None
            self.in_folder_view = False
            self.back_button.configure(state="disabled")
            self.load_environment_folders(self.current_environment)

class ConfluenceTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        try:
            import requests
            import base64
            import json
            import logging
            from datetime import datetime
            import re
            import webbrowser
            
            self.requests = requests
            self.base64 = base64
            self.json = json
            self.datetime = datetime
            self.re = re
            self.webbrowser = webbrowser
            
            # Configurações do Confluence (diretas)
            self.token = "ATATT3xFfGF0XW9ZKoYXmlSXGtrB1BLwl3r-uIWgtiMubToPiyr7L4Ow02aXCYKSYD1h7wFghA6zMJq3eCwVGPdC-UZaDgR_C1XWGoSCQ7tsBTB-U0S2gMx7glGAN03tu9rEW3Uq_dyaVNEfPPTc8QJmozet0aivakcz28dfeOIyh13xtSBx-A8=185E9FFF"
            self.email = "almelo@topazevolution.com"
            self.base_url = "https://topsystems.atlassian.net"
            
            self.directories = {
                "TEST": r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Evidências\Test",
                "QA": r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Evidências\Qa"
            }
            
            self.confluence_paths = {
                "TEST": "3256811546",
                "QA": "3257565326"
            }
            
            self.template_id = "2134016126"
            
            self.setup_logging()
            self.criar_interface()
            
        except ImportError as e:
            self.criar_interface_erro(str(e))
    
    def get_root(self):
        return self.parent_frame.winfo_toplevel()
    
    def setup_logging(self):
        os.makedirs("logs", exist_ok=True)
        log_filename = f"logs/confluence_upload_{self.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def criar_interface_erro(self, erro):
        """Interface de erro quando módulos não estão disponíveis"""
        main_frame = ctk.CTkFrame(self.parent_frame, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="❌ Erro ao carregar sistema", 
                    font=ctk.CTkFont(size=18, weight="bold"), text_color="red").pack(pady=50)
        
        ctk.CTkLabel(main_frame, text=f"Erro: {erro}", 
                    font=ctk.CTkFont(size=12)).pack(pady=10)
        
        ctk.CTkLabel(main_frame, text="Verifique se o diretório do sistema existe:", 
                    font=ctk.CTkFont(size=11)).pack(pady=5)
        
        ctk.CTkLabel(main_frame, text="C:\\Users\\alessandro.melo\\OneDrive - Stefanini\\Ailos\\IMPORTAR-EVIDENCIA-CONFLUENCE", 
                    font=ctk.CTkFont(size=10), text_color="gray").pack(pady=5)
    
    def criar_interface(self):
        """Cria interface compacta do sistema Confluence"""
        main_frame = ctk.CTkFrame(self.parent_frame, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cabeçalho compacto
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=60)
        header_frame.pack(fill="x", pady=(5, 5))
        header_frame.pack_propagate(False)
        
        # Título centralizado
        titulo = ctk.CTkLabel(header_frame, text="📝 Confluence Evidence Uploader", 
                             font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(expand=True, pady=(10, 5))
        
        subtitulo = ctk.CTkLabel(header_frame, text="Duplicar página template e importar arquivo PDF", 
                                font=ctk.CTkFont(size=11))
        subtitulo.pack()
        
        # Frame de configurações
        config_frame = ctk.CTkFrame(main_frame, corner_radius=8)
        config_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        # Grid de configurações (2 colunas)
        grid_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=10)
        
        # Coluna 1
        col1_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        col1_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Ambiente
        ctk.CTkLabel(col1_frame, text="📋 Ambiente:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 2))
        
        self.env_var = ctk.StringVar()
        self.env_combo = ctk.CTkComboBox(col1_frame, values=["TEST", "QA"], 
                                        variable=self.env_var, command=self.on_env_change,
                                        font=ctk.CTkFont(size=11), height=30)
        self.env_combo.pack(fill="x", pady=(0, 8))
        
        # Arquivo PDF
        ctk.CTkLabel(col1_frame, text="📄 Arquivo PDF:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(5, 2))
        
        self.file_var = ctk.StringVar()
        self.file_combo = ctk.CTkComboBox(col1_frame, variable=self.file_var,
                                         font=ctk.CTkFont(size=11), height=30)
        self.file_combo.pack(fill="x", pady=(0, 8))
        
        # Coluna 2
        col2_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        col2_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Versão
        ctk.CTkLabel(col2_frame, text="🔢 Versão (X.X.XXX (IB)):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 2))
        
        self.version_var = ctk.StringVar()
        self.version_entry = ctk.CTkEntry(col2_frame, textvariable=self.version_var, 
                                         font=ctk.CTkFont(size=11), height=30,
                                         placeholder_text="Ex: 4.1.266 (IB)")
        self.version_entry.pack(fill="x", pady=(0, 8))
        
        # Caminho Confluence (readonly)
        ctk.CTkLabel(col2_frame, text="🔗 Caminho Confluence:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(5, 2))
        
        self.confluence_var = ctk.StringVar()
        self.confluence_entry = ctk.CTkEntry(col2_frame, textvariable=self.confluence_var, 
                                            font=ctk.CTkFont(size=10), height=30, state="disabled")
        self.confluence_entry.pack(fill="x", pady=(0, 8))
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=5)
        
        # Centralizar botões
        btn_center_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        btn_center_frame.pack(expand=True)
        
        self.upload_btn = ctk.CTkButton(btn_center_frame, text="📤 Duplicar e Importar", 
                                       command=self.upload_file, height=35, width=160,
                                       font=ctk.CTkFont(size=12, weight="bold"))
        self.upload_btn.pack(side="left", padx=3)
        
        self.open_confluence_btn = ctk.CTkButton(btn_center_frame, text="🌐 Abrir Confluence", 
                                                command=self.open_confluence, height=35, width=140,
                                                font=ctk.CTkFont(size=12, weight="bold"), 
                                                fg_color="#2196F3", hover_color="#1976D2")
        self.open_confluence_btn.pack(side="left", padx=3)
        
        # Área de log
        log_frame = ctk.CTkFrame(main_frame, corner_radius=8)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        ctk.CTkLabel(log_frame, text="📜 Log de Execução", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
        
        # Log com scrollbar
        self.log_textbox = ctk.CTkTextbox(log_frame, height=200, font=ctk.CTkFont(size=10))
        self.log_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Animação de entrada
        self.animate_entrance()
        
        # Verificar conexão com Confluence
        self.check_confluence_connection()
    
    def on_env_change(self, choice=None):
        """Atualiza quando ambiente muda"""
        env = self.env_var.get()
        if env:
            # Atualizar lista de arquivos PDF
            pdf_files = self.get_pdf_files(env)
            self.file_combo.configure(values=pdf_files)
            if pdf_files:
                self.file_var.set(pdf_files[0])
            
            # Atualizar caminho Confluence
            confluence_url = f"{self.base_url}/wiki/spaces/PSCECRED1/folder/{self.confluence_paths[env]}"
            self.confluence_var.set(confluence_url)
            
            # Atualizar campo versão baseado no ambiente
            if env == "TEST":
                self.version_var.set("4.1.XXX (IB)")
            elif env == "QA":
                self.version_var.set("2.1.XXX (IB)")
            
            self.log_message(f"Ambiente selecionado: {env}")
    
    def get_pdf_files(self, env):
        """Obtém lista de arquivos PDF do ambiente"""
        directory = self.directories[env]
        try:
            if os.path.exists(directory):
                files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
                self.log_message(f"Encontrados {len(files)} arquivos PDF em {directory}")
                return files
            else:
                self.log_message(f"Diretório não encontrado: {directory}")
                return []
        except Exception as e:
            self.log_message(f"Erro ao listar arquivos: {str(e)}")
            return []
    
    def validate_version(self, version):
        """Valida formato da versão"""
        pattern = r'^\d+\.\d+\.\d{3}\s+\(IB\)$'
        return self.re.match(pattern, version) is not None
    
    def animate_entrance(self):
        """Animação de entrada da interface"""
        self.get_root().attributes('-alpha', 0.8)
        self.get_root().after(100, lambda: self.get_root().attributes('-alpha', 1.0))
    
    def check_confluence_connection(self):
        """Verifica conexão com o Confluence em thread separada"""
        def check():
            import time
            # Animação de carregamento
            for i in range(3):
                dots = "." * (i + 1)
                self.get_root().after(0, lambda d=dots: self.log_message(f"Verificando conexão com Confluence{d}"))
                time.sleep(0.5)
            
            try:
                # Teste simples de conexão
                headers = {
                    'Authorization': f'Basic {self.base64.b64encode(f"{self.email}:{self.token}".encode()).decode()}'
                }
                response = self.requests.get(f"{self.base_url}/wiki/rest/api/space", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    self.get_root().after(0, lambda: [
                        self.log_message("✓ Conectado ao Confluence com sucesso!"),
                        self.enable_confluence_interface()
                    ])
                else:
                    self.get_root().after(0, lambda: self.log_message("✗ Erro de conexão com o Confluence"))
            except Exception as e:
                self.get_root().after(0, lambda: self.log_message(f"✗ Erro de conexão: {str(e)}"))
        
        import threading
        threading.Thread(target=check, daemon=True).start()
    
    def enable_confluence_interface(self):
        """Habilita a interface após conexão bem-sucedida"""
        # Interface já está habilitada, apenas animação
        self.animate_activation()
    
    def animate_activation(self):
        """Animação quando interface é ativada"""
        # Efeito de destaque nos campos ativados
        for widget in [self.env_combo, self.file_combo, self.version_entry]:
            try:
                self.get_root().after(100, lambda: None)  # Placeholder para animação
            except:
                pass
    
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        timestamp = self.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_textbox.insert("end", log_entry)
        self.log_textbox.see("end")
        self.get_root().update_idletasks()
        self.logger.info(message)
    
    def duplicate_template_page(self, version_name, target_folder_id):
        """Duplica página template"""
        template_id = self.template_id
        
        headers = {
            'Authorization': f'Basic {self.base64.b64encode(f"{self.email}:{self.token}".encode()).decode()}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Obter conteúdo da página template
            get_url = f"{self.base_url}/wiki/rest/api/content/{template_id}?expand=body.storage"
            
            self.log_message(f"Obtendo template: {template_id}")
            response = self.requests.get(get_url, headers=headers)
            
            if response.status_code != 200:
                self.log_message(f"Erro ao obter template: {response.status_code} - {response.text}")
                return None
            
            template_data = response.json()
            
            # Criar nova página
            create_url = f"{self.base_url}/wiki/rest/api/content"
            
            current_date = self.datetime.now().strftime("%d/%m/%Y")
            content = template_data['body']['storage']['value']
            
            new_page_data = {
                "type": "page",
                "title": version_name,
                "space": {
                    "key": "PSCECRED1"
                },
                "body": {
                    "storage": {
                        "value": content,
                        "representation": "storage"
                    }
                }
            }
            
            self.log_message(f"Criando nova página: {version_name}")
            response = self.requests.post(create_url, headers=headers, json=new_page_data)
            
            if response.status_code == 200:
                page_data = response.json()
                page_id = page_data['id']
                self.log_message(f"Página criada com sucesso: {version_name} (ID: {page_id})")
                
                # Mover página para a pasta correta
                if self.move_page_to_folder(page_id, target_folder_id):
                    return page_id
                else:
                    return page_id  # Retorna mesmo se não conseguir mover
            else:
                self.log_message(f"Erro ao criar página: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.log_message(f"Erro na requisição: {str(e)}")
            return None
    
    def move_page_to_folder(self, page_id, folder_id):
        """Move página para pasta"""
        headers = {
            'Authorization': f'Basic {self.base64.b64encode(f"{self.email}:{self.token}".encode()).decode()}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Obter dados completos da página
            get_url = f"{self.base_url}/wiki/rest/api/content/{page_id}?expand=body.storage,version"
            response = self.requests.get(get_url, headers=headers)
            
            if response.status_code != 200:
                self.log_message(f"Erro ao obter página: {response.status_code}")
                return False
            
            page_data = response.json()
            
            # Forçar movimentação usando PUT com ancestors
            update_url = f"{self.base_url}/wiki/rest/api/content/{page_id}"
            
            update_data = {
                "id": page_id,
                "type": "page",
                "title": page_data['title'],
                "space": {"key": "PSCECRED1"},
                "body": page_data['body'],
                "version": {
                    "number": page_data['version']['number'] + 1
                },
                "ancestors": [{"id": folder_id}]
            }
            
            self.log_message(f"Movendo página {page_id} para pasta {folder_id}")
            response = self.requests.put(update_url, headers=headers, json=update_data)
            
            if response.status_code == 200:
                self.log_message(f"Página movida com sucesso para pasta {folder_id}")
                return True
            else:
                self.log_message(f"Erro ao mover: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.log_message(f"Erro ao mover página: {str(e)}")
            return False
    
    def upload_file_to_page(self, page_id, file_path):
        """Faz upload do arquivo para a página"""
        url = f"{self.base_url}/wiki/rest/api/content/{page_id}/child/attachment"
        
        headers = {
            'Authorization': f'Basic {self.base64.b64encode(f"{self.email}:{self.token}".encode()).decode()}',
            'X-Atlassian-Token': 'no-check'
        }
        
        try:
            with open(file_path, 'rb') as file:
                files = {
                    'file': (os.path.basename(file_path), file, 'application/pdf')
                }
                
                response = self.requests.post(url, headers=headers, files=files)
                
                if response.status_code == 200:
                    self.log_message(f"Arquivo enviado com sucesso: {os.path.basename(file_path)}")
                    return True
                else:
                    self.log_message(f"Erro ao enviar arquivo: {response.status_code} - {response.text}")
                    return False
        except Exception as e:
            self.log_message(f"Erro ao enviar arquivo: {str(e)}")
            return False
    
    def upload_file(self):
        """Processo principal de upload"""
        env = self.env_var.get()
        file_name = self.file_var.get()
        version = self.version_var.get()
        
        if not env:
            messagebox.showerror("Erro", "Selecione um ambiente")
            return
        
        if not file_name:
            messagebox.showerror("Erro", "Selecione um arquivo PDF")
            return
        
        if not version:
            messagebox.showerror("Erro", "Digite a versão")
            return
        
        if not self.validate_version(version):
            messagebox.showerror("Erro", "Formato de versão inválido. Use: X.X.XXX (IB)")
            return
        
        self.log_message("Iniciando processo de upload...")
        
        # Caminho completo do arquivo
        file_path = os.path.join(self.directories[env], file_name)
        
        if not os.path.exists(file_path):
            messagebox.showerror("Erro", f"Arquivo não encontrado: {file_path}")
            return
        
        def upload_thread():
            try:
                # Duplicar página template e mover para pasta correta
                target_folder_id = self.confluence_paths[env]
                page_id = self.duplicate_template_page(version, target_folder_id)
                
                if page_id:
                    # Upload do arquivo
                    if self.upload_file_to_page(page_id, file_path):
                        self.get_root().after(0, lambda: [
                            self.log_message("Processo concluído com sucesso!"),
                            messagebox.showinfo("Sucesso", "Página duplicada e arquivo importado com sucesso!")
                        ])
                    else:
                        self.get_root().after(0, lambda: messagebox.showerror("Erro", "Falha ao enviar o arquivo"))
                else:
                    self.get_root().after(0, lambda: messagebox.showerror("Erro", "Falha ao duplicar a página template"))
            except Exception as e:
                self.get_root().after(0, lambda: [
                    self.log_message(f"Erro no processo: {str(e)}"),
                    messagebox.showerror("Erro", f"Erro no processo: {str(e)}")
                ])
        
        import threading
        threading.Thread(target=upload_thread, daemon=True).start()
    
    def open_confluence(self):
        """Abre Confluence no navegador"""
        confluence_url = "https://topsystems.atlassian.net/wiki/spaces/PSCECRED1/pages/2091779346/Evid+ncias+de+Testes+-+IB?atlOrigin=eyJpIjoiMWI0NGM4OTA0M2UzNDZmNWFlZTdlNmQxMzNlODRiYWQiLCJwIjoiYyJ9"
        self.webbrowser.open(confluence_url)
        self.log_message("Abrindo diretório de evidências no Confluence")

if __name__ == "__main__":
    app = SistemaAbas()
    app.executar()