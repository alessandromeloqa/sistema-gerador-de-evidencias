import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import threading
from processador_documentos import ProcessadorDocumentos

# Configurar tema moderno (será alterado dinamicamente)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GeradorEvidencias:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🔧 Gerador de Evidências de Testes")
        self.root.geometry("1100x900")
        
        # Variáveis de controle
        self.tema_escuro = True
        self.arquivo_gerado = None
        
        # Diretórios base
        self.base_test = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Test"
        self.base_qa = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Qa"
        self.base_templates = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\SISTEMA-GERADOR-DE-EVIDENCIAS\Modelo de doc para geracao"
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame do cabeçalho com indicador de status
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(20, 0))
        
        # Frame do indicador de status
        status_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        status_frame.pack(side="left", padx=(10, 0))
        
        # Indicador de status dos diretórios (canto superior esquerdo)
        self.status_indicator = ctk.CTkLabel(status_frame, text="●", font=ctk.CTkFont(size=28), 
                                           text_color="#FFA500", width=40)
        self.status_indicator.pack()
        
        # Texto explicativo
        status_text = ctk.CTkLabel(status_frame, text="Status Conexão com\ndiretórios do sistema", 
                                  font=ctk.CTkFont(size=9), justify="center")
        status_text.pack()
        
        # Título centralizado
        titulo_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        titulo_frame.pack(expand=True, fill="x")
        
        titulo = ctk.CTkLabel(titulo_frame, text="🔧 Gerador de Evidências de Testes", 
                             font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(expand=True, pady=(5, 5))
        
        # Subtítulo e controles de tema
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Frame centralizado para subtítulo
        subtitle_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        subtitle_frame.pack(expand=True, fill="x")
        
        subtitulo = ctk.CTkLabel(subtitle_frame, text="Sistema automatizado para geração de documentos de evidências",
                                font=ctk.CTkFont(size=14))
        subtitulo.pack()
        
        # Switch de tema (posicionado à direita)
        tema_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        tema_frame.pack(side="right", padx=(0, 10))
        
        ctk.CTkLabel(tema_frame, text="🌙", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 5))
        self.tema_switch = ctk.CTkSwitch(tema_frame, text="", command=self.alternar_tema, width=50)
        self.tema_switch.select()  # Inicia em dark
        self.tema_switch.pack(side="left")
        ctk.CTkLabel(tema_frame, text="☀️", font=ctk.CTkFont(size=16)).pack(side="left", padx=(5, 0))
        
        # Frame de configurações
        config_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        config_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        # Seleção de versão
        ctk.CTkLabel(config_frame, text="📋 Ambiente:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.versao_var = ctk.StringVar()
        self.versao_combo = ctk.CTkComboBox(config_frame, values=["TEST", "QA"], 
                                           variable=self.versao_var, command=self.on_versao_change,
                                           font=ctk.CTkFont(size=12), height=35)
        self.versao_combo.pack(fill="x", padx=20, pady=(0, 2))
        
        # Frame para crítica e botão ambiente
        ambiente_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        ambiente_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.critica_ambiente = ctk.CTkLabel(ambiente_frame, text="", 
                                           font=ctk.CTkFont(size=10), text_color="#FF0000")
        self.critica_ambiente.pack(side="left")
        
        self.btn_navegar_ambiente = ctk.CTkButton(ambiente_frame, text="📁 Navegar", 
                                                 command=self.navegar_ambiente, width=80, height=25,
                                                 font=ctk.CTkFont(size=10))
        # Botão inicialmente oculto
        
        # Seleção de pasta
        ctk.CTkLabel(config_frame, text="📁 Pasta:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.pasta_var = ctk.StringVar()
        self.pasta_combo = ctk.CTkComboBox(config_frame, variable=self.pasta_var,
                                          font=ctk.CTkFont(size=12), height=35)
        self.pasta_combo.pack(fill="x", padx=20, pady=(0, 15))
        
        # Seleção de template
        ctk.CTkLabel(config_frame, text="📄 Template:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.template_var = ctk.StringVar()
        self.template_combo = ctk.CTkComboBox(config_frame, variable=self.template_var,
                                             font=ctk.CTkFont(size=12), height=35)
        self.template_combo.pack(fill="x", padx=20, pady=(0, 2))
        
        # Frame para crítica e botão template
        template_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        template_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.critica_template = ctk.CTkLabel(template_frame, text="", 
                                           font=ctk.CTkFont(size=10), text_color="#FF0000")
        self.critica_template.pack(side="left")
        
        self.btn_navegar_template = ctk.CTkButton(template_frame, text="📁 Navegar", 
                                                 command=self.navegar_template, width=80, height=25,
                                                 font=ctk.CTkFont(size=10))
        # Botão inicialmente oculto
        
        # Frame para configurações em linha
        config_inline_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        config_inline_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Largura das imagens
        largura_frame = ctk.CTkFrame(config_inline_frame, fg_color="transparent")
        largura_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(largura_frame, text="🖼️ Largura (pol.):", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        
        self.largura_var = ctk.StringVar(value="6.0")
        largura_entry = ctk.CTkEntry(largura_frame, textvariable=self.largura_var, 
                                    font=ctk.CTkFont(size=12), height=35, width=80)
        largura_entry.pack(fill="x")
        
        # Qualidade da imagem
        qualidade_frame = ctk.CTkFrame(config_inline_frame, fg_color="transparent")
        qualidade_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(qualidade_frame, text="📊 Qualidade:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        
        self.qualidade_var = ctk.StringVar(value="Alta")
        qualidade_combo = ctk.CTkComboBox(qualidade_frame, values=["Alta (Padrão)", "Média (Otimizada)", "Baixa (Documentos Grandes)"],
                                         variable=self.qualidade_var, font=ctk.CTkFont(size=12), height=35)
        qualidade_combo.pack(fill="x")
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=10)
        
        gerar_btn = ctk.CTkButton(button_frame, text="🚀 Gerar Documento", 
                                 command=self.gerar_documento, height=45, width=180,
                                 font=ctk.CTkFont(size=14, weight="bold"))
        gerar_btn.pack(side="left", padx=5)
        
        templates_btn = ctk.CTkButton(button_frame, text="📁 Gerenciar Templates", 
                                     command=self.gerenciar_templates, height=45, width=180,
                                     font=ctk.CTkFont(size=14, weight="bold"), fg_color="orange", hover_color="darkorange")
        templates_btn.pack(side="left", padx=5)
        
        sair_btn = ctk.CTkButton(button_frame, text="❌ Sair", command=self.root.quit,
                                height=45, width=100, fg_color="gray", hover_color="darkgray",
                                font=ctk.CTkFont(size=14, weight="bold"))
        sair_btn.pack(side="left", padx=5)
        
        # Área de progresso (sempre visível)
        self.progress_frame = ctk.CTkFrame(main_frame, corner_radius=10, height=80)
        self.progress_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        ctk.CTkLabel(self.progress_frame, text="🚀 Progresso da Geração", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Aguardando...", 
                                          font=ctk.CTkFont(size=12))
        self.progress_label.pack(pady=(0, 8))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=300, height=15, 
                                              progress_color="#008000")
        self.progress_bar.pack(pady=(0, 15))
        self.progress_bar.set(0)
        
        # Inicializar dados
        self.root.after(100, self.inicializar_dados)
        
        # Verificar status dos diretórios
        self.root.after(200, self.verificar_status_diretorios)
    
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
    
    def verificar_status_diretorios(self):
        """Verifica se todos os diretórios estão acessíveis"""
        # Verificar cada diretório individualmente
        test_ok = os.path.exists(self.base_test) and os.path.isdir(self.base_test)
        qa_ok = os.path.exists(self.base_qa) and os.path.isdir(self.base_qa)
        templates_ok = os.path.exists(self.base_templates) and os.path.isdir(self.base_templates)
        
        status_list = [test_ok, qa_ok, templates_ok]
        
        # Atualizar indicador geral
        if all(status_list):
            self.status_indicator.configure(text_color="#008000")
        elif any(status_list):
            self.status_indicator.configure(text_color="#FFA500")
        else:
            self.status_indicator.configure(text_color="#FF0000")
        
        # Controlar estado dos campos
        self.controlar_campos_por_status(test_ok, qa_ok, templates_ok)
    
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
    
    def alternar_tema(self):
        self.tema_escuro = not self.tema_escuro
        modo = "dark" if self.tema_escuro else "light"
        ctk.set_appearance_mode(modo)
        self.log(f"🎨 Tema alterado para: {modo}")
    
    def mostrar_progresso(self, texto="Processando..."):
        self.progress_label.configure(text=texto)
        self.progress_bar.set(0)
        self.root.update()
    
    def ocultar_progresso(self):
        self.progress_label.configure(text="Aguardando...")
        self.progress_bar.set(0)
        self.root.update()
    
    def atualizar_progresso(self, valor, texto, status=""):
        self.progress_bar.set(valor)
        if status:
            self.progress_label.configure(text=f"{texto} - {status}")
        else:
            self.progress_label.configure(text=texto)
        self.root.update()
    
    def gerenciar_templates(self):
        # Janela de gerenciamento de templates
        template_window = ctk.CTkToplevel(self.root)
        template_window.title("📁 Gerenciar Templates")
        template_window.geometry("600x400")
        template_window.transient(self.root)
        
        # Lista de templates
        ctk.CTkLabel(template_window, text="Templates Disponíveis", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))
        
        # Frame para lista
        list_frame = ctk.CTkFrame(template_window)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.template_listbox = ctk.CTkTextbox(list_frame, height=200)
        self.template_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        # Implementação simplificada - remove o template selecionado
        templates = [f for f in os.listdir(self.base_templates) if f.endswith('.docx')]
        if templates:
            # Para simplicidade, remove o primeiro template (pode ser melhorado)
            template_para_remover = templates[0]
            resposta = messagebox.askyesno("Confirmar", f"Remover template '{template_para_remover}'?")
            if resposta:
                try:
                    os.remove(os.path.join(self.base_templates, template_para_remover))
                    self.log(f"🗑️ Template removido: {template_para_remover}")
                    self.atualizar_lista_templates()
                    self.carregar_templates()
                except Exception as e:
                    self.log(f"❌ Erro ao remover template: {str(e)}")
    
    def atualizar_lista_templates(self):
        if hasattr(self, 'template_listbox'):
            self.template_listbox.delete("1.0", "end")
            try:
                templates = [f for f in os.listdir(self.base_templates) if f.endswith('.docx')]
                for i, template in enumerate(templates, 1):
                    self.template_listbox.insert("end", f"{i}. {template}\n")
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
                self.root.after(100, self.mostrar_opcoes_pos_geracao)
            else:
                self.log("❌ Erro na geração do documento")
                self.root.after(100, lambda: messagebox.showerror("Erro", "Falha na geração do documento"))
                
        except Exception as e:
            self.log(f"❌ Erro: {str(e)}")
            self.root.after(100, lambda: messagebox.showerror("Erro", f"Erro na geração: {str(e)}"))
        finally:
            self.root.after(3000, self.ocultar_progresso)
    
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
        pass  # Log removido
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GeradorEvidencias()
    app.executar()