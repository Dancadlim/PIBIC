import os
import sys
import json
import re
import time
from google import genai
from google.genai import types

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

# Inicializa o carregamento da chave de API no escopo do módulo
carregar_chave_api()

# ==============================================================================
def programar_fatia_teoria(dados_subtopico: dict, nome_simulador: str, motor_grafico: str = "plotly", chave_suffix: str = "", cor_principal: str = "#1E3A8A", cor_critica: str = "#991B1B", cor_secundaria: str = "#10B981", cor_alerta: str = "#F59E0B") -> str:
    # Garante a inicialização da chave
    carregar_chave_api()
    client = genai.Client()
    
    if motor_grafico.lower() == "seaborn":
        grafico_especifico = f"""Crie um gráfico Seaborn/Matplotlib premium altamente científico e estilizado. 
        Configure o tema usando `sns.set_theme(style="whitegrid", rc={{"grid.linestyle": "--", "grid.alpha": 0.5, "grid.color": "#E2E8F0", "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"]}})` e use a fonte 'sans-serif'.
        Use `fig, ax = plt.subplots(figsize=(10, 5), dpi=300)` e configure as cores de fundo `fig.patch.set_facecolor('#FFFFFF')` e `ax.set_facecolor('#FFFFFF')`. Garanta a remoção de bordas com `sns.despine(left=True, bottom=False, right=True, top=True)`.
        Assegure que as cores usadas sigam a paleta estrita: PRIMARY_BLUE = "{cor_principal}", SECONDARY_GREEN = "{cor_secundaria}", WARNING_AMBER = "{cor_alerta}", CRITICAL_RED = "{cor_critica}", LIGHT_SLATE = "#F8FAFC", GRID_GRAY = "#E2E8F0", TEXT_MAIN = "#1E293B", TEXT_MUTED = "#64748B".
        Use títulos de eixos e título principal formatados com tamanho de fonte estrito: título 14 (negrito, TEXT_MAIN), eixos 11 (TEXT_MAIN), ticks 9 (TEXT_MUTED) e legenda 9 (TEXT_MUTED) em fundo LIGHT_SLATE com borda GRID_GRAY.
        Renderize no Streamlit usando `st.pyplot(fig)`. Libere a memória no final chamando `plt.close(fig)`."""
    else:
        grafico_especifico = f"""Crie um gráfico Plotly premium altamente interativo e condizente com a proposta. 
        Configure o gráfico com as seguintes diretrizes estritas de layout de forma absoluta:
        - `template="plotly_white"`
        - `height=420`
        - `margin=dict(l=55, r=30, t=65, b=55, pad=4)`
        - Fundo do plot (`plot_bgcolor`) e do papel (`paper_bgcolor`) brancos ou transparentes. Nunca use fundos pretos ou coloridos.
        - Título com tag HTML `<b>` e fonte de tamanho 14, cor "#1E293B", família "Arial, sans-serif", alinhado à esquerda: `title=dict(text="<b>Título Estruturado</b>", font=dict(size=14, color="#1E293B", family="Arial, sans-serif"), x=0.0, y=0.95)`.
        - Eixos 2D configurados with `fixedrange=True` para estabilidade mobile nas propriedades de `xaxis` e `yaxis`. Se for gráfico 3D, nunca use `fixedrange` em scene, xaxis, yaxis ou zaxis.
        - Eixos configurados exatamente neste formato: `xaxis=dict(title=dict(text="Texto", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")), tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"), gridcolor="#E2E8F0", zerolinecolor="#CBD5E1", fixedrange=True)`. NUNCA use 'titlefont' ou 'title_font' diretamente no dicionário do eixo.
        - Legenda horizontal no topo do gráfico para economizar espaço e evitar desalinhamento: `legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0, font=dict(size=9, color="#64748B", family="Arial, sans-serif"), bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="#E2E8F0", borderwidth=1)`.
        - Caixa de dica flutuante (hoverlabel) customizada: `hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_color="#1E293B", font_family="Arial, sans-serif")`.
        - Assegure que as cores usadas sigam a paleta estrita de cores: PRIMARY_BLUE = "{cor_principal}", SECONDARY_GREEN = "{cor_secundaria}", WARNING_AMBER = "{cor_alerta}", CRITICAL_RED = "{cor_critica}", LIGHT_SLATE = "#F8FAFC", GRID_GRAY = "#E2E8F0", TEXT_MAIN = "#1E293B", TEXT_MUTED = "#64748B".
        - Renderize no Streamlit usando `st.plotly_chart(fig, use_container_width=True, key=r"plotly_chart_{chave_suffix}")`."""

    prompt = f"""
    Você é um UI/UX Designer Frontend especialista em Streamlit para Educação Executiva.
    Sua missão é ler o JSON do subtópico, pegar a prosa densa recebida e criar um layout de livro acadêmico de luxo com um "ritmo de leitura" dinâmico e elegante.
    
    O código que você gerar será injetado diretamente dentro do bloco 'with tab_conteudo:' do script principal.
    
    CRÍTICO - CÓDIGO 100% ESTÁTICO E HARDCODED (TOLERÂNCIA ZERO PARA AVALIAÇÕES DINÂMICAS OU LOOPS EM TEMPO DE EXECUÇÃO):
    É TERMINANTEMENTE PROIBIDO gerar código Python que faça referências ou tente ler variáveis, parâmetros ou dicionários dinâmicos (como tentar acessar `data`, `dados_subtopico`, `pagina`, `exemplo`, `passo` em tempo de execução no script gerado).
    Toda prosa teórica, títulos, equações matemáticas, exemplos práticos e laudos contidos no JSON recebido devem ser extraídos durante a geração e escritos diretamente como **strings literais estáticas (hardcoded)** usando o prefixo 'r' (raw string) no código Streamlit gerado.
    
    Se houver listas de exemplos (`exemplos_praticos_ricos`) ou deduções (`deducao_analitica_linhas`), você deve iterar sobre elas durantes a geração do código e gerar fisicamente blocos de código estáticos sequenciais para cada item individualmente na string de saída (por exemplo, gerando múltiplos blocos `with st.container(border=True):` estáticos com os textos reais já escritos por extenso no código Python, sem loops `for` no script final).
    
    DIRETRIZES OBRIGATÓRIAS DE LAYOUT (RITMO E QUEBRA DE TEXTO):
    1. PARCELAMENTO DE TEXTO: Nunca exiba mais de 2 parágrafos corridos seguidos. Quebre a monotonia do texto transformando explicações sequenciais, propriedades ou pressupostos em listas de tópicos (bullet points) limpas.
    2. BLOCOS COLORIDOS DE DESTAQUE: 
       - Use as classes HTML/CSS injetadas no topo do script para envelopar partes do texto.
       - Fragmentos teóricos muito complexos ou intuições devem entrar dentro de caixas usando os estilos customizados ou os componentes nativos (`st.info(r"...")`, `st.warning(r"...")`, `st.error(r"...")`, `st.success(r"...")`).
       - ATENÇÃO: Os componentes `st.info()`, `st.warning()`, `st.error()` e `st.success()` são chamadas de função diretas. É TERMINANTEMENTE PROIBIDO utilizá-los com a palavra-chave 'with' (ex: NUNCA faça 'with st.info(r"..."):'). Use-os apenas como chamadas diretas normais.
    3. CONTAINER PARA EXEMPLOS RESOLVIDOS: Cada exemplo prático da lista DEVE ser isolado visualmente dentro de um `with st.container(border=True):`. Use títulos em markdown bem definidos (ex: "##### 📖 Exemplo Prático: ...") e use `st.success()` ou um bloco destacado para a conclusão/laudo comercial do exemplo.
    4. FORMALISMO MATEMÁTICO: Centralize e destaque todas as equações principais em blocos de `st.latex(r"...")`.
    5. TABELAS E DATAFRAMES ESTILIZADOS (RITMO E ESTRUTURA): Sempre que o JSON contiver dados formatados como tabelas Markdown (ou estruturas comparativas/descritivas de dados), você deve convertê-los e renderizá-los como tabelas Streamlit nativas premium (`st.dataframe` ou `st.table`) criadas dinamicamente com Pandas (`pd.DataFrame`). Nunca exiba dados tabulares estruturados como puro texto corrido sem necessidade.
    
    REGRAS ESTRITAS DE INTERFACE (TOLERÂNCIA ZERO PARA NOMES DE SEÇÕES GENÉRICOS):
    - É terminantemente proibido utilizar títulos de seções genéricos como 'Exemplos Práticos', 'Demonstração Analítica e Propriedades' ou 'Formalismo Matemático'.
    - Todos os cabeçalhos de seções (`st.subheader`, `st.markdown("### ...")`) devem ser contextualizados dinamicamente com o tema específico do subtópico (Exemplo: em vez de 'Demonstração Analítica e Propriedades', use '### 📐 O Coração Matemático: [Nome do Subtópico]'; em vez de 'Exemplos Práticos', use '### 📈 Casos de Aplicação Prática: [Nome do Subtópico]').
    
    1. CABEÇALHO DO SUBTÓPICO: Crie o cabeçalho usando `st.header(r"[Título do Subtópico literal e estático]")` (NUNCA acesse dinamicamente variáveis como `data["titulo_subtopico"]`).
    
    2. DEMONSTRAÇÃO FORA DO EXPANDER: É terminantemente proibido colocar as deduções matemáticas em expanders. Exiba cada linha contida no campo 'deducao_analitica_linhas' de forma estática sequencialmente usando `st.latex(r"...")` uma abaixo da outra, intercaladas por pequenas frases explicativas que conectem os passos logicamente.
    
    3. CARDS DE EXEMPLOS RESOLVIDOS: Para cada item da lista 'exemplos_praticos_ricos', monte uma seção estruturada contínua física utilizando um container com borda:
       with st.container(border=True):
           st.markdown(r"##### 📖 Exemplo Resolvido: [Título do Exemplo]")
           st.markdown(r"[Enunciado literal e estático do exemplo]")
           st.latex(r"[Dados sumarizados literais e estáticos em LaTeX]")
           st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
           st.markdown(r"- [Passo 1 literal e estático]")
           st.markdown(r"- [Passo 2 literal e estático]")
           st.success(r"[Conclusão e laudo comercial literal e estático]")
            
    4. GRÁFICOS NO MEIO DO TEXTO: Se o parâmetro 'nome_simulador' for fornecido (não vazio), insira os sliders e o gráfico correspondente a esse conceito (utilizando a biblioteca '{motor_grafico}') imediatamente após o bloco de formalismo matemático (`st.info` / `st.latex`), dividindo as variáveis em colunas elegantes (`st.columns`) para que os seletores/sliders não fiquem gigantes na tela.
       O simulador a ser programado é: '{nome_simulador}'.
       {grafico_especifico}
       Use chaves únicas que terminem obrigatoriamente com o sufixo '_{chave_suffix}' para todos os widgets e sliders do Streamlit para evitar DuplicateWidgetID.
        
    5. TRATAMENTO DE LATEX E BARRAS INVERTIDAS: Use raw strings (prefixadas por 'r', ex: st.write(r"...") ou st.markdown(r"...")) em absolutamente todos os componentes markdown e latex para evitar SyntaxWarnings ou quebras de renderização no Streamlit. NUNCA use f-strings dinâmicas combinadas com chaves matemáticas (como rf"...") pois isso quebra a sintaxe do Python.
     
    6. PROIBIÇÃO DE SCIKIT-LEARN: É terminantemente proibido importar, utilizar ou depender de `sklearn` ou `scikit-learn` no código gerado. Para qualquer cálculo estatístico ou ajuste de regressão linear nos simuladores, utilize `scipy.stats` (como `stats.linregress`) ou álgebra linear/cálculo manual com `numpy` (ambas já estão importadas no script pai).
    
    7. EVITAR TRIPLE QUOTES QUEBRADOS E CARACTERES ESCAPADOS INCORRETOS: Garanta que todas as strings de texto longas geradas em Python sejam raw strings válidas (ex: r\"\"\"texto\"\"\"). Se o texto contiver aspas triplas internas, substitua-as por aspas normais simples ou duplas. Não termine uma raw string com uma barra invertida (ex: r"texto\"), pois isso causa erro de sintaxe no compilador do Python (a barra invertida antes das aspas finais escapa as aspas, deixando a string aberta).
    
    8. COMPATIBILIDADE SINTÁTICA TOTAL: Seu código gerado DEVE ser código Python 3.12+ sintaticamente correto. Ele será analisado pelo parser AST do Python. Não inclua comentários fora de blocos válidos, nem códigos incompletos ou blocos interrompidos.
    
    9. Escreva o seu código iniciando no recuo base de 0 espaços. O orquestrador cuidará do alinhamento.
    
    Retorne APENAS o código Python puro dentro do bloco de marcação:
    ```python
    # Seu código aqui
    ```
    """
    
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high"),
        temperature=1.0
    )
    
    max_tentativas = 5
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=json.dumps(dados_subtopico, ensure_ascii=False)),
                types.Part.from_text(text=prompt)
            ]
        )
    ]
    
    ultimo_codigo = ""
    
    for tentativa in range(max_tentativas):
        try:
            resposta = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=contents,
                config=config
            )
            
            resposta_texto = resposta.text
            match = re.search(r"```python\s*(.*?)\s*```", resposta_texto, re.DOTALL)
            codigo_gerado = match.group(1).strip() if match else resposta_texto.strip()
            ultimo_codigo = codigo_gerado
            
            # Validação sintática e de execução mockada
            ok, erro_msg = validar_fatia(codigo_gerado)
            if ok:
                print(f"[OK] Fatia de teoria gerada e validada com sucesso na tentativa {tentativa+1}.")
                return codigo_gerado
            else:
                print(f"[AVISO] Tentativa {tentativa+1}/{max_tentativas} falhou na validação da fatia de teoria. Erro:\n{erro_msg}")
                
                # Prepara o prompt de autocorreção enviando o código incorreto e a mensagem de erro
                prompt_correcao = f"""[MENSAGEM DE ERRO NA VALIDAÇÃO]
O código Python gerado anteriormente falhou nos testes de compilação ou execução simulada com o seguinte erro:
---
{erro_msg}
---

Por favor, analise a mensagem de erro acima e corrija o código gerado.
Instruções de autocorreção:
1. NÃO use nem referencie variáveis ou dicionários dinâmicos em tempo de execução no script gerado (como tentar acessar 'dados_subtopico', 'pagina', 'exemplo', 'passo', 'data', etc.). Todo o conteúdo do JSON recebido na primeira mensagem deve ser escrito diretamente como strings literais estáticas (hardcoded) no código Streamlit final.
2. Certifique-se de que todas as strings de texto longas sejam raw strings válidas (ex: r"texto" ou r\"\"\"texto\"\"\").
3. NUNCA termine uma raw string com uma barra invertida (ex: r"texto\") para não quebrar a compilação do Python. Se precisar colocar uma barra invertida antes de aspas, use string normal ou escape-a corretamente.
4. NUNCA use 'with' com st.info, st.warning, st.error ou st.success. Chame-os diretamente: st.info(r"...")
5. O código gerado deve ser sintaticamente correto para o Python 3.12+.

Retorne APENAS o código Python corrigido completo dentro do bloco:
```python
# Seu código corrigido aqui
```"""
                # Registra o histórico da conversa
                contents.append(
                    types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=resposta_texto)]
                    )
                )
                contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=prompt_correcao)]
                    )
                )
                
                if tentativa < max_tentativas - 1:
                    tempo_espera = 1
                    print(f"[AVISO] Aguardando {tempo_espera}s antes de tentar autocorreção...")
                    time.sleep(tempo_espera)
        except Exception as e:
            print(f"[AVISO] Chamada da API falhou na tentativa {tentativa+1}/{max_tentativas} na fatia de teoria: {e}")
            if tentativa < max_tentativas - 1:
                tempo_espera = 2 ** tentativa
                print(f"[AVISO] Aguardando {tempo_espera}s antes de tentar novamente...")
                time.sleep(tempo_espera)
            else:
                print(f"[ERRO] Todas as {max_tentativas} tentativas falharam na fatia de teoria: {e}")
                return ultimo_codigo if ultimo_codigo else f"# Falha na geracao do subtopico apos {max_tentativas} tentativas: {e}"

    print(f"[ALERTA] Excedeu o número máximo de tentativas de autocorreção na fatia de teoria. Retornando o último código gerado.")
    return ultimo_codigo

# ==============================================================================
# FASE B: FUNÇÃO ESPECIALISTA EM PROCESSAR A FATIA DE EXERCÍCIOS
# ==============================================================================
def programar_fatia_exercicios(dados_exercicios: dict) -> str:
    carregar_chave_api()
    client = genai.Client()
    
    prompt = """
    Você é um Engenheiro de Software especialista em interfaces educacionais interativas no Streamlit.
    Sua tarefa é gerar o código Python/Streamlit interativo para renderizar a aba de exercícios da aula.
    
    O código gerado será injetado diretamente dentro do bloco 'with tab_exercicios:' do script principal.
    
    CRÍTICO - DESACOPLAMENTO DE DADOS (TOLERÂNCIA ZERO PARA TRANSCRIÇÃO OU HARDCODING DOS DADOS DO CADERNO):
    É TERMINANTEMENTE PROIBIDO transcrever, copiar ou escrever no código gerado os textos, enunciados, alternativas ou gabaritos das questões de forma estática (hardcoded). 
    Assuma que um dicionário chamado 'dados_exercicios' já foi carregado e está disponível no escopo atual. Este dicionário possui a seguinte estrutura de dados:
    {
        "topico_aula": "Tema",
        "questoes_multipla_escolha": [
            {
                "enunciado": "...",
                "alternativas": {"A": "...", "B": "...", ...},
                "alternativa_correta": "A",
                "dica": "...",
                "gabarito_comentado": "..."
            }
        ],
        "questoes_discursivas": [
            {
                "enunciado": "...",
                "dica": "...",
                "gabarito_passo_a_passo": ["Passo 1", "Passo 2", ...]
            }
        ]
    }
    
    REGRAS DE INTERATIVIDADE E SEGURANÇA CONTRA KEYERRORS:
    1. Crie uma interface interativa que itera dinamicamente sobre a lista 'dados_exercicios["questoes_multipla_escolha"]'.
       - Transcreva e monte as alternativas utilizando `st.radio()` com chaves únicas baseadas no índice da iteração (key=f"radio_mcq_{i}").
       - Crie um botão de dica usando a estrutura de acesso seguro: `st.info(questao.get("dica", "Dica indisponível"))` ativado por um `st.button()` com chave única.
       - Crie um botão de verificação: `if st.button("✅ Verificar Resposta", key=...):` que extrai a letra marcada pelo aluno e exibe `st.success("Correto! Muito bem.")` ou `st.error` com explicação a partir de questao.get("alternativa_correta").
       - Oculte o gabarito comentado dentro de um `st.expander("✅ Ver Gabarito Comentado")`. Você DEVE extrair as chaves do dicionário usando sempre o método seguro `.get("gabarito_comentado", "Gabarito indisponível")` para evitar KeyErrors.
    2. Crie uma interface para iterar sobre a lista 'dados_exercicios["questoes_discursivas"]'.
       - Crie um campo `st.text_area("Sua resposta:", key=...)`.
       - Renderize a dica de forma segura with `.get("dica", "Dica indisponível")` num botão de dica.
       - Oculte a resolução detalhada passo a passo dentro de um `st.expander("✅ Ver Resolução Detalhada")` iterando de forma segura sobre a lista obtida por `.get("gabarito_passo_a_passo", [])`.
    3. NÃO inclua importações globais ou redefinição de variáveis globais. O código deve iniciar no recuo de 0 espaços.
    
    4. SEGURANÇA SINTÁTICA E COMPATIBILIDADE SINTÁTICA TOTAL: Seu código gerado DEVE ser código Python 3.12+ sintaticamente correto. Nunca coloque aspas triplas dentro de outras aspas triplas sem escapar, e evite colocar barras invertidas no final de raw strings (ex: r"texto\"). Não inclua comentários soltos ou blocos incompletos.
    
    Retorne APENAS o código Python puro dentro do bloco:
    ```python
    # Seu código aqui
    ```
    """
    
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high"),
        temperature=1.0
    )
    
    max_tentativas = 5
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=json.dumps(dados_exercicios, ensure_ascii=False)),
                types.Part.from_text(text=prompt)
            ]
        )
    ]
    
    ultimo_codigo = ""
    
    for tentativa in range(max_tentativas):
        try:
            resposta = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=contents,
                config=config
            )
            
            resposta_texto = resposta.text
            match = re.search(r"```python\s*(.*?)\s*```", resposta_texto, re.DOTALL)
            codigo_gerado = match.group(1).strip() if match else resposta_texto.strip()
            ultimo_codigo = codigo_gerado
            
            # Validação (passando dados_exercicios nos globals mockados para evitar NameError)
            ok, erro_msg = validar_fatia(codigo_gerado, extra_globals={'dados_exercicios': dados_exercicios})
            if ok:
                print(f"[OK] Fatia de exercicios gerada e validada com sucesso na tentativa {tentativa+1}.")
                return codigo_gerado
            else:
                print(f"[AVISO] Tentativa {tentativa+1}/{max_tentativas} falhou na validação de código de exercicios. Erro:\n{erro_msg}")
                
                # Prepara o prompt de autocorreção
                prompt_correcao = f"""[MENSAGEM DE ERRO NA VALIDAÇÃO]
O código Python gerado anteriormente falhou nos testes de compilação ou execução simulada com o seguinte erro:
---
{erro_msg}
---

Por favor, analise a mensagem de erro acima e corrija o código gerado.
Instruções de autocorreção:
1. O dicionário de exercícios chamado 'dados_exercicios' já está disponível no escopo do Streamlit. Acesse os enunciados, dicas, alternativas e gabaritos dinamicamente a partir de 'dados_exercicios' (tolerância zero para hardcoding dos dados do caderno).
2. Acesse chaves do dicionário de forma segura utilizando .get() (ex: questao.get("dica", "...")).
3. Certifique-se de que todas as strings de texto longas sejam raw strings válidas.
4. NUNCA termine uma raw string com uma barra invertida (ex: r"texto\").
5. NUNCA use 'with' com st.info, st.warning, st.error ou st.success.
6. O código gerado deve ser sintaticamente correto para o Python 3.12+.

Retorne APENAS o código Python corrigido completo dentro do bloco:
```python
# Seu código corrigido aqui
```"""
                # Registra o histórico da conversa
                contents.append(
                    types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=resposta_texto)]
                    )
                )
                contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=prompt_correcao)]
                    )
                )
                
                if tentativa < max_tentativas - 1:
                    tempo_espera = 1
                    print(f"[AVISO] Aguardando {tempo_espera}s antes de tentar autocorreção...")
                    time.sleep(tempo_espera)
        except Exception as e:
            print(f"[AVISO] Chamada da API falhou na tentativa {tentativa+1}/{max_tentativas} na fatia de exercicios: {e}")
            if tentativa < max_tentativas - 1:
                tempo_espera = 2 ** tentativa
                print(f"[AVISO] Aguardando {tempo_espera}s antes de tentar novamente...")
                time.sleep(tempo_espera)
            else:
                print(f"[ERRO] Todas as {max_tentativas} tentativas falharam na fatia de exercicios: {e}")
                return ultimo_codigo if ultimo_codigo else f"# Falha na geracao de exercicios apos {max_tentativas} tentativas: {e}"

    print(f"[ALERTA] Excedeu o número máximo de tentativas de autocorreção na fatia de exercicios. Retornando o último código gerado.")
    return ultimo_codigo

def validar_sintaxe(codigo_python: str) -> tuple[bool, str]:
    """
    Verifica se o código possui erros de sintaxe sem executá-lo.
    Retorna (True, "") se estiver tudo ok, ou (False, "mensagem de erro") caso contrário.
    """
    import ast
    try:
        ast.parse(codigo_python)
        return True, ""
    except SyntaxError as se:
        erro_msg = f"SyntaxError na linha {se.lineno}, coluna {se.offset}: {se.msg}\nTrecho: {se.text}"
        return False, erro_msg
    except Exception as e:
        return False, f"Erro ao analisar sintaxe: {e}"

def validar_execucao_codigo(codigo_python: str, extra_globals: dict = None):
    """
    Tenta executar o código gerado em um ambiente mockado para detectar erros de runtime
    (como chamadas de layout inválidas no Plotly, erros de tipo, variáveis indefinidas, etc.)
    antes de salvar o arquivo no disco.
    """
    import numpy as np
    import pandas as pd
    import scipy.stats as stats
    from scipy.stats import norm
    import plotly.graph_objects as go
    import plotly.express as px
    import json
    import base64
    
    # 1. Definição do Mock de Streamlit e Valores em uma classe unificada robusta
    class MockStreamlitElement:
        def __init__(self, parent=None):
            self._parent = parent
            
        def __getattr__(self, name): 
            if name in ['__enter__', '__exit__']:
                raise AttributeError()
            
            def func(*args, **kwargs):
                key = kwargs.get('key')
                if self._parent:
                    self._parent._register_key(key)
                return MockStreamlitElement(self._parent)
            return func
            
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass
        def __call__(self, *args, **kwargs): return MockStreamlitElement(self._parent)
        def __iter__(self): return iter([MockStreamlitElement(self._parent), MockStreamlitElement(self._parent)])
        
        # Operações de string comuns (evita AttributeError quando a IA trata retorno de widget como string)
        def split(self, *args, **kwargs): return [self]
        def strip(self, *args, **kwargs): return self
        def lower(self, *args, **kwargs): return self
        def upper(self, *args, **kwargs): return self
        def replace(self, *args, **kwargs): return self
        def startswith(self, *args, **kwargs): return False
        def endswith(self, *args, **kwargs): return False
        
        # Operações matemáticas e operadores (evita erros ao tratar retorno de widget como número)
        def __add__(self, other): return self
        def __radd__(self, other): return self
        def __sub__(self, other): return self
        def __rsub__(self, other): return self
        def __mul__(self, other): return self
        def __rmul__(self, other): return self
        def __truediv__(self, other): return self
        def __rtruediv__(self, other): return self
        def __pow__(self, other): return self
        def __rpow__(self, other): return self
        def __neg__(self): return self
        def __pos__(self): return self
        def __abs__(self): return self
        def __getitem__(self, item): return self
        def __setitem__(self, key, value): pass
        def __len__(self): return 1
        def __lt__(self, other): return False
        def __le__(self, other): return False
        def __gt__(self, other): return False
        def __ge__(self, other): return False
        def __eq__(self, other): return True
        def __ne__(self, other): return False
        def __float__(self): return 1.0
        def __int__(self): return 1
        def __str__(self): return "1.0"

    class MockSessionState:
        def __getattr__(self, name): return MockStreamlitElement()
        def __setattr__(self, name, value): pass
        def __getitem__(self, item): return MockStreamlitElement()
        def __setitem__(self, key, value): pass
        def __contains__(self, item): return False

    class MockStreamlit:
        def __init__(self):
            self.sidebar = MockStreamlitElement(self)
            self.session_state = MockSessionState()
            self._keys = set()
            
        def _register_key(self, key):
            if key is not None:
                key_str = str(key)
                if key_str in self._keys:
                    raise ValueError(f"StreamlitDuplicateElementKey: There are multiple elements with the same key='{key_str}'.")
                self._keys.add(key_str)
                
        def __getattr__(self, name):
            if name in ['columns', 'tabs']:
                def func(spec, *args, **kwargs):
                    if isinstance(spec, int):
                        return [MockStreamlitElement(self) for _ in range(spec)]
                    else:
                        return [MockStreamlitElement(self) for _ in range(len(spec))]
                return func
            
            def func(*args, **kwargs):
                key = kwargs.get('key')
                self._register_key(key)
                return MockStreamlitElement(self)
            return func

    # Mocks para Matplotlib / Seaborn
    class MockPlot:
        def __getattr__(self, name):
            return lambda *args, **kwargs: MockPlot()
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass

    mock_st = MockStreamlit()

    globals_dict = {
        'st': mock_st,
        'np': np,
        'pd': pd,
        'go': go,
        'px': px,
        'stats': stats,
        'norm': norm,
        'plt': MockPlot(),
        'sns': MockPlot(),
        'json': json,
        'base64': base64,
        '__name__': '__main__'
    }
    
    if extra_globals:
        globals_dict.update(extra_globals)
        
    import sys
    original_streamlit = sys.modules.get('streamlit')
    sys.modules['streamlit'] = mock_st
    
    try:
        # Executa o código. Se disparar qualquer erro, nós capturamos e levantamos.
        exec(codigo_python, globals_dict)
    finally:
        if original_streamlit is not None:
            sys.modules['streamlit'] = original_streamlit
        else:
            sys.modules.pop('streamlit', None)

def validar_fatia(codigo_fatia: str, extra_globals: dict = None) -> tuple[bool, str]:
    """
    Verifica a sintaxe e tenta executar a fatia de código em ambiente mockado.
    Retorna (True, "") em caso de sucesso, ou (False, "mensagem de erro") se houver falha.
    """
    ok_sintaxe, erro_sintaxe = validar_sintaxe(codigo_fatia)
    if not ok_sintaxe:
        return False, erro_sintaxe
    
    try:
        validar_execucao_codigo(codigo_fatia, extra_globals=extra_globals)
        return True, ""
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        erro_exec = f"Erro de Execução ({type(e).__name__}): {e}\n\nTraceback completo:\n{tb}"
        return False, erro_exec

# ==============================================================================
# FASE C: ORQUESTRADOR LOCAL DE MONTAGEM E COMPILAÇÃO (PYTHON SEWING)
# ==============================================================================
def compilar_aula_completa_por_fatias(caminho_teoria_lapidada: str, caminho_exercicios: str, motor_grafico: str = "plotly", cor_principal: str = "#1E3A8A", cor_critica: str = "#991B1B", cor_secundaria: str = "#10B981", cor_alerta: str = "#F59E0B"):
    if not os.path.exists(caminho_teoria_lapidada) or not os.path.exists(caminho_exercicios):
        print("[ERRO] Erro critico: Payloads de entrada ausentes no diretorio.")
        return

    with open(caminho_teoria_lapidada, "r", encoding="utf-8") as f:
        teoria = json.load(f)
    with open(caminho_exercicios, "r", encoding="utf-8") as f:
        exercicios = json.load(f)
        
    import base64
    
    # Serialização 100% segura dos metadados da aula para evitar SyntaxError por conta de aspas ou caracteres especiais
    metadata = {
        "tema_global": teoria["tema_global"],
        "referencias_bibliograficas_finais": teoria.get("referencias_bibliograficas_finais", [])
    }
    metadata_json = json.dumps(metadata, ensure_ascii=False)
    metadata_b64 = base64.b64encode(metadata_json.encode("utf-8")).decode("utf-8")

    # Serialização 100% segura dos exercícios para evitar quebras por aspas triplas ou caracteres especiais
    exercicios_json = json.dumps(exercicios, ensure_ascii=False)
    exercicios_b64 = base64.b64encode(exercicios_json.encode("utf-8")).decode("utf-8")

    print(f"\n[OK] [Orquestrador Local] Compilando a aplicacao Streamlit por fatias incrementais usando o motor '{motor_grafico}'...")
    
    # Adiciona imports com base no motor gráfico
    imports_grafico = "import plotly.graph_objects as go"
    if motor_grafico.lower() == "seaborn":
        imports_grafico += "\nimport matplotlib.pyplot as plt\nimport seaborn as sns"

    # 1. Escreve a casca fixa de topo e estilos CSS do Livro Interativo (Economiza tokens do LLM)
    codigo_completo = f"""import streamlit as st
import numpy as np
import pandas as pd
{imports_grafico}
import scipy.stats as stats
from scipy.stats import norm
import base64
import json

# Carregamento seguro dos metadados da aula para evitar SyntaxError
metadata = json.loads(base64.b64decode('{metadata_b64}').decode('utf-8'))

# Injeção de Estilos CSS Acadêmicos Premium
st.markdown(\"\"\"
    <style>
        .premium-title {{ font-size: 2.2rem; font-weight: 800; color: {cor_principal}; margin-bottom: 0.2rem; }}
        .premium-subtitle {{ font-size: 1.1rem; color: #64748B; margin-bottom: 1.5rem; font-style: italic; }}
    </style>
    \"\"\", unsafe_allow_html=True)

st.markdown(f'<div class="premium-title">{{metadata["tema_global"]}}</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">Conteúdo Acadêmico Digital e Simuladores Integrados</div>', unsafe_allow_html=True)

# Definição de Cores Globais da Paleta Premium
PRIMARY_BLUE = "{cor_principal}"
SECONDARY_GREEN = "{cor_secundaria}"
WARNING_AMBER = "{cor_alerta}"
CRITICAL_RED = "{cor_critica}"

# Criação das Duas Grandes Abas Globais
tab_conteudo, tab_exercicios = st.tabs(["📚 Conteúdo Acadêmico Interativo", "📝 Caderno de Exercícios"])

with tab_conteudo:
"""

    # Converte a lista de simuladores em um dicionário de busca rápida
    simuladores_dict = {}
    for sim in teoria.get("simuladores_da_aula", []):
        simuladores_dict[str(sim.get("indice_pagina", ""))] = sim.get("nome_simulador", "")

    # 2. Laço Incremental: Processa e costura cada página de conteúdo separadamente
    for idx, pagina in enumerate(teoria["paginas_conteudo"]):
        print(f"   -> Solicitando codificação da página teórica {idx+1}: {pagina['titulo_subtopico']}")
        
        # Consulta o plano do orquestrador editorial para saber se deve carregar o plot e qual o seu nome
        chave_str = str(idx + 1)
        nome_simulador = simuladores_dict.get(chave_str, "")
        
        fatia_teoria_codigo = programar_fatia_teoria(pagina, nome_simulador=nome_simulador, motor_grafico=motor_grafico, chave_suffix=f"subtopico_{idx + 1}", cor_principal=cor_principal, cor_critica=cor_critica, cor_secundaria=cor_secundaria, cor_alerta=cor_alerta)
        
        # AJUSTE DEFENSIVO DE INDENTAÇÃO: Remove recuo base indesejado que a IA possa ter gerado
        linhas = fatia_teoria_codigo.split("\n")
        recuo_minimo = min([len(l) - len(l.lstrip()) for l in linhas if l.strip()] or [0])
        if recuo_minimo > 0:
            linhas = [l[recuo_minimo:] if l.strip() else l for l in linhas]
        fatia_teoria_codigo = "\n".join(linhas)
        
        # Aplica o recuo de 4 espaços para o Python não quebrar a indentação do 'with tab_conteudo:'
        codigo_indendado = "\n".join([f"    {linha}" for linha in fatia_teoria_codigo.split("\n")])
        codigo_completo += f"\n{codigo_indendado}\n"
        
    # 3. Injeta a Seção ÚNICA de Referências Bibliográficas consolidadas bem no final da primeira Aba
    codigo_completo += "\n    st.markdown('---')\n    st.markdown('##### 📚 Referências Bibliográficas Consolidadas (Rodapé da Aula)')\n"
    codigo_completo += "    for ref in metadata['referencias_bibliograficas_finais']:\n        st.markdown(f'- {ref}')\n"

    # 4. Abre a segunda Aba global e injeta a fatia dos exercícios práticos
    print("   -> Solicitando codificação do caderno de exercícios...")
    codigo_completo += "\nwith tab_exercicios:\n"
    codigo_completo += f"    import json, base64\n    dados_exercicios = json.loads(base64.b64decode('{exercicios_b64}').decode('utf-8'))\n\n"
    
    fatia_exercicios_codigo = programar_fatia_exercicios(exercicios)
    
    # Ajuste defensivo de indentação nos exercícios
    linhas_ex = fatia_exercicios_codigo.split("\n")
    recuo_min_ex = min([len(l) - len(l.lstrip()) for l in linhas_ex if l.strip()] or [0])
    if recuo_min_ex > 0:
        linhas_ex = [l[recuo_min_ex:] if l.strip() else l for l in linhas_ex]
    fatia_exercicios_codigo = "\n".join(linhas_ex)
    
    codigo_ex_indendado = "\n".join([f"    {linha}" for linha in fatia_exercicios_codigo.split("\n")])
    codigo_completo += f"\n{codigo_ex_indendado}\n"

    # 5. Descobre o número incremental e grava fisicamente o arquivo executável final na pasta /aulas
    pasta_aulas = "aulas"
    if not os.path.exists(pasta_aulas):
        os.makedirs(pasta_aulas)
    
    arquivos_existentes = [f for f in os.listdir(pasta_aulas) if f.startswith("aula") and f.endswith(".py")]
    prox_numero = 1
    for aula in arquivos_existentes:
        match = re.search(r'aula(\d+)', aula)
        if match:
            num = int(match.group(1))
            if num >= prox_numero:
                prox_numero = num + 1

    tema_limpo = re.sub(r'[^a-zA-Z0-9]', '_', teoria["tema_global"].lower())
    tema_limpo = re.sub(r'_+', '_', tema_limpo).strip('_')
    nome_arquivo = f"aula{prox_numero}_{tema_limpo}.py"
    caminho_final_script = os.path.join(pasta_aulas, nome_arquivo)

    with open(caminho_final_script, "w", encoding="utf-8") as f:
        f.write(codigo_completo)
        
    print(f"\n[SUCESSO] Aula gerada e compilada em fatias: {caminho_final_script}")

    # Teste de compilação
    try:
        import py_compile
        py_compile.compile(caminho_final_script, doraise=True)
        print("[OK] Teste de Compilação: Aprovado sem erros de sintaxe!")
    except py_compile.PyCompileError as pye:
        print(f"[ERRO] A costura apresentou problemas de compilação: {pye}")
        if os.path.exists(caminho_final_script):
            try:
                os.remove(caminho_final_script)
            except Exception:
                pass
        raise RuntimeError(f"O script gerado contém erro de sintaxe Python e foi removido para evitar falha do app. Detalhes: {pye}")

    # Teste de execução simulado em Sandbox
    try:
        validar_execucao_codigo(codigo_completo)
        print("[OK] Teste de Execução Simulado: Passou sem erros de runtime!")
    except Exception as e:
        print(f"[ERRO] Teste de Execução Simulado falhou: {e}")
        if os.path.exists(caminho_final_script):
            try:
                os.remove(caminho_final_script)
            except Exception:
                pass
        # Captura apenas o nome do erro e a mensagem para evitar estourar limites do terminal
        raise RuntimeError(f"O script gerado contém erros de execução (ex: Plotly/Pandas) e foi removido para evitar falhas no carregamento. Detalhes: {type(e).__name__}: {str(e)[:500]}")

    return caminho_final_script

if __name__ == "__main__":
    print("[AVISO] A compilação da interface deve ser executada a partir da interface do Streamlit.")
    print("Por favor, execute o comando: streamlit run app.py")
