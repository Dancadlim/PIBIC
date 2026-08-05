import sys
import os
import re

# Wrapper global para fluxos de saída (stdout/stderr) para evitar erros de encoding (charmap/Unicode) no Windows
class SafeStreamWrapper:
    def __init__(self, original_stream):
        self.original_stream = original_stream
        
    def write(self, data):
        if not data:
            return
        encoding = getattr(self.original_stream, 'encoding', 'utf-8') or 'utf-8'
        try:
            self.original_stream.write(data)
        except UnicodeEncodeError:
            safe_data = data.encode(encoding, errors='replace').decode(encoding)
            self.original_stream.write(safe_data)
            
    def flush(self):
        try:
            self.original_stream.flush()
        except Exception:
            pass

    def __getattr__(self, name):
        return getattr(self.original_stream, name)

if sys.stdout:
    sys.stdout = SafeStreamWrapper(sys.stdout)
if sys.stderr:
    sys.stderr = SafeStreamWrapper(sys.stderr)

import streamlit as st

# 1. Configuração global da página - Executada antes de qualquer elemento UI
st.set_page_config(
    page_title="Plataforma de Aulas Premium 2.0",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS sutil na sidebar para visual premium (identidade visual)
st.markdown("""
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1E3A8A;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            font-size: 1.1rem;
            color: #64748B;
            margin-bottom: 2rem;
        }
        .welcome-card {
            background-color: #F8FAFC;
            border-left: 5px solid #1E3A8A;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

pasta_aulas = "aulas"
paginas_aulas = []

# Varredura dinâmica das aulas na pasta /aulas
if os.path.exists(pasta_aulas):
    arquivos = sorted(os.listdir(pasta_aulas))
    for arquivo in arquivos:
        if arquivo.startswith("aula") and arquivo.endswith(".py"):
            caminho_completo = os.path.join(pasta_aulas, arquivo)
            
            # Limpa o nome do arquivo "aula1_teste_t.py" -> "Aula 01: Teste T"
            match = re.match(r'^aula(\d+)_?(.*)', arquivo, flags=re.IGNORECASE)
            if match:
                num_aula = int(match.group(1))
                nome_resto = match.group(2).replace(".py", "").replace("_", " ").strip().title()
                titulo_bonito = f"Aula {num_aula:02d}: {nome_resto}"
            else:
                titulo_bonito = arquivo.replace(".py", "").replace("_", " ").title()
            
            # Cria o st.Page associado
            paginas_aulas.append(st.Page(caminho_completo, title=titulo_bonito, icon="📐"))

# Importação da página do gerador de aulas
import gerador_page

# Página fixa de administração/geração
pagina_gerador = st.Page(gerador_page.run_page, title="Criar Nova Aula", icon="🪄")

# Configuração da navegação dinâmica
secoes = {}
if paginas_aulas:
    secoes["📚 Trilha de Aprendizagem"] = paginas_aulas
secoes["⚙️ Administração"] = [pagina_gerador]

pg = st.navigation(secoes)
pg.run()
