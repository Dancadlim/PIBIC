import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stats
from scipy.stats import norm
import base64
import json

# Carregamento seguro dos metadados da aula para evitar SyntaxError
metadata = json.loads(base64.b64decode('eyJ0ZW1hX2dsb2JhbCI6ICJBbsOhbGlzZSBCaXZhcmlhZGEgZSBNb2RlbGFnZW0gZGUgUmVncmVzc8OjbyBMaW5lYXI6IEZ1bmRhbWVudG9zLCBPdGltaXphw6fDo28gZSBEaWFnbsOzc3RpY28iLCAicmVmZXJlbmNpYXNfYmlibGlvZ3JhZmljYXNfZmluYWlzIjogWyJCdXNzYWIgJiBNb3JldHRpbiwgRXN0YXTDrXN0aWNhIELDoXNpY2EgLSBDYXAuIDksIHBwLiAyMTAtMjE1IiwgIkJ1c3NhYiAmIE1vcmV0dGluLCBFc3RhdMOtc3RpY2EgQsOhc2ljYSAtIENhcC4gMTEsIHBwLiAyNDUtMjQ4IiwgIkJ1c3NhYiAmIE1vcmV0dGluLCBFc3RhdMOtc3RpY2EgQsOhc2ljYSAtIENhcC4gMTUsIHBwLiAzNDUtMzUyIiwgIkJ1c3NhYiAmIE1vcmV0dGluLCBFc3RhdMOtc3RpY2EgQsOhc2ljYSAtIENhcC4gMTYsIHBwLiAzMDItMzA4IiwgIkJ1c3NhYiAmIE1vcmV0dGluLCBFc3RhdMOtc3RpY2EgQsOhc2ljYSAtIENhcC4gMTYsIHBwLiAzMTAtMzE1IiwgIldvb2xkcmlkZ2UsIEludHJvZHXDp8OjbyDDoCBFY29ub21ldHJpYSAtIENhcC4gMiwgcHAuIDIzLTQyIiwgIldvb2xkcmlkZ2UsIEludHJvZHXDp8OjbyDDoCBFY29ub21ldHJpYSAtIENhcC4gMywgcHAuIDcwLTg1IiwgIldvb2xkcmlkZ2UsIEludHJvZHXDp8OjbyDDoCBFY29ub21ldHJpYSAtIENhcC4gNiwgcHAuIDE4NS0xOTAiLCAiR3VqYXJhdGkgJiBQb3J0ZXIsIEVjb25vbWV0cmlhIELDoXNpY2EgLSBDYXAuIDMsIHBwLiA2MC03NSJdfQ==').decode('utf-8'))

# Injeção de Estilos CSS Acadêmicos Premium
st.markdown("""
    <style>
        .premium-title { font-size: 2.2rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0.2rem; }
        .premium-subtitle { font-size: 1.1rem; color: #64748B; margin-bottom: 1.5rem; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="premium-title">{metadata["tema_global"]}</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">Conteúdo Acadêmico Digital e Simuladores Integrados</div>', unsafe_allow_html=True)

# Definição de Cores Globais da Paleta Premium
PRIMARY_BLUE = "#1E3A8A"
SECONDARY_GREEN = "#10B981"
WARNING_AMBER = "#F59E0B"
CRITICAL_RED = "#991B1B"

# Criação das Duas Grandes Abas Globais
tab_conteudo, tab_exercicios = st.tabs(["📚 Conteúdo Acadêmico Interativo", "📝 Caderno de Exercícios"])

with tab_conteudo:

    import streamlit as st
    
    # Cabeçalho do Subtópico
    st.header(r"A Análise de Bivariada: Diagrama de Dispersão e Covariância")
    
    # Introdução e Contextualização
    st.markdown(r"""
    A transição da estatística univariada para a análise bivariada representa um salto epistemológico fundamental no método científico. Deixamos de contemplar fenômenos como entidades isoladas para compreendê-los como componentes integrantes de um sistema de interdependências dinâmicas.
    """)
    
    st.markdown(r"""
    A análise bivariada surge como uma resposta necessária à necessidade humana de identificar padrões de co-variação. Ao contrário da descrição univariada, que se limita à tendência central e dispersão de uma única variável, esta abordagem busca compreender como duas grandezas comportam-se conjuntamente, sendo o alicerce para a inferência estatística e a modelagem preditiva.
    """)
    
    st.info(r"💡 **Nota de Rigor:** A análise bivariada não é apenas uma extensão aritmética, mas sim uma ferramenta de investigação que permite discernir se desvios ocorrem de forma coordenada ou se são produtos do acaso.")
    
    # Ferramentas de Investigação
    st.subheader(r"👁️ Instrumentos de Análise: Dispersão e Covariância")
    st.markdown(r"""
    Para explorar a estrutura oculta entre duas variáveis, utilizamos dois instrumentos fundamentais:
    * **Diagrama de Dispersão (*Scatter Plot*):** Nossa ferramenta visual primordial. Permite identificar linearidades, tendências curvilíneas e a presença de *outliers* que podem enviesar severamente a análise.
    * **Covariância:** A métrica que quantifica a tendência de duas variáveis variarem juntas, servindo como base para a compreensão da direção da associação.
    """)
    
    # Lógica Matemática
    st.subheader(r"📐 A Lógica Matemática da Covariância")
    st.markdown(r"A covariância amostral entre duas variáveis aleatórias $X$ e $Y$ quantifica o grau em que as variáveis mudam em conjunto. O formalismo matemático é definido como:")
    st.latex(r"S_{XY} = \frac{1}{n-1} \sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})")
    st.markdown(r"A correção de Bessel ($n-1$) é aplicada no denominador para garantir que a estimativa da covariância populacional seja não viesada, compensando a redução dos graus de liberdade inerente ao uso das médias amostrais.")
    
    # Desenvolvimento Analítico
    st.subheader(r"⚙️ Desenvolvimento Analítico da Fórmula")
    st.markdown(r"Podemos decompor o somatório para uma computação mais eficiente. Partimos da definição original:")
    st.latex(r"S_{XY} = \frac{1}{n-1} \sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})")
    st.markdown(r"Expandindo o produto dos desvios dentro do somatório:")
    st.latex(r"(X_i - \bar{X})(Y_i - \bar{Y}) = X_i Y_i - X_i \bar{Y} - Y_i \bar{X} + \bar{X} \bar{Y}")
    st.markdown(r"Distribuindo o somatório:")
    st.latex(r"\sum (X_i Y_i - X_i \bar{Y} - Y_i \bar{X} + \bar{X} \bar{Y}) = \sum X_i Y_i - \bar{Y} \sum X_i - \bar{X} \sum Y_i + n \bar{X} \bar{Y}")
    st.markdown(r"Aplicando as identidades das médias ($\sum X_i = n \bar{X}$):")
    st.latex(r"\sum X_i Y_i - \bar{Y} (n \bar{X}) - \bar{X} (n \bar{Y}) + n \bar{X} \bar{Y}")
    st.markdown(r"Chegamos à fórmula computacional simplificada:")
    st.latex(r"S_{XY} = \frac{1}{n-1} (\sum X_i Y_i - n \bar{X} \bar{Y})")
    
    # Exemplo Prático
    st.subheader(r"📈 Caso de Aplicação: Controle de Qualidade na Manufatura")
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Correlação entre Temperatura e Desgaste")
        st.markdown(r"Um engenheiro de qualidade mede a temperatura de operação ($X$, em °C) e o desgaste de peças ($Y$, em μm) em 5 unidades. Analisamos a relação entre estas variáveis para prever falhas.")
        st.latex(r"X = \{20, 22, 24, 26, 28\}, \quad Y = \{5, 7, 8, 10, 12\}, \quad \bar{X} = 24, \quad \bar{Y} = 8.4")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Desvios de $X$: $\{-4, -2, 0, 2, 4\}$")
        st.markdown(r"- Desvios de $Y$: $\{-3.4, -1.4, -0.4, 1.6, 3.6\}$")
        st.markdown(r"- Produtos dos desvios: $\{13.6, 2.8, 0, 3.2, 14.4\}$")
        st.markdown(r"- Somatório: $34$")
        st.markdown(r"- Covariância: $34 / (5-1) = 8.5$")
        
        st.success(r"**Conclusão:** A covariância de 8.5 indica uma associação linear positiva forte. O aumento da temperatura está diretamente vinculado ao desgaste das peças, recomendando a implementação de sistemas de refrigeração.")

    import streamlit as st
    import pandas as pd
    import numpy as np
    
    # Cabeçalho do subtópico
    st.header(r"Mensuração da Associação: O Coeficiente de Correlação de Pearson")
    
    # Introdução e Contextualização
    st.markdown(r"A busca pela quantificação sistemática da interdependência entre variáveis fenômenas constitui um dos pilares fundamentais da estatística inferencial. Historicamente, o desenvolvimento do coeficiente de Pearson foi a resposta matemática à necessidade dos biometristas em compreender fenômenos como a hereditariedade e a variação antropométrica, problemas nos quais a intuição falhava diante da complexidade dos dados.")
    
    st.markdown(r"Para compreender a essência do coeficiente de Pearson, devemos considerar os seguintes princípios fundamentais:")
    
    st.markdown(r"""
    * **Normalização:** O coeficiente transforma a covariância em um índice adimensional entre -1 e 1, permitindo comparações independentes de unidades de medida.
    * **Termômetro de Linearidade:** Valores próximos a 1 indicam forte associação positiva, enquanto valores próximos a -1 indicam forte associação negativa.
    * **Limitações:** A ausência de correlação linear (0) não implica independência total, apenas a inexistência de uma relação de linha reta; o coeficiente é cego a padrões não-lineares.
    """)
    
    st.info(r"Nota Importante: É imprescindível realizar a inspeção visual prévia através de diagramas de dispersão, dado que o coeficiente é sensível a ruídos e outliers, que podem distorcer artificialmente a interpretação do fenômeno.")
    
    # Formalismo Matemático
    st.subheader(r"📐 O Formalismo Matemático: A Essência do Coeficiente")
    st.latex(r"r = \frac{\sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^{n} (X_i - \bar{X})^2 \sum_{i=1}^{n} (Y_i - \bar{Y})^2}}")
    
    # Deduções Analíticas
    st.markdown(r"### 🧠 Demonstração Analítica e Propriedades")
    st.markdown(r"Podemos decompor o coeficiente relacionando-o com a covariância e os desvios-padrão. A forma simplificada é dada pela razão entre a covariância e o produto dos desvios-padrão:")
    st.latex(r"r = S_{XY} / (S_X S_Y)")
    
    st.markdown(r"Expandindo os termos para a notação de somatórios, obtemos a expressão completa:")
    st.latex(r"r = \frac{\sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^{n} (X_i - \bar{X})^2} \sqrt{\sum_{i=1}^{n} (Y_i - \bar{Y})^2}}")
    
    st.markdown(r"A validade dos limites do coeficiente é garantida matematicamente pela desigualdade de Cauchy-Schwarz:")
    st.latex(r"| \sum u_i v_i | \leq \sqrt{\sum u_i^2} \sqrt{\sum v_i^2}")
    
    st.markdown(r"Dessa forma, demonstramos a restrição fundamental do índice:")
    st.latex(r"-1 \leq r \leq 1")
    
    # Casos de Aplicação Prática
    st.subheader(r"📈 Casos de Aplicação Prática: Eficácia Publicitária")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Análise de Campanha Publicitária")
        st.markdown(r"Uma empresa de software analisa o investimento em marketing (X, milhares de dólares) versus volume de vendas (Y, milhares de unidades).")
        
        # Dados estruturados
        df_exemplo = pd.DataFrame({
            "Investimento (X)": [2, 3, 5, 7, 8],
            "Vendas (Y)": [4, 5, 7, 10, 12]
        })
        st.dataframe(df_exemplo, use_container_width=True)
        
        st.latex(r"\bar{X} = 5, \bar{Y} = 7.6, \sum (X_i - \bar{X})(Y_i - \bar{Y}) = 34, \sum (X_i - \bar{X})^2 = 26, \sum (Y_i - \bar{Y})^2 = 45.2")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Passo 1: $r = 34 / \sqrt{26 * 45.2}$")
        st.markdown(r"- Passo 2: $r = 34 / \sqrt{1175.2}$")
        st.markdown(r"- Passo 3: $r = 34 / 34.281$")
        st.markdown(r"- Passo 4: $r \approx 0.9918$")
        
        st.success(r"Com r=0.99, existe uma correlação linear extremamente forte entre o investimento em marketing e vendas. A estratégia de alocação de recursos demonstra alta eficiência, sendo o volume de vendas previsível conforme o aumento do aporte publicitário.")

    import numpy as np
    import plotly.graph_objects as go
    import streamlit as st
    
    # Título Principal do Subtópico
    st.header(r"Estrutura do Modelo de Regressão Linear Simples")
    
    # Introdução e Prosa
    st.markdown(r"""
    A gênese da regressão linear simples não deve ser compreendida meramente como um exercício de ajuste de curvas, mas sim como um dos pilares mais robustos da inferência estatística. Antes do advento formal deste modelo, a ciência frequentemente se via limitada a descrições qualitativas ou à mera observação de correlações triviais, sem um arcabouço matemático que permitisse a decomposição sistemática da variabilidade de um fenômeno em componentes explicáveis e estocásticos.
    
    A regressão linear surge, portanto, como uma resposta à necessidade premente de simplificar a complexidade inerente aos fenômenos empíricos através de um prisma de parcimônia. Ao postularmos que a relação entre uma variável resposta ($Y$) e uma variável preditora ($X$) pode ser aproximada por uma função linear, exercemos um ato de abstração científica que nos permite isolar o efeito marginal de uma variável sobre a outra, mantendo o controle sobre as flutuações inevitáveis do mundo real.
    """)
    
    st.info(r"O modelo de regressão linear simples busca filtrar o 'ruído' dos dados para nos apresentar a tendência central da relação, permitindo previsões que, embora não isentas de erro, representam a melhor estimativa não viesada disponível sob os pressupostos estabelecidos.")
    
    st.markdown(r"""
    A formalização matemática que sustenta este paradigma é expressa pela equação fundamental abaixo, onde cada observação individual é decomposta em uma porção determinística (a combinação linear dos parâmetros) e uma porção estocástica (o termo de erro).
    """)
    
    st.latex(r"Y_i = \beta_0 + \beta_1 X_i + \varepsilon_i")
    
    st.markdown(r"""
    - **$\beta_0$ (Intercepto):** Estabelece o valor basal ou a expectativa da variável resposta quando a preditora é nula, atuando como um ponto de ancoragem no espaço cartesiano.
    - **$\beta_1$ (Coeficiente Angular):** É o coração dinâmico da equação, quantificando a magnitude e a direção da resposta em $Y$ para cada unidade incremental adicionada em $X$.
    - **$\varepsilon_i$ (Resíduo/Erro):** Carrega o peso ontológico de todos os fatores não incluídos no modelo ou inerentemente imprevisíveis. Não é um simples 'erro de medição', mas a variabilidade residual do sistema.
    """)
    
    # O Coração Matemático
    st.subheader(r"📐 O Coração Matemático: Deducão dos Estimadores da Regressão Linear Simples")
    
    st.markdown(r"A estimativa dos parâmetros é obtida minimizando a Soma dos Quadrados dos Erros (SQE):")
    st.latex(r"SQE = \sum (Y_i - \beta_0 - \beta_1 X_i)^2")
    
    st.markdown(r"Ao derivar parcialmente em relação a $\beta_0$ e igualar a zero, encontramos o intercepto:")
    st.latex(r"\frac{\partial SQE}{\partial \beta_0} = -2 \sum (Y_i - \beta_0 - \beta_1 X_i) = 0 \implies \hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}")
    
    st.markdown(r"De forma análoga, para a inclinação $\beta_1$:")
    st.latex(r"\frac{\partial SQE}{\partial \beta_1} = -2 \sum X_i (Y_i - \beta_0 - \beta_1 X_i) = 0")
    
    st.markdown(r"Resultando no estimador de mínimos quadrados ordinários:")
    st.latex(r"\hat{\beta}_1 = \frac{S_{XY}}{S_{XX}}")
    
    # Simulador Interativo
    st.subheader(r"📈 Simulador Interativo: Modelador Linear Dinâmico")
    
    col1, col2 = st.columns(2)
    with col1:
        beta0_sim = st.slider(r"Intercepto ($\beta_0$)", -5.0, 15.0, 1.0, 0.5, key="b0_subtopico_3")
    with col2:
        beta1_sim = st.slider(r"Inclinação ($\beta_1$)", -2.0, 5.0, 2.0, 0.1, key="b1_subtopico_3")
    
    # Gerando dados puramente como listas de float para evitar erro de __array_struct__
    x_plot = [float(v) for v in np.linspace(0, 10, 20)]
    y_vals_plot = [float(beta0_sim + beta1_sim * x) for x in x_plot]
    y_obs_plot = [float(y + np.random.normal(0, 1.5)) for y in y_vals_plot]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_plot, y=y_obs_plot, mode='markers', name='Dados Observados', marker=dict(color="#64748B")))
    fig.add_trace(go.Scatter(x=x_plot, y=y_vals_plot, mode='lines', name='Linha de Regressão', line=dict(color="#1E3A8A", width=3)))
    
    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        plot_bgcolor="white",
        paper_bgcolor="white",
        title=dict(text="<b>Modelador Linear Dinâmico</b>", font=dict(size=14, color="#1E293B", family="Arial, sans-serif"), x=0.0, y=0.95),
        xaxis=dict(title=dict(text="Variável X", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")), tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"), gridcolor="#E2E8F0", zerolinecolor="#CBD5E1", fixedrange=True),
        yaxis=dict(title=dict(text="Variável Y", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")), tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"), gridcolor="#E2E8F0", zerolinecolor="#CBD5E1", fixedrange=True),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0, font=dict(size=9, color="#64748B", family="Arial, sans-serif"), bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="#E2E8F0", borderwidth=1),
        hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_color="#1E293B", font_family="Arial, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True, key="plotly_chart_subtopico_3")
    
    # Exemplo Prático
    st.subheader(r"📊 Casos de Aplicação Prática: Modelo de Publicidade e Receita")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Impacto de Investimento em Publicidade")
        st.markdown(r"Um analista deseja estimar o efeito do investimento em publicidade ($X$) sobre a receita gerada ($Y$), em milhares de reais. Dados coletados: (1, 3), (2, 5), (3, 7), (4, 9), (5, 11).")
        st.latex(r"\bar{X} = 3, \quad \bar{Y} = 7, \quad S_{XY} = 20, \quad S_{XX} = 10")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- **Passo 1:** Cálculo da inclinação $\hat{\beta}_1 = S_{XY} / S_{XX} = 20 / 10 = 2$.")
        st.markdown(r"- **Passo 2:** Cálculo do intercepto $\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X} = 7 - 2(3) = 1$.")
        st.markdown(r"- **Passo 3:** Equação resultante $\hat{Y} = 1 + 2X$.")
        
        st.success(r"Conclusão: O modelo indica que cada R$ 1.000 investidos adicionam R$ 2.000 em receita, com uma base de R$ 1.000, validando o retorno positivo do investimento.")

    # Título do Subtópico
    st.header(r"Otimização Paramétrica: O Método dos Mínimos Quadrados")
    
    # Introdução e Contexto Histórico
    st.markdown(r"""
    A busca pela compreensão das relações entre variáveis constitui a pedra angular da ciência estatística moderna, representando uma transição fundamental da simples observação descritiva para a modelagem preditiva e inferencial. Historicamente, a necessidade de sintetizar conjuntos de dados complexos — um desafio clássico que perseguiu astrônomos e geodetas do século XVIII — exigiu o desenvolvimento de uma metodologia capaz de harmonizar observações conflitantes em uma estrutura analítica coerente.
    """)
    
    st.markdown(r"""
    Antes da formalização do Método dos Mínimos Quadrados (OLS), a resolução de sistemas de equações sobre-determinados dependia de heurísticas subjetivas. O advento desta técnica, creditada ao trabalho de Legendre e Gauss, permitiu que a comunidade científica tratasse o erro residual como uma métrica quantificável a ser minimizada, estabelecendo assim uma base objetiva para a estimação paramétrica.
    """)
    
    # Destaque do Conceito Central
    st.info(r"O cerne da metodologia reside na minimização da soma das distâncias verticais ao quadrado entre os dados observados e a reta de previsão. Esta escolha não é arbitrária: ao elevar os resíduos ao quadrado, o método garante a diferenciabilidade da função objetivo e penaliza desproporcionalmente valores discrepantes (*outliers*), conferindo estabilidade ao estimador.")
    
    # Equação Principal
    st.latex(r"SQE(\hat{\beta}_0, \hat{\beta}_1) = \sum_{i=1}^n (Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i)^2")
    
    # Detalhamento Teórico
    st.markdown(r"""
    Na prática, o modelo propõe que a "melhor" reta é aquela que minimiza a SQE. Esta formulação matemática resolve elegantemente o problema do cancelamento de sinais: resíduos positivos e negativos não se anulam, mas contribuem de forma cumulativa para a magnitude total do erro.
    """)
    
    st.markdown(r"""
    Além disso, as condições clássicas para a validade do OLS incluem:
    - **Linearidade:** O modelo é linear nos parâmetros.
    - **Independência:** Erros não possuem correlação serial.
    - **Homoscedasticidade:** A variância do erro é constante.
    - **Exogeneidade:** Os regressores são fixos ou independentes do erro.
    """)
    
    # Seção de Formalismo
    st.subheader(r"📐 O Coração Matemático: Derivação e Otimização")
    
    st.markdown(r"""
    Ao aplicar o cálculo diferencial para encontrar o ponto de otimalidade (onde as derivadas parciais são iguais a zero), chegamos às chamadas Equações Normais. Este procedimento revela que a solução ótima ocorre quando a média dos resíduos é nula e a informação contida neles é ortogonal ao espaço dos dados.
    """)
    
    st.latex(r"SQE = \sum (Y_i - \beta_0 - \beta_1 X_i)^2")
    
    st.markdown(r"Igualando as derivadas parciais a zero para o intercepto, encontramos a relação estrutural entre a média dos dados e a inclinação:")
    
    st.latex(r"\sum Y_i = n\hat{\beta}_0 + \hat{\beta}_1 \sum X_i")
    
    st.markdown(r"Resolvendo para o coeficiente angular, obtemos a fórmula do estimador, que captura a covariância entre as variáveis ajustada pela variância do regressor:")
    
    st.latex(r"\hat{\beta}_1 = \frac{\sum (X_i - \bar{X})(Y_i - \bar{Y})}{\sum (X_i - \bar{X})^2}")
    
    # Considerações Estratégicas
    st.subheader(r"🛡️ Considerações Estratégicas: Limitações e Robustez")
    
    st.warning(r"Embora o OLS seja o 'Best Linear Unbiased Estimator' (BLUE) sob condições ideais, o estatístico deve estar atento: por depender da elevação ao quadrado, o método é altamente sensível a observações extremas. Um único dado atípico pode exercer uma 'alavancagem' indevida, distorcendo os parâmetros. Diagnósticos de resíduos são, portanto, obrigatórios em qualquer análise rigorosa.")
    
    # Exemplo Prático
    st.subheader(r"📈 Casos de Aplicação Prática: Estimativa de Faturamento")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Elasticidade do Marketing no E-commerce")
        st.markdown(r"Pretendemos estimar o faturamento ($Y$) com base no investimento em marketing ($X$). Dados: $X=\{1,2,3,4,5\}$, $Y=\{3,5,7,9,11\}$.")
        
        st.latex(r"\bar{X}=3, \bar{Y}=7, \sum(X-\bar{X})(Y-\bar{Y})=20, \sum(X-\bar{X})^2=10")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Cálculo da inclinação: $\hat{\beta}_1 = 20 / 10 = 2$")
        st.markdown(r"- Cálculo do intercepto: $\hat{\beta}_0 = 7 - (2 \times 3) = 1$")
        
        st.success(r"O faturamento autônomo é 1 (mil reais) e cada unidade de marketing tem elasticidade de 2, permitindo previsões financeiras precisas.")

    import streamlit as st
    import numpy as np
    import plotly.graph_objects as go
    from scipy import stats
    
    # Título do Subtópico
    st.header(r"Diagnóstico de Ajuste: Análise e Interpretação de Resíduos")
    
    # Prosa Inicial
    st.markdown(r"""
    A modelagem estatística, em sua essência, não é apenas um exercício de ajuste de curvas ou de minimização de funções de perda, mas sim um ato epistemológico de representação de um fenômeno estocástico subjacente por meio de uma estrutura matemática finita. Quando propomos um modelo de regressão linear, estamos presumindo que a realidade observada pode ser decomposta em uma estrutura determinística, capturada pelos parâmetros do modelo, e um componente aleatório, frequentemente denominado erro.
    """)
    
    st.info(r"A presunção de que esse componente aleatório realmente se comporta como um ruído branco — independente e identicamente distribuído — é frequentemente violada na prática. A análise de resíduos é, portanto, a auditoria mais rigorosa e indispensável de todo o processo de inferência.")
    
    st.markdown(r"""
    Historicamente, a importância da análise de resíduos remonta aos primórdios da estatística inferencial. Com o advento da era computacional moderna, a capacidade de inspeção gráfica profunda permitiu que estatísticos transcendessem a simples métrica do coeficiente de determinação, percebendo que um R² elevado pode mascarar falhas estruturais profundas.
    
    **Por que a análise de resíduos é essencial?**
    *   **Detecção de Padrões:** Identifica se o modelo capturou toda a informação estrutural ou se restou sinal (tendência, curvatura) no erro.
    *   **Verificação de Hipóteses:** Confirma a homocedasticidade (variância constante) e a normalidade dos erros, fundamentais para a validade dos testes t.
    *   **Identificação de Outliers:** Revela pontos influentes que podem estar distorcendo as estimativas dos coeficientes.
    """)
    
    # Formalismo Matemático
    st.subheader(r"### 🔍 O Formalismo Matemático do Resíduo")
    st.markdown(r"Para formalizar esta discussão, definimos o resíduo como a diferença entre o observado e o estimado, funcionando como o substituto empírico do erro teórico:")
    st.latex(r"e_i = Y_i - \hat{Y}_i")
    
    # Simulador
    st.subheader(r"### 🛠️ Simulador: Analisador de Resíduos Estudentizados")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        val_n = st.slider(r"Número de Observações", 20, 100, 50, key="n_pts_subtopico_5")
        val_noise = st.slider(r"Nível de Ruído", 1.0, 5.0, 2.0, key="noise_subtopico_5")
    
    # Tratamento seguro dos inputs para evitar erros em ambientes Mock
    n_points = int(val_n) if hasattr(val_n, '__int__') else 50
    noise_level = float(val_noise) if hasattr(val_noise, '__float__') else 2.0
    
    np.random.seed(42)
    x_sim = np.linspace(0, 10, n_points)
    y_sim = 2 * x_sim + 5 + np.random.normal(0, noise_level, n_points)
    slope, intercept, _, _, _ = stats.linregress(x_sim, y_sim)
    y_pred = intercept + slope * x_sim
    residuals = y_sim - y_pred
    
    # Gráfico Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=y_pred, y=residuals,
        mode='markers',
        name='Resíduos',
        marker=dict(color="#1E3A8A", size=8, line=dict(width=1, color="white"))
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="#991B1B")
    
    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title=dict(
            text="<b>Análise de Resíduos vs Valores Preditos</b>",
            font=dict(size=14, color="#1E293B", family="Arial, sans-serif"),
            x=0.0, y=0.95
        ),
        xaxis=dict(
            title=dict(text="Valores Preditos", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0", zerolinecolor="#CBD5E1", fixedrange=True
        ),
        yaxis=dict(
            title=dict(text="Resíduos", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")),
            tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            gridcolor="#E2E8F0", zerolinecolor="#CBD5E1", fixedrange=True
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0,
            font=dict(size=9, color="#64748B", family="Arial, sans-serif"),
            bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="#E2E8F0", borderwidth=1
        ),
        hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_color="#1E293B", font_family="Arial, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True, key=r"plotly_chart_subtopico_5")
    
    # Dedução Analítica
    st.subheader(r"### 📐 O Rigor Analítico: Propriedades da Soma")
    st.markdown(r"A dedução do comportamento dos resíduos revela propriedades cruciais da estimativa de mínimos quadrados:")
    st.latex(r"e_i = Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i")
    st.markdown(r"Por construção algébrica, a soma dos resíduos em uma regressão linear é sempre nula:")
    st.latex(r"\sum e_i = \sum Y_i - n\hat{\beta}_0 - \hat{\beta}_1 \sum X_i = 0")
    
    # Exemplos Práticos
    st.subheader(r"### 📈 Casos de Aplicação Prática: Verificação de Modelos")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Validação Linear Simples")
        st.markdown(r"Verificação de modelo $\hat{Y} = 150 + 2.5X$ com observações $X=\{10, 20, 30, 40, 50\}$ e $Y=\{178, 202, 224, 248, 276}$.")
        st.latex(r"Preditos: \{175, 200, 225, 250, 275\}")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- $e_1 = 178 - 175 = 3$")
        st.markdown(r"- $e_2 = 202 - 200 = 2$")
        st.markdown(r"- $e_3 = 224 - 225 = -1$")
        st.markdown(r"- $e_4 = 248 - 250 = -2$")
        st.markdown(r"- $e_5 = 276 - 275 = 1$")
        st.success(r"Soma dos resíduos = 0. A aleatoriedade sugere um bom ajuste linear do modelo para os dados de qualidade.")

    # Extensão da Modelagem: Ajustamento de Funções de Potência e Exponenciais
    
    st.header(r"Extensão da Modelagem: Ajustamento de Funções de Potência e Exponenciais")
    
    st.markdown(r"""
    A inferência estatística moderna busca constantemente o equilíbrio entre a elegância da linearidade e a complexidade dos fenômenos naturais. Historicamente, desde a consolidação do método dos mínimos quadrados por Legendre e Gauss, a regressão linear simples estabeleceu-se como o paradigma dominante, dada sua robustez analítica na modelagem de relações aditivas.
    """)
    
    st.markdown(r"""
    Entretanto, ao analisarmos dinâmicas como crescimento biológico, elasticidades de mercado ou propagação de patógenos, a premissa de variação constante torna-se insuficiente. Fenômenos onde o efeito de uma variável independente sobre a dependente é proporcional à magnitude da própria dependente exigem modelos **não-lineares**.
    """)
    
    st.info(r"""
    ### 💡 A Transição Ontológica para a Não-Linearidade
    A modelagem de potências e exponenciais permite descrever sistemas de crescimento acelerado ou atenuado que desafiam a linearidade aditiva. A transição para esses modelos é viabilizada por transformações logarítmicas, que reconfiguram o espaço amostral, permitindo a linearização e facilitando o uso de estimadores de mínimos quadrados ordinários.
    """)
    
    st.markdown(r"""
    ### Os Pilares da Modelagem Funcional
    Ao utilizar logaritmos, convertemos espaços métricos multiplicativos em espaços aditivos. Esta manipulação não é um mero artifício, mas uma redefinição da interpretação dos coeficientes:
    
    *   **Linearização de Potência:** Permite converter relações do tipo $Y = AX^{\beta}$ para uma forma onde a regressão linear é aplicável.
    *   **Interpretação de Elasticidade:** No modelo log-log, o coeficiente $\beta_1$ representa a elasticidade constante de $Y$ em relação a $X$, quantificando a variação percentual esperada em $Y$ para cada 1% de variação em $X$.
    *   **Vigilância Estatística:** A transformação logarítmica estabiliza a variância, mas exige diagnóstico rigoroso quanto à homocedasticidade e à estrutura do termo de erro.
    """)
    
    st.warning(r"""
    ### ⚠️ A Armadilha de Jensen e a Retransformação
    Ao retornar da escala logarítmica para a original, é fundamental considerar a **Desigualdade de Jensen** ($E[\ln(Y)] \neq \ln(E[Y])$). O modelo linearizado fornece a mediana da distribuição condicional; ignorar essa distinção resulta em subestimação sistemática, sendo necessária a aplicação de correções baseadas nos momentos do termo de erro para garantir a validade das estimativas.
    """)
    
    st.subheader(r"### 📐 O Coração Matemático: Derivação do Modelo Log-Log")
    
    st.markdown(r"A dedução analítica parte da função potência fundamental, passando pela aplicação do logaritmo natural em ambos os membros para viabilizar a regressão:")
    
    st.latex(r"Y = A X^{\beta_1} \nu")
    
    st.markdown(r"Aplicando o logaritmo natural ($\ln$) em ambos os lados, transformamos a relação multiplicativa em aditiva:")
    
    st.latex(r"\ln(Y) = \ln(A) + \beta_1 \ln(X) + \ln(\nu)")
    
    st.markdown(r"Definimos o intercepto transformado, onde o valor original é recuperado pela função exponencial:")
    
    st.latex(r"\beta_0 = \ln(A)")
    
    st.subheader(r"### 📊 Aplicação Prática: Elasticidade de Escala")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Análise de Rendimentos de Escala")
        st.markdown(r"Considerando o modelo de produção $Y=AX^{\beta}$, uma regressão linearizada sobre dados de investimento e produção resultou na equação: $\ln(Y) = 2.3 + 0.75 \ln(X)$.")
        
        st.latex(r"\hat{\beta}_0 = 2.3, \quad \hat{\beta}_1 = 0.75")
        
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- **Recuperação do termo constante:** $A = e^{2.3} \approx 9.97$")
        st.markdown(r"- **Interpretação do coeficiente:** $\beta_1 = 0.75$ (representa a elasticidade)")
        
        st.success(r"**Laudo Comercial:** A elasticidade de 0.75 indica rendimentos decrescentes de escala. Isso significa que, neste cenário, um aumento de 1% no capital investido resulta em um crescimento de apenas 0.75% na produção, sugerindo ineficiências ou restrições de capacidade conforme o sistema se expande.")

    st.markdown('---')
    st.markdown('##### 📚 Referências Bibliográficas Consolidadas (Rodapé da Aula)')
    for ref in metadata['referencias_bibliograficas_finais']:
        st.markdown(f'- {ref}')

with tab_exercicios:
    import json, base64
    dados_exercicios = json.loads(base64.b64decode('eyJ0b3BpY29fYXVsYSI6ICJBbsOhbGlzZSBCaXZhcmlhZGEgZSBSZWdyZXNzw6NvIExpbmVhciIsICJxdWVzdG9lc19tdWx0aXBsYV9lc2NvbGhhIjogW3siZW51bmNpYWRvIjogIkVtIHVtYSBwbGFudGEgaW5kdXN0cmlhbCBhdXRvbWF0aXphZGEsIGVuZ2VuaGVpcm9zIG1vbml0b3JhbSBhIHRlbXBlcmF0dXJhIGRvcyBtb3RvcmVzICgkWCQsIGVtICReXHRleHR7b31DJCkgZSBhIHRheGEgZGUgdmlicmHDp8OjbyAoJFkkLCBlbSAkbW0vcyQpLiBBbyBhbmFsaXNhciB1bWEgYW1vc3RyYSBkZSAkbj0xMDAkIG9ic2VydmHDp8O1ZXMsIG9idGV2ZS1zZSB1bSBjb2VmaWNpZW50ZSBkZSBjb3JyZWxhw6fDo28gZGUgUGVhcnNvbiBkZSAkciA9IDAsODUkLiBDb25zaWRlcmFuZG8gYXMgcHJvcHJpZWRhZGVzIGRlc3RlIGNvZWZpY2llbnRlLCBxdWFsIMOpIGEgaW50ZXJwcmV0YcOnw6NvIG1haXMgYWRlcXVhZGEgcGFyYSBlc3NlIGNlbsOhcmlvPyIsICJhbHRlcm5hdGl2YXMiOiB7IkEiOiAiRXhpc3RlIHVtYSByZWxhw6fDo28gbGluZWFyIHBlcmZlaXRhIGVudHJlIHRlbXBlcmF0dXJhIGUgdmlicmHDp8Ojbywgb25kZSBvIGF1bWVudG8gZGUgMSAkXlx0ZXh0e299QyQgY2F1c2EgdW0gYXVtZW50byBleGF0byBkZSAwLDg1ICRtbS9zJCBuYSB2aWJyYcOnw6NvLiIsICJCIjogIkEgcmVsYcOnw6NvIGVudHJlIGFzIHZhcmnDoXZlaXMgw6kgZm9ydGUgZSBwb3NpdGl2YSwgaW5kaWNhbmRvIHF1ZSwgZW0gbcOpZGlhLCBtb3RvcmVzIGNvbSB0ZW1wZXJhdHVyYXMgbWFpcyBhbHRhcyB0ZW5kZW0gYSBhcHJlc2VudGFyIG1haW9yZXMgdGF4YXMgZGUgdmlicmHDp8Ojby4iLCAiQyI6ICJPIHZhbG9yICRyID0gMCw4NSQgaW5kaWNhIHF1ZSA4NSUgZGEgdmFyaWHDp8OjbyBuYSB2aWJyYcOnw6NvICgkWSQpIMOpIGV4cGxpY2FkYSBwZWxvIG1vZGVsbyBkZSByZWdyZXNzw6NvIGxpbmVhciBiYXNlYWRvIG5hIHRlbXBlcmF0dXJhICgkWCQpLiIsICJEIjogIk8gY29lZmljaWVudGUgZGUgY29ycmVsYcOnw6NvIMOpIGluZGVwZW5kZW50ZSBkYXMgdW5pZGFkZXMgZGUgbWVkaWRhLCBtYXMgbsOjbyBwZXJtaXRlIGFmaXJtYXIgYSBkaXJlw6fDo28gZGEgYXNzb2NpYcOnw6NvIGVudHJlICRYJCBlICRZJC4iLCAiRSI6ICJBIGNvcnJlbGHDp8OjbyBkZSAwLDg1IHN1Z2VyZSBxdWUgYSByZWxhw6fDo28gZW50cmUgJFgkIGUgJFkkIMOpIG9icmlnYXRvcmlhbWVudGUgZXhwb25lbmNpYWwsIHZpc3RvIHF1ZSDDqSB1bSB2YWxvciBhbHRvIGUgcG9zaXRpdm8uIn0sICJhbHRlcm5hdGl2YV9jb3JyZXRhIjogIkIiLCAiZGljYSI6ICJMZW1icmUtc2UgcXVlIG8gY29lZmljaWVudGUgZGUgUGVhcnNvbiAoJHIkKSBxdWFudGlmaWNhIGEgZm9yw6dhIGUgYSBkaXJlw6fDo28gZGEgZGVwZW5kw6puY2lhIGxpbmVhciwgbWFzIG7Do28gaW1wbGljYSBjYXVzYWxpZGFkZSBkaXJldGEgb3UgcG9yY2VudGFnZW0gZGUgZXhwbGljYcOnw6NvIGRhIHZhcmnDom5jaWEgKGVzdGEgw7psdGltYSDDqSBwYXBlbCBkbyAkUl4yJCkuIiwgImdhYmFyaXRvX2NvbWVudGFkbyI6ICJBIGFsdGVybmF0aXZhIEIgZXN0w6EgY29ycmV0YS4gTyBjb2VmaWNpZW50ZSAkciA9IDAsODUkIHNpdHVhLXNlIHByw7N4aW1vIGEgMSwgaW5kaWNhbmRvIHVtYSBmb3J0ZSBhc3NvY2lhw6fDo28gbGluZWFyIHBvc2l0aXZhLiBBIGFsdGVybmF0aXZhIEEgZXN0w6EgaW5jb3JyZXRhIHBvaXMgJHIkIG7Do28gZm9ybmVjZSBhIHRheGEgZGUgdmFyaWHDp8OjbyAoaW5jbGluYcOnw6NvICRcYmV0YV8xJCBmYXogaXNzbykuIEEgQyBlc3TDoSBpbmNvcnJldGEgcG9ycXVlIGEgcG9yY2VudGFnZW0gZGUgdmFyacOibmNpYSBleHBsaWNhZGEgw6kgZGFkYSBwZWxvIGNvZWZpY2llbnRlIGRlIGRldGVybWluYcOnw6NvICgkUl4yID0gMCw4NV4yID0gMCw3MjI1JCBvdSA3MiwyNSUpLCBuw6NvIHBlbG8gJHIkLiBBIEQgZXN0w6EgaW5jb3JyZXRhIHBvaXMgJHIkIGluZGljYSBhIGRpcmXDp8OjbyAoc2luYWwgcG9zaXRpdm8pLiBBIEUgw6kgaW5jb3JyZXRhIHBvaXMgUGVhcnNvbiDDqSBjZWdvIGEgbsOjby1saW5lYXJpZGFkZXMuIn0sIHsiZW51bmNpYWRvIjogIlVtIGFuYWxpc3RhIGZpbmFuY2Vpcm8gaW52ZXN0aWdhIGEgY292YXJpw6JuY2lhIGVudHJlIG8gcmV0b3JubyBkZSBkb2lzIGF0aXZvcywgJFgkIGUgJFkkLCBlbSB1bWEgY2FydGVpcmEgZGUgaW52ZXN0aW1lbnRvcy4gQXDDs3MgY2FsY3VsYXIgJFNfe1hZfSA9IDQ1MCQsIG8gYW5hbGlzdGEgcXVlc3Rpb25hIHNlIGVzc2EgYXNzb2NpYcOnw6NvIMOpICdmb3J0ZScuIFF1YWwgZGFzIGFsdGVybmF0aXZhcyBtZWxob3IgZGVzY3JldmUgYSBsaW1pdGHDp8OjbyBkZXNzYSBtZWRpZGE/IiwgImFsdGVybmF0aXZhcyI6IHsiQSI6ICJBIGNvdmFyacOibmNpYSAkU197WFl9ID0gNDUwJCBpbmRpY2EgdW1hIGFzc29jaWHDp8OjbyBmb3J0ZSwgcG9pcyBvIHZhbG9yIMOpIG1haW9yIHF1ZSAxLiIsICJCIjogIkEgY292YXJpw6JuY2lhIG7Do28gcG9zc3VpIHVuaWRhZGUgZGUgbWVkaWRhLCBwb3J0YW50bywgbyB2YWxvciA0NTAgw6kgYWJzb2x1dG8gZSBjb21wYXLDoXZlbCBlbnRyZSBxdWFscXVlciBjb25qdW50byBkZSBkYWRvcy4iLCAiQyI6ICJBIGNvdmFyacOibmNpYSDDqSBkZXBlbmRlbnRlIGRhcyB1bmlkYWRlcyBkZSBtZWRpZGEgZGFzIHZhcmnDoXZlaXMgb3JpZ2luYWlzLCBsb2dvLCB1bSB2YWxvciBkZSA0NTAgcG9kZSBzZXIgY29uc2lkZXJhZG8gYmFpeG8gb3UgYWx0byBkZXBlbmRlbmRvIGRhIGVzY2FsYSBkb3MgYXRpdm9zIChleDogcGVyY2VudHVhbCB2cy4gdmFsb3JlcyBtb25ldMOhcmlvcykuIiwgIkQiOiAiQSBjb3ZhcmnDom5jaWEgc8OzIHBvZGUgc2VyIGludGVycHJldGFkYSBzZSBvcyBkYWRvcyBzZWd1aXJlbSB1bWEgZGlzdHJpYnVpw6fDo28gbm9ybWFsICROKDAsIFx0ZXh0e3NpZ21hfV4yKSQsIGNhc28gY29udHLDoXJpbywgZWxhIMOpIG1hdGVtYXRpY2FtZW50ZSBpbmRlZmluaWRhLiIsICJFIjogIk8gdmFsb3IgcG9zaXRpdm8gZGEgY292YXJpw6JuY2lhIGluZGljYSBxdWUgYSBjb3JyZWxhw6fDo28gw6kgb2JyaWdhdG9yaWFtZW50ZSBwZXJmZWl0YSAoJHIgPSAxJCksIHBvaXMgbsOjbyBow6EgZGlzcGVyc8OjbyByZXNpZHVhbC4ifSwgImFsdGVybmF0aXZhX2NvcnJldGEiOiAiQyIsICJkaWNhIjogIlBlbnNlIG5hIGRlZmluacOnw6NvIGRlIGNvdmFyacOibmNpYTogJFNfe1hZfSA9IFxmcmFjezF9e24tMX0gXHRleHRzdHlsZSDiiJEgKFhfaSAtIFxiYXJ7WH0pKFlfaSAtIFxiYXJ7WX0pJC4gQXMgdW5pZGFkZXMgZGFzIHZhcmnDoXZlaXMgc2UgbXVsdGlwbGljYW0gbmEgZsOzcm11bGEuIiwgImdhYmFyaXRvX2NvbWVudGFkbyI6ICJBIGFsdGVybmF0aXZhIEMgZXN0w6EgY29ycmV0YS4gQSBjb3ZhcmnDom5jaWEgw6kgZGltZW5zaW9uYWwgKHVuaWRhZGUgZGUgJFgkICRcdGltZXMkIHVuaWRhZGUgZGUgJFkkKSwgZGlmaWN1bHRhbmRvIGEgYXZhbGlhw6fDo28gZGEgaW50ZW5zaWRhZGUgZGEgYXNzb2NpYcOnw6NvIHNlbSBub3JtYWxpemHDp8OjbyAoY29tbyBubyBjYXNvIGRvIGNvZWZpY2llbnRlIGRlIGNvcnJlbGHDp8OjbyAkciQpLiBBIGFsdGVybmF0aXZhIEEgZSBFIGVzdMOjbyBpbmNvcnJldGFzIHBvcnF1ZSBhIGNvdmFyacOibmNpYSBuw6NvIMOpIGxpbWl0YWRhIGFvIGludGVydmFsbyAkWy0xLCAxXSQuIEEgQiBlc3TDoSBpbmNvcnJldGEgcG9pcyBhIGNvdmFyacOibmNpYSBwb3NzdWkgdW5pZGFkZS4gQSBEIGVzdMOhIGluY29ycmV0YSBwb2lzIGEgY292YXJpw6JuY2lhIMOpIHVtIG1vbWVudG8gY2VudHJhbCBhbW9zdHJhbCBjYWxjdWzDoXZlbCBwYXJhIHF1YWxxdWVyIGNvbmp1bnRvIGRlIHBhcmVzIHF1YW50aXRhdGl2b3MuIn0sIHsiZW51bmNpYWRvIjogIkVtIHVtIG1vZGVsbyBkZSByZWdyZXNzw6NvIGxpbmVhciBzaW1wbGVzICRZX2kgPSBcYmV0YV8wICsgXGJldGFfMSBYX2kgKyBcdGV4dHt1fV9pJCwgbyBpbnRlcmNlcHRvICRcYmV0YV8wJCBwb3NzdWkgdW1hIGludGVycHJldGHDp8OjbyBlc3RhdMOtc3RpY2EgZXNwZWPDrWZpY2EuIEVtIHVtIGVzdHVkbyBzb2JyZSBvIHRlbXBvIGRlIGVudHJlZ2EgZGUgbWVyY2Fkb3JpYXMgKCRZJCwgZW0gaG9yYXMpIGVtIGZ1bsOnw6NvIGRhIGRpc3TDom5jaWEgcGVyY29ycmlkYSAoJFgkLCBlbSBrbSksIHF1YWwgw6kgYSBpbnRlcnByZXRhw6fDo28gY29ycmV0YSBkZSAkXGJldGFfMCQ/IiwgImFsdGVybmF0aXZhcyI6IHsiQSI6ICIkXGJldGFfMCQgcmVwcmVzZW50YSBvIHRlbXBvIGRlIGVudHJlZ2EgbcOpZGlvIHF1YW5kbyBhIGRpc3TDom5jaWEgcGVyY29ycmlkYSDDqSBpZ3VhbCBhIHplcm8gKGV4OiB0ZW1wbyBmaXhvIGRlIHByb2Nlc3NhbWVudG8gZG8gcGVkaWRvKS4iLCAiQiI6ICIkXGJldGFfMCQgcmVwcmVzZW50YSBhIHZhcmlhw6fDo28gZXNwZXJhZGEgbm8gdGVtcG8gZGUgZW50cmVnYSBwYXJhIGNhZGEgcXVpbMO0bWV0cm8gYWRpY2lvbmFsIHBlcmNvcnJpZG8uIiwgIkMiOiAiJFxiZXRhXzAkIGRldmUgc2VyIG9icmlnYXRvcmlhbWVudGUgaWd1YWwgYSB6ZXJvIHNlIG8gbW9kZWxvIHBhc3NhciBwZWxhIG9yaWdlbSBkbyBwbGFubyBjYXJ0ZXNpYW5vLiIsICJEIjogIiRcYmV0YV8wJCDDqSBvIHJlc8OtZHVvIG3DqWRpbyBkbyBtb2RlbG8sIGluZGljYW5kbyBhIHByZWNpc8OjbyBkYSBwcmV2aXPDo28gZGFzIGVudHJlZ2FzLiIsICJFIjogIiRcYmV0YV8wJCDDqSBvIGRlc3ZpbyBwYWRyw6NvIGRvcyB0ZW1wb3MgZGUgZW50cmVnYSBxdWFuZG8gYSBkaXN0w6JuY2lhIMOpIGNvbnN0YW50ZS4ifSwgImFsdGVybmF0aXZhX2NvcnJldGEiOiAiQSIsICJkaWNhIjogIkF2YWxpZSBhIGRlZmluacOnw6NvIGRlIGludGVyY2VwdG8gZW0gdW1hIGZ1bsOnw6NvIGxpbmVhciAkZih4KSA9IGF4ICsgYiQuIE8gcXVlIGFjb250ZWNlIGNvbSAkZih4KSQgcXVhbmRvICR4PTAkPyIsICJnYWJhcml0b19jb21lbnRhZG8iOiAiQSBhbHRlcm5hdGl2YSBBIGVzdMOhIGNvcnJldGEuIE8gaW50ZXJjZXB0byAkXGJldGFfMCQgw6kgZGVmaW5pZG8gY29tbyBvIHZhbG9yIGVzcGVyYWRvIGRhIHZhcmnDoXZlbCByZXNwb3N0YSAkWSQgcXVhbmRvIGEgdmFyacOhdmVsIHByZWRpdG9yYSAkWCQgw6kgemVyby4gQSBhbHRlcm5hdGl2YSBCIGRlc2NyZXZlIGEgaW5jbGluYcOnw6NvICRcYmV0YV8xJC4gQSBDIG7Do28gw6kgb2JyaWdhdMOzcmlhLCBwb2lzIG8gbW9kZWxvIHBvZGUgdGVyIGludGVyY2VwdG8gZGlmZXJlbnRlIGRlIHplcm8uIEEgRCBlc3TDoSBpbmNvcnJldGEsIHBvaXMgbyByZXPDrWR1byBtw6lkaW8gw6ksIHBvciBjb25zdHJ1w6fDo28gZG8gT0xTLCB6ZXJvLiBBIEUgZXN0w6EgaW5jb3JyZXRhIHBvaXMgJFxiZXRhXzAkIMOpIHVtIHBhcsOibWV0cm8gZGUgbG9jYcOnw6NvLCBuw6NvIGRlIGRpc3BlcnPDo28uIn0sIHsiZW51bmNpYWRvIjogIkFvIHJlYWxpemFyIG8gZGlhZ27Ds3N0aWNvIGRlIHVtIG1vZGVsbyBkZSByZWdyZXNzw6NvIGxpbmVhciwgdW0gcGVzcXVpc2Fkb3Igb2JzZXJ2YSBxdWUgbyBncsOhZmljbyBkZSByZXPDrWR1b3MgdmVyc3VzIHZhbG9yZXMgYWp1c3RhZG9zICgkXHRleHR7ZX1faSQgdnMgJFx0ZXh0e157WX19X2kkKSBhcHJlc2VudGEgdW0gZm9ybWF0byBkZSBmdW5pbCAoYSBkaXNwZXJzw6NvIGF1bWVudGEgY29uZm9ybWUgbyB2YWxvciBhanVzdGFkbyBhdW1lbnRhKS4gTyBxdWUgZXNzYSBldmlkw6puY2lhIHN1Z2VyZT8iLCAiYWx0ZXJuYXRpdmFzIjogeyJBIjogIk8gbW9kZWxvIGVzdMOhIHBlcmZlaXRhbWVudGUgYWp1c3RhZG8sIHBvaXMgbyBmdW5pbCDDqSB1bSBwYWRyw6NvIGFjZWl0w6F2ZWwgZW0gZXN0YXTDrXN0aWNhLiIsICJCIjogIk8gbW9kZWxvIGFwcmVzZW50YSB2aW9sYcOnw6NvIGRhIHByZW1pc3NhIGRlIG5vcm1hbGlkYWRlIGRvcyByZXPDrWR1b3MuIiwgIkMiOiAiTyBtb2RlbG8gYXByZXNlbnRhIGluZMOtY2lvcyBkZSBoZXRlcm9jZWRhc3RpY2lkYWRlLCBvdSBzZWphLCBhIHZhcmnDom5jaWEgZG8gZXJybyBuw6NvIMOpIGNvbnN0YW50ZS4iLCAiRCI6ICJPIG1vZGVsbyBzb2ZyZSBkZSBhdXRvY29ycmVsYcOnw6NvIHNlcmlhbCwgdMOtcGljYSBkZSBkYWRvcyBkZSBjb3J0ZSB0cmFuc3ZlcnNhbC4iLCAiRSI6ICJPIGNvZWZpY2llbnRlIGRlIGNvcnJlbGHDp8OjbyAkciQgZGV2ZSBzZXIgb2JyaWdhdG9yaWFtZW50ZSBpZ3VhbCBhIHplcm8uIn0sICJhbHRlcm5hdGl2YV9jb3JyZXRhIjogIkMiLCAiZGljYSI6ICJMZW1icmUtc2UgZG9zIHByZXNzdXBvc3RvcyBjbMOhc3NpY29zOiBvcyBlcnJvcyAkXHRleHR7dX1faSQgKG91ICRcdGV4dHtlfV9pJCkgZGV2ZW0gdGVyIG3DqWRpYSB6ZXJvIGUgdmFyacOibmNpYSBjb25zdGFudGUgKCRcdGV4dHtzaWdtYX1eMiQpLiBPIHF1ZSBzaWduaWZpY2EgYSBwYWxhdnJhICdoZXRlcm9jZWRhc3RpY2lkYWRlJz8iLCAiZ2FiYXJpdG9fY29tZW50YWRvIjogIkEgYWx0ZXJuYXRpdmEgQyBlc3TDoSBjb3JyZXRhLiBPIGZvcm1hdG8gZGUgZnVuaWwgbm8gZ3LDoWZpY28gZGUgcmVzw61kdW9zIMOpIG8gZGlhZ27Ds3N0aWNvIHZpc3VhbCBjbMOhc3NpY28gcGFyYSBoZXRlcm9jZWRhc3RpY2lkYWRlLCBvbmRlIGEgdmFyacOibmNpYSBkbyB0ZXJtbyBkZSBlcnJvICgkXHRleHR7dX1faSQpIG7Do28gw6kgY29uc3RhbnRlLCB2aW9sYW5kbyB1bWEgZGFzIHByZW1pc3NhcyBmdW5kYW1lbnRhaXMgZG8gbcOpdG9kbyBkZSBtw61uaW1vcyBxdWFkcmFkb3Mgb3JkaW7DoXJpb3MgY2zDoXNzaWNvLiBBIGFsdGVybmF0aXZhIEEgZXN0w6EgaW5jb3JyZXRhLCBwb2lzIG8gcGFkcsOjbyBpZGVhbCBzZXJpYSB1bWEgbnV2ZW0gYWxlYXTDs3JpYSBzZW0gZm9ybWF0by4gQSBCIGUgRCByZWZlcmVtLXNlIGEgb3V0cm9zIHByb2JsZW1hcyAobm9ybWFsaWRhZGUgZSBhdXRvY29ycmVsYcOnw6NvKSBxdWUgbsOjbyBzw6NvIGRpYWdub3N0aWNhZG9zIHByaW1hcmlhbWVudGUgcGVsbyBmb3JtYXRvIGRlIGZ1bmlsLiJ9LCB7ImVudW5jaWFkbyI6ICJQYXJhIG1vZGVsYXIgdW1hIHJlbGHDp8OjbyBuw6NvIGxpbmVhciBvbmRlICRZID0gQSBYXntcdGV4dHvOsn1fMX0gXHRleHR7zr19JCwgb25kZSAkXHRleHR7zr19JCDDqSB1bSBlcnJvIG11bHRpcGxpY2F0aXZvLCB1dGlsaXphLXNlIGEgdHJhbnNmb3JtYcOnw6NvIGxvZ2Fyw610bWljYS4gUXVhbCBhIGZvcm1hIGxpbmVhcml6YWRhIHJlc3VsdGFudGUgcXVlIHBlcm1pdGUgYXBsaWNhciBhIHJlZ3Jlc3PDo28gbGluZWFyIHNpbXBsZXM/IiwgImFsdGVybmF0aXZhcyI6IHsiQSI6ICIkWSA9IFx0ZXh0e86yfV8wICsgXHRleHR7zrJ9XzEgWCQiLCAiQiI6ICIkXHRleHR7bG59KFkpID0gXHRleHR7zrJ9XzAgKyBcdGV4dHvOsn1fMSBcdGV4dHtsbn0oWCkgKyBlJCIsICJDIjogIiRcdGV4dHtsbn0oWSkgPSBcdGV4dHvOsn1fMCBcdGV4dHtsbn0oWCkgKyBcdGV4dHvOsn1fMSQiLCAiRCI6ICIkWSA9IFx0ZXh0e2xufShBKSArIFx0ZXh0e86yfV8xIFgkIiwgIkUiOiAiJFx0ZXh0e2xufShZKSA9IFx0ZXh0e2V4cH0oXHRleHR7zrJ9XzAgKyBcdGV4dHvOsn1fMSBYKSQifSwgImFsdGVybmF0aXZhX2NvcnJldGEiOiAiQiIsICJkaWNhIjogIkFwbGlxdWUgbyBsb2dhcml0bW8gbmF0dXJhbCBlbSBhbWJvcyBvcyBsYWRvcyBkYSBlcXVhw6fDo286ICRcdGV4dHtsbn0oWSkgPSBcdGV4dHtsbn0oQSBcdGltZXMgWF57XHRleHR7zrJ9XzF9IFx0aW1lcyBcdGV4dHvOvX0pJC4gVXRpbGl6ZSBhcyBwcm9wcmllZGFkZXM6ICRcdGV4dHtsbn0oYWIpID0gXHRleHR7bG59KGEpICsgXHRleHR7bG59KGIpJCBlICRcdGV4dHtsbn0oYV5iKSA9IGIgXHRleHR7bG59KGEpJC4iLCAiZ2FiYXJpdG9fY29tZW50YWRvIjogIkEgYWx0ZXJuYXRpdmEgQiBlc3TDoSBjb3JyZXRhLiBBcGxpY2FuZG8gbyBsb2dhcml0bW86ICRcdGV4dHtsbn0oWSkgPSBcdGV4dHtsbn0oQSkgKyBcdGV4dHtsbn0oWF57XHRleHR7zrJ9XzF9KSArIFx0ZXh0e2xufShcdGV4dHvOvX0pJC4gRGVmaW5pbmRvICRcdGV4dHvOsn1fMCA9IFx0ZXh0e2xufShBKSQgZSAkZSA9IFx0ZXh0e2xufShcdGV4dHvOvX0pJCwgb2J0ZW1vcyAkXHRleHR7bG59KFkpID0gXHRleHR7zrJ9XzAgKyBcdGV4dHvOsn1fMSBcdGV4dHtsbn0oWCkgKyBlJCwgcXVlIMOpIHVtYSBlcXVhw6fDo28gbGluZWFyIG5hIGZvcm1hICRZJyA9IFx0ZXh0e86yfV8wICsgXHRleHR7zrJ9XzEgWCcgKyBlJC4ifV0sICJxdWVzdG9lc19kaXNjdXJzaXZhcyI6IFt7ImVudW5jaWFkbyI6ICJDb25zaWRlcmUgdW0gcGVxdWVubyBjb25qdW50byBkZSBkYWRvcyBkZSAkbj0zJCBvYnNlcnZhw6fDtWVzOiAkKDEsIDIpLCAoMiwgNCksICgzLCA1KSQuIENhbGN1bGUgbWFudWFsbWVudGUgb3MgcGFyw6JtZXRyb3MgZGEgcmV0YSBkZSByZWdyZXNzw6NvIGxpbmVhciBzaW1wbGVzICRcdGV4dHvMqHtZfX1faSA9IFx0ZXh0e8yCe86yfX1fMCArIFx0ZXh0e8yCe86yfX1fMSBYX2kkLiBDYWxjdWxlIHByaW1laXJhbWVudGUgYXMgbcOpZGlhcyAkXHRleHR7zIR7WH19JCBlICRcdGV4dHvMhHtZfX0kLCBhIGNvdmFyacOibmNpYSBhbW9zdHJhbCAkU197WFl9JCBlIGEgdmFyacOibmNpYSBkZSAkWCQgKCRTX1heMiQpIHBhcmEgZW5jb250cmFyICRcdGV4dHvMgnvOsn19XzEgPSBTX3tYWX0gLyBTX1heMiQgZSAkXHRleHR7zIJ7zrJ9fV8wID0gXHRleHR7zIR7WX19IC0gXHRleHR7zIJ7zrJ9fV8xIFx0ZXh0e8yEe1h9fSQuIiwgImRpY2EiOiAiTGVtYnJlLXNlIHF1ZSAkU197WFl9ID0gXGZyYWN7MX17bi0xfSBcdGV4dHN0eWxlIOKIkShYX2kgLSBcdGV4dHvMhHtYfX0pKFlfaSAtIFx0ZXh0e8yEe1l9fSkkIGUgJFNfWF4yID0gXGZyYWN7MX17bi0xfSBcdGV4dHN0eWxlIOKIkShYX2kgLSBcdGV4dHvMhHtYfX0pXjIkLiIsICJnYWJhcml0b19wYXNzb19hX3Bhc3NvIjogWyIkJCBcdGV4dHvMhHtYfX0gPSAoMSsyKzMpLzMgPSAyICQkIiwgIiQkIFx0ZXh0e8yEe1l9fSA9ICgyKzQrNSkvMyA9IDMsNjY2NyAkJCIsICIkJCBcdGV4dHtOdW1lcmFkb3IgZGEgQ292YXJpw6JuY2lhIChTb21hIGRvcyBwcm9kdXRvcyk6IH0gKDEtMikoMi0zLDY2NjcpICsgKDItMikoNC0zLDY2NjcpICsgKDMtMikoNS0zLDY2NjcpID0gKC0xKSgtMSw2NjY3KSArICgwKSgwLDMzMzMpICsgKDEpKDEsMzMzMykgPSAxLDY2NjcgKyAxLDMzMzMgPSAzICQkIiwgIiQkIFNfe1hZfSA9IDMgLyAoMy0xKSA9IDEsNSAkJCIsICIkJCBcdGV4dHtTb21hIGRvcyBxdWFkcmFkb3MgZGUgWDogfSAoMS0yKV4yICsgKDItMileMiArICgzLTIpXjIgPSAxICsgMCArIDEgPSAyICQkIiwgIiQkIFNfWF4yID0gMiAvICgzLTEpID0gMSAkJCIsICIkJCBcdGV4dHvMgnvOsn19XzEgPSBTX3tYWX0gLyBTX1heMiA9IDEsNSAvIDEgPSAxLDUgJCQiLCAiJCQgXHRleHR7zIJ7zrJ9fV8wID0gMyw2NjY3IC0gKDEsNSBcdGltZXMgMikgPSAzLDY2NjcgLSAzID0gMCw2NjY3ICQkIiwgIiQkIFx0ZXh0e1JldGEgZXN0aW1hZGE6IH0gXHRleHR7zKh7WX19X2kgPSAwLDY2NjcgKyAxLDUgWF9pICQkIl19LCB7ImVudW5jaWFkbyI6ICJFeHBsaXF1ZSBvIGNvbmNlaXRvIGRlIHJlc8OtZHVvIGVzdHVkZW50aXphZG8gZSBwb3IgcXVlIGVsZSDDqSBtYWlzIMO6dGlsIHBhcmEgbyBkaWFnbsOzc3RpY28gZGUgbW9kZWxvcyBkbyBxdWUgbyByZXPDrWR1byBzaW1wbGVzICgkZV9pID0gWV9pIC0gXHRleHR7zKh7WX19X2kkKS4iLCAiZGljYSI6ICJDb25zaWRlcmUgYSBmw7NybXVsYSAkcl9pID0gXGZyYWN7ZV9pfXtTXHRleHR74oiafXsxIC0gaF97aWl9fX0kLiBPIHF1ZSBvIHRlcm1vICRoX3tpaX0kIHJlcHJlc2VudGEgZSBjb21vIGVsZSBlc2NhbGEgbyByZXPDrWR1bz8iLCAiZ2FiYXJpdG9fcGFzc29fYV9wYXNzbyI6IFsiJCQgZV9pID0gWV9pIC0gXHRleHR7zKh7WX19X2kgXHRleHR7IHJlcHJlc2VudGEgbyBkZXN2aW8gYWJzb2x1dG8sIHF1ZSBwb3NzdWkgYSBtZXNtYSB1bmlkYWRlIGRhIHZhcmnDoXZlbCByZXNwb3N0YS59ICQkIiwgIiQkIFx0ZXh0e08gcmVzw61kdW8gZXN0dWRlbnRpemFkbyB9IHJfaSA9IFxmcmFje2VfaX17U1x0ZXh0e+KImn17MSAtIGhfe2lpfX19IFx0ZXh0eyBub3JtYWxpemEgbyByZXPDrWR1byBwZWxhIHN1YSB2YXJpYWJpbGlkYWRlIGVzdGltYWRhLn0gJCQiLCAiJCQgXHRleHR7TyB0ZXJtbyB9IGhfe2lpfSBcdGV4dHsgKGRpYWdvbmFsIGRhIG1hdHJpeiBjaGFww6l1KSBtZWRlIGEgYWxhdmFuY2FnZW0gZGUgY2FkYSBwb250bzogcG9udG9zIGNvbSB9IFhfaSBcdGV4dHsgbG9uZ2UgZGEgbcOpZGlhIH0gXHRleHR7zIR7WH19IFx0ZXh0eyB0w6ptIG1haW9yIH0gaF97aWl9IFx0ZXh0ey59ICQkIiwgIiQkIFx0ZXh0e0FvIGRpdmlkaXIgcGVsbyBlcnJvIHBhZHLDo28gZXN0aW1hZG8gYWp1c3RhZG8gcGVsbyB0ZXJtbyBkZSBhbGF2YW5jYWdlbSwgbyByZXPDrWR1byBlc3R1ZGVudGl6YWRvIHRvcm5hLXNlIGFkaW1lbnNpb25hbCBlIHBlcm1pdGUgY29tcGFyYXIgYSBtYWduaXR1ZGUgZGUgZXJyb3MgZW0gb2JzZXJ2YcOnw7VlcyBkaWZlcmVudGVzLn0gJCQiLCAiJCQgXHRleHR7SXNzbyBmYWNpbGl0YSBhIGlkZW50aWZpY2HDp8OjbyBkZSBvdXRsaWVycyBlIHBvbnRvcyBpbmZsdWVudGVzLCBwb2lzIHJlc8OtZHVvcyBlc3R1ZGVudGl6YWRvcyBtdWl0byBncmFuZGVzIChleDogfSB8cl9pfCA+IDMgXHRleHR7KSBpbmRpY2FtIHZpb2xhw6fDtWVzIHNldmVyYXMgb3UgcG9udG9zIHF1ZSBkaXN0b3JjZW0gbyBhanVzdGUufSAkJCJdfSwgeyJlbnVuY2lhZG8iOiAiRGFkbyBvIG1vZGVsbyBkZSBwb3TDqm5jaWEgJFkgPSBBIFhee1x0ZXh0e86yfV8xfSBcdGV4dHvOvX0kLCBkZW1vbnN0cmUgY29tbyB0cmFuc2Zvcm3DoS1sbyBlbSB1bWEgcmVncmVzc8OjbyBsaW5lYXIgc2ltcGxlcyBuYSBmb3JtYSAkWScgPSBcYmV0YV8wICsgXGJldGFfMSBYJyArIFx0ZXh0e2Vycm99JCwgaWRlbnRpZmljYW5kbyBjbGFyYW1lbnRlIG8gcXVlIHPDo28gJFknJCwgJFxiZXRhXzAkLCAkXGJldGFfMSQgZSAkWCckIGUgbyB0ZXJtbyBkZSBlcnJvIHJlc3VsdGFudGUuIiwgImRpY2EiOiAiQXBsaXF1ZSBhIHRyYW5zZm9ybWHDp8OjbyAkXHRleHR7bG59KFx0ZXh0e+KLhX0pJCBlbSBhbWJvcyBvcyBsYWRvcyBlIHVzZSBhcyBwcm9wcmllZGFkZXMgbG9nYXLDrXRtaWNhcy4iLCAiZ2FiYXJpdG9fcGFzc29fYV9wYXNzbyI6IFsiJCQgXHRleHR7RXF1YcOnw6NvIG9yaWdpbmFsOiB9IFkgPSBBIFhee1x0ZXh0e86yfV8xfSBcdGV4dHvOvX0gJCQiLCAiJCQgXHRleHR7QXBsaWNhbmRvIGxvZ2FyaXRtbyBuYXR1cmFsOiB9IFx0ZXh0e2xufShZKSA9IFx0ZXh0e2xufShBIFhee1x0ZXh0e86yfV8xfSBcdGV4dHvOvX0pICQkIiwgIiQkIFx0ZXh0e1VzYW5kbyBwcm9wcmllZGFkZXM6IH0gXHRleHR7bG59KFkpID0gXHRleHR7bG59KEEpICsgXHRleHR7bG59KFhee1x0ZXh0e86yfV8xfSkgKyBcdGV4dHtsbn0oXHRleHR7zr19KSAkJCIsICIkJCBcdGV4dHtTaW1wbGlmaWNhbmRvIHBvdMOqbmNpYTogfSBcdGV4dHtsbn0oWSkgPSBcdGV4dHtsbn0oQSkgKyBcdGV4dHvOsn1fMSBcdGV4dHtsbn0oWCkgKyBcdGV4dHtsbn0oXHRleHR7zr19KSAkJCIsICIkJCBcdGV4dHtJZGVudGlmaWNhw6fDo28gZG9zIHRlcm1vcyBsaW5lYXJlczogfSAkJCIsICIkJCBZJyA9IFx0ZXh0e2xufShZKSAkJCIsICIkJCBcYmV0YV8wID0gXHRleHR7bG59KEEpICQkIiwgIiQkIFgnID0gXHRleHR7bG59KFgpICQkIiwgIiQkIFx0ZXh0e0Vycm8gfSBlID0gXHRleHR7bG59KFx0ZXh0e869fSkgJCQiLCAiJCQgXHRleHR7UmVzdWx0YWRvOiB9IFknID0gXGJldGFfMCArIFx0ZXh0e86yfV8xIFgnICsgZSAkJCJdfV19').decode('utf-8'))


    # Título da seção baseado no tópico
    st.header(f"Exercícios: {dados_exercicios.get('topico_aula', 'Análise de Dados')}")
    
    # Seção de Questões de Múltipla Escolha
    st.subheader("Questões de Múltipla Escolha")
    questoes_mcq = dados_exercicios.get("questoes_multipla_escolha", [])
    
    for i, questao in enumerate(questoes_mcq):
        with st.container(border=True):
            st.markdown(f"**Questão {i + 1}**")
            st.write(questao.get("enunciado", "Enunciado não disponível."))
    
            # Formatação das alternativas para o widget de rádio
            alternativas_dict = questao.get("alternativas", {})
            opcoes = [f"{chave}: {valor}" for chave, valor in alternativas_dict.items()]
            
            escolha = st.radio(
                "Selecione uma alternativa:", 
                opcoes, 
                key=f"radio_mcq_{i}", 
                index=None
            )
    
            col_dica, col_check = st.columns(2)
            
            with col_dica:
                if st.button("💡 Dica", key=f"btn_dica_mcq_{i}"):
                    st.info(questao.get("dica", "Dica indisponível."))
    
            with col_check:
                if st.button("✅ Verificar Resposta", key=f"btn_check_mcq_{i}"):
                    if escolha:
                        # Extrai a letra da alternativa selecionada (ex: 'A')
                        letra_selecionada = escolha.split(":")[0].strip()
                        gabarito = questao.get("alternativa_correta")
                        
                        if letra_selecionada == gabarito:
                            st.success("Correto! Muito bem.")
                        else:
                            st.error(f"Incorreto. A alternativa correta era {gabarito}.")
                    else:
                        st.warning("Por favor, selecione uma alternativa antes de verificar.")
    
            # Gabarito comentado escondido
            with st.expander("✅ Ver Gabarito Comentado"):
                st.write(questao.get("gabarito_comentado", "Gabarito indisponível."))
    
    st.divider()
    
    # Seção de Questões Discursivas
    st.subheader("Questões Discursivas")
    questoes_disc = dados_exercicios.get("questoes_discursivas", [])
    
    for i, questao in enumerate(questoes_disc):
        with st.container(border=True):
            st.markdown(f"**Questão Discursiva {i + 1}**")
            st.write(questao.get("enunciado", "Enunciado não disponível."))
            
            st.text_area("Sua resposta:", key=f"txt_disc_{i}")
    
            if st.button("💡 Dica", key=f"btn_dica_disc_{i}"):
                st.info(questao.get("dica", "Dica indisponível."))
    
            with st.expander("✅ Ver Resolução Detalhada"):
                passos = questao.get("gabarito_passo_a_passo", [])
                for passo in passos:
                    st.latex(passo)
