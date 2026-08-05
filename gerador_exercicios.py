import os
import sys
import json
import re
from google import genai
from google.genai import types

# Importando o contrato estruturado do caderno de exercícios
from schemas import CadernoExerciciosValidado

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
                            print(f"[KEY] Chave de API carregada com sucesso a partir de '{path}'.")
                            return True
        except Exception as e:
            print(f"[ALERTA] Erro ao tentar ler {path}: {e}")
                
    return False

# Inicializa o carregamento da chave de API
carregar_chave_api()

# ==============================================================================
# FUNÇÃO PRINCIPAL DE ORQUESTRAÇÃO DE EXERCÍCIOS
# ==============================================================================
def gerar_caderno_exercicios(caminho_payload_teoria: str, diretrizes_texto: str = None):
    # Garante que temos a chave configurada
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("Chave de API 'GEMINI_API_KEY' não configurada. Configure a chave nos Secrets do Streamlit ou no ambiente.")

    try:
        client = genai.Client()
    except Exception as e:
        print(f"[ERRO] Erro ao inicializar o cliente do Google GenAI: {e}")
        return None
    
    # 1. Valida se o insumo do Agente 2 existe na máquina local
    if not os.path.exists(caminho_payload_teoria):
        print(f"[ERRO] Erro crítico: O arquivo '{caminho_payload_teoria}' não foi encontrado. Gere a teoria primeiro.")
        return None
        
    with open(caminho_payload_teoria, "r", encoding="utf-8") as f:
        payload_teoria = json.load(f)
        
    tema_aula = payload_teoria["tema"]
    print(f"\n[Agente 3] Iniciando a criação do caderno de exercícios para a aula: '{tema_aula}'...")

    # 2. Valida as diretrizes de estilo do professor (enviadas obrigatoriamente pelo Streamlit)
    if not diretrizes_texto or not diretrizes_texto.strip():
        raise ValueError("As diretrizes de notação e estilo são obrigatórias e devem ser fornecidas pelo Streamlit.")

    # Convertendo a teoria gerada em texto legível para o contexto do criador de questões
    contexto_teorico_acumulado = ""
    for pag in payload_teoria["conteudo_paginas"]:
        contexto_teorico_acumulado += f"\n--- Subtópico: {pag['titulo_subtopico']} ---\n"
        contexto_teorico_acumulado += f"Intuição: {pag['conteudo']['conceito_intuitivo']}\n"
        contexto_teorico_acumulado += f"Formalismo: {pag['conteudo']['conceito_formal']}\n"

    # 3. Engenharia de Prompt focada em Auto-Revisão e Validação Estrita
    prompt_exercicios = fr"""
Você é um Professor Adjunto de Estatística e Avaliador Acadêmico da UFBA.

### CONTEXTO E MISSÃO
Você receberá o [RESUMO_DA_TEORIA] que acabou de ser gerada e as [DIRETRIZES_DE_ESTILO] estritas de notação.
Sua missão é atuar como avaliador acadêmico: você deve projetar um caderno de exercícios de altíssimo nível universitário e rigor conceitual, preenchendo a estrutura 'CadernoExerciciosValidado'.

---

### DIRETRIZES DE ESCOPO E COMPLEXIDADE (MANDATÓRIO)
1. Alinhamento ao Escopo: Baseie-se estritamente e exclusivamente nos conceitos descritos no resumo teórico. Proibido exigir teorias ou distribuições que não constem no resumo.
2. Cenários Reais e Práticos: Crie enunciados contextualizados em problemas reais de engenharia, negócios, ensaios clínicos, economia ou IoT. Banir formulações puramente abstratas (ex: "Seja X...").
3. Rigor de LaTeX e Cálculos Completos: Toda notação e equações devem ser escritas em LaTeX ($ ou $$) usando os símbolos obrigatórios do professor. No gabarito, descreva numericamente todas as etapas da substituição algébrica.

---

### INSTRUÇÕES PARA PREENCHIMENTO DO SCHEMA DE RETORNO

1. 'topico_aula' (string):
   - Nome do tema central da aula: '{tema_aula}'.

2. 'questoes_multipla_escolha' (lista contendo exatamente 5 objetos QuestaoFechada):
   Cada item representa uma questão de múltipla escolha e deve conter:
   - 'enunciado' (string): Enunciado realista, complexo e detalhado que introduz a situação estatística e a pergunta de forma envolvente.
   - 'alternativas' (objeto AlternativasFechadas): Deve possuir exatamente as opções 'A', 'B', 'C', 'D' e 'E' com respostas completas e cientificamente plausíveis.
   - 'alternativa_correta' (string): Uma única letra correspondente à opção correta ('A', 'B', 'C', 'D' ou 'E').
   - 'dica' (string): Insight conceitual sutil que ajude o aluno sem entregar o gabarito.
   - 'gabarito_comentado' (string): Demonstração aritmética completa de todos os cálculos e justificativa minuciosa da alternativa correta.

3. 'questoes_discursivas' (lista contendo exatamente 3 objetos QuestaoAberta):
   Cada item representa uma questão discursiva/problema de cálculo e deve conter:
   - 'enunciado' (string): Problema discursivo que exija contas complexas ou análise qualitativa.
   - 'dica' (string): Direcionamento ou fórmula teórica inicial que guie a resposta.
   - 'gabarito_passo_a_passo' (lista de strings): As passagens e etapas de cálculo passo a passo expressas detalhadamente em LaTeX ($$).

---

### ENTRADAS DO USUÁRIO
- [RESUMO_DA_TEORIA]:
{contexto_teorico_acumulado}
- [DIRETRIZES_DE_ESTILO]:
{diretrizes_texto}
"""

    # Configuração estável do Gemini 3.1 Flash utilizando o Schema de Exercícios
    config_exercicios = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high"), # Ativação do modo analítico de auto-revisão
        temperature=1.0, # Pequena flexibilidade para criar enunciados criativos e práticos
        response_mime_type="application/json",
        response_schema=CadernoExerciciosValidado
    )

    try:
        resposta_exercicios = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[contexto_teorico_acumulado, prompt_exercicios],
            config=config_exercicios
        )
        
        # O Pydantic valida a estrutura e garante conformidade de chaves e tipos
        caderno_validado = CadernoExerciciosValidado.model_validate_json(resposta_exercicios.text)
        print(f"   [OK] Caderno gerado: {len(caderno_validado.questoes_multipla_escolha)} questões fechadas e {len(caderno_validado.questoes_discursivas)} questões abertas validadas!")
        return caderno_validado.model_dump()

    except Exception as e:
        print(f"   [ERRO] Falha crítica ao gerar ou validar o caderno de exercícios: {e}")
        return None

if __name__ == "__main__":
    print("[AVISO] A geração de exercícios deve ser executada a partir da interface do Streamlit.")
    print("Por favor, execute o comando: streamlit run app.py")
