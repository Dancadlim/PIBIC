import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from schemas import CadernoExerciciosValidado

def carregar_chave_api():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não encontrada no .env")

PROMPT_CRIADOR_EXERCICIOS = """
Você é um Professor Titular e elaborador chefe de exames (Banca Examinadora) em uma universidade de ponta.
Sua missão é ler o conteúdo de uma aula recém-criada e elaborar um caderno de exercícios rigoroso, desafiador e perfeitamente alinhado ao material didático.

[CONTEXTO DA AULA]
{conteudo_aula}

[DIRETRIZES PARA OS EXERCÍCIOS]
1. As questões de múltipla escolha devem apresentar cenários práticos (aplicação da teoria) em vez de apenas memorização de fórmulas.
2. Cada questão fechada deve ter uma "dica" estratégica e um "gabarito_comentado" extenso e detalhado.
3. As questões discursivas (abertas) devem ser complexas, exigindo cálculos em múltiplas etapas ou deduções baseadas na teoria ensinada.
4. O gabarito das questões discursivas DEVE ser passo a passo e utilizar formatação matemática rigorosa (LaTeX) quando houver cálculo.
5. Assegure que não há ambiguidades nas alternativas e que a alternativa correta seja matematicamente inquestionável.
"""

def gerar_caderno_exercicios(conteudo_aula_json: dict) -> dict:
    """
    Recebe a aula unificada e lapidada e gera o Caderno de Exercícios correspondente,
    garantindo a saída como um dicionário JSON compatível com o schema CadernoExerciciosValidado.
    """
    carregar_chave_api()
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "vertex-key.json")
    client = genai.Client(vertexai=True, project="plataformas-aulas-ufba", location="us-central1")
    
    # Reduzindo o conteúdo apenas para os textos essenciais para economizar tokens
    resumo_aula = f"Tema: {conteudo_aula_json.get('tema_global', 'Aula')}\n"
    for idx, pag in enumerate(conteudo_aula_json.get("paginas_conteudo", [])):
        resumo_aula += f"\n--- Tópico {idx+1}: {pag.get('titulo_subtopico')} ---\n"
        resumo_aula += f"{pag.get('discussao_teorica_prosa', '')[:1000]}...\n" # pega um pedaço do conceito para balizar o modelo
        resumo_aula += f"Fórmula principal: {pag.get('formalismo_latex', 'N/A')}\n"

    prompt = PROMPT_CRIADOR_EXERCICIOS.format(conteudo_aula=resumo_aula)
    
    print(f"\n[Agente de Exercícios] Elaborando caderno de exercícios para '{conteudo_aula_json.get('tema_global', 'Aula')}'...")
    
    try:
        resposta = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json",
                response_schema=CadernoExerciciosValidado
            )
        )
        
        caderno_dict = json.loads(resposta.text)
        print(" [OK] Caderno de Exercícios gerado com sucesso!")
        return caderno_dict
        
    except Exception as e:
        print(f" [ERRO] Falha ao gerar caderno de exercícios: {e}")
        return None

if __name__ == "__main__":
    # Teste rápido
    dummy_aula = {
        "tema_global": "Introdução à Probabilidade",
        "paginas_conteudo": [
            {
                "titulo_subtopico": "Conceitos Básicos",
                "discussao_teorica_prosa": "A probabilidade mede a chance de um evento...",
                "formalismo_latex": "P(A) = \\frac{n(A)}{n(\\Omega)}"
            }
        ]
    }
    resultado = gerar_caderno_exercicios(dummy_aula)
    if resultado:
        print("Múltipla Escolha geradas:", len(resultado.get("questoes_multipla_escolha", [])))
        print("Abertas geradas:", len(resultado.get("questoes_discursivas", [])))
