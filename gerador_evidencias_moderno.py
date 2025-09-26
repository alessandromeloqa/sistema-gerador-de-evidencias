import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from processador_documentos import ProcessadorDocumentos

# Configurar tema moderno
ctk.set_appearance_mode("dark")  # "dark" ou "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class GeradorEvidenciasModerno:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🔧 Gerador de Evidências de Testes")
        self.root.geometry("1000x750")
        
        # Diretórios base
        self.base_test = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Test"
        self.base_qa = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Qa"
        self.base_templates = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Modelo de doc para geracao"
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(main_frame, text="🔧 Gerador de Evidências de Testes", 
                             font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(pady=(30, 10))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(main_frame, text="Sistema automatizado para geração de documentos de evidências",
                                font=ctk.CTkFont(size=14))
        subtitulo.pack(pady=(0, 30))
        
        # Frame de configurações
        config_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        config_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Seleção de versão
        ctk.CTkLabel(config_frame, text="📋 Ambiente:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        
        self.versao_var = ctk.StringVar()
        self.versao_combo = ctk.CTkComboBox(config_frame, values=["TEST", "QA"], 
                                           variable=self.versao_var, command=self.on_versao_change,
                                           font=ctk.CTkFont(size=12), height=35)
        self.versao_combo.pack(fill="x", padx=20, pady=(0, 15))
        
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
        self.template_combo.pack(fill="x", padx=20, pady=(0, 15))
        
        # Largura das imagens
        ctk.CTkLabel(config_frame, text="🖼️ Largura das imagens (polegadas):", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.largura_var = ctk.StringVar(value="6.0")
        largura_entry = ctk.CTkEntry(config_frame, textvariable=self.largura_var, 
                                    font=ctk.CTkFont(size=12), height=35)
        largura_entry.pack(fill="x", padx=20, pady=(0, 20))
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        gerar_btn = ctk.CTkButton(button_frame, text="🚀 Gerar Documento", 
                                 command=self.gerar_documento, height=45, width=200,
                                 font=ctk.CTkFont(size=14, weight="bold"))
        gerar_btn.pack(side="left", padx=10)
        
        sair_btn = ctk.CTkButton(button_frame, text="❌ Sair", command=self.root.quit,
                                height=45, width=120, fg_color="gray", hover_color="darkgray",
                                font=ctk.CTkFont(size=14, weight="bold"))
        sair_btn.pack(side="left", padx=10)
        
        # Log
        log_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        log_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        ctk.CTkLabel(log_frame, text="📋 Log de Execução", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        self.log_text = ctk.CTkTextbox(log_frame, height=150, font=ctk.CTkFont(family="Consolas", size=11))
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Inicializar dados
        self.root.after(100, self.inicializar_dados)
    
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
                self.log(f"❌ Diretório não encontrado")
        except Exception as e:
            self.log(f"❌ Erro ao carregar pastas: {str(e)}")
    
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
                self.log(f"✅ Carregados {len(templates)} templates")
            else:
                self.template_combo.configure(values=[])
                self.log(f"❌ Diretório de templates não encontrado")
        except Exception as e:
            self.log(f"❌ Erro ao carregar templates: {str(e)}")
    
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
        
        # Construir caminhos
        base_dir = self.base_test if self.versao_var.get() == "TEST" else self.base_qa
        diretorio_selecionado = os.path.join(base_dir, self.pasta_var.get())
        template_selecionado = os.path.join(self.base_templates, self.template_var.get())
        
        try:
            largura = float(self.largura_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Largura deve ser um número válido")
            return
        
        # Nome do arquivo
        from datetime import datetime
        data_atual = datetime.now().strftime("%d%m%Y")
        nome_padrao = f"RELEASE NOTE - PROJETO AILOS - VERSÃO V00XC001RXXX - {data_atual}.docx"
        
        arquivo_saida = filedialog.asksaveasfilename(
            title="Salvar documento como",
            initialfile=nome_padrao,
            defaultextension=".docx",
            filetypes=[("Documentos Word", "*.docx")]
        )
        
        if not arquivo_saida:
            return
        
        self.log("🔄 Iniciando geração do documento...")
        
        try:
            processador = ProcessadorDocumentos(template_selecionado, largura)
            sucesso = processador.processar_diretorio(diretorio_selecionado, arquivo_saida)
            
            if sucesso:
                self.log("✅ Documento gerado com sucesso!")
                messagebox.showinfo("Sucesso", f"Documento gerado:\n{arquivo_saida}")
            else:
                self.log("❌ Erro na geração do documento")
                messagebox.showerror("Erro", "Falha na geração do documento")
                
        except Exception as e:
            self.log(f"❌ Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro na geração: {str(e)}")
    
    def log(self, mensagem):
        if hasattr(self, 'log_text'):
            self.log_text.insert("end", f"[{self.get_timestamp()}] {mensagem}\n")
            self.log_text.see("end")
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GeradorEvidenciasModerno()
    app.executar()