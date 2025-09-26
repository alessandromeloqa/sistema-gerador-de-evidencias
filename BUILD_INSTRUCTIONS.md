# 🚀 Instruções para Build do Executável

## 📋 Pré-requisitos

1. **Python 3.7+** instalado
2. **Todas as dependências** do projeto instaladas
3. **Windows** (para executável .exe)

## 🔧 Opções de Build

### **Opção 1: Script Automático (Recomendado)**
```bash
python build_exe.py
```

### **Opção 2: Batch Script**
```bash
build.bat
```

### **Opção 3: Manual**
```bash
# Instalar PyInstaller
pip install pyinstaller

# Gerar executável
pyinstaller --onefile --windowed --name=GeradorEvidencias gerador_evidencias.py
```

### **Opção 4: Usando arquivo .spec**
```bash
pyinstaller gerador_evidencias.spec
```

## 📁 Estrutura após Build

```
SISTEMA-GERADOR-DE-EVIDENCIAS/
├── dist/
│   └── GeradorEvidencias.exe    # ← Executável final
├── build/                       # Arquivos temporários
└── gerador_evidencias.spec      # Configuração PyInstaller
```

## ⚙️ Configurações do Build

- **--onefile**: Gera um único arquivo executável
- **--windowed**: Remove console (interface gráfica apenas)
- **--name**: Nome do executável final
- **--add-data**: Inclui arquivos necessários

## 🎯 Resultado

- **Arquivo**: `dist/GeradorEvidencias.exe`
- **Tamanho**: ~50-80 MB (inclui Python + dependências)
- **Portabilidade**: Roda em qualquer Windows sem Python instalado

## 🔍 Troubleshooting

### **Erro: ModuleNotFoundError**
```bash
pip install -r requirements_build.txt
```

### **Erro: customtkinter não encontrado**
```bash
pip install customtkinter
```

### **Executável muito grande**
Use `--exclude-module` para remover módulos desnecessários

### **Erro ao executar**
Teste primeiro com: `python gerador_evidencias.py`

## 📦 Distribuição

1. Copie `GeradorEvidencias.exe` para o destino
2. Certifique-se que os diretórios de templates existem
3. Execute o .exe diretamente

## 🎉 Pronto!

O executável estará em `dist/GeradorEvidencias.exe` e pode ser distribuído independentemente!