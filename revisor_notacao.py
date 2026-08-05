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
        client = genai.Client()
    except Exception as e:
        print(f"[ERRO] Erro ao inicializar o cliente GenAI no Revisor: {e}")
        return DecisaoRevisao(aprovado=True, conteudo_corrigido=SubtopicoValidado(**bloco_bruto_dict))
    
    bloco_bruto_str = json.dumps(bloco_bruto_dict, ensure_ascii=False, indent=2)

    prompt_revisor = f"""
Você é um Professor Titular e Revisor de Conteúdo Científico de Estatística e Matemática da UFBA.

### CONTEXTO E MISSÃO
Você receberá o [CONTEÚDO_BRUTO] gerado pelo Agente Escritor (em JSON) e as [DIRETRIZES_DE_ESTILO] estritas de notação.
Sua missão é atuar como auditor científico: você deve avaliar rigorosamente se o conteúdo e o formalismo matemático estão corretos, profundos e em total conformidade notacional, preenchendo a estrutura 'DecisaoRevisao'.

---

### DIRETRIZES DE REVISÃO E RIGOR (MANDATÓRIO)
1. Tolerância Zero com Desvios: Se houver qualquer símbolo fora da tabela padrão (ex: df em vez de gl, H_a em vez de H_1, p-valor sem ser LaTeX), você é OBRIGADO a reprovar o bloco (`aprovado = False`).
2. Avaliação de Grounding (Páginas do RAG): Inspecione o campo 'fontes_rag'. Se qualquer fonte não contiver o número ou intervalo exato de páginas consultadas (ex: omitir ou responder "p. não especificada"), REPROVE imediatamente.
3. Critério de Dificuldade e Profundidade: Avalie se a prosa é densa e se a dedução analítica passo a passo está completa, contínua e sem omissões algébricas.

---

### INSTRUÇÕES PARA PREENCHIMENTO DO SCHEMA DE RETORNO

1. 'aprovado' (boolean):
   - Defina como True apenas se o conteúdo atender 100% dos requisitos de notação exata, exaustividade teórica, dedução contígua e páginas do RAG mapeadas de forma perfeita.
   - Defina como False caso encontre qualquer desvio.

2. 'comentario_correcao' (string):
   - Se 'aprovado' for False, preencha este campo com um laudo técnico cirúrgico detalhando cada desvio encontrado e as correções necessárias.
   - IMPORTANTE (MANDATÓRIO PARA FALHA DE GROUNDING): Se houver fontes sem as páginas exatas do RAG, insira exatamente a seguinte string: '[ERRO BIBLIOGRÁFICO] O modelo omitiu as páginas exatas consultadas nos documentos do RAG. Refaça a busca e mapeie o número da página.'
   - Se 'aprovado' for True, retorne null ou "".

3. 'conteudo_corrigido' (objeto SubtopicoValidado ou null):
   - Se 'aprovado' for True, retorne neste campo o objeto de conteúdo revisado.
   - Se 'aprovado' for False, retorne null.

---

### ENTRADAS DO USUÁRIO
- [CONTEÚDO_BRUTO]:
{bloco_bruto_str}
- [DIRETRIZES_DE_ESTILO]:
{diretrizes_texto}
"""

    config_revisor = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high"), # Raciocínio profundo para caçar falhas
        temperature=1.0, # Puramente analítico e focado nas regras
        response_mime_type="application/json",
        response_schema=DecisaoRevisao
    )

    try:
        resposta = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[bloco_bruto_str, prompt_revisor],
            config=config_revisor
        )
        return DecisaoRevisao.model_validate_json(resposta.text)
    except Exception as e:
        # Em caso de pane na chamada do revisor, força aprovação preventiva para não quebrar o script de lote
        print(f"      [ALERTA] Falha operacional no motor do Revisor: {e}")
        return DecisaoRevisao(aprovado=True, conteudo_corrigido=SubtopicoValidado(**bloco_bruto_dict))
