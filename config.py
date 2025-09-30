"""
Configurações do IntegraEvidências
Carrega variáveis de ambiente de forma segura
"""
import os
from pathlib import Path

def load_env_file():
    """Carrega arquivo .env se existir"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Carregar variáveis de ambiente
load_env_file()

# === CONFIGURAÇÕES PADRÃO (podem ser sobrescritas por .env) ===

# Nexus Repository
NEXUS_URL = os.getenv('NEXUS_URL', 'https://nexus.exemplo.com')
NEXUS_USERNAME = os.getenv('NEXUS_USERNAME', 'usuario')
NEXUS_PASSWORD = os.getenv('NEXUS_PASSWORD', 'senha')
NEXUS_REPOSITORY = os.getenv('NEXUS_REPOSITORY', 'repositorio')

# Confluence
CONFLUENCE_URL = os.getenv('CONFLUENCE_URL', 'https://empresa.atlassian.net')
CONFLUENCE_EMAIL = os.getenv('CONFLUENCE_EMAIL', 'email@empresa.com')
CONFLUENCE_TOKEN = os.getenv('CONFLUENCE_TOKEN', 'token_exemplo')
CONFLUENCE_SPACE_KEY = os.getenv('CONFLUENCE_SPACE_KEY', 'SPACE')
CONFLUENCE_TEMPLATE_ID = os.getenv('CONFLUENCE_TEMPLATE_ID', '123456789')

# Diretórios
BASE_TEST_DIR = os.getenv('BASE_TEST_DIR', r'C:\Testes\Test')
BASE_QA_DIR = os.getenv('BASE_QA_DIR', r'C:\Testes\Qa')
BASE_TEMPLATES_DIR = os.getenv('BASE_TEMPLATES_DIR', r'C:\Templates')
CONFLUENCE_TEST_DIR = os.getenv('CONFLUENCE_TEST_DIR', r'C:\Evidencias\Test')
CONFLUENCE_QA_DIR = os.getenv('CONFLUENCE_QA_DIR', r'C:\Evidencias\Qa')

# Confluence Paths
CONFLUENCE_TEST_PATH = os.getenv('CONFLUENCE_TEST_PATH', 'path_test')
CONFLUENCE_QA_PATH = os.getenv('CONFLUENCE_QA_PATH', 'path_qa')

# Configurações de diretórios
DIRECTORIES = {
    "TEST": BASE_TEST_DIR,
    "QA": BASE_QA_DIR
}

CONFLUENCE_DIRECTORIES = {
    "TEST": CONFLUENCE_TEST_DIR,
    "QA": CONFLUENCE_QA_DIR
}

CONFLUENCE_PATHS = {
    "TEST": CONFLUENCE_TEST_PATH,
    "QA": CONFLUENCE_QA_PATH
}