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

st.markdown('<div class="premium-title">5.1 – O procedimento geral da análise de variância</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">Conteúdo Acadêmico Digital e Simuladores Integrados</div>', unsafe_allow_html=True)

# Definição de Cores Globais da Paleta Premium
PRIMARY_BLUE = "#1E3A8A"
SECONDARY_GREEN = "#10B981"
WARNING_AMBER = "#F59E0B"
CRITICAL_RED = "#991B1B"

# Criação das Duas Grandes Abas Globais
tab_conteudo, tab_exercicios = st.tabs(["📚 Conteúdo Acadêmico Interativo", "📝 Caderno de Exercícios"])

with tab_conteudo:

    # Título do Subtópico
    st.header(r"A Arquitetura da Variância: Fundamentos Matemáticos da Decomposição na ANOVA")
    
    # Introdução e Contexto
    st.markdown(r"""
    A gênese da Análise de Variância (ANOVA) representa um dos saltos paradigmáticos mais significativos na estatística inferencial, transcendendo a limitação binária do teste-t de Student. Enquanto procedimentos anteriores aprisionavam a investigação em comparações pareadas ineficientes, a ANOVA permite a análise simultânea de múltiplas populações, garantindo que o rigor experimental não seja sacrificado pela fragmentação dos testes.
    
    A problemática central que a ANOVA soluciona é a **inflação do Erro Tipo I**. Ao realizar múltiplos testes-t independentes, a probabilidade acumulada de um falso positivo cresce exponencialmente, degradando a confiabilidade das conclusões científicas. Abaixo, destacamos os pilares teóricos dessa abordagem:
    """)
    
    # Cards de Destaque para Pressupostos
    col1, col2 = st.columns(2)
    with col1:
        st.info(r"**Controle de Erro Global**")
        st.write(r"Mantém o nível de significância nominal (alfa) constante, avaliando o sistema sob uma hipótese nula global, em vez de múltiplas comparações fragmentadas.")
    with col2:
        st.info(r"**Decomposição de Variância**")
        st.write(r"Segrega o 'sinal' (efeito do tratamento) do 'ruído' (variabilidade residual), permitindo uma visão holística do fenômeno experimental.")
    
    # Seção de Formalismo
    st.markdown(r"### 🧠 O Modelo Linear: Decomposição da Realidade")
    st.markdown(r"No coração da ANOVA reside o modelo linear, que desdobra cada observação em seus constituintes latentes:")
    st.latex(r"Y_{ij} = \mu + \alpha_i + \epsilon_{ij}")
    st.markdown(r"Onde os resíduos devem obedecer estritamente à condição de normalidade e homoscedasticidade:")
    st.latex(r"\epsilon_{ij} \sim N(0, \sigma^2)")
    st.markdown(r"A hipótese nula que testamos, pressupondo a ausência de efeitos de tratamento, é formulada como:")
    st.latex(r"H_0: \alpha_1 = \dots = \alpha_k = 0")
    
    # Demonstração Analítica
    st.markdown(r"### 📐 A Geometria da Partição da Variância")
    st.markdown(r"A dedução da soma de quadrados total segue uma lógica de partição ortogonal dos desvios da média:")
    
    st.latex(r"Y_{ij} - \bar{Y}_{..} = (\bar{Y}_{i.} - \bar{Y}_{..}) + (Y_{ij} - \bar{Y}_{i.})")
    st.markdown(r"Elevando ambos os lados ao quadrado e somando sobre todas as observações, obtemos a base da decomposição:")
    st.latex(r"\sum_{i=1}^{k} \sum_{j=1}^{n_i} (Y_{ij} - \bar{Y}_{..})^2 = \sum_{i=1}^{k} \sum_{j=1}^{n_i} ((\bar{Y}_{i.} - \bar{Y}_{..}) + (Y_{ij} - \bar{Y}_{i.}))^2")
    st.markdown(r"Ao expandir os termos, o produto cruzado anula-se, resultando na partição clássica:")
    st.latex(r"SQT = \sum n_i(\bar{Y}_{i.} - \bar{Y}_{..})^2 + \sum \sum (Y_{ij} - \bar{Y}_{i.})^2 + 2 \sum \sum (\bar{Y}_{i.} - \bar{Y}_{..})(Y_{ij} - \bar{Y}_{i.})")
    st.markdown(r"Concluímos com a estrutura final da variância observada:")
    st.latex(r"SQT = SQTrat + SQRes + 0")
    
    # Caso Prático
    st.markdown(r"### 📈 Caso de Aplicação: Eficácia de Analgésicos")
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Teste de Formulações Farmacêuticas")
        st.markdown(r"Um laboratório avalia três formulações (A, B, C) de um novo analgésico. Dados de latência (n=5 por grupo):")
        st.latex(r"n_A=5, \bar{Y}_A=22; \quad n_B=5, \bar{Y}_B=16; \quad n_C=5, \bar{Y}_C=29; \quad \bar{Y}_{..} = 22.33")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- **SQTrat (Entre Grupos):**")
        st.latex(r"SQTrat = 5[(22-22.33)^2 + (16-22.33)^2 + (29-22.33)^2] = 423.35")
        
        st.markdown(r"- **SQRes (Dentro dos Grupos):**")
        st.write(r"Calculando o resíduo para cada grupo individualmente:")
        st.latex(r"SQRes_A = 26; \quad SQRes_B = 10; \quad SQRes_C = 10")
        st.latex(r"SQRes = 26 + 10 + 10 = 46")
        
        st.success(r"**Laudo da Análise:** A disparidade significativa entre o efeito de tratamento (423.35) e o erro residual (46) confirma a relevância estatística. Recomenda-se a adoção do Fármaco B devido à sua performance superior na redução da latência da dor.")
 
    # O código abaixo é estático, hardcoded e desenhado para o contexto educacional de alto nível.
    
    # 1. Cabeçalho do Subtópico
    st.header(r"O Modelo Linear de Efeitos Fixos: Suposições e Formalismo")
    
    # 2. Introdução: O Contexto da Inferencia
    st.markdown(r"""
    A estatística moderna, enquanto ciência da inferência indutiva a partir de dados amostrais, encontrou no desenvolvimento da Análise de Variância (ANOVA) um de seus pilares mais robustos. A transição para o modelo de efeitos fixos representou uma mudança de paradigma: deixamos de apenas comparar médias para **parametrizar o processo gerador de dados**.
    """)
    
    st.markdown(r"""
    Nesta abordagem, reconhecemos que a observação experimental é composta por uma combinação aditiva de:
    *   **Tendência Central ($\mu$):** O nível de base do fenômeno.
    *   **Efeito de Tratamento ($\alpha_i$):** A magnitude do desvio imposta pelo nível do fator.
    *   **Ruído Estocástico ($\epsilon_{ij}$):** Flutuações aleatórias inerentes ao sistema.
    """)
    
    # 3. Formalismo do Modelo
    st.subheader(r"📐 Estrutura Matemática: O Modelo de Efeitos Fixos")
    st.markdown(r"O formalismo que sustenta esta estrutura é expresso pela equação fundamental que rege o comportamento dos dados sob a hipótese de linearidade e aditividade:")
    
    st.latex(r"Y_{ij} = \mu + \alpha_i + \epsilon_{ij}, \quad \sum \alpha_i = 0, \quad \epsilon_{ij} \sim i.i.d. N(0, \sigma^2)")
    
    st.info(r"**Nota de Identificabilidade:** A restrição $\sum \alpha_i = 0$ não é uma convenção trivial, mas uma necessidade lógica. Sem ela, o sistema seria sobre-parametrizado, impedindo a inversão matricial necessária para estimar os parâmetros do modelo.")
    
    # 4. Demonstração Analítica (Linhas estáticas, sem loops)
    st.subheader(r"🧮 Propriedades Analíticas dos Estimadores")
    
    st.markdown(r"Abaixo, destacamos as propriedades fundamentais que permitem a partição da variância, coração da ANOVA:")
    
    st.markdown(r"**Expectativa da observação:**")
    st.latex(r"E[Y_{ij}] = \mu + \alpha_i")
    
    st.markdown(r"**Variância da observação (Homocedasticidade):**")
    st.latex(r"Var(Y_{ij}) = Var(\epsilon_{ij}) = \sigma^2")
    
    st.markdown(r"**Estimativa do Erro Quadrático Médio (MSE):**")
    st.latex(r"MSE = \frac{SQRes}{n_T - k}")
    
    st.markdown(r"**Valor esperado do MSE (Consistência):**")
    st.latex(r"E[MSE] = \sigma^2")
    
    # 5. Exemplo Prático
    st.subheader(r"📈 Caso de Aplicação: Resistência de Polímeros")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Estudo de Tensão de Ruptura")
        st.markdown(r"""
        Em um estudo de engenharia de materiais, testou-se a tensão de ruptura de um polímero submetido a três temperaturas de cura (100°C, 150°C, 200°C), com 6 espécimes por grupo.
        """)
        
        # Criando tabela de dados sumários de forma estática
        import pandas as pd
        df_sumario = pd.DataFrame({
            "Parâmetro": ["Níveis (k)", "Amostras por grupo (n)", "Total (N)", "Nível de Significância (α)"],
            "Valor": [3, 6, 18, 0.05]
        })
        st.table(df_sumario)
    
        st.markdown(r"**Parâmetros de Variância:**")
        st.latex(r"SQTrat = 450, \quad SQRes = 300")
    
        st.markdown(r"**Desenvolvimento Aritmético:**")
        st.markdown(r"- $gl_{Trat} = k - 1 = 2$")
        st.markdown(r"- $gl_{Res} = N - k = 15$")
        st.markdown(r"- $QMTrat = 450 / 2 = 225$")
        st.markdown(r"- $QMRes = 300 / 15 = 20$")
        st.markdown(r"- $F_{calc} = 225 / 20 = 11.25$")
    
        st.success(r"**Conclusão e Laudo:** O valor calculado de $F=11.25$ excede o valor crítico da tabela para $(2, 15)$ graus de liberdade. Rejeita-se a hipótese nula: a temperatura de cura exerce uma influência estatisticamente significante na resistência do polímero.")
    
    # 6. Considerações Finais
    st.markdown(r"""
    **Nota sobre Validação:** O processo de inferência não termina no cálculo do valor-p. A inspeção diagnóstica dos resíduos (análise de *Q-Q Plots* e resíduos vs. valores ajustados) é indispensável para garantir que as premissas de normalidade e homocedasticidade não foram violadas, sob o risco de invalidar a integridade estatística da análise.
    """)

    import streamlit as st
    import plotly.graph_objects as go
    import numpy as np
    
    # Cabeçalho do Subtópico
    st.header(r"Graus de Liberdade e a Dinâmica da Variabilidade")
    
    # Introdução e Contextualização
    st.markdown(r"""
    A compreensão profunda da estatística inferencial, particularmente no domínio da Análise de Variância (ANOVA), exige que transcendamos a mera aplicação de fórmulas e alcancemos uma visão geométrica e algébrica do espaço amostral. O conceito de "Graus de Liberdade" (gl) não é, como frequentemente confundido por estudantes iniciantes, uma métrica de contagem simples, mas sim uma medida da dimensão funcional da variabilidade que reside em um conjunto de dados.
    
    Quando observamos um conjunto de $N$ valores, a intuição matemática nos dita que possuímos $N$ unidades de informação. Contudo, ao impormos a estrutura de um modelo estatístico — como a estimativa de uma média amostral para definir um centro de referência —, sacrificamos uma dimensão dessa liberdade. A restrição imposta pelo cálculo da média faz com que, dado o conhecimento de $N-1$ observações e do valor da média, o último ponto do conjunto de dados torne-se automaticamente determinado.
    """)
    
    st.info(r"**Princípio Fundamental:** A perda de graus de liberdade não é uma falha procedimental, mas o preço necessário para ancorar nossas estimativas em parâmetros populacionais desconhecidos, corrigindo o enviesamento inerente às amostras finitas.")
    
    st.markdown(r"""
    ### 📐 A Arquitetura Algébrica dos Graus de Liberdade
    
    A sistematização deste conceito, impulsionada pelo rigor geométrico de Ronald A. Fisher, permite-nos tratar o erro residual e a variância dos tratamentos como vetores em um espaço de alta dimensão. A decomposição formal segue a arquitetura abaixo:
    """)
    
    # Exibição do Formalismo
    st.latex(r"gl_{Total} = N - 1, \quad gl_{Trat} = k - 1, \quad gl_{Res} = N - k")
    
    # Simulação Dinâmica
    st.subheader(r"🎛️ Visualizador da Partição de Variância (SQTrat vs SQRes)")
    st.markdown(r"Utilize os controles abaixo para observar como a partição da variabilidade total altera a magnitude relativa das fontes de variação.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        sq_total = st.slider(r"Soma de Quadrados Total (SQ_Total)", min_value=1000, max_value=5000, value=3600, step=100, key=r"slider_sq_total")
    with col_b:
        perc_trat = st.slider(r"% Explicada pelo Tratamento", min_value=0, max_value=100, value=33, step=1, key=r"slider_perc_trat")
    
    sq_trat = (perc_trat / 100) * sq_total
    sq_res = sq_total - sq_trat
    
    # Gráfico de Partição
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=r'SQ Tratamento',
        x=[r'Partição de Variabilidade'],
        y=[sq_trat],
        marker_color=PRIMARY_BLUE
    ))
    fig.add_trace(go.Bar(
        name=r'SQ Residual (Erro)',
        x=[r'Partição de Variabilidade'],
        y=[sq_res],
        marker_color=SECONDARY_GREEN
    ))
    
    fig.update_layout(
        template="plotly_white",
        barmode='stack',
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title=dict(
            text="<b>Distribuição da Variabilidade Total</b>",
            font=dict(size=14, color="#1E293B", family="Arial, sans-serif"),
            x=0.0,
            y=0.95
        ),
        xaxis=dict(
            title=dict(text="Partição da Variabilidade", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            fixedrange=True
        ),
        yaxis=dict(
            title=dict(text="Soma de Quadrados (SQ)", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
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
    st.plotly_chart(fig, use_container_width=True, key=r"plotly_chart_subtopico_gl")
    
    # Dedução Analítica
    st.subheader(r"🧮 A Decomposição da Variabilidade")
    st.markdown(r"A natureza aditiva e ortogonal da ANOVA garante que a soma dos graus de liberdade do tratamento e do erro resulte exatamente no total disponível:")
    
    st.latex(r"gl_{Total} = gl_{Trat} + gl_{Res}")
    st.markdown(r"Substituindo pelos valores estruturais do delineamento:")
    st.latex(r"N - 1 = (k - 1) + (N - k)")
    
    st.markdown(r"Esses valores são os divisores essenciais para converter a dispersão bruta (SQ) em estimativas de variância imparciais (Quadrados Médios):")
    st.latex(r"QMTrat = \frac{SQTrat}{k-1}")
    st.latex(r"QMRes = \frac{SQRes}{N-k}")
    
    # Exemplo Prático
    st.subheader(r"📈 Casos de Aplicação Prática: Análise de Produtividade Agrícola")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Variabilidade em Culturas de Soja")
        st.markdown(r"Um agrônomo analisa a produtividade (kg/ha) de 4 variedades de soja (V1, V2, V3, V4). Foram realizadas 10 parcelas para cada variedade ($N=40$). As somas de quadrados calculadas foram: SQTrat = 1200 e SQRes = 2400.")
        
        st.latex(r"k=4, \quad N=40, \quad SQTrat=1200, \quad SQRes=2400")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- $gl_{Trat} = 4 - 1 = 3$")
        st.markdown(r"- $gl_{Res} = 40 - 4 = 36$")
        st.markdown(r"- $QMTrat = 1200 / 3 = 400$")
        st.markdown(r"- $QMRes = 2400 / 36 = 66.67$")
        st.markdown(r"- $F_{calc} = 400 / 66.67 = 6.00$")
        
        st.success(r"**Conclusão e Laudo:** Com uma estatística F de 6.00, superior ao valor crítico (alpha=0.05), concluímos que as variedades de soja diferem em produtividade. A variabilidade entre variedades supera em 6 vezes o ruído experimental, justificando a escolha da variedade de maior rendimento.")

    import streamlit as st
    import numpy as np
    import plotly.graph_objects as go
    from scipy.stats import f
    
    # Definição das Cores do Tema
    PRIMARY_BLUE = "#1E3A8A"
    SECONDARY_GREEN = "#10B981"
    WARNING_AMBER = "#F59E0B"
    CRITICAL_RED = "#991B1B"
    
    st.header(r"A Estatística F e a Regra de Decisão Inferencial")
    
    st.markdown(r"""
    A conclusão do procedimento de ANOVA culmina na construção da estatística F de Snedecor. Esta estatística, definida como a razão entre o Quadrado Médio do Tratamento (que quantifica a variação entre grupos) e o Quadrado Médio do Resíduo (que quantifica a variação interna), atua como o termômetro inferencial do experimento.
    """)
    
    st.info(r"""
    **O Paradigma Inferencial da ANOVA:**
    - **Sob a Hipótese Nula ($H_0$):** Ambos os quadrados médios são estimadores da mesma variância populacional $\sigma^2$, resultando em um valor F próximo à unidade.
    - **Sob o Efeito do Tratamento:** O numerador é inflado pela presença dos efeitos $\alpha_i$, deslocando a estatística para a cauda superior da distribuição F.
    - **Decisão:** Quando a probabilidade acumulada (p-valor) torna-se inferior ao nível de significância, rejeitamos a hipótese nula.
    """)
    
    st.markdown(r"""
    O advento da Análise de Variância, concebida por Sir Ronald A. Fisher, resolveu o dilema das comparações múltiplas, onde a aplicação sucessiva de testes t de Student inflava descontroladamente a probabilidade de erro do Tipo I. Ao particionar a variabilidade total, Fisher criou um método holístico capaz de avaliar efeitos independentemente do número de grupos.
    """)
    
    st.subheader(r"📐 O Coração Matemático: Formalismo e Particionamento")
    
    st.latex(r"F_{calc} = \frac{QMTrat}{QMRes} \sim F_{(k-1, N-k)}")
    
    st.markdown(r"A dedução analítica desta relação observa os graus de liberdade como divisores essenciais para a obtenção de estimadores não viciados:")
    
    st.latex(r"F_{calc} = \frac{SQTrat / (k - 1)}{SQRes / (N - k)}")
    
    st.markdown(r"A decisão estatística é tomada confrontando o valor calculado com o limiar crítico da distribuição:")
    
    st.latex(r"P(F_{calc} > F_{crit; \alpha, k-1, N-k}) = \alpha")
    
    st.markdown(r"Ou, de forma mais moderna, pela avaliação da significância p:")
    
    st.latex(r"p\text{-valor} = P(F_{(k-1, N-k)} > F_{calc})")
    
    st.subheader(r"📊 Simulador: Explorador da Curva de Distribuição F")
    
    # Setup do Simulador
    col1, col2 = st.columns(2)
    with col1:
        df1 = st.slider(r"Graus de Liberdade do Numerador (k-1)", 1, 10, 2, key=r"slider_df1_f_dist")
    with col2:
        df2 = st.slider(r"Graus de Liberdade do Denominador (N-k)", 5, 50, 27, key=r"slider_df2_f_dist")
    
    # Cálculo do Gráfico
    x = np.linspace(0, 5, 500)
    y = f.pdf(x, df1, df2)
    f_crit = f.ppf(0.95, df1, df2)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=r"Distribuição F", line=dict(color=PRIMARY_BLUE, width=3)))
    fig.add_shape(type="line", x0=f_crit, y0=0, x1=f_crit, y1=max(y), line=dict(color=CRITICAL_RED, dash="dash"))
    
    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title=dict(
            text="<b>Distribuição F e Região Crítica (α = 0.05)</b>",
            font=dict(size=14, color="#1E293B", family="Arial, sans-serif"),
            x=0.0,
            y=0.95
        ),
        xaxis=dict(
            title=dict(text="Valor de F", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            fixedrange=True
        ),
        yaxis=dict(
            title=dict(text="Densidade", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
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
    st.plotly_chart(fig, use_container_width=True, key=r"plotly_chart_subtopico_4")
    
    st.subheader(r"📈 Casos de Aplicação Prática: Análise de Semicondutores")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Indústria de Semicondutores")
        st.markdown(r"Uma indústria de semicondutores avalia a taxa de falha (ppm) de microchips sob três condições de voltagem (3.3V, 5V, 12V) com 10 chips testados em cada condição. Obteve-se $QMTrat = 500$ e $QMRes = 250$. Calcule o valor de F e determine a significância ao nível de 0.05.")
        
        st.latex(r"QMTrat=500, \quad QMRes=250, \quad gl_{Trat}=2, \quad gl_{Res}=27")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Cálculo da Estatística F: $F_{calc} = 500 / 250 = 2$")
        st.markdown(r"- Comparação com valor crítico: $F_{crit(2, 27) @ 0.05} \approx 3.35$")
        st.markdown(r"- Verificação da condição: $2 < 3.35$")
        
        st.success(r"Conclusão: Como a estatística F (2.0) é menor que o valor crítico (3.35), não há evidência estatística para rejeitar a hipótese nula. A taxa de falha não apresenta diferenças significativas entre as voltagens testadas. Recomenda-se manter o processo atual de voltagem, pois as variações observadas são estatisticamente atribuíveis ao acaso.")

    st.markdown('---')
    st.markdown('##### 📚 Referências Bibliográficas Consolidadas (Rodapé da Aula)')
    st.markdown(r'- Bispo, Nívea - Introdução aos Modelos Lineares, Aula 15: O procedimento geral da Análise de Variância, pp. 8-12.')
    st.markdown(r'- Montgomery, D. C. - Design and Analysis of Experiments, 8th Edition, Cap 3: Experiments with a Single Factor, pp. 65-80.')
    st.markdown(r'- Morettin, P. A. & Bussab, W. O. - Estatística Básica, 9ª Edição, Cap 15: Análise de Variância, pp. 410-425.')

with tab_exercicios:
    import json
    dados_exercicios = json.loads(r"""{"topico_aula": "5.1 – O procedimento geral da análise de variância (ANOVA)", "questoes_multipla_escolha": [{"enunciado": "Em um estudo clínico para avaliar a eficácia de quatro novos fármacos neurotrópicos na redução da latência de disparo neural, um pesquisador decide comparar as médias dos tempos de resposta entre os quatro grupos utilizando múltiplos testes t de Student para cada par de grupos (ex: Drug 1 vs. Drug 2, Drug 1 vs. Drug 3, etc.). Considerando o rigor estatístico, qual é a principal falha procedimental deste pesquisador ao não utilizar a ANOVA?", "alternativas": {"A": "O teste t de Student não possui poder estatístico suficiente para comparar médias de diferentes grupos experimentais, independentemente da quantidade de grupos.", "B": "A utilização de múltiplos testes t de Student inflaciona severamente o Erro Tipo I (probabilidade de detectar uma diferença falsa onde não existe), devido ao problema da taxa de erro familiar (family-wise error rate).", "C": "O modelo ANOVA exige necessariamente que os dados sigam uma distribuição de Poisson, enquanto o teste t exige normalidade, tornando a comparação matematicamente incompatível.", "D": "O teste t de Student é restrito a amostras com tamanho $n < 30$, sendo a ANOVA a única técnica capaz de lidar com amostras grandes.", "E": "A ANOVA é, na verdade, uma simplificação do teste t de Student, e não existe diferença procedimental entre os dois métodos para mais de dois grupos."}, "alternativa_correta": "B", "dica": "Reflita sobre o que acontece com a probabilidade acumulada de rejeitar a hipótese nula quando você realiza vários testes sucessivos de comparação de médias ao nível $\alpha$.", "gabarito_comentado": "A utilização de múltiplos testes t de Student para comparar $k$ grupos resulta na inflação do Erro Tipo I. Se cada teste é realizado com um nível de significância $\alpha = 0,05$, a probabilidade de cometer pelo menos um Erro Tipo I ao realizar múltiplos testes cresce exponencialmente. A ANOVA corrige isso ao avaliar todas as médias simultaneamente sob a hipótese $H_0: \alpha_1 = \alpha_2 = \dots = \alpha_k = 0$, mantendo a taxa de erro global sob controle."}, {"enunciado": "Considere que, na decomposição da variabilidade total de um experimento sobre o efeito de diferentes dietas na plasticidade sináptica, observou-se que a $SQTrat$ é muito próxima de zero e a $SQRes$ é elevada. Qual conclusão estatística é mais provável para a estatística $F_{\text{calc}}$ e a decisão sobre a hipótese nula?", "alternativas": {"A": "A estatística $F_{\text{calc}}$ será muito alta, levando à rejeição de $H_0$ e indicando que os efeitos dos tratamentos são altamente significativos.", "B": "A estatística $F_{\text{calc}}$ será aproximadamente 1, indicando que o tratamento explica a maior parte da variabilidade dos dados.", "C": "A estatística $F_{\text{calc}}$ será muito baixa (próxima de zero), indicando que a variabilidade entre grupos é desprezível comparada ao ruído residual, sugerindo a não rejeição de $H_0$.", "D": "O valor de $F_{\text{calc}}$ será negativo, o que é matematicamente impossível, indicando erro na coleta dos dados experimentais.", "E": "A estatística $F_{\text{calc}}$ será igual à $SQTot$, o que invalida o teste de hipótese realizado.", "F": "A estatística $F_{\text{calc}}$ será zero, pois o tratamento não causa efeito e a variação interna é nula."}, "alternativa_correta": "C", "dica": "Lembre-se que $F_{\text{calc}} = \frac{QMTrat}{QMRes}$. Se o numerador é quase zero e o denominator é grande, qual o comportamento da razão?", "gabarito_comentado": "A estatística $F_{\text{calc}}$ é a razão entre o Quadrado Médio do Tratamento ($QMTrat$) e o Quadrado Médio do Erro ($QMRes$). Se a $SQTrat$ é próxima de zero, significa que as médias dos grupos são muito semelhantes entre si e próximas da média global ($\bar{Y}_{..}$). Com um $QMRes$ elevado (muito ruído), a razão $QMTrat / QMRes$ tende a zero. Valores de $F_{\text{calc}}$ próximos de zero indicam que não há evidência suficiente para rejeitar a hipótese nula de que as médias são iguais."}, {"enunciado": "Em uma análise de variância de um experimento com $k=3$ grupos e $n=10$ observações por grupo, o número total de observações é $N=30$. Quais são os graus de liberdade associados ao numerador ($gl_{\text{num}}$) e ao denominador ($gl_{\text{den}}$) para a estatística $F_{\text{calc}}$?", "alternativas": {"A": "$gl_{\text{num}} = 3$ e $gl_{\text{den}} = 30$.", "B": "$gl_{\text{num}} = 2$ e $gl_{\text{den}} = 27$.", "C": "$gl_{\text{num}} = 29$ e $gl_{\text{den}} = 3$.", "D": "$gl_{\text{num}} = 30$ e $gl_{\text{den}} = 2$.", "E": "$gl_{\text{num}} = 10$ e $gl_{\text{den}} = 20$."}, "alternativa_correta": "B", "dica": "Verifique a definição de graus de liberdade na teoria: $gl_{\text{num}} = k - 1$ e $gl_{\text{den}} = N - k$.", "gabarito_comentado": "Aplicando as fórmulas fornecidas na teoria: $gl_{\text{num}} = k - 1$. Como temos $k=3$ grupos, $gl_{\text{num}} = 3 - 1 = 2$. Para o denominador, usamos $gl_{\text{den}} = N - k$. Com $N=30$ e $k=3$, temos $gl_{\text{den}} = 30 - 3 = 27$. Portanto, a distribuição $F$ utilizada para o teste terá parâmetros $(2, 27)$."}, {"enunciado": "Qual das seguintes suposições é fundamental para a validade do procedimento de ANOVA descrito no modelo $Y_{ij} = \mu + \alpha_i + \epsilon_{ij}$?", "alternativas": {"A": "Os erros aleatórios $\epsilon_{ij}$ devem seguir uma distribuição não-paramétrica qualquer.", "B": "A variância do erro $\sigma^2$ deve variar proporcionalmente entre os grupos, conforme aumenta a média do grupo.", "C": "Os erros aleatórios $\epsilon_{ij}$ devem ser independentes, identicamente distribuídos e seguir uma distribuição normal $N(0, \sigma^2)$.", "D": "O efeito do tratamento $\alpha_i$ deve ser sempre positivo para garantir a estabilidade da variância.", "E": "A média global $\mu$ deve ser igual a zero para que o teste $F$ seja válido."}, "alternativa_correta": "C", "dica": "Releia a seção sobre o formalismo do termo de erro $\epsilon_{ij}$ no modelo linear.", "gabarito_comentado": "O modelo linear de efeitos fixos assume que os erros $\epsilon_{ij}$ são independentes, têm média zero, variância constante $\sigma^2$ (homocedasticidade) e seguem uma distribuição normal. Essas premissas garantem que a estatística $F_{\text{calc}}$ siga exatamente a distribuição $F$ de Snedecor sob a hipótese nula."}, {"enunciado": "No contexto da ANOVA, o que representa a Soma de Quadrados dos Tratamentos ($SQTrat$)?", "alternativas": {"A": "A variabilidade total observada entre todas as unidades experimentais independentemente do grupo.", "B": "A variação inerente de cada observação em relação à média do seu próprio grupo, representando o ruído experimental.", "C": "A dispersão das médias dos grupos em relação à média global, capturando o efeito sistemático dos tratamentos.", "D": "O valor quadrático da média aritmética de todas as observações do experimento.", "E": "A diferença entre o maior valor observado e o menor valor observado em todo o conjunto de dados."}, "alternativa_correta": "C", "dica": "Pense em termos de 'sinal vs ruído'. O que a ANOVA tenta isolar quando compara grupos?", "gabarito_comentado": "A $SQTrat$ (ou soma de quadrados entre grupos) quantifica o quanto as médias dos grupos ($\bar{Y}_{i.}$) desviam-se da média global ($\bar{Y}_{..}$). É a componente que reflete o 'sinal' ou o efeito dos níveis do fator. Se esta componente for grande, as médias dos grupos são distantes entre si, o que é evidência contra a hipótese de igualdade de médias."}], "questoes_discursivas": [{"enunciado": "Considere um experimento neurocientífico onde três regiões do hipocampo (Grupos A, B e C) tiveram a expressão de uma proteína medida. Os dados (em unidades arbitrárias) são: Grupo A: {10, 12, 11}; Grupo B: {15, 17, 16}; Grupo C: {11, 13, 12}. Calcule a Média Global ($\bar{Y}_{..}$), a $SQTrat$ e a $SQRes$.", "dica": "Lembre-se de calcular primeiro a média de cada grupo e depois a média de todas as observações (média global).", "gabarito_passo_a_passo": ["Passo 1: Calcular médias dos grupos. $\bar{Y}_{A} = (10+12+11)/3 = 11$; $\bar{Y}_{B} = (15+17+16)/3 = 16$; $\bar{Y}_{C} = (11+13+12)/3 = 12$.", "Passo 2: Calcular a Média Global $\bar{Y}_{..} = (11+16+12)/3 = 13$.", "Passo 3: Calcular $SQTrat = n \sum (\bar{Y}_{i.} - \bar{Y}_{..})^2$. Aqui $n=3$. $SQTrat = 3 * [(11-13)^2 + (16-13)^2 + (12-13)^2] = 3 * [4 + 9 + 1] = 3 * 14 = 42$.", "Passo 4: Calcular $SQRes = \sum (Y_{ij} - \bar{Y}_{i.})^2$. Grupo A: $(10-11)^2 + (12-11)^2 + (11-11)^2 = 1+1+0 = 2$. Grupo B: $(15-16)^2 + (17-16)^2 + (16-16)^2 = 1+1+0 = 2$. Grupo C: $(11-12)^2 + (13-12)^2 + (12-12)^2 = 1+1+0 = 2$.", "Passo 5: $SQRes = 2 + 2 + 2 = 6$."]}, {"enunciado": "Explique, do ponto de vista do formalismo matemático da ANOVA, por que a variância é decomposta em 'Tratamento' e 'Resíduo'. Como essa decomposição afeta a construção do teste $F$?", "dica": "Considere a identidade algébrica $SQTot = SQTrat + SQRes$ e a natureza dos estimadores de variância.", "gabarito_passo_a_passo": ["Passo 1: A identidade $SQTot = SQTrat + SQRes$ deriva da partição dos desvios de cada observação: $(Y_{ij} - \bar{Y}_{..}) = (Y_{ij} - \bar{Y}_{i.}) + (\bar{Y}_{i.} - \bar{Y}_{..})$.", "Passo 2: Ao elevar ao quadrado e somar, os termos cruzados se anulam (ortogonalidade), restando a soma das somas dos quadrados.", "Passo 3: O termo $SQTrat$ capta a variação sistemática (efeito dos fatores). O termo $SQRes$ capta a variação aleatória (ruído).", "Passo 4: Construímos $QMTrat = SQTrat / (k-1)$ e $QMRes = SQRes / (N-k)$, que são estimadores da variância populacional $\sigma^2$ sob a hipótese nula.", "Passo 5: A estatística $F = QMTrat / QMRes$ compara esses dois estimadores. Se $H_0$ é falsa, $QMTrat$ infla devido aos efeitos reais $\alpha_i$, tornando $F$ grande e levando à rejeição de $H_0$."]}, {"enunciado": "Você possui um output de uma ANOVA com os seguintes dados: $N=20$ observações totais, $k=4$ grupos, $SQTot = 100$ e $SQRes = 40$. Calcule o valor da estatística $F_{\text{calc}}$ e determine os graus de liberdade.", "dica": "Utilize a relação $SQTot = SQTrat + SQRes$ para encontrar $SQTrat$ antes de calcular os Quadrados Médios.", "gabarito_passo_a_passo": ["Passo 1: Identificar os componentes: $N=20$, $k=4$.", "Passo 2: Calcular $SQTrat = SQTot - SQRes = 100 - 40 = 60$.", "Passo 3: Calcular os Graus de Liberdade: $gl_{\text{num}} = k - 1 = 4 - 1 = 3$. $gl_{\text{den}} = N - k = 20 - 4 = 16$.", "Passo 4: Calcular Quadrados Médios: $QMTrat = SQTrat / gl_{\text{num}} = 60 / 3 = 20$. $QMRes = SQRes / gl_{\text{den}} = 40 / 16 = 2.5$.", "Passo 5: Calcular $F_{\text{calc}} = QMTrat / QMRes = 20 / 2.5 = 8.0$."]}]}""")
 
    import streamlit as st
    
    # Assumindo que 'dados_exercicios' já está disponível no escopo
    
    st.header(f"Exercícios: {dados_exercicios.get('topico_aula', 'Aula')}")
    
    # --- Seção de Questões de Múltipla Escolha ---
    st.subheader("📝 Questões de Múltipla Escolha")
    
    for i, questao in enumerate(dados_exercicios.get("questoes_multipla_escolha", [])):
        st.markdown(f"**Questão {i+1}:** {questao.get('enunciado', 'Enunciado não disponível')}")
        
        alternativas = questao.get("alternativas", {})
        
        # Renderização da radio button com formatação
        escolha = st.radio(
            "Selecione uma alternativa:",
            options=list(alternativas.keys()),
            format_func=lambda x: f"{x}) {alternativas.get(x, '')}",
            key=f"mcq_radio_{i}"
        )
        
        # Botão de Dica
        if st.button("💡 Dica", key=f"mcq_hint_{i}"):
            st.info(questao.get("dica", "Dica não disponível."))
            
        # Botão de Verificação
        if st.button("✅ Verificar Resposta", key=f"mcq_check_{i}"):
            if escolha == questao.get("alternativa_correta"):
                st.success("Correto! Muito bem.")
            else:
                st.error(f"Incorreto. A alternativa correta era a letra {questao.get('alternativa_correta')}.")
                
        # Gabarito Comentado
        with st.expander("✅ Ver Gabarito Comentado"):
            st.write(questao.get("gabarito_comentado", "Gabarito não disponível."))
        
        st.divider()
    
    # Questões Discursivas
    st.subheader("Questões Discursivas")
    for i, questao in enumerate(dados_exercicios.get("questoes_discursivas", [])):
        st.markdown(f"**Questão {i + 1}:** {questao.get('enunciado', 'Enunciado não disponível')}")
        
        # Área de texto para resposta
        st.text_area("Sua resposta:", key=f"disc_text_{i}")
        
        # Botão de Dica
        if st.button("💡 Dica", key=f"disc_hint_{i}"):
            st.info(questao.get("dica", "Dica não disponível."))
            
        # Resolução Detalhada
        with st.expander("✅ Ver Resolução Detalhada"):
            passos = questao.get("gabarito_passo_a_passo", [])
            if passos:
                for idx, passo in enumerate(passos):
                    st.write(f"**Passo {idx + 1}:** {passo}")
            else:
                st.write("Resolução não disponível.")
                
        st.divider()
