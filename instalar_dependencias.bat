@echo off
echo Instalando dependencias do Sistema Gerador de Evidencias...
echo.

pip install python-docx==0.8.11
pip install Pillow==10.0.1
pip install pywin32

echo.
echo Instalacao concluida!
echo.
echo Para executar o sistema, use:
echo python gerador_evidencias.py
echo.
pause