# Sistema Gerador de Evidências de Testes

Sistema automatizado em Python para geração de documentos de evidências de testes a partir de estruturas de diretórios com imagens.

## Funcionalidades

- ✅ Leitura recursiva de diretórios e subdiretórios
- ✅ Identificação automática de arquivos .jpg
- ✅ Geração de títulos baseados na hierarquia de pastas
- ✅ Preservação da primeira e última página do template
- ✅ Inserção automática de imagens com redimensionamento
- ✅ Exportação em .docx e .pdf
- ✅ Interface gráfica intuitiva
- ✅ Suporte a caracteres especiais e acentuação
- ✅ Sistema de logs para auditoria

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

### Interface Gráfica
```bash
python gerador_evidencias.py
```

### Uso Programático
```python
from processador_documentos import ProcessadorDocumentos

processador = ProcessadorDocumentos("template.docx", largura_imagem=6.0)
sucesso = processador.processar_diretorio("C:/imagens", "evidencias.docx")
```

## Estrutura do Template

O template .docx deve ter:
- **Primeira página**: Capa/informações fixas (não será alterada)
- **Última página**: Rodapé/assinaturas (não será alterada)
- O conteúdo será inserido entre essas páginas

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

Os logs são salvos em `gerador_evidencias.log` e incluem:
- Pastas processadas
- Imagens inseridas
- Erros encontrados
- Tempo de processamento

## Requisitos do Sistema

- Python 3.7+
- Windows (para conversão PDF)
- Microsoft Word (para conversão PDF)