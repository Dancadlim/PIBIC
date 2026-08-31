import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

def carregar_chave_api():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

PROMPT_ENGENHEIRO_SIMULACAO = """
Você é um Engenheiro de Frontend Sênior especializado em Data Visualization e interfaces educacionais altamente responsivas.
Sua missão é criar uma simulação interativa baseada em tecnologias web nativas (HTML, Tailwind CSS via CDN, Javascript) e bibliotecas de gráficos (Plotly.js via CDN).

[CONTEXTO DA AULA]
Tema Geral da Aula: {tema_aula}
Simulação Solicitada: {nome_simulador}

[DIRETRIZES DE ARQUITETURA E LAYOUT VERTICAL - CRÍTICO]
1. HIERARQUIA DE ELEMENTOS (DISPOSIÇÃO VERTICAL):
   - A página DEVE ser estruturada de cima para baixo na seguinte ordem:
     a) CABEÇALHO: Título e subtítulo em HTML no topo (`<h2 class="text-xl font-bold text-slate-800">{nome_simulador}</h2>`).
     b) PAINEL DE CONTROLES: Sliders (`<input type="range">`) agrupados em um card com Tailwind CSS no topo/centro.
     c) CONTAINER DO GRÁFICO (LARGURA TOTAL 100%): O gráfico DEVE ficar em seu próprio bloco de largura total (`w-full`), ABAIXO dos controles. É PROIBIDO colocar a div do gráfico dentro de uma coluna de grid ao lado de sliders, pois em dispositivos móveis isso empurra ou oculta o gráfico.
     d) RODAPÉ / CARD EXPLICATIVO (OPCIONAL): Breve explicação ao final.

2. ALTURA E VISIBILIDADE DO GRÁFICO (MANDATÓRIO):
   - A div do gráfico DEVE ter estilo inline com largura e altura explícitas para NUNCA colapsar para 0px:
     `<div id="grafico" class="w-full my-4" style="width: 100%; min-height: 420px; height: 450px;"></div>`
   - NO JS DO PLOTLY: Mantenha o título interno VAZIO (`title: {{ text: '' }}` ou omitido).
   - Configure margens limpas e legenda horizontal abaixo:
     `margin: {{ t: 20, b: 60, l: 50, r: 30 }}, autosize: true, legend: {{ orientation: 'h', x: 0.5, xanchor: 'center', y: -0.2 }}`
   - Ative responsividade: `Plotly.newPlot('grafico', data, layout, {{ responsive: true, displayModeBar: false }});`

3. INICIALIZAÇÃO IMEDIATA E NOTIFICAÇÃO DE REDIMENSIONAMENTO:
   - Conecte o evento `input` dos sliders à função de re-renderização (`Plotly.react('grafico', ...)`).
   - Ao final do script, execute a função de renderização IMEDIATAMENTE (sem depender apenas de eventos que já possam ter disparado).
   - Sempre que renderizar ou atualizar o gráfico, envie mensagem de redimensionamento para a página pai:
     `if (window.parent) {{ window.parent.postMessage({{ type: 'resize', height: document.body.scrollHeight + 40 }}, '*'); }}`

[CÓDIGO DE PARTIDA ESPERADO]
Retorne APENAS um documento HTML completo e válido (começando com <!DOCTYPE html> e terminando com </html>). É PROIBIDO usar marcadores de markdown (como ```html).

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
</head>
<body class="bg-slate-50 p-4 md:p-6 font-sans">
  <div class="max-w-4xl mx-auto bg-white rounded-2xl p-6 shadow-sm border border-slate-200 space-y-6">
    <div class="text-center">
      <h2 class="text-xl font-bold text-slate-800 mb-1">{nome_simulador}</h2>
      <p class="text-xs text-slate-500">Laboratório Interativo Virtual | {tema_aula}</p>
    </div>
    
    <!-- Painel de Controles no topo -->
    <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
      <!-- Sliders aqui -->
    </div>

    <!-- Div do Gráfico ocupando 100% da largura -->
    <div id="grafico" class="w-full" style="width: 100%; min-height: 420px; height: 450px;"></div>
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
    
    from gemini_retry import executar_chamada_com_retry

    try:
        if logger:
            logger.update_agent("simulador", "rodando", prompt=prompt)
            logger.log("Agente Simulador: Programando a interface...", "info")
        
        def chamar_simulador():
            return client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="text/plain"
                )
            )

        resposta = executar_chamada_com_retry(
            chamar_simulador,
            max_retries=5,
            logger=logger,
            nome_agente="Simulador",
            descricao=f"geração do simulador '{nome_simulador}'"
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
        msg_erro = f"Falha definitiva de gerar simulador '{nome_simulador}': {str(e)}"
        print(f" [ERRO] {msg_erro}")
        if logger:
            logger.update_agent("simulador", "erro")
            logger.log(f"Agente Simulador: Falha - {msg_erro}", "error")
        return f"<div class='p-4 text-red-500'>Erro ao gerar a simulação após várias tentativas.</div>"


if __name__ == "__main__":
    # Teste rápido
    html = gerar_simulador_html("Distribuição Normal", "Impacto da Variância na Curva de Gauss")
    print("\nCódigo Gerado (primeiros 500 chars):")
    print(html[:500])
