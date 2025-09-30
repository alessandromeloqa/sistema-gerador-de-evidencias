#!/usr/bin/env python3
"""
Script para gerar executável do Gerador de Evidências
"""

import subprocess
import sys
import os

def instalar_pyinstaller():
    """Instala PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("PyInstaller ja esta instalado")
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller instalado com sucesso!")

def gerar_executavel():
    """Gera o executável usando PyInstaller"""
    print("Gerando executavel...")
    
    comando = [
        "pyinstaller",
        "--onefile",                    # Arquivo único
        "--windowed",                   # Sem console
        "--name=IntegraEvidencias",     # Nome do executável
        "--hidden-import=cryptography.fernet",  # Fix cryptography
        "--hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2",
        "--hidden-import=cryptography.hazmat.backends.openssl",
# "--icon=icon.ico",              # Ícone (se existir)
        "--add-data=processador_documentos.py;.",  # Incluir módulo
        "IntegraEvidencias.py"         # Arquivo principal
    ]
    
    try:
        subprocess.run(comando, check=True)
        print("Executavel gerado com sucesso!")
        print("Localizacao: dist/IntegraEvidencias.exe")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerar executavel: {e}")
    except FileNotFoundError:
        print("PyInstaller nao encontrado. Execute: pip install pyinstaller")

if __name__ == "__main__":
    print("IntegraEvidencias - Build para Windows")
    print("=" * 50)
    
    instalar_pyinstaller()
    gerar_executavel()
    
    print("\nBuild concluido!")
    print("Execute: dist/IntegraEvidencias.exe")