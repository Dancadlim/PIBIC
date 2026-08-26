import os
import json
from typing import Optional, Dict
from google import genai
from google.genai import types
from dotenv import load_dotenv
from schemas import RegraOverride

load_dotenv()

PROMPT_EXTRATOR = """
Você é um Especialista em Extração de Diretrizes e Notações Acadêmicas de Inteligência Artificial.
Sua missão é ler o documento de diretrizes ou anotações fornecido pelo professor e extrair com extrema precisão:
1. Notações Estatísticas e Matemáticas Específicas: Mapeie o conceito/variável para a notação exata exigida pelo professor em LaTeX (ex: "média populacional" -> "\\mu", "desvio padrão" -> "\\sigma", "independência" -> "\\perp").
2. Tópicos Obrigatórios: Quaisquer assuntos ou tópicos específicos que o professor declarou que devem ser cobertos.
3. Estilo de Exercícios: Instruções sobre nivelamento, formato, estilo ou quantidade de questões.
4. Outras Diretrizes: Observações pedagógicas ou avisos contextuais relevantes.

DOCUMENTO DO PROFESSOR:
{texto_documento}
"""

def extrair_regras_override(texto_documento: str, logger=None) -> Optional[Dict]:
    """
    Lê o texto/documento de notações/diretrizes do professor e usa o Gemini 2.5 Flash
    com Structured Output (schema RegraOverride) para retornar as regras estruturadas.
    """
    if not texto_documento or not texto_documento.strip():
        return None
        
    try:
        os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "vertex-key.json")
        client = genai.Client(vertexai=True, location="us-central1")
        
        prompt = PROMPT_EXTRATOR.format(texto_documento=texto_documento)
        
        if logger:
            logger.update_agent("extrator", "rodando", prompt=prompt)
            logger.log("Agente Extrator: Lendo notações e diretrizes específicas...", "info")
            
        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=RegraOverride
            )
        )
        
        if resposta.text:
            override_dict = json.loads(resposta.text)
            if logger:
                logger.log("Agente Extrator: Notações e diretrizes extraídas com sucesso!", "info")
            return override_dict
            
    except Exception as e:
        print(f"[ERRO] Falha no Agente Extrator: {e}")
        if logger:
            logger.log(f"[ERRO] Agente Extrator falhou: {e}", "erro")
            
    return None

def formatar_override_para_prompt(override_dict: dict) -> str:
    """
    Converte o dicionário RegraOverride em um bloco de texto formatado
    pronto para injeção nos prompts dos micro-agentes com prioridade absoluta.
    """
    if not override_dict:
        return ""
        
    linhas = ["[OVERRIDE DE DIRETRIZES DO PROFESSOR - PRIORIDADE ABSOLUTA]"]
    
    # 1. Notações específicas (Dicionário de Conceito -> Notação)
    notacoes = override_dict.get("notacoes_estatisticas_especificas")
    if notacoes and isinstance(notacoes, dict) and len(notacoes) > 0:
        linhas.append("\nREGRAS DE NOTAÇÃO MATEMÁTICA ESTATÍSTICA (SOBRESCREVE O PADRÃO):")
        for conceito, notacao in notacoes.items():
            linhas.append(f"  - Conceito: '{conceito}' -> Notação Exata Obrigatória: {notacao}")
            
    # 2. Tópicos Obrigatórios
    topicos = override_dict.get("topicos_obrigatorios")
    if topicos and isinstance(topicos, list) and len(topicos) > 0:
        linhas.append("\nTÓPICOS E SUBTÓPICOS OBRIGATÓRIOS NESTA AULA:")
        for t in topicos:
            linhas.append(f"  - {t}")
            
    # 3. Estilo de Exercícios
    estilo = override_dict.get("estilo_exercicios")
    if estilo and isinstance(estilo, str) and estilo.strip():
        linhas.append(f"\nESTILO E FORMATO DOS EXERCÍCIOS:\n  - {estilo.strip()}")
        
    # 4. Outras Diretrizes
    outras = override_dict.get("outras_diretrizes")
    if outras and isinstance(outras, str) and outras.strip():
        linhas.append(f"\nOUTRAS DIRETRIZES E INSTRUÇÕES ESPECÍFICAS:\n  - {outras.strip()}")
        
    linhas.append("\n[FIM DO OVERRIDE DE DIRETRIZES DO PROFESSOR]\n")
    return "\n".join(linhas)
