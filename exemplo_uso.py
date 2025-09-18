"""
Exemplo de uso do Gerador de Evidências de Testes

Este arquivo demonstra como usar o sistema tanto pela interface gráfica
quanto programaticamente.
"""

from processador_documentos import ProcessadorDocumentos
import os

def exemplo_uso_programatico():
    """Exemplo de uso direto da classe ProcessadorDocumentos"""
    
    # Configurações
    template_path = "template_evidencias.docx"  # Caminho para seu template
    diretorio_imagens = "C:/caminho/para/suas/imagens"  # Diretório com imagens
    arquivo_saida = "evidencias_geradas.docx"
    
    # Verificar se arquivos existem
    if not os.path.exists(template_path):
        print(f"Template não encontrado: {template_path}")
        return
    
    if not os.path.exists(diretorio_imagens):
        print(f"Diretório não encontrado: {diretorio_imagens}")
        return
    
    # Criar processador
    processador = ProcessadorDocumentos(template_path, largura_imagem=6.0)
    
    # Processar
    sucesso = processador.processar_diretorio(diretorio_imagens, arquivo_saida)
    
    if sucesso:
        print(f"Documento gerado com sucesso: {arquivo_saida}")
    else:
        print("Erro na geração do documento")

def exemplo_uso_interface():
    """Exemplo de uso da interface gráfica"""
    from gerador_evidencias import GeradorEvidencias
    
    app = GeradorEvidencias()
    app.executar()

if __name__ == "__main__":
    print("Escolha o modo de uso:")
    print("1 - Interface gráfica")
    print("2 - Uso programático")
    
    escolha = input("Digite sua escolha (1 ou 2): ")
    
    if escolha == "1":
        exemplo_uso_interface()
    elif escolha == "2":
        exemplo_uso_programatico()
    else:
        print("Opção inválida")