@echo off
echo 🔧 Gerador de Evidencias - Build para Windows
echo ================================================

echo 📦 Instalando PyInstaller...
pip install pyinstaller

echo 🚀 Gerando executavel...
pyinstaller --onefile --windowed --name=GeradorEvidencias --add-data="processador_documentos.py;." gerador_evidencias.py

echo ✅ Build concluido!
echo 📁 Executavel gerado em: dist\GeradorEvidencias.exe

pause