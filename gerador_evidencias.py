import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from processador_documentos import ProcessadorDocumentos

class GeradorEvidencias:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gerador de Evidências de Testes")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilo moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Diretórios base
        self.base_test = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Test"
        self.base_qa = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Qa"
        self.base_templates = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\SISTEMA-GERADOR-DE-EVIDENCIAS\Modelo de doc para geracao"
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal com estilo moderno
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Título moderno
        titulo = ttk.Label(main_frame, text="🔧 Gerador de Evidências de Testes", 
                          font=("Segoe UI", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Subtítulo
        subtitulo = ttk.Label(main_frame, text="Sistema automatizado para geração de documentos de evidências", 
                             font=("Segoe UI", 10))
        subtitulo.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de seleções
        selecao_frame = ttk.LabelFrame(main_frame, text="⚙️ Configurações", padding="20")
        selecao_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        selecao_frame.columnconfigure(1, weight=1)
        
        # Seleção de versão
        ttk.Label(selecao_frame, text="📋 Ambiente:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.versao_var = tk.StringVar()
        self.versao_combo = ttk.Combobox(selecao_frame, textvariable=self.versao_var, 
                                        values=["TEST", "QA"], state="readonly", width=50, font=('Segoe UI', 10))
        self.versao_combo.grid(row=0, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        self.versao_combo.bind('<<ComboboxSelected>>', self.on_versao_change)
        
        # Seleção de pasta
        ttk.Label(selecao_frame, text="📁 Pasta:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.pasta_var = tk.StringVar()
        self.pasta_combo = ttk.Combobox(selecao_frame, textvariable=self.pasta_var, 
                                       state="readonly", width=50, font=('Segoe UI', 10))
        self.pasta_combo.grid(row=1, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        
        # Seleção de template
        ttk.Label(selecao_frame, text="📄 Template:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(selecao_frame, textvariable=self.template_var, 
                                          state="readonly", width=50, font=('Segoe UI', 10))
        self.template_combo.grid(row=2, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        
        # Inicializar após criar todos os componentes
        self.root.after(100, self.inicializar_dados)
        
        # Configurações avançadas
        config_frame = ttk.LabelFrame(main_frame, text="🔧 Configurações Avançadas", padding="20")
        config_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="Largura das imagens (polegadas):", font=("Segoe UI", 10)).grid(row=0, column=0, sticky=tk.W)
        self.largura_var = tk.StringVar(value="6.0")
        largura_entry = ttk.Entry(config_frame, textvariable=self.largura_var, width=15)
        largura_entry.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Botões de ação modernos
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=30)
        
        # Estilo para botões
        self.style.configure('Modern.TButton', font=('Segoe UI', 11, 'bold'), padding=(20, 10))
        
        gerar_btn = ttk.Button(button_frame, text="🚀 Gerar Documento", command=self.gerar_documento, 
                              style="Modern.TButton")
        gerar_btn.pack(side=tk.LEFT, padx=10)
        
        sair_btn = ttk.Button(button_frame, text="❌ Sair", command=self.root.quit, 
                             style="Modern.TButton")
        sair_btn.pack(side=tk.LEFT, padx=10)
        
        # Área de log moderna
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log de Execução", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_frame, height=8, width=80, font=("Consolas", 9),
                               bg='#2d2d2d', fg='#ffffff', insertbackground='white', wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def on_versao_change(self, event=None):
        versao = self.versao_var.get()
        if versao == "TEST":
            self.carregar_pastas(self.base_test)
            self.log(f"🔄 Versão selecionada: {versao} - Carregando pastas de teste...")
        elif versao == "QA":
            self.carregar_pastas(self.base_qa)
            self.log(f"🔄 Versão selecionada: {versao} - Carregando pastas de QA...")
    
    def carregar_pastas(self, base_dir):
        try:
            if os.path.exists(base_dir):
                pastas = [d for d in os.listdir(base_dir) 
                         if os.path.isdir(os.path.join(base_dir, d))]
                self.pasta_combo['values'] = pastas
                self.pasta_var.set('')
                self.log(f"✅ Carregadas {len(pastas)} pastas disponíveis")
            else:
                self.pasta_combo['values'] = []
                self.log(f"❌ Diretório não encontrado: {base_dir}")
        except Exception as e:
            self.log(f"❌ Erro ao carregar pastas: {str(e)}")
    
    def inicializar_dados(self):
        self.carregar_templates()
        self.log("🚀 Sistema inicializado com sucesso! Pronto para uso.")
    
    def carregar_templates(self):
        try:
            if os.path.exists(self.base_templates):
                templates = [f for f in os.listdir(self.base_templates) 
                           if f.endswith('.docx')]
                self.template_combo['values'] = templates
                if templates:
                    self.template_var.set(templates[0])
                self.log(f"✅ Carregados {len(templates)} templates disponíveis")
            else:
                self.template_combo['values'] = []
                self.log(f"❌ Diretório de templates não encontrado")
        except Exception as e:
            self.log(f"❌ Erro ao carregar templates: {str(e)}")
    
    def gerar_documento(self):
        if not self.versao_var.get():
            messagebox.showerror("Erro", "Selecione uma versão (TEST ou QA)")
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
            self.log_text.insert(tk.END, f"[{self.get_timestamp()}] {mensagem}\n")
            self.log_text.see(tk.END)
            self.root.update()
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GeradorEvidencias()
    app.executar()