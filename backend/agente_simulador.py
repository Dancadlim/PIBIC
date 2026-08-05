import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

def carregar_chave_api():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não encontrada no .env")

PROMPT_ENGENHEIRO_SIMULACAO = """
Você é um Engenheiro de Frontend Sênior especializado em Data Visualization e interatividade educacional.
Sua missão é criar uma simulação interativa baseada em tecnologias web nativas (HTML, Tailwind CSS via CDN, Javascript) e bibliotecas de gráficos (Plotly.js ou Chart.js via CDN).

[CONTEXTO]
O aluno está estudando: {tema_aula}
Subtópico específico: {nome_simulador}

[DIRETRIZES TÉCNICAS MANDATÓRIAS]
1. Retorne APENAS um bloco de código HTML válido (começando com <!DOCTYPE html> e terminando com </html>). Proibido markdown adicional (```html).
2. O design deve ser moderno, usando Tailwind CSS para estilização das barras deslizantes (sliders), botões e painéis.
3. A interatividade é crucial: deve haver sliders (ex: tamanho da amostra, variância, nível de confiança) que, quando movidos, atualizem o gráfico instantaneamente no Javascript.
4. O gráfico deve ser bonito, usando paletas de cores institucionais (azuis, indigos, slates).
5. Inclua pequenas caixas de texto ou tooltips que expliquem o que está acontecendo matematicamente quando o parâmetro muda.

[CÓDIGO DE PARTIDA ESPERADO]
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
</head>
<body class="bg-slate-50 p-6 rounded-xl font-sans">
  ... (Seu painel de controle interativo e div do gráfico) ...
</body>
</html>
"""

def gerar_simulador_html(tema_aula: str, nome_simulador: str) -> str:
    """
    Gera um código HTML/JS completo para uma simulação interativa usando Gemini Pro.
    """
    carregar_chave_api()
    client = genai.Client(vertexai=True, api_key=os.environ.get("GEMINI_API_KEY"))
    
    prompt = PROMPT_ENGENHEIRO_SIMULACAO.format(
        tema_aula=tema_aula,
        nome_simulador=nome_simulador
    )
    
    print(f"\n[Agente Simulador] Gerando simulação interativa para '{nome_simulador}' com Gemini Pro...")
    
    try:
        # AQUI USAMOS O PRO PARA TAREFAS COMPLEXAS DE PROGRAMAÇÃO/RACIOCÍNIO COMO PEDIDO PELO USUÁRIO
        resposta = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="text/plain"
            )
        )
        
        codigo_html = resposta.text.strip()
        
        # Limpar crases de markdown se o modelo desobedecer
        if codigo_html.startswith("```html"):
            codigo_html = codigo_html[7:]
        if codigo_html.startswith("```"):
            codigo_html = codigo_html[3:]
        if codigo_html.endswith("```"):
            codigo_html = codigo_html[:-3]
            
        print(" [OK] Simulador gerado com sucesso!")
        return codigo_html.strip()
        
    except Exception as e:
        print(f" [ERRO] Falha ao gerar simulador: {e}")
        return f"<div class='p-4 text-red-500'>Erro ao gerar a simulação: {e}</div>"

if __name__ == "__main__":
    # Teste rápido
    html = gerar_simulador_html("Distribuição Normal", "Impacto da Variância na Curva de Gauss")
    print("\nCódigo Gerado (primeiros 500 chars):")
    print(html[:500])
