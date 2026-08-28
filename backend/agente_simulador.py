import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

def carregar_chave_api():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

PROMPT_ENGENHEIRO_SIMULACAO = """
Você é um Engenheiro de Frontend Sênior especializado em Data Visualization e interatividade educacional.
Sua missão é criar uma simulação interativa baseada em tecnologias web nativas (HTML, Tailwind CSS via CDN, Javascript) e bibliotecas de gráficos (Plotly.js ou Chart.js via CDN).

[CONTEXTO DA AULA]
Tema Geral da Aula: {tema_aula}
Simulação Solicitada: {nome_simulador}

[DIRETRIZES DE LAYOUT E EVITAÇÃO DE SOBREPOSIÇÃO - CRÍTICO]
1. TÍTULO HIERÁRQUICO FORA DO GRÁFICO (PROIBIDO SOBREPOSIÇÃO):
   - O título principal da simulação DEVE ser colocado em HTML puro, ACIMA do container do gráfico (ex: `<div class="text-center mb-4"><h3 class="text-lg font-bold text-slate-800">{nome_simulador}</h3><p class="text-xs text-slate-500">Ajuste os parâmetros abaixo para observar a convergência em tempo real</p></div>`).
   - NO JS DO PLOTLY / CHART.JS: Mantenha o título interno do gráfico VAZIO (`title: {{ text: '' }}` ou omitido). NUNCA insira texto no `title` do Plotly, pois ele sobrepõe a legenda e o eixo Y.

2. POSICIONAMENTO DA LEGENDA E MARGENS:
   - A legenda do gráfico DEVE ficar obrigatoriamente ABAIXO da área plotada.
   - No Plotly.js, configure a legenda com:
     `legend: {{ orientation: 'h', x: 0.5, xanchor: 'center', y: -0.25 }}`
   - Configure margens limpas no Plotly layout:
     `margin: {{ t: 25, b: 65, l: 60, r: 35 }}`
   - No Plotly.newPlot, ative a responsividade: `Plotly.newPlot('divId', data, layout, {{ responsive: true, displayModeBar: false }})`.

3. PAINEL DE CONTROLES E SLIDERS INTERATIVOS:
   - Crie sliders (input type="range") e botões elegantes estilizados com Tailwind CSS.
   - Exiba o valor numérico atual ao lado de cada slider (ex: `<span id="val-n" class="font-bold text-blue-600 font-mono">100</span>`).
   - Conecte o evento `oninput` para atualizar os dados e re-plotar instantaneamente no JS (`Plotly.react` ou `chart.update()`).

4. CARD EXPLICATIVO MATEMÁTICO:
   - Inclua um card explicativo ao rodapé da página contextualizando os resultados matemáticos de {tema_aula}.

[CÓDIGO DE PARTIDA ESPERADO]
Retorne APENAS um documento HTML completo e válido (começando com <!DOCTYPE html> e terminando com </html>). É PROIBIDO usar marcadores de markdown (como ```html).

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
</head>
<body class="bg-slate-50 p-6 font-sans">
  <div class="max-w-4xl mx-auto bg-white rounded-2xl p-6 shadow-sm border border-slate-200 space-y-6">
    <div class="text-center">
      <h2 class="text-xl font-bold text-slate-800 mb-1">{nome_simulador}</h2>
      <p class="text-xs text-slate-500">Laboratório Interativo Virtual | {tema_aula}</p>
    </div>
    <!-- Seu painel de controle e div do gráfico -->
  </div>
</body>
</html>
"""

def sanitizar_layout_grafico(html_code: str) -> str:
    """
    Higieniza o código HTML para garantir que títulos do Plotly/Chart.js não fiquem sobrepostos à legenda.
    """
    import re
    if "Plotly.newPlot" in html_code or "Plotly.react" in html_code:
        # Garante que title.text no Plotly fique vazio para evitar colisão visual
        html_code = re.sub(r'title\s*:\s*\{[^}]*text\s*:\s*["\'][^"\']+["\'][^}]*\}', 'title: { text: "" }', html_code)
        html_code = re.sub(r'title\s*:\s*["\'][^"\']+["\']', 'title: ""', html_code)
    return html_code

def gerar_simulador_html(tema_aula: str, nome_simulador: str, logger=None) -> str:
    """
    Gera um código HTML/JS completo para uma simulação interativa usando Gemini Pro.
    """
    carregar_chave_api()
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "vertex-key.json")
    client = genai.Client(vertexai=True, location="us-central1")
    
    prompt = PROMPT_ENGENHEIRO_SIMULACAO.format(
        tema_aula=tema_aula,
        nome_simulador=nome_simulador
    )
    
    print(f"\n[Agente Simulador] Gerando simulação interativa para '{nome_simulador}' com Gemini Pro...")
    
    import time
    max_retries = 10
    
    for tentativa in range(max_retries):
        try:
            if logger and tentativa == 0:
                logger.update_agent("simulador", "rodando", prompt=prompt)
                logger.log("Agente Simulador: Programando a interface...", "info")
            
            resposta = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="text/plain"
                )
            )
            
            codigo_html = resposta.text.strip()
            
            import re
            
            # Limpar crases de markdown se o modelo desobedecer e extrair apenas o código
            match = re.search(r"```(?:html)?\s*(.*?)\s*```", codigo_html, re.DOTALL | re.IGNORECASE)
            if match:
                codigo_html = match.group(1)
                
            codigo_html = sanitizar_layout_grafico(codigo_html.strip())
            if logger:
                logger.update_agent("simulador", "concluido", resposta=codigo_html)
                logger.log("Agente Simulador: Concluído com sucesso!", "success")
            print(" [OK] Simulador gerado e higienizado com sucesso!")
            return codigo_html
            
        except Exception as e:
            msg_erro = f"Falha na tentativa {tentativa + 1} de gerar simulador: {str(e)}"
            print(f" [AVISO] {msg_erro}")
            if logger:
                logger.log(f"Agente Simulador: Aviso - {msg_erro}", "warning")
            time.sleep(5)
            
    # Se esgotar as tentativas
    if logger:
        logger.update_agent("simulador", "erro")
        logger.log("Agente Simulador: Falha definitiva após várias tentativas.", "error")
    return f"<div class='p-4 text-red-500'>Erro ao gerar a simulação após várias tentativas.</div>"


if __name__ == "__main__":
    # Teste rápido
    html = gerar_simulador_html("Distribuição Normal", "Impacto da Variância na Curva de Gauss")
    print("\nCódigo Gerado (primeiros 500 chars):")
    print(html[:500])
