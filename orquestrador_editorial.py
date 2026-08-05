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

def lapidar_conteudo_global(caminho_payload_teoria: str):
    # Garante a inicialização da chave
    carregar_chave_api()
    client = genai.Client()

    if not os.path.exists(caminho_payload_teoria):
        print(f"[ERRO] O arquivo '{caminho_payload_teoria}' não foi encontrado.")
        return None

    with open(caminho_payload_teoria, "r", encoding="utf-8") as f:
        payload_bruto = json.load(f)

    dados_entrada_str = json.dumps(payload_bruto, ensure_ascii=False)

    print("\n[Agente 3.5] Assumindo o controle editorial. Unificando e eliminando repetições da aula...")

    prompt_editorial = f"""
Você é o Editor-Chefe de uma prestigiada editora de livros de Estatística Matemática da UFBA.

### CONTEXTO E MISSÃO
Você receberá o [CAPÍTULO_BRUTO_AULA] (em JSON), contendo as páginas geradas separadamente pelo Agente Escritor para a aula '{payload_bruto['tema']}'.
Sua missão é atuar como editor unificador: você deve lapidar, costurar e organizar as páginas para que funcionem como um capítulo contínuo, fluido e visualmente impecável de um livro didático premium, preenchendo a estrutura 'AulaUnificadaELapidada'.

---

### DIRETRIZES DE ORGANIZAÇÃO E LAPIDAÇÃO (MANDATÓRIO)
1. Divisão de Trabalho e Lapidação: Sua função é puramente de ORGANIZAÇÃO, COERÊNCIA e POLIMENTO. Não invente teorias novas ou novos conteúdos. Costure as transições de prosa, elimine introduções ou fórmulas repetitivas, e faça a aula fluir harmonicamente.
2. Centralização de Gráficos e Simuladores: Analise as recomendações de simulador. Selecione no máximo 2 ou 3 simuladores realmente distintos e úteis para a aula inteira, alocando-os no campo 'simuladores_da_aula' indicando a página correta.
3. Rigor de Rodapé Bibliográfico: Colete todas as fontes do RAG, elimine as duplicatas e monte uma lista bibliográfica final limpa no rodapé (com autor, livro, capítulo e intervalo de páginas exatas no formato "Bussab & Morettin, Estatística Básica - Cap. 4.5, pp. 83-85").

---

### INSTRUÇÕES PARA PREENCHIMENTO DO SCHEMA DE RETORNO

1. 'tema_global' (string):
   - O título principal e premium que define a aula inteira de forma sofisticada.

2. 'paginas_conteudo' (lista de objetos PaginaLapidada):
   Cada item representa a versão unificada de um subtópico da aula e deve conter:
   - 'titulo_subtopico' (string): Título com alta sonoridade acadêmica e elegância temática.
   - 'discussao_teorica_prosa' (string): Texto em prosa denso e elegante costurando o material conceitual do Escritor de forma contínua e sem repetições conceituais.
   - 'prosa_longa_expandida' (string ou null): Espaço reservado para expansão futura (inicialmente copie o valor de 'discussao_teorica_prosa').
   - 'formalismo_latex' (string): Bloco LaTeX ($$) com as fórmulas mais marcantes da página, sem equações duplicadas.
   - 'deducao_analitica_linhas' (lista de strings): As passagens matemáticas completas e analíticas linha por linha em LaTeX ($$).
   - 'exemplos_praticos_ricos' (lista de objetos ExemploResolvidoRico): Mapeie de 2 a 3 exemplos práticos e exaustivos da teoria, cada um contendo:
     * 'contexto_e_enunciado' (string): Enunciado longo em cenário real complexo (mínimo 2 parágrafos).
     * 'dados_brutos_sumarizados' (string): Exibição dos dados organizados em LaTeX ($ ou $$).
     * 'desenvolvimento_aritmético_passo_a_passo' (lista de strings): Substituição numérica detalhada nas equações sem saltar passos algébricos.
     * 'conclusao_e_laudo_comercial' (string): Interpretação qualitativa robusta para tomador de decisão (min 1 parágrafo).

3. 'simuladores_da_aula' (lista de objetos MapeamentoSimulador):
   Cada item mapeia a localização de um gráfico Plotly e deve conter:
   - 'indice_pagina' (string): O índice da página (ex: "1", "2").
   - 'nome_simulador' (string): Nome descritivo sutil do simulador interativo.

4. 'referencias_bibliograficas_finais' (lista de strings):
   - Lista consolidada de obras com capítulos e intervalos de páginas explícitos.

---

### ENTRADAS DO USUÁRIO
- [CAPÍTULO_BRUTO_AULA]:
{dados_entrada_str}
"""

    config_editorial = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high"), # Carga pesada de pensamento para analisar a coerência global
        temperature=1.0,
        response_mime_type="application/json",
        response_schema=AulaUnificadaELapidada
    )

    try:
        resposta = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[dados_entrada_str, prompt_editorial],
            config=config_editorial
        )

        print(" [OK] Aula unificada, referências compiladas no rodapé e livre de repetições!")
        return json.loads(resposta.text)

    except Exception as e:
        print(f" [ERRO] Erro crítico no processo editorial: {e}")
        return payload_bruto

def expandir_subtopico_para_prosa_livro(dados_subtopico: dict) -> str:
    carregar_chave_api()
    client = genai.Client()
    
    prompt = """
    Você é um Professor Catedrático de Estatística Matemática. Sua única missão é pegar o esboço conceitual e formal de um subtópico e expandi-lo em um capítulo longo, denso e exaustivo de um livro didático de nível universitário premium.
    
    REGRAS DE CONSTRUÇÃO DE TEXTO:
    1. ESCREVA EM PROSA FLUIDA E EXTREMAMENTE LONGA: Escreva no mínimo de 6 a 8 parágrafos muito longos, explicativos e extremamente detalhados. Use o máximo de espaço de saída de tokens possível para dar profundidade enciclopédica ao texto. É terminantemente proibido resumir, abreviar ou usar listas com tópicos/bullets (-). Seja o mais exaustivo possível.
    2. PROFUNDIDADE HISTÓRICA E MOTIVAÇÃO: Explique o porquê desse conceito existir, qual problem prático da ciência ele resolve, como os pesquisadores pensavam antes dele e as implicações práticas de sua aplicação.
    3. RIGOR: Conecte o texto de forma elegante com as fórmulas em LaTeX ($$) fornecidas, explicando o significado estatístico de cada componente no meio do texto.
    
    Retorne o texto limpo em Markdown contendo os parágrafos de prosa profundos.
    """
    
    resposta = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[json.dumps(dados_subtopico, ensure_ascii=False), prompt],
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="high"),
            temperature=1.0
        )
    )
    return resposta.text.strip()

if __name__ == "__main__":
    print("[AVISO] O processo editorial deve ser executado a partir da interface do Streamlit.")
    print("Por favor, execute o comando: streamlit run app.py")
