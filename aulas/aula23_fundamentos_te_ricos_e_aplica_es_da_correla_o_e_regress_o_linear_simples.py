import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stats
from scipy.stats import norm

# Injeção de Estilos CSS Acadêmicos Premium
st.markdown("""
    <style>
        .premium-title { font-size: 2.2rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0.2rem; }
        .premium-subtitle { font-size: 1.1rem; color: #64748B; margin-bottom: 1.5rem; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="premium-title">Fundamentos Teóricos e Aplicações da Correlação e Regressão Linear Simples</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">Conteúdo Acadêmico Digital e Simuladores Integrados</div>', unsafe_allow_html=True)

# Definição de Cores Globais da Paleta Premium
PRIMARY_BLUE = "#1E3A8A"
SECONDARY_GREEN = "#10B981"
WARNING_AMBER = "#F59E0B"
CRITICAL_RED = "#991B1B"

# Criação das Duas Grandes Abas Globais
tab_conteudo, tab_exercicios = st.tabs(["📚 Conteúdo Acadêmico Interativo", "📝 Caderno de Exercícios"])

with tab_conteudo:

    # Importações necessárias caso não estejam presentes no contexto (assumindo disponibilidade das bibliotecas mencionadas)
    import numpy as np
    import plotly.graph_objects as go
    
    # Cabeçalho do Subtópico
    st.header(r"A Arquitetura da Associação Linear: Do Diagrama de Dispersão à Covariância")
    
    # Prosa Teórica Estática e Formatada
    st.markdown(r"""
    A análise bivariada representa a fronteira fundamental na transição da estatística descritiva para a inferência multivariada, onde buscamos compreender a interdependência entre variáveis. O ponto de partida é a representação gráfica via **diagrama de dispersão**, que permite visualizar a estrutura de relação em um plano cartesiano.
    """)
    
    st.info(r"""
    **Intuição Estatística:** A correlação quantifica a força e a direção desta relação, operando sobre o conceito de **covariância**, que mede como as variáveis se movem conjuntamente em relação às suas médias. Se observamos que desvios positivos de X tendem a coincidir com desvios positivos de Y, estamos diante de uma associação linear positiva.
    """)
    
    st.markdown(r"""
    É imperativo distinguir, contudo, que a correlação mede **associação linear**, mas não implica causalidade, um equívoco comum que pode comprometer a análise comercial. A estrutura de dados para esta análise requer a observação de pares $(X_i, Y_i)$, permitindo o cálculo do coeficiente de correlação de Pearson.
    """)
    
    # O Coração Matemático
    st.subheader(r"📐 O Coração Matemático: Do Cálculo da Covariância ao Coeficiente de Pearson")
    
    st.markdown(r"A dedução do coeficiente de correlação segue uma lógica progressiva de normalização da variância conjunta:")
    
    st.latex(r"Cov(X,Y) = \frac{1}{n-1} \sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})")
    st.markdown(r"A covariância mede a magnitude da dispersão conjunta, mas é dependente das unidades de medida das variáveis originais.")
    
    st.latex(r"Var(X) = \frac{1}{n-1} \sum_{i=1}^{n} (X_i - \bar{X})^2")
    st.markdown(r"Para obter uma métrica adimensional (entre -1 e 1), normalizamos a covariância pelo produto dos desvios padrão (raízes quadradas das variâncias):")
    
    st.latex(r"r = \frac{Cov(X,Y)}{\sqrt{Var(X)Var(Y)}} = \frac{\sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^{n} (X_i - \bar{X})^2 \sum_{i=1}^{n} (Y_i - \bar{Y})^2}}")
    
    # Simulador de Correlação
    st.subheader(r"📊 Explorador de Correlação de Pearson")
    st.markdown(r"Ajuste a correlação esperada ($r$) para visualizar a estrutura de dispersão dos dados.")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        r_val = st.slider(r"Selecione o coeficiente r:", -1.0, 1.0, 0.7, step=0.1, key=r"slider_correlacao_001")
    
    # Geração de dados sintéticos para o simulador
    n_samples = 100
    np.random.seed(42)
    x_data = np.random.normal(0, 1, n_samples)
    z_data = np.random.normal(0, 1, n_samples)
    y_data = r_val * x_data + np.sqrt(1 - r_val**2) * z_data
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers', marker=dict(color=PRIMARY_BLUE, size=8)))
    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title=dict(
            text=f"<b>Diagrama de Dispersão (r = {r_val})</b>",
            font=dict(size=14, color="#1E293B", family="Arial, sans-serif"),
            x=0.0,
            y=0.95
        ),
        xaxis=dict(
            title=dict(text="Variável X", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            fixedrange=True
        ),
        yaxis=dict(
            title=dict(text="Variável Y", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            fixedrange=True
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=12,
            font_color="#1E293B",
            font_family="Arial, sans-serif"
        )
    )
    st.plotly_chart(fig, use_container_width=True, key=r"plotly_chart_subtopico_1")
    
    # Seção de Casos de Aplicação
    st.subheader(r"📈 Casos de Aplicação Prática: Análises de Performance e Processos")
    
    # Exemplo 1: Marketing
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Investimento em Marketing vs. Vendas")
        st.markdown(r"Um analista de marketing deseja avaliar a correlação entre o investimento mensal em publicidade digital (X) e o volume de vendas gerado (Y). Com dados de 5 meses, busca-se validar a estratégia atual.")
        
        st.latex(r"n=5; \sum X=15; \sum Y=30; \sum X^2=55; \sum Y^2=200; \sum XY=100")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- $S_{XX} = 55 - (15^2)/5 = 10$")
        st.markdown(r"- $S_{YY} = 200 - (30^2)/5 = 20$")
        st.markdown(r"- $S_{XY} = 100 - (15 \times 30)/5 = 10$")
        st.markdown(r"- $r = 10 / \sqrt{10 \times 20} = 0.707$")
        
        st.success(r"Com um coeficiente de correlação de 0,707, identificamos uma associação positiva forte entre investimento e vendas. O laudo sugere que o incremento na verba publicitária tem efeito positivo no volume de vendas, validando a estratégia.")
    
    # Exemplo 2: Engenharia
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Temperatura de Forno vs. Viscosidade")
        st.markdown(r"Um engenheiro de processos analisa a relação entre a temperatura do forno (X) e a viscosidade do polímero resultante (Y). Com 6 amostras, verifica-se a viabilidade do controle de qualidade via temperatura.")
        
        st.latex(r"n=6; \sum X=120; \sum Y=150; \sum X^2=2500; \sum Y^2=4000; \sum XY=3100")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- $S_{XX} = 2500 - (120^2)/6 = 100$")
        st.markdown(r"- $S_{YY} = 4000 - (150^2)/6 = 250$")
        st.markdown(r"- $S_{XY} = 3100 - (120 \times 150)/6 = 100$")
        st.markdown(r"- $r = 100 / \sqrt{100 \times 250} = 0.632$")
        
        st.warning(r"A correlação de 0,632 indica uma associação positiva moderada. Embora exista uma tendência, a variabilidade residual é significativa, sugerindo que outros fatores além da temperatura influenciam a viscosidade.")

    # Importações necessárias (assumindo que o ambiente pai já as possui, mas garantindo aqui)
    import streamlit as st
    import numpy as np
    import plotly.graph_objects as go
    
    # --- CABEÇALHO DO SUBTÓPICO ---
    st.header(r"Otimização de Parâmetros: A Derivação do Modelo de Mínimos Quadrados Ordinários")
    
    # --- PROSA: INTRODUÇÃO E FORMULAÇÃO ---
    st.markdown(r"""
    A transição do paradigma descritivo, puramente preocupado com a organização e sumarização de dados observados, para o paradigma inferencial e preditivo, marca um dos pontos de inflexão mais críticos na história da ciência moderna. O problema fundamental não era apenas desenhar uma linha através de uma nuvem de pontos, mas sim encontrar o ajuste "ótimo" que minimizasse a distância entre a realidade observada e a abstração teórica.
    
    Este processo exige uma formalização rigorosa do fenômeno, onde pressupomos que cada observação $i$ é regida por uma estrutura linear subjacente:
    """)
    
    st.latex(r"Y_i = \beta_0 + \beta_1 X_i + \epsilon_i")
    
    st.markdown(r"""
    Nesta formulação, a variável $Y_i$ é decomposta no componente sistemático (a reta de regressão) e no componente aleatório ($\epsilon_i$), que incorpora a variabilidade intrínseca e o erro de medição. Para quantificar o ajuste, utilizamos a soma dos quadrados dos resíduos, uma função convexa e suave que garante um mínimo global único:
    """)
    
    st.latex(r"S(\beta_0, \beta_1) = \sum_{i=1}^n (Y_i - \beta_0 - \beta_1 X_i)^2")
    
    # --- SIMULADOR DE MINIMIZAÇÃO DE RESÍDUOS ---
    st.markdown(r"### 🎛️ Visualizador de Minimização de Resíduos (MQO)")
    
    # Dados fixos para o simulador
    x_sim = np.array([1, 2, 3, 4, 5, 6])
    y_sim = np.array([1.2, 2.8, 3.1, 4.5, 5.2, 6.8])
    
    col_slider1, col_slider2 = st.columns(2)
    with col_slider1:
        b0_val = st.slider(r"Intercepto ($\beta_0$)", 0.0, 3.0, 1.0, 0.1, key=r"mqo_slider_b0")
    with col_slider2:
        b1_val = st.slider(r"Inclinação ($\beta_1$)", 0.0, 2.0, 1.0, 0.1, key=r"mqo_slider_b1")
    
    # Cálculo da reta
    y_pred = b0_val + b1_val * x_sim
    
    # Plotly Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_sim, y=y_sim, mode='markers', name=r"Observações", marker=dict(color=PRIMARY_BLUE, size=10)))
    fig.add_trace(go.Scatter(x=x_sim, y=y_pred, mode='lines', name=r"Modelo ($Y = \beta_0 + \beta_1 X$)", line=dict(color=SECONDARY_GREEN, width=3)))
    
    # Adicionando linhas de resíduos
    for i in range(len(x_sim)):
        fig.add_trace(go.Scatter(x=[x_sim[i], x_sim[i]], y=[y_sim[i], y_pred[i]], mode='lines', line=dict(color=CRITICAL_RED, width=1, dash='dash'), showlegend=False))
    
    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title=dict(
            text="<b>Minimização Geométrica da Soma dos Quadrados</b>",
            font=dict(size=14, color="#1E293B", family="Arial, sans-serif"),
            x=0.0,
            y=0.95
        ),
        xaxis=dict(
            title=dict(text="Variável Independente X", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            fixedrange=True
        ),
        yaxis=dict(
            title=dict(text="Variável Dependente Y", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            fixedrange=True
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#E2E8F0",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=12,
            font_color="#1E293B",
            font_family="Arial, sans-serif"
        )
    )
    st.plotly_chart(fig, use_container_width=True, key=r"plotly_chart_subtopico_2")
    
    # --- O CORAÇÃO MATEMÁTICO: DERIVAÇÃO ---
    st.markdown(r"### 📐 O Coração Matemático: Derivação do Estimador")
    st.markdown(r"Para encontrar o ponto de mínimo da função de perda $S$, aplicamos o cálculo diferencial, derivando em relação a $\beta_0$ e $\beta_1$ e igualando a zero.")
    
    st.markdown(r"**1. Condição de primeira ordem para o Intercepto ($\beta_0$):**")
    st.latex(r"\frac{\partial S}{\partial \beta_0} = -2 \sum (Y_i - \beta_0 - \beta_1 X_i) = 0")
    
    st.markdown(r"**2. Condição de primeira ordem para a Inclinação ($\beta_1$):**")
    st.latex(r"\frac{\partial S}{\partial \beta_1} = -2 \sum X_i (Y_i - \beta_0 - \beta_1 X_i) = 0")
    
    st.markdown(r"Resolvendo este sistema linear, conhecido como **Equações Normais**, obtemos:")
    st.latex(r"n\beta_0 + \beta_1 \sum X_i = \sum Y_i")
    st.latex(r"\beta_0 \sum X_i + \beta_1 \sum X_i^2 = \sum X_i Y_i")
    
    st.markdown(r"Isolando os parâmetros, chegamos às soluções analíticas para os estimadores $\hat{\beta}_1$ e $\hat{\beta}_0$:")
    st.latex(r"\hat{\beta}_1 = \frac{n\sum XY - \sum X \sum Y}{n\sum X^2 - (\sum X)^2}")
    st.latex(r"\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}")
    
    # --- EXEMPLOS PRÁTICOS ---
    st.markdown(r"### 📈 Casos de Aplicação Prática: Estimativas de MQO")
    
    # Exemplo 1
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Logística de Manutenção")
        st.markdown(r"Uma empresa de logística deseja estimar o custo de manutenção (Y) com base na quilometragem rodada (X).")
        st.latex(r"n=4; \sum X=100; \sum Y=15; \sum X^2=3000; \sum XY=430")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- $\hat{\beta}_1 = \frac{4*430 - 100*15}{4*3000 - 100^2} = \frac{1720 - 1500}{12000 - 10000} = \frac{220}{2000} = 0.11$")
        st.markdown(r"- $\hat{\beta}_0 = \frac{15}{4} - 0.11 * \frac{100}{4} = 3.75 - 2.75 = 1.0$")
        st.success(r"O modelo indica um custo fixo de 100 reais e um custo variável de 11 reais por mil km. A gestão pode usar esta equação para orçamentar a manutenção preventiva.")
    
    # Exemplo 2
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Farmacologia Experimental")
        st.markdown(r"Laboratório farmacêutico estudando a resposta de um fármaco (Y) ao tempo de exposição (X).")
        st.latex(r"n=5; \sum X=15; \sum Y=78; \sum X^2=55; \sum XY=268")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- $\hat{\beta}_1 = \frac{5*268 - 15*78}{5*55 - 15^2} = \frac{1340 - 1170}{275 - 225} = \frac{170}{50} = 3.4$")
        st.markdown(r"- $\hat{\beta}_0 = \frac{78}{5} - 3.4 * \frac{15}{5} = 15.6 - 10.2 = 5.4$")
        st.success(r"Cada hora adicional de exposição aumenta a resposta em 3,4 mg/dL. O modelo demonstra uma clara relação linear, permitindo prever a dosagem acumulada.")

    import streamlit as st
    import numpy as np
    import plotly.graph_objects as go
    from scipy import stats
    
    # Cabeçalho do Subtópico
    st.header(r"Inferência e Diagnóstico: Validando a Qualidade e Significância do Ajuste")
    
    # Introdução e Contexto Teórico
    st.markdown(r"""
    A estimação dos parâmetros de um modelo de regressão linear, geralmente alcançada pelo Método dos Mínimos Quadrados Ordinários (MQO), representa apenas o estágio inaugural de uma investigação estatística rigorosa. É um equívoco comum acreditar que a simples obtenção dos coeficientes encerra o ciclo de modelagem.
    
    A transição de um mero exercício de cálculo algébrico para uma ferramenta científica de inferência exige que o pesquisador considere, de forma crítica e metódica, a natureza do resíduo e a robustez da estrutura estatística subjacente.
    """)
    
    st.info(r"""
    **A Vigilância Epistemológica:** Sem uma validação diagnóstica exaustiva, o pesquisador corre o risco de apresentar resultados que, embora matematicamente computáveis, são estatisticamente espúrios, falhando em capturar a verdadeira dinâmica da relação entre as variáveis.
    """)
    
    st.markdown(r"""
    ### 📊 Simulador: Dinâmica da Significância Estatística e Intervalos de Confiança
    
    Abaixo, exploramos como a variabilidade dos dados e o tamanho da amostra impactam diretamente a nossa capacidade de rejeitar a hipótese nula.
    """)
    
    # Setup do Simulador
    col_slider1, col_slider2 = st.columns(2)
    n_samples = col_slider1.slider(r"Tamanho da Amostra (n)", 10, 100, 30, key=r"sim_n_samples_inferencia")
    noise_level = col_slider2.slider(r"Nível de Ruído (σ)", 0.1, 3.0, 1.0, key=r"sim_noise_inferencia")
    
    # Cálculo interno (sem dependências externas de data)
    np.random.seed(42)
    x_sim = np.linspace(0, 10, n_samples)
    y_sim = 2.0 * x_sim + 1.0 + np.random.normal(0, noise_level, n_samples)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_sim, y_sim)
    
    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_sim, y=y_sim, mode='markers', name=r"Dados Observados", marker=dict(color=PRIMARY_BLUE)))
    fig.add_trace(go.Scatter(x=x_sim, y=slope*x_sim + intercept, mode='lines', name=r"Reta Ajustada", line=dict(color=SECONDARY_GREEN, width=3)))
    
    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title=dict(
            text="<b>Relação X e Y (Significância p-value: {:.4f})</b>".format(p_value),
            font=dict(size=14, color="#1E293B", family="Arial, sans-serif"),
            x=0.0,
            y=0.95
        ),
        xaxis=dict(
            title=dict(text="Variável Independente X", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            fixedrange=True
        ),
        yaxis=dict(
            title=dict(text="Variável Dependente Y", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            fixedrange=True
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#E2E8F0",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=12,
            font_color="#1E293B",
            font_family="Arial, sans-serif"
        )
    )
    st.plotly_chart(fig, use_container_width=True, key=r"plotly_chart_subtopico_3")
    
    # Métricas do Modelo
    st.markdown(r"### 🎯 Interpretação do Ajuste e Resíduos")
    
    col_metric1, col_metric2 = st.columns(2)
    col_metric1.metric(r"Coeficiente de Determinação ($R^2$)", value=r"{:.2%}".format(r_value**2))
    col_metric2.metric(r"P-Valor da Inclinação", value=r"{:.4f}".format(p_value))
    
    st.markdown(r"""
    O coeficiente de determinação ($R^2$) encapsula a proporção da variabilidade total da variável resposta explicada pelo modelo. Entretanto, o $R^2$ elevado não é garantia de validade. É imperativo observar a análise de resíduos para detectar violações como heterocedasticidade ou não-normalidade.
    """)
    
    st.latex(r"R^2 = 1 - \frac{\sum (Y_i - \hat{Y}_i)^2}{\sum (Y_i - \bar{Y})^2}")
    
    st.markdown(r"""
    Quando os resíduos exibem padrões sistemáticos, a inferência estatística, baseada na distribuição t de Student, torna-se fragilizada. O teste t avalia a significância da relação:
    """)
    
    st.latex(r"t = \frac{\hat{\beta}_1}{se(\hat{\beta}_1)}")
    
    st.markdown(r"### 📐 O Coração Matemático: Dedução e Propriedades")
    
    st.markdown(r"A decomposição da variância é o fundamento do $R^2$:")
    st.latex(r"SQT = SQR + SQE")
    
    st.markdown(r"Definimos o poder explicativo do modelo como a razão entre a soma dos quadrados explicada e o total:")
    st.latex(r"R^2 = \frac{SQR}{SQT}")
    
    st.markdown(r"Para a inferência dos coeficientes, utilizamos o erro padrão, que mede a precisão da estimativa:")
    st.latex(r"se(\hat{\beta}_1) = \sqrt{\frac{MQE}{\sum (X_i - \bar{X})^2}}")
    
    st.markdown(r"Por fim, construímos o intervalo de confiança para o parâmetro populacional:")
    st.latex(r"IC_{\beta_1} = \hat{\beta}_1 \pm t_{\alpha/2, n-2} \cdot se(\hat{\beta}_1)")
    
    st.markdown(r"### 📈 Casos de Aplicação Prática: Validação de Hipóteses")
    
    # Exemplo 1
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Resistência de Materiais")
        st.markdown(r"Em um estudo de resistência de materiais, avalia-se a tensão (Y) em função da carga (X). Com n=10, obteve-se um R-quadrado de 0.85 e um coeficiente beta_1 de 0.5 com erro padrão de 0.05. Teste a hipótese de que a carga não influencia a tensão ao nível de 5%.")
        st.latex(r"\hat{\beta}_1=0.5; se(\hat{\beta}_1)=0.05; n=10; \alpha=0.05")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Cálculo da estatística t: $t = 0.5 / 0.05 = 10.0$")
        st.markdown(r"- Graus de Liberdade (gl): $n-2 = 8$")
        st.markdown(r"- Comparação: $10.0 > 2.306$ (t crítico para 5%)")
        st.success(r"Rejeitamos a hipótese nula. A carga tem um impacto estatisticamente significativo na tensão. O modelo de 85% de explicação (R^2) é validado estatisticamente para uso em engenharia.")
    
    # Exemplo 2
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Produtividade Agrícola")
        st.markdown(r"Analise a eficácia de um novo fertilizante (X, em doses) na produtividade de soja (Y, em sacas). Com n=15, a estimativa da inclinação foi 2.0 com erro padrão 0.8. Teste a significância ao nível de 5%.")
        st.latex(r"\hat{\beta}_1=2.0; se(\hat{\beta}_1)=0.8; n=15; \alpha=0.05")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Cálculo da estatística t: $t = 2.0 / 0.8 = 2.5$")
        st.markdown(r"- Graus de Liberdade (gl): $n-2 = 13$")
        st.markdown(r"- Comparação: $2.5 > 2.16$ (t crítico para 5%)")
        st.success(r"Rejeitamos H0, confirmando que o fertilizante afeta a produtividade. A estatística t demonstra robustez para a inferência.")

    st.markdown('---')
    st.markdown('##### 📚 Referências Bibliográficas Consolidadas (Rodapé da Aula)')
    st.markdown(r'- Bussab & Morettin, Estatística Básica - Cap. 4, pp. 83-85')
    st.markdown(r'- Bussab & Morettin, Estatística Básica - Cap. 16, pp. 450-454')
    st.markdown(r'- Bussab & Morettin, Estatística Básica - Cap. 16, pp. 464-466')
    st.markdown(r'- Montgomery & Runger, Estatística Aplicada e Probabilidade para Engenheiros - Cap. 11, pp. 236-239')
    st.markdown(r'- Montgomery & Runger, Estatística Aplicada e Probabilidade para Engenheiros - Cap. 11, pp. 238-243')
    st.markdown(r'- Montgomery & Runger, Estatística Aplicada e Probabilidade para Engenheiros - Cap. 11, pp. 244-247')

with tab_exercicios:
    import json
    dados_exercicios = json.loads(r"""{"topico_aula": "3.1. Correlação e Regressão Linear Simples", "questoes_multipla_escolha": [{"enunciado": "Em um estudo sobre a eficiência de um processo industrial de produção de polímeros, um engenheiro químico deseja modelar a temperatura de reação ($X$, em °C) em função da taxa de conversão do produto final ($Y$, em %). Após coletar uma amostra de $n = 30$ observações, ele obtém um coeficiente de correlação de Pearson $r = 0,85$. Assumindo que a relação é linear, qual é a interpretação estatística mais adequada para o coeficiente de determinação ($R^2$) neste contexto?", "alternativas": {"A": "A variável temperatura explica 85% da variabilidade na taxa de conversão do produto.", "B": "A variável temperatura explica aproximadamente 72,25% da variabilidade na taxa de conversão do produto.", "C": "O coeficiente $R^2$ é igual a 0,85, indicando uma relação linear forte e positiva entre as variáveis.", "D": "Existe uma correlação de 72,25% entre a temperatura e a taxa de conversão, indicando causalidade direta.", "E": "O valor de $R^2$ sugere que 15% da variação em $Y$ não é explicada pelo modelo de regressão linear."}, "alternativa_correta": "B", "dica": "Lembre-se que o coeficiente de determinação $R^2$ é o quadrado do coeficiente de correlação $r$. Pense sobre o que o $R^2$ representa em termos de proporção de variância explicada.", "gabarito_comentado": "O coeficiente de determinação $R^2$ é definido como o quadrado do coeficiente de correlação de Pearson ($r^2$). Neste caso, $R^2 = (0,85)^2 = 0,7225$. Estatisticamente, o $R^2$ quantifica a proporção da variância total da variável resposta ($Y$) que é explicada pelo modelo de regressão linear ajustado com a variável preditora ($X$). Portanto, o valor 0,7225 (ou 72,25%) indica que 72,25% da variação na taxa de conversão é explicada pelo modelo linear da temperatura, enquanto o restante (1 - 0,7225 = 27,75%) deve-se a outros fatores ou ao erro aleatório não capturado pelo modelo. As alternativas A e C confundem $r$ com $R^2$. A alternativa D está incorreta pois correlação não implica causalidade e o cálculo percentual está mal aplicado. A alternativa E cita 15%, mas o valor correto não explicado é 27,75%"}, {"enunciado": "Um economista está analisando a relação entre o investimento em marketing ($X$, em milhares de reais) e o volume de vendas ($Y$, em milhares de unidades) de uma empresa. Com os dados coletados, ele ajustou o modelo de regressão linear simples $Y_i = \beta_0 + \beta_1 X_i + \text{e}_i$ e encontrou os estimadores $\\hat{\\beta}_0 = 15$ e $\\hat{\\beta}_1 = 2,5$. Qual é a previsão correta para o volume de vendas se a empresa decidir investir 20 mil reais em marketing?", "alternativas": {"A": "40 mil unidades.", "B": "50 mil unidades.", "C": "65 mil unidades.", "D": "75 mil unidades.", "E": "100 mil unidades."}, "alternativa_correta": "C", "dica": "Aplique a equação da reta de regressão estimada $\\hat{Y} = \\hat{\\beta}_0 + \\hat{\\beta}_1 X$ substituindo o valor de $X$ fornecido.", "gabarito_comentado": "A equação da reta estimada é $\\hat{Y} = 15 + 2,5X$. Para um investimento de $X = 20$, substituímos na equação: $\\hat{Y} = 15 + 2,5(20)$. Calculando: $\\hat{Y} = 15 + 50 = 65$. Portanto, a previsão é de 65 mil unidades. A alternativa A ignorou o intercepto. A alternativa B cometeu erro de cálculo na multiplicação. As alternativas D e E estão incorretas matematicamente."}, {"enunciado": "Ao realizar uma análise de resíduos ($e_i = Y_i - \\hat{Y}_i$) após ajustar um modelo de regressão linear simples, um estatístico observa que, conforme o valor de $X$ aumenta, a dispersão dos resíduos aumenta drasticamente, formando um padrão de 'funil'. Como deve ser interpretado esse diagnóstico?", "alternativas": {"A": "O modelo está perfeitamente ajustado, pois os resíduos mostram uma tendência clara.", "B": "O modelo apresenta homocedasticidade, confirmando que a variância do erro $\\sigma^2$ é constante.", "C": "O modelo apresenta heterocedasticidade, violando uma das premissas clássicas de Gauss-Markov.", "D": "O modelo sofre de autocorrelação, indicando que os erros dependem do tempo.", "E": "O coeficiente $R^2$ será necessariamente igual a 1, devido à variabilidade crescente dos resíduos."}, "alternativa_correta": "C", "dica": "O termo técnico para a constância da variância dos resíduos é homocedasticidade. O oposto disso, observado graficamente como um funil, é uma violação importante.", "gabarito_comentado": "A análise de resíduos é fundamental para validar as suposições do modelo linear. A suposição de homocedasticidade exige que a variância dos erros ($\\sigma^2$) seja constante para todos os níveis de $X$. O aparecimento de um padrão de 'funil' ou 'leque' no gráfico de resíduos vs. valores ajustados indica claramente a presença de heterocedasticidade (variância não constante). Isso viola as premissas de Gauss-Markov, invalidando os intervalos de confiança e testes de hipóteses padrão, a menos que correções como mínimos quadrados ponderados sejam aplicadas. Alternativa A e B são falsas pois a tendência nos resíduos é indesejável. Alternativa D está incorreta pois o problem é de variância, não de autocorrelação. E é falsa."}, {"enunciado": "Considere o teste de hipóteses para a inclinação da reta de regressão populacional: $H_0: \\beta_1 = 0$ contra $H_1: \\beta_1 \\neq 0$. Em uma amostra de $n = 22$, o erro padrão estimado do coeficiente angular é $se(\\hat{\\beta}_1) = 0,5$ e o estimador calculado é $\\hat{\\beta}_1 = 1,2$. Qual é o valor da estatística $t_{\\text{calc}}$ e qual a conclusão estatística ao nível de significância $\\alpha = 0,05$ (dado que $t_{\\text{crit}(0,025, 20)} \\approx 2,086$)?", "alternativas": {"A": "$t_{\\text{calc}} = 0,6$; não rejeitamos $H_0$.", "B": "$t_{\\text{calc}} = 2,4$; rejeitamos $H_0$.", "C": "$t_{\\text{calc}} = 2,4$; não rejeitamos $H_0$.", "D": "$t_{\\text{calc}} = 0,6$; rejeitamos $H_0$.", "E": "$t_{\\text{calc}} = 1,7$; não rejeitamos $H_0$."}, "alternativa_correta": "B", "dica": "A estatística $t_{\\text{calc}}$ é dada pela razão entre o estimador e seu erro padrão: $t_{\\text{calc}} = \\hat{\\beta}_1 / se(\\hat{\\beta}_1)$. Compare com $t_{\\text{crit}}$.", "gabarito_comentado": "Calculamos $t_{\\text{calc}} = \\frac{\\hat{\\beta}_1}{se(\\hat{\\beta}_1)} = \\frac{1,2}{0,5} = 2,4$. Com $n=22$, os graus de liberdade são $n-2 = 20$. O valor crítico para $\\alpha = 0,05$ (bicaudal) é $t_{0,025, 20} = 2,086$. Como $|t_{\\text{calc}}| = 2,4 > 2,086$, caímos na região de rejeição. Portanto, rejeitamos $H_0$ e concluímos que $\beta_1$ é estatisticamente diferente de zero ao nível de significância de 5%. A alternativa B está correta. A alternativa C ignora a regra de rejeição, e A, D e E calculam ou interpretam incorretamente."}, {"enunciado": "Qual é a principal distinção teórica entre um Intervalo de Confiança para a média condicional $E[Y|X=x_0]$ e um Intervalo de Predição para um valor individual $Y_h$ em uma regressão linear simples?", "alternativas": {"A": "Não há distinção; ambos utilizam a mesma fórmula de erro padrão.", "B": "O intervalo de predição é mais estreito que o intervalo de confiança, pois lida com um único valor.", "C": "O intervalo de confiança considera apenas a incerteza da estimação dos parâmetros, enquanto o intervalo de predição incorpora, adicionalmente, a variabilidade intrínseca do termo de erro $\\epsilon$.", "D": "O intervalo de predição depende apenas do tamanho amostral $n$, enquanto o de confiança depende da variância amostral $S^2$.", "E": "Apenas o intervalo de predição exige que os resíduos sejam normalmente distribuídos."}, "alternativa_correta": "C", "dica": "Pense na fonte de incerteza: ao prever um indivíduo, estamos tentando acertar um ponto específico que possui um erro aleatório associado, enquanto estimar uma média busca apenas o valor esperado da reta naquele ponto.", "gabarito_comentado": "A distinção é fundamental. Ao estimar a média $E[Y|X=x_0]$, a única incerteza provém da estimativa dos parâmetros ($\\hat{\\beta}_0, \\hat{\\beta}_1$). Ao prever um valor individual $Y_h$, enfrentamos essa mesma incerteza dos parâmetros acrescida da variabilidade intrínseca da variável resposta, representada pelo termo de erro $\\epsilon$. Logo, o Intervalo de Predição é sempre mais largo que o Intervalo de Confiança para a média. A alternativa C descreve exatamente essa diferença. A alternativa B inverte a lógica de largura. A alternativa A está incorreta, pois as fórmulas de erro padrão diferem. D e E estão incorretas pois ambos os intervalos dependem de $n$ e da variância dos resíduos."}], "questoes_discursivas": [{"enunciado": "Considere um conjunto de dados com $n = 10$ observações sobre o custo de manutenção ($Y$) e a idade do equipamento ($X$). Suponha que os seguintes valores amostrais foram obtidos: $\\bar{X} = 5$, $\\bar{Y} = 20$, $\\sum (X_i - \\bar{X})^2 = 40$ e $\\sum (X_i - \\bar{X})(Y_i - \\bar{Y}) = 120$. Calcule os estimadores de Mínimos Quadrados Ordinários (MQO) para a inclinação ($\\hat{\\beta}_1$) e para o intercepto ($\\hat{\\beta}_0$).", "dica": "Utilize as fórmulas: $\\hat{\\beta}_1 = \\frac{S_{XY}}{S_{XX}}$ e $\\hat{\\beta}_0 = \\bar{Y} - \\hat{\\beta}_1 \\bar{X}$. Lembre-se que $S_{XX} = \\sum (X_i - \\bar{X})^2$ e $S_{XY} = \\sum (X_i - \\bar{X})(Y_i - \\bar{Y})$.", "gabarito_passo_a_passo": ["Identificar os dados fornecidos: $\\sum (X_i - \\bar{X})^2 = 40$, $\\sum (X_i - \\bar{X})(Y_i - \\bar{Y}) = 120$, $\\bar{X} = 5$, $\\bar{Y} = 20$.", "Calcular $\\hat{\\beta}_1$: $\\hat{\\beta}_1 = \\frac{120}{40} = 3$.", "Calcular $\\hat{\\beta}_0$: $\\hat{\\beta}_0 = \\bar{Y} - \\hat{\\beta}_1 \\bar{X} = 20 - (3 \\times 5) = 20 - 15 = 5$.", "Conclusão: A equação de regressão estimada é $\\hat{Y} = 5 + 3X$."]}, {"enunciado": "Em uma análise de regressão, obteve-se $SQT = 1000$ e $SQE = 200$ para uma amostra de tamanho $n=25$. (a) Calcule o coeficiente de determinação $R^2$ e interprete-o. (b) Determine o Erro Padrão da Estimativa ($S_e$).", "dica": "Use $R^2 = 1 - (SQE/SQT)$ e a fórmula $S_e = \\sqrt{SQE / (n-2)}$. Lembre-se que o denominador para $S_e$ no modelo linear simples é $n-2$.", "gabarito_passo_a_passo": ["Cálculo de $R^2$: $R^2 = 1 - (200 / 1000) = 1 - 0,2 = 0,8$. Isso significa que 80% da variabilidade em $Y$ é explicada pela variável $X$ no modelo.", "Cálculo de $S_e$: $S_e = \\sqrt{\\frac{SQE}{n-2}} = \\sqrt{\\frac{200}{25-2}} = \\sqrt{\\frac{200}{23}}$.", "Resultado do erro padrão: $S_e \\approx \\sqrt{8,695} \\approx 2,949$."]}, {"enunciado": "Dado o modelo $Y_i = \\beta_0 + \\beta_1 X_i + \\epsilon_i$, explique o papel do Método dos Mínimos Quadrados (MQO) na minimização da função $S(\\beta_0, \\beta_1) = \\sum_{i=1}^{n} (Y_i - \\beta_0 - \\beta_1 X_i)^2$. Por que minimizamos os quadrados dos resíduos em vez dos valores absolutos dos resíduos?", "dica": "Considere as propriedades de diferenciabilidade das funções quadráticas em comparação com a função módulo (valor absoluto) no ponto zero.", "gabarito_passo_a_passo": ["O MQO busca encontrar os parâmetros que tornam a reta o mais próxima possível dos dados observados, minimizando a soma das distâncias verticais ao quadrado.", "Matematicamente, a função $f(x) = |x|$ (valor absoluto) não é diferenciável em $x=0$, o que dificulta o uso de métodos de cálculo diferencial para encontrar o mínimo em sistemas complexos.", "A função quadrática $f(x) = x^2$ é contínua e infinitamente diferenciável, permitindo encontrar o mínimo através da igualdade das derivadas parciais a zero (sistema de equações normais).", "Além disso, minimizar quadrados penaliza resíduos grandes mais intensamente do que resíduos pequenos, resultando em estimadores com propriedades estatísticas ótimas (como a não-tendenciosidade e variância mínima sob as hipóteses clássicas)."]}]}""")


    import streamlit as st
    
    # Assumindo que 'dados_exercicios' já está disponível no escopo
    
    st.header(f"Exercícios: {dados_exercicios.get('topico_aula', 'Aula')}")
    
    # --- Seção de Questões de Múltipla Escolha ---
    st.subheader("📝 Questões de Múltipla Escolha")
    
    for i, questao in enumerate(dados_exercicios.get("questoes_multipla_escolha", [])):
        st.markdown(f"**Questão {i+1}:** {questao.get('enunciado', 'Enunciado indisponível')}")
        
        alternativas = questao.get("alternativas", {})
        # O radio retorna a chave (A, B, C...) selecionada
        selecao = st.radio(
            "Escolha uma alternativa:",
            options=list(alternativas.keys()),
            format_func=lambda x: f"{x}: {alternativas[x]}",
            key=f"radio_mcq_{i}"
        )
        
        # Botão para dica
        if st.button("💡 Dica", key=f"dica_mcq_{i}"):
            st.info(questao.get("dica", "Dica indisponível"))
            
        # Botão para verificar resposta
        if st.button("✅ Verificar Resposta", key=f"verificar_mcq_{i}"):
            correta = questao.get("alternativa_correta")
            if selecao == correta:
                st.success("Correto! Muito bem.")
            else:
                st.error(f"Incorreto. A alternativa correta era a {correta}.")
                
        # Gabarito comentado
        with st.expander("✅ Ver Gabarito Comentado"):
            st.write(questao.get("gabarito_comentado", "Gabarito indisponível"))
        
        st.divider()
    
    # --- Seção de Questões Discursivas ---
    st.subheader("✍️ Questões Discursivas")
    
    for i, questao in enumerate(dados_exercicios.get("questoes_discursivas", [])):
        st.markdown(f"**Questão Discursiva {i+1}:** {questao.get('enunciado', 'Enunciado indisponível')}")
        
        # Área de texto para resposta do aluno
        st.text_area("Sua resposta:", key=f"text_discursiva_{i}")
        
        # Botão para dica
        if st.button("💡 Dica", key=f"dica_discursiva_{i}"):
            st.info(questao.get("dica", "Dica indisponível"))
            
        # Resolução detalhada
        with st.expander("✅ Ver Resolução Detalhada"):
            passos = questao.get("gabarito_passo_a_passo", [])
            if passos:
                for idx, passo in enumerate(passos):
                    st.write(f"{idx + 1}. {passo}")
            else:
                st.write("Resolução não disponível.")
                
        st.divider()
