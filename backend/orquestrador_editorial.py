import os
import json
import re
from google import genai
from google.genai import types
from schemas import AulaUnificadaELapidada

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
        
    path = os.path.join(".streamlit", "secrets.toml")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for linha in f:
                    if "GEMINI_API_KEY" in linha:
                        match = re.search(r'(?:GEMINI_API_KEY\s*=\s*["\'])(.*?)(?:["\'])', linha)
                        if match:
                            os.environ["GEMINI_API_KEY"] = match.group(1).strip()
                            print(f"[KEY] Chave de API carregada com sucesso a partir de '{path}'.")
                            return True
        except Exception as e:
            print(f"[ALERTA] Erro ao tentar ler {path}: {e}")
    return False

from model_utils import prepare_model_and_config

def lapidar_conteudo_global(payload_bruto: dict, modelo_ia: str = "padrao"):
    # Garante a inicialização da chave
    carregar_chave_api()
    client = genai.Client(vertexai=True, api_key=os.environ.get("GEMINI_API_KEY"))

    dados_entrada_str = json.dumps(payload_bruto, ensure_ascii=False)

    print("\n[Agente 3.5] Assumindo o controle editorial. Unificando e eliminando repetições da aula...")

    from prompts import PROMPT_ORQUESTRADOR
    prompt_editorial = PROMPT_ORQUESTRADOR.replace("[CAPÍTULO_BRUTO_AULA]", dados_entrada_str)

    model_name, config_editorial = prepare_model_and_config(
        modelo_solicitado=modelo_ia,
        default_model="gemini-2.5-flash",
        default_temp=1.0,
        response_mime_type="application/json",
        response_schema=AulaUnificadaELapidada
    )

    try:
        resposta = client.models.generate_content(
            model=model_name,
            contents=[dados_entrada_str, prompt_editorial],
            config=config_editorial
        )

        print(" [OK] Aula unificada, referências compiladas no rodapé e livre de repetições!")
        
        # --- PASSO ADICIONAL: FORMATADOR DE LATEX ---
        aula_unificada_json = json.loads(resposta.text)
        aula_formatada = formatar_latex_final(aula_unificada_json, client, modelo_ia=modelo_ia)
        
        # --- PASSO ADICIONAL: GERADOR DE SIMULADORES INTERATIVOS ---
        import agente_simulador
        simuladores = aula_formatada.get("simuladores_da_aula", [])
        if simuladores:
            tema = aula_formatada.get("tema_global", "Aula")
            for sim in simuladores:
                nome = sim.get("nome_simulador")
                if nome:
                    print(f" [Orquestrador] Requisitando código do simulador: {nome}")
                    html_code = agente_simulador.gerar_simulador_html(tema, nome, modelo_ia=modelo_ia)
                    sim["codigo_html_gerado"] = html_code
        
        return aula_formatada

    except Exception as e:
        print(f" [ERRO] Erro crítico no processo editorial: {e}")
        return payload_bruto

def formatar_latex_final(aula_json: dict, client, modelo_ia: str = "padrao") -> dict:
    from prompts import PROMPT_FORMATADOR_LATEX
    print("\n[Formatador LaTeX] Inspecionando e corrigindo delimitadores matemáticos...")
    
    model_name, config_formatador = prepare_model_and_config(
        modelo_solicitado=modelo_ia,
        default_model="gemini-2.5-flash",
        default_temp=0.1,
        response_mime_type="application/json",
        response_schema=AulaUnificadaELapidada
    )
    
    try:
        dados_str = json.dumps(aula_json, ensure_ascii=False)
        resposta_formatada = client.models.generate_content(
            model=model_name,
            contents=[dados_str, PROMPT_FORMATADOR_LATEX],
            config=config_formatador
        )
        print(" [OK] LaTeX validado e formatado com sucesso!")
        return json.loads(resposta_formatada.text)
    except Exception as e:
        print(f" [ERRO] Falha ao formatar LaTeX. Retornando a versão sem correção extra. Erro: {e}")
        return aula_json

def expandir_subtopico_para_prosa_livro(dados_subtopico: dict) -> str:
    carregar_chave_api()
    client = genai.Client(vertexai=True, api_key=os.environ.get("GEMINI_API_KEY"))
    
    from prompts import PROMPT_PROFESSOR_EXPANSOR, DICIONARIO_LATEX
    prompt = PROMPT_PROFESSOR_EXPANSOR.replace("{dicionario_latex}", DICIONARIO_LATEX)
    
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[json.dumps(dados_subtopico, ensure_ascii=False), prompt],
        config=types.GenerateContentConfig(
            temperature=1.0,
            response_mime_type="text/plain"
        )
    )
    return resposta.text.strip()

if __name__ == "__main__":
    print("[AVISO] O processo editorial deve ser executado a partir da interface do Streamlit.")
    print("Por favor, execute o comando: streamlit run app.py")
