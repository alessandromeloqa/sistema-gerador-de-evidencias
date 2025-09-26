# Sistema Gerador de Evidências de Testes

Sistema automatizado em Python para geração de documentos de evidências de testes a partir de estruturas de diretórios com imagens.

## Funcionalidades

- ✅ Leitura recursiva de diretórios e subdiretórios
- ✅ Identificação automática de arquivos .jpg
- ✅ Geração de títulos baseados na hierarquia de pastas
- ✅ Preservação da primeira e última página do template
- ✅ Inserção automática de imagens com redimensionamento
- ✅ Exportação em .docx e .pdf
- ✅ **Interface gráfica moderna e intuitiva**
- ✅ **ComboBoxes dinâmicos para seleção de versão (TEST/QA)**
- ✅ **Seleção automática de pastas baseada na versão**
- ✅ **Templates pré-carregados automaticamente**
- ✅ Suporte a caracteres especiais e acentuação
- ✅ **Sistema de logs com timestamp e ícones**

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

### Interface Gráfica Moderna
```bash
python gerador_evidencias.py
```

#### Passos para usar a nova interface:
1. **Selecione a Versão**: Escolha entre TEST ou QA no primeiro combo
2. **Escolha a Pasta**: O segundo combo será populado automaticamente com as pastas disponíveis
3. **Selecione o Template**: Já vem pré-selecionado o template padrão
4. **Configure a Largura**: Ajuste se necessário (padrão: 6.0 polegadas)
5. **Gere o Documento**: Clique no botão 🚀 Gerar Documento

### Uso Programático
```python
from processador_documentos import ProcessadorDocumentos

# Exemplo com os novos diretórios
template = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\SISTEMA-GERADOR-DE-EVIDENCIAS\Modelo de doc para geracao\EVIDENCIAS - MODELO.docx"
diretorio_test = r"C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Test\01-09-2025_4.1.266"

processador = ProcessadorDocumentos(template, largura_imagem=6.0)
sucesso = processador.processar_diretorio(diretorio_test, "evidencias.docx")
```

## Estrutura do Template

O template .docx deve ter:
- **Primeira página**: Capa/informações fixas (não será alterada)
- **Última página**: Rodapé/assinaturas (não será alterada)
- O conteúdo será inserido entre essas páginas

## Diretórios Configurados

### Versão TEST
- **Diretório**: `C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Test`
- **Pastas**: Listadas automaticamente no combo

### Versão QA  
- **Diretório**: `C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\IB\Testes\Qa`
- **Pastas**: Listadas automaticamente no combo

### Templates
- **Diretório**: `C:\Users\alessandro.melo\OneDrive - Stefanini\Ailos\SISTEMA-GERADOR-DE-EVIDENCIAS\Modelo de doc para geracao`
- **Arquivos**: Todos os .docx são carregados automaticamente

## Estrutura de Diretórios Suportada

```
Pasta Principal/
├── Subpasta 1/
│   ├── imagem1.jpg
│   └── imagem2.jpg
├── Subpasta 2/
│   ├── Subsubpasta A/
│   │   └── imagem3.jpg
│   └── imagem4.jpg
```

Resultado no documento:
- **Pasta Principal** (Título 1)
- **Subpasta 1** (Título 2)
  - imagem1.jpg
  - imagem2.jpg
- **Subpasta 2** (Título 2)
  - **Subsubpasta A** (Título 3)
    - imagem3.jpg
  - imagem4.jpg

## Logs

Os logs são exibidos em tempo real na interface e salvos em `gerador_evidencias.log`:
- 🚀 Inicialização do sistema
- 🔄 Seleções de versão e pastas
- ✅ Sucessos nas operações
- ❌ Erros encontrados
- 📋 Pastas e imagens processadas
- ⏰ Timestamp de cada operação

## Requisitos do Sistema

- Python 3.7+
- Windows (para conversão PDF)
- Microsoft Word (para conversão PDF)
- Acesso aos diretórios configurados

## Melhorias da Nova Interface

- 🎨 **Design Moderno**: Interface atualizada com cores e ícones
- 📦 **ComboBoxes Inteligentes**: Seleção dinâmica baseada na versão
- ⚙️ **Configuração Automática**: Diretórios e templates pré-configurados
- 📋 **Logs Visuais**: Sistema de log com ícones e cores
- ✅ **Validações Aprimoradas**: Verificações antes da geração
- 🚀 **Experiência do Usuário**: Processo simplificado e intuitivo