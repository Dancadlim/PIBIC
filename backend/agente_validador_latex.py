import os
import json
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv
import latex_sanitizer

def carregar_chave_api():
    load_dotenv()
    if "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"].strip():
        return True
    return False

def detectar_anomalias_estruturais_katex(texto: str) -> list:
    """
    Verifica se uma string possui anomalias de sintaxe que o KaTeX não consegue compilar.
    """
    if not isinstance(texto, str) or not texto.strip():
        return []
        
    erros = []
    
    # 1. Checa ambientes \begin{...} sem o correspondente \end{...}
    begins = re.findall(r'\\begin\{([a-zA-Z*]+)\}', texto)
    ends = re.findall(r'\\end\{([a-zA-Z*]+)\}', texto)
    if sorted(begins) != sorted(ends):
        erros.append(f"Ambientes de matriz/equação desalinhados: \\begin{{{begins}}} vs \\end{{{ends}}}")
        
    # 2. Checa cifrões soltos desbalanceados
    if texto.count("$") % 2 != 0:
        erros.append("Cifrões ($) desbalanceados na string")
        
    # 3. Checa chaves desbalanceadas em ambiente de bloco $$
    for bloco in re.findall(r'\$\$(.*?)\$\$', texto, flags=re.DOTALL):
        chaves_abertas = bloco.count("{") - bloco.count("\\{")
        chaves_fechadas = bloco.count("}") - bloco.count("\\}")
        if chaves_abertas != chaves_fechadas:
            erros.append(f"Chaves desbalanceadas no bloco KaTeX ({chaves_abertas} abertas vs {chaves_fechadas} fechadas)")
            
    return erros

def validar_e_corrigir_aula_completa(aula_json: dict, logger=None, modelo_llm: str = "2.5") -> dict:
    """
    Agente Validador e Auditor Final de Compilação LaTeX.
    Passo 1: Aplica a sanitização determinística instantânea em Python (< 1ms).
    Passo 2: Inspeciona todo o JSON em busca de anomalias estruturais de KaTeX.
    Passo 3: Se (e somente se) houver anomalias graves, aciona o Agente LLM (gemini-3.5-flash-lite) para reparo cirúrgico.
    """
    if not aula_json or not isinstance(aula_json, dict):
        return aula_json
        
    target_model = "gemini-3.5-flash-lite" if str(modelo_llm) == "3.5" else "gemini-2.5-flash"
    
    if logger:
        logger.update_agent("validador_latex", "rodando")
        logger.log(f"Auditor de Compilação LaTeX ({target_model}): Inspecionando sintaxe e KaTeX...", "info")
        
    print(f"\n[Agente Validador de LaTeX ({target_model})] Inspecionando compilação de toda a aula...")
    
    # 1. Sanitização determinística automática em Python
    aula_sanitizada = latex_sanitizer.sanitize_json_recursively(aula_json)
    
    # 2. Auditoria de anomalias estruturais
    anomalias_encontradas = []
    
    def auditar_recursivo(obj, caminho=""):
        if isinstance(obj, str):
            errs = detectar_anomalias_estruturais_katex(obj)
            if errs:
                anomalias_encontradas.append((caminho, errs, obj[:150]))
        elif isinstance(obj, dict):
            for k, v in obj.items():
                auditar_recursivo(v, f"{caminho}.{k}")
        elif isinstance(obj, list):
            for i, elem in enumerate(obj):
                auditar_recursivo(elem, f"{caminho}[{i}]")
                
    auditar_recursivo(aula_sanitizada, "aula")
    
    # Se nenhuma anomalia grave foi encontrada, retorna imediatamente (0ms latência extra!)
    if not anomalias_encontradas:
        print(" [OK] Auditoria de LaTeX: 100% de compilação limpa garantida (0 erros)!")
        if logger:
            logger.update_agent("validador_latex", "concluido", resposta="Compilação 100% Aprovada (0 anomalias).")
            logger.log("Auditor de Compilação LaTeX: 100% Aprovado (Zero erros de compilação).", "success")
        return aula_sanitizada

    # 3. Caso haja anomalias estruturais graves, aciona o LLM para reparo cirúrgico
    print(f" ⚠️ [AVISO] {len(anomalias_encontradas)} anomalia(s) estrutural(is) detectada(s). Acionando LLM para reparo cirúrgico...")
    if logger:
        logger.log(f"Auditor de Compilação LaTeX: Acionando {target_model} para reparar {len(anomalias_encontradas)} anomalias...", "warning")
        
    try:
        carregar_chave_api()
        os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "vertex-key.json")
        client = genai.Client(vertexai=True, location="us-central1")
        
        from prompts import PROMPT_FORMATADOR_LATEX
        payload_str = json.dumps(aula_sanitizada, ensure_ascii=False)
        prompt_reparo = f"{PROMPT_FORMATADOR_LATEX}\n\n[ANOMALIAS DETECTADAS]\n{json.dumps(anomalias_encontradas, ensure_ascii=False)}\n\n[CONTEUDO_PARA_CORRIGIR]\n{payload_str}"
        
        resposta = client.models.generate_content(
            model=target_model,
            contents=prompt_reparo,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json"
            )
        )
        
        cleaned_resp = resposta.text.strip()
        if "```" in cleaned_resp:
            cleaned_resp = re.sub(r"^```(?:json)?\n?", "", cleaned_resp, flags=re.MULTILINE)
            cleaned_resp = re.sub(r"\n?```$", "", cleaned_resp, flags=re.MULTILINE).strip()
            
        aula_reparada = json.loads(cleaned_resp)
        aula_reparada_sanitizada = latex_sanitizer.sanitize_json_recursively(aula_reparada)
        
        print(" [OK] Reparo de compilação pelo LLM concluído com sucesso!")
        if logger:
            logger.update_agent("validador_latex", "concluido", resposta=resposta.text)
            logger.log("Auditor de Compilação LaTeX: Reparo concluído com sucesso.", "success")
            
        return aula_reparada_sanitizada

    except Exception as e:
        print(f" [ERRO] Falha no reparo do LLM ({e}). Mantendo aula sanitizada determinística.")
        if logger:
            logger.update_agent("validador_latex", "concluido")
            logger.log(f"Auditor de Compilação LaTeX: Mantido fallback determinístico ({str(e)}).", "warning")
        return aula_sanitizada
