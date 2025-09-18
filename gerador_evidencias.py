import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from processador_documentos import ProcessadorDocumentos

class GeradorEvidencias:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gerador de Evidências de Testes")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        self.diretorio_selecionado = ""
        self.template_selecionado = ""
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Gerador de Evidências de Testes", 
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seleção de diretório
        ttk.Label(main_frame, text="Diretório com imagens:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dir_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.dir_var, width=65, state="readonly").grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Selecionar", command=self.selecionar_diretorio).grid(row=1, column=2)
        
        # Seleção de template
        ttk.Label(main_frame, text="Template (.docx):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.template_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.template_var, width=65, state="readonly").grid(row=2, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Selecionar", command=self.selecionar_template).grid(row=2, column=2)
        
        # Configurações
        config_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="10")
        config_frame.grid(row=3, column=0, columnspan=3, pady=20, sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="Largura das imagens (polegadas):").grid(row=0, column=0, sticky=tk.W)
        self.largura_var = tk.StringVar(value="6.0")
        ttk.Entry(config_frame, textvariable=self.largura_var, width=10).grid(row=0, column=1, padx=5)
        
        # Botões de ação
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Gerar Documento", command=self.gerar_documento, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sair", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="Log de Execução", padding="5")
        log_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_frame, height=12, width=85)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def selecionar_diretorio(self):
        diretorio = filedialog.askdirectory(title="Selecione o diretório com as imagens")
        if diretorio:
            self.diretorio_selecionado = diretorio
            self.dir_var.set(diretorio)
            self.log(f"Diretório selecionado: {diretorio}")
    
    def selecionar_template(self):
        template = filedialog.askopenfilename(
            title="Selecione o template",
            filetypes=[("Documentos Word", "*.docx")]
        )
        if template:
            self.template_selecionado = template
            self.template_var.set(template)
            self.log(f"Template selecionado: {template}")
    
    def gerar_documento(self):
        if not self.diretorio_selecionado:
            messagebox.showerror("Erro", "Selecione um diretório com imagens")
            return
        
        if not self.template_selecionado:
            messagebox.showerror("Erro", "Selecione um template")
            return
        
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
        
        self.log("Iniciando geração do documento...")
        
        try:
            processador = ProcessadorDocumentos(self.template_selecionado, largura)
            sucesso = processador.processar_diretorio(self.diretorio_selecionado, arquivo_saida)
            
            if sucesso:
                self.log("Documento gerado com sucesso!")
                messagebox.showinfo("Sucesso", f"Documento gerado:\n{arquivo_saida}")
            else:
                self.log("Erro na geração do documento")
                messagebox.showerror("Erro", "Falha na geração do documento")
                
        except Exception as e:
            self.log(f"Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro na geração: {str(e)}")
    
    def log(self, mensagem):
        self.log_text.insert(tk.END, f"{mensagem}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GeradorEvidencias()
    app.executar()