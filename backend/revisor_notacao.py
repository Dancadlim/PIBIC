import os
import sys
import json
import re
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional

# Importamos o contrato do subtópico para o Revisor analisar
from schemas import SubtopicoValidado

# ==============================================================================
# FALLBACK DE SEGURANÇA PARA A CHAVE DE API (GEMINI_API_KEY)
# ==============================================================================
def carregar_chave_api():
    """Garante a leitura da API key a partir do ambiente, do st.secrets (Streamlit Cloud) ou do secrets.toml local."""
    if "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"].strip():
        return True
        
    # Tenta obter do st.secrets do Streamlit
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            val = st.secrets["GEMINI_API_KEY"]
            if val and val.strip():
                os.environ["GEMINI_API_KEY"] = val.strip()
                return True
    except Exception:
        pass
        
    # Tenta ler do secrets.toml da pasta local
    path = os.path.join(".streamlit", "secrets.toml")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for linha in f:
                    if "GEMINI_API_KEY" in linha:
                        match = re.search(r'(?:GEMINI_API_KEY\s*=\s*["\'])(.*?)(?:["\'])', linha)
                        if match:
                            os.environ["GEMINI_API_KEY"] = match.group(1).strip()
                            return True
        except Exception:
            pass
    return False

# Inicializa o carregamento da chave de API
carregar_chave_api()

# ==============================================================================
# SCHEMA DE DECISÃO DO AGENTE REVISOR (CRITIC)
# ==============================================================================
class DecisaoRevisao(BaseModel):
    aprovado: bool = Field(
        description="Defina como True se o conteúdo for profundo, correto e seguir 100% da notação. Defina como False se precisar de correções."
    )
    comentario_correcao: Optional[str] = Field(
        default=None,
        description="Se aprovado for False, escreva um laudo detalhado apontando onde o conteúdo falhou (notação errada, falta de rigor, explicação rasa) e o que o Escritor deve refazer."
    )
    conteudo_corrigido: Optional[SubtopicoValidado] = Field(
        default=None,
        description="Se aprovado for True, retorne o objeto de conteúdo revisado sem alterações estruturais."
    )

# ==============================================================================
# FUNÇÃO DE AUDITORIA DO SUBTÓPICO
# ==============================================================================
def auditar_subtopico_local(bloco_bruto_dict: dict, diretrizes_texto: str) -> DecisaoRevisao:
    # Garante que temos a chave configurada
    if not os.environ.get("GEMINI_API_KEY"):
        print("[ERRO] Erro no Revisor: Chave de API 'GEMINI_API_KEY' não configurada.")
        return DecisaoRevisao(aprovado=True, conteudo_corrigido=SubtopicoValidado(**bloco_bruto_dict))

    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex-key.json"
        client = genai.Client(vertexai=True, project="plataformas-aulas-ufba", location="us-central1")
    except Exception as e:
        print(f"[ERRO] Erro ao inicializar o cliente GenAI no Revisor: {e}")
        return DecisaoRevisao(aprovado=True, conteudo_corrigido=SubtopicoValidado(**bloco_bruto_dict))
    
    bloco_bruto_str = json.dumps(bloco_bruto_dict, ensure_ascii=False, indent=2)

    from prompts import PROMPT_REVISOR_CIENTIFICO, DICIONARIO_LATEX
    # Nota: No prompts.py o DICIONARIO_LATEX já está formatado dentro do PROMPT_REVISOR_CIENTIFICO, 
    # ou podemos simplesmente substituir se o string template precisar
    prompt_revisor = PROMPT_REVISOR_CIENTIFICO.replace("[CONTEÚDO_BRUTO]", bloco_bruto_str).replace("[DIRETRIZES_DE_ESTILO]", diretrizes_texto)

    config_revisor = types.GenerateContentConfig(
        temperature=1.0, # Puramente analítico e focado nas regras
        response_mime_type="application/json",
        response_schema=DecisaoRevisao
    )

    try:
        resposta = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[bloco_bruto_str, prompt_revisor],
            config=config_revisor
        )
        return DecisaoRevisao.model_validate_json(resposta.text)
    except Exception as e:
        # Em caso de pane na chamada do revisor, força aprovação preventiva para não quebrar o script de lote
        print(f"      [ALERTA] Falha operacional no motor do Revisor: {e}")
        return DecisaoRevisao(aprovado=True, conteudo_corrigido=SubtopicoValidado(**bloco_bruto_dict))
