import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stats
from scipy.stats import norm
import base64
import json

# Carregamento seguro dos metadados da aula para evitar SyntaxError
metadata = json.loads(base64.b64decode('eyJ0ZW1hX2dsb2JhbCI6ICJBbsOhbGlzZSBkZSBSZXPDrWR1b3MgZW0gTW9kZWxvcyBkZSBSZWdyZXNzw6NvOiBEaWFnbsOzc3RpY28gZSBWYWxpZGHDp8OjbyIsICJyZWZlcmVuY2lhc19iaWJsaW9ncmFmaWNhc19maW5haXMiOiBbIkx1bmEgJiBFc3RldmVzLCAnU29sdcOnw7VlcyBkZSBFcXVhw6fDtWVzIExpbmVhcmVzJyAtIENhcC4gMi41LCBwcC4gNTMtNTgiLCAiTHVuYSAmIEVzdGV2ZXMsICdBbsOhbGlzZSBkZSBWYXJpw6JuY2lhJyAtIENhcC4gNC42LCBwcC4gMTA3LTExMSIsICJMdW5hICYgRXN0ZXZlcywgJ0ludHJvZHXDp8OjbyDDoCBBbsOhbGlzZSBkZSBSZWdyZXNzw6NvJyAtIENhcC4gMy41LCBwcC4gNjktNzEiLCAiTW9udGdvbWVyeSwgRC4gQy4sIFBlY2ssIEUuIEEuLCAmIFZpbmluZywgRy4gRy4sICdJbnRyb2R1Y3Rpb24gdG8gTGluZWFyIFJlZ3Jlc3Npb24gQW5hbHlzaXMnIC0gQ2FwLiA2LCBwcC4gMjEwLTIxNSIsICJGYXJhd2F5LCBKLiBKLiwgJ0xpbmVhciBNb2RlbHMgd2l0aCBSJyAtIENhcC4gNywgcHAuIDgwLTkwIl19').decode('utf-8'))

# Injeção de Estilos CSS Acadêmicos Premium
st.markdown("""
    <style>
        .premium-title { font-size: 2.2rem; font-weight: 800; color: #58d5d8; margin-bottom: 0.2rem; }
        .premium-subtitle { font-size: 1.1rem; color: #64748B; margin-bottom: 1.5rem; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="premium-title">{metadata["tema_global"]}</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">Conteúdo Acadêmico Digital e Simuladores Integrados</div>', unsafe_allow_html=True)

# Definição de Cores Globais da Paleta Premium
PRIMARY_BLUE = "#58d5d8"
SECONDARY_GREEN = "#ffff81"
WARNING_AMBER = "#F59E0B"
CRITICAL_RED = "#991B1B"

# Criação das Duas Grandes Abas Globais
tab_conteudo, tab_exercicios = st.tabs(["📚 Conteúdo Acadêmico Interativo", "📝 Caderno de Exercícios"])

with tab_conteudo:

    import streamlit as st
    import numpy as np
    import plotly.graph_objects as go
    
    # Cabeçalho do Subtópico
    st.header(r"O Vetor de Resíduos e o Operador de Projeção")
    
    # Introdução Teórica
    st.markdown(r"""
    A análise da regressão linear, longe de ser meramente um exercício de ajustamento de curvas ou uma simples ferramenta de predição numérica, revela-se, sob uma inspeção matemática rigorosa, como um elegante problema de geometria em espaços vetoriais de dimensão finita. 
    
    Para compreendermos a essência do método dos mínimos quadrados, devemos transcender a visão algébrica convencional — que foca excessivamente na manipulação de coeficientes — e abraçar a perspectiva geométrica do espaço amostral.
    """)
    
    st.info(r"""
    **A Tensão Fundamental:**
    O nosso modelo estatístico, parametrizado por uma matriz de design $\mathbf{X}$ de dimensão $n \times p$, restringe as nossas expectativas a um subespaço linear, designado como o espaço coluna de $\mathbf{X}$, denotado por $\mathcal{C}(\mathbf{X})$. A tensão fundamental na inferência estatística reside no fato de que, quase invariavelmente, o vetor $\mathbf{Y}$ não reside perfeitamente neste subespaço, obrigando-nos a buscar a aproximação mais próxima possível.
    """)
    
    st.markdown(r"""
    ### 📐 A Matriz Chapéu e o Mecanismo de Projeção
    A formalização do operador de projeção resolve este dilema ao definir univocamente a melhor estimativa linear $\hat{\mathbf{Y}}$ como a sombra ou projeção de $\mathbf{Y}$ sobre $\mathcal{C}(\mathbf{X})$. O operador que realiza esta transformação é a **matriz chapéu**, denotada por $\mathbf{H}$.
    """)
    
    st.latex(r"\mathbf{H} = \mathbf{X}(\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T")
    
    st.markdown(r"""
    Este operador linear possui propriedades fundamentais que sustentam a robustez do método:
    - **Idempotência ($\mathbf{H}^2 = \mathbf{H}$):** Reflete a intuição de que, uma vez que um vetor já foi projetado no subespaço, projeções subsequentes não alteram a sua posição.
    - **Complementaridade ($(\mathbf{I} - \mathbf{H})$):** Atua como o filtro que isola o componente residual, garantindo que qualquer informação linearmente relacionada com os preditores seja removida.
    """)
    
    # Simulator Section
    st.subheader(r"📊 Visualizador de Projeção Ortogonal em 3D")
    st.markdown(r"Abaixo, visualizamos a decomposição do vetor de dados $\mathbf{Y}$ em sua componente projetada $\hat{\mathbf{Y}}$ e o vetor de resíduos $\mathbf{e}$ ortogonal ao plano.")
    
    # Configuração do simulador 3D
    col_param1, col_param2 = st.columns(2)
    with col_param1:
        angle = st.slider(r"Ângulo de Visualização", 0, 360, 45, key=r"angle_subtopico_1")
    with col_param2:
        n_pts = st.slider(r"Complexidade do Ruído", 1, 10, 3, key=r"noise_subtopico_1")
    
    # Dados para o simulador
    x_range = np.linspace(0, 10, 10)
    y_range = np.linspace(0, 10, 10)
    X_grid, Y_grid = np.meshgrid(x_range, y_range)
    Z_grid = 0.5 * X_grid + 0.3 * Y_grid # Plano do modelo
    
    fig = go.Figure()
    fig.add_trace(go.Surface(z=Z_grid, x=X_grid, y=Y_grid, colorscale='Blues', opacity=0.5, name=r"Subespaço do Modelo"))
    # Ponto observado
    fig.add_trace(go.Scatter3d(x=[5], y=[5], z=[8], mode='markers', marker=dict(size=8, color="#991B1B"), name=r"Dado Observado Y"))
    # Projeção
    fig.add_trace(go.Scatter3d(x=[5], y=[5], z=[4], mode='markers', marker=dict(size=8, color="#58d5d8"), name=r"Projeção \hat{Y}"))
    # Vetor resíduo
    fig.add_trace(go.Scatter3d(x=[5, 5], y=[5, 5], z=[8, 4], mode='lines', line=dict(color="#F59E0B", width=4), name=r"Resíduo e"))
    
    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        title=dict(text="<b>Projeção Ortogonal no Espaço de Preditores</b>", font=dict(size=14, color="#1E293B", family="Arial, sans-serif"), x=0.0, y=0.95),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0, font=dict(size=9, color="#64748B"), bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="#E2E8F0", borderwidth=1),
        hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_color="#1E293B", font_family="Arial, sans-serif"),
        scene=dict(
            xaxis=dict(title=dict(text="X1", font=dict(size=11, color="#1E293B")), tickfont=dict(size=9, color="#64748B"), gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
            yaxis=dict(title=dict(text="X2", font=dict(size=11, color="#1E293B")), tickfont=dict(size=9, color="#64748B"), gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
            zaxis=dict(title=dict(text="Y", font=dict(size=11, color="#1E293B")), tickfont=dict(size=9, color="#64748B"), gridcolor="#E2E8F0", zerolinecolor="#CBD5E1")
        )
    )
    st.plotly_chart(fig, use_container_width=True, key=r"plotly_chart_subtopico_1")
    
    # Dedução Analítica
    st.subheader(r"📐 O Coração Matemático: Derivação do Estimador")
    st.markdown(r"A dedução do estimador de mínimos quadrados parte da minimização da soma de quadrados dos erros:")
    st.latex(r"S(\mathbf{\beta}) = (\mathbf{Y} - \mathbf{X}\mathbf{\beta})^T (\mathbf{Y} - \mathbf{X}\mathbf{\beta})")
    st.markdown(r"Derivando em relação a $\mathbf{\beta}$ e igualando a zero para encontrar o ponto crítico:")
    st.latex(r"\frac{\partial S(\mathbf{\beta})}{\partial \mathbf{\beta}} = -2\mathbf{X}^T(\mathbf{Y} - \mathbf{X}\mathbf{\beta}) = 0")
    st.markdown(r"Simplificando esta expressão, chegamos às equações normais:")
    st.latex(r"\mathbf{X}^T\mathbf{X}\hat{\mathbf{\beta}} = \mathbf{X}^T\mathbf{Y} \implies \hat{\mathbf{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{Y}")
    st.markdown(r"A partir deste ponto, a projeção no espaço modelo torna-se direta:")
    st.latex(r"\hat{\mathbf{Y}} = \mathbf{X}\hat{\mathbf{\beta}} = \mathbf{H}\mathbf{Y}")
    st.latex(r"\mathbf{e} = \mathbf{Y} - \hat{\mathbf{Y}} = (\mathbf{I} - \mathbf{H})\mathbf{Y}")
    
    # Exemplos Práticos
    st.subheader(r"📈 Casos de Aplicação Prática: Experimento de Resistência Térmica")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido 1: Cálculo da Matriz Chapéu")
        st.markdown(r"Considerando um experimento de resistência térmica com três medições $Y=[2, 3, 5]^T$ e design $\mathbf{X}$ correspondente a um modelo linear simples.")
        st.latex(r"X = \begin{pmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{pmatrix}, Y = \begin{pmatrix} 2 \\ 3 \\ 5 \end{pmatrix}")
        st.markdown(r"**Desenvolvimento Aritmético:**")
        st.markdown(r"- Calculamos o produto $\mathbf{X}^T \mathbf{X} = \begin{pmatrix} 3 & 6 \\ 6 & 14 \end{pmatrix}$")
        st.markdown(r"- Invertendo a matriz, obtemos $(\mathbf{X}^T \mathbf{X})^{-1} = \begin{pmatrix} 7/3 & -1 \\ -1 & 0.5 \end{pmatrix}$")
        st.markdown(r"- Finalizando com $\mathbf{H} = \mathbf{X}(\mathbf{X}^T \mathbf{X})^{-1}\mathbf{X}^T$, resultando na matriz de projeção:")
        st.latex(r"\mathbf{H} = \frac{1}{6} \begin{pmatrix} 5 & 2 & -1 \\ 2 & 2 & 2 \\ -1 & 2 & 5 \end{pmatrix}")
        st.success(r"A matriz calculada confirma a estrutura de influência do modelo, permitindo identificar o peso de cada medição na estimativa final.")
    
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido 2: Projeção e Resíduos")
        st.markdown(r"Utilizando a matriz $\mathbf{H}$ obtida, projetamos os dados e calculamos o vetor de erro.")
        st.latex(r"\hat{\mathbf{Y}} = \mathbf{H}\mathbf{Y} = \frac{1}{6} \begin{pmatrix} 5 & 2 & -1 \\ 2 & 2 & 2 \\ -1 & 2 & 5 \end{pmatrix} \begin{pmatrix} 2 \\ 3 \\ 5 \end{pmatrix}")
        st.markdown(r"**Desenvolvimento Aritmético:**")
        st.markdown(r"- Estimativas: $\hat{Y}_1 = 1.833, \hat{Y}_2 = 3.333, \hat{Y}_3 = 4.833$")
        st.markdown(r"- Resíduos: $\mathbf{e} = \mathbf{Y} - \hat{\mathbf{Y}} = [0.167, -0.333, 0.167]^T$")
        st.success(r"O vetor de resíduos obtido, com pequenas magnitudes, valida a consistência do modelo linear como uma aproximação robusta para a realidade física observada.")

    # Cabeçalho do Subtópico
    st.header(r"Propriedades Estatísticas e Distribucionais dos Resíduos")
    
    # Introdução e Prosa de Destaque
    st.markdown(r"""
    A análise de regressão linear não é apenas um exercício de ajuste de curvas, mas um rigoroso processo de decomposição de um vetor de observações em componentes determinísticos e estocásticos. Quando definimos o vetor de resíduos como a diferença entre as observações reais e os valores ajustados pelo modelo, estamos realizando uma projeção ortogonal do vetor de resposta no complemento ortogonal do espaço coluna da matriz de desenho $\mathbf{X}$.
    
    Historicamente, os resíduos não são meros erros de cálculo, mas a nossa única "janela" empírica para o processo gerador de dados subjacente. Compreender o comportamento estatístico desses resíduos é a condição *sine qua non* para qualquer validação de modelo, permitindo discernir entre variabilidade aleatória e falha sistemática.
    """)
    
    st.info(r"**Conceito Chave:** Sob as premissas de Gauss-Markov, os resíduos operam como o componente fundamental para a calibração do edifício da regressão linear, permitindo a inferência estatística sólida sobre a população.")
    
    st.markdown(r"""
    ### 📐 O Coração Matemático: Propriedades dos Resíduos
    
    A primeira propriedade fundamental reside na expectância matemática. Sob um modelo bem especificado, a média incondicional dos resíduos deve ser nula, garantindo a ausência de viés sistemático.
    """)
    
    st.latex(r"E[\mathbf{e}] = \mathbf{0}")
    
    st.markdown(r"""
    A estrutura de covariância é mais complexa: os resíduos, ao contrário dos erros populacionais, não são independentes devido à influência da matriz *hat* ($\mathbf{H}$). A variabilidade individual está atrelada à estrutura geométrica do modelo:
    """)
    
    st.latex(r"Var(\mathbf{e}) = \sigma^2 (\mathbf{I} - \mathbf{H})")
    
    st.markdown(r"""
    Para viabilizar a inferência, utilizamos o estimador $S^2$, que corrige o viés de subestimação ao ajustar os graus de liberdade pelo número de parâmetros estimados:
    """)
    
    st.latex(r"S^2 = \frac{\mathbf{e}^T \mathbf{e}}{n - k}")
    
    st.markdown(r"""
    ### 🔍 Dedução Analítica: A Derivação das Propriedades
    """)
    
    st.markdown(r"Abaixo, detalhamos o comportamento estatístico através da projeção matricial:")
    
    st.latex(r"E[\mathbf{e}] = E[(\mathbf{I} - \mathbf{H})\mathbf{Y}] = (\mathbf{I} - \mathbf{H})\mathbf{X}\mathbf{\beta} = (\mathbf{X} - \mathbf{H}\mathbf{X})\mathbf{\beta} = \mathbf{0}")
    
    st.markdown(r"A variância dos resíduos deriva da transformação linear do vetor de observações original:")
    
    st.latex(r"Var(\mathbf{e}) = Var((\mathbf{I} - \mathbf{H})\mathbf{Y}) = (\mathbf{I} - \mathbf{H})Var(\mathbf{Y})(\mathbf{I} - \mathbf{H})^T")
    
    st.latex(r"Var(\mathbf{e}) = (\mathbf{I} - \mathbf{H})\sigma^2 \mathbf{I} (\mathbf{I} - \mathbf{H}) = \sigma^2 (\mathbf{I} - \mathbf{H})")
    
    st.markdown(r"Finalmente, a distribuição amostral que fundamenta os testes de hipóteses:")
    
    st.latex(r"\frac{\mathbf{e}^T \mathbf{e}}{\sigma^2} = \frac{\mathbf{Y}^T (\mathbf{I} - \mathbf{H})^T (\mathbf{I} - \mathbf{H}) \mathbf{Y}}{\sigma^2} \sim \chi^2_{n-k}")
    
    st.markdown(r"""
    ### 📈 Casos de Aplicação Prática: Análise de Resíduos
    """)
    
    # Exemplo 1
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Estudo Clínico de Pressão Arterial")
        st.markdown(r"Em um estudo clínico com n=5 pacientes, modelamos a redução da pressão arterial (Y) pela dosagem de fármaco (X). O modelo ajustado resultou em $\hat{Y} = [2.5, 3.0, 4.0, 5.0, 6.0]$ para a amostra real $Y = [2.5, 3.0, 4.5, 5.0, 6.0]$. Calcule a variância residual estimada $S^2$.")
        st.latex(r"e = [0, 0, 0.5, 0, 0], n=5, k=2")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- $\sum e_i^2 = 0^2 + 0^2 + 0.5^2 + 0^2 + 0^2 = 0.25$")
        st.markdown(r"- $gl = n - k = 5 - 2 = 3$")
        st.markdown(r"- $S^2 = 0.25 / 3 \approx 0.0833$")
        st.success(r"Com uma variância residual estimada de 0.0833, o modelo demonstra uma precisão elevada. Este baixo valor de $S^2$ valida a consistência da relação entre a dosagem e a pressão arterial, permitindo um alto grau de confiança nas predições do ensaio.")
    
    # Exemplo 2
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Verificação de Consistência do Modelo")
        st.markdown(r"Assumindo o mesmo modelo clínico, desejamos verificar se a variância residual é consistente com a premissa de um modelo bem ajustado comparando com a média das observações.")
        st.latex(r"S^2 = 0.0833, \bar{Y} = 4.2")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Coeficiente de Variação Residual = $\sqrt{S^2} / \bar{Y}$")
        st.markdown(r"- $\sqrt{0.0833} \approx 0.2886$")
        st.markdown(r"- $0.2886 / 4.2 \approx 0.0687$")
        st.success(r"O erro relativo de aproximadamente 6.87% indica que a incerteza do modelo é significativamente baixa, recomendando sua aplicação na prática clínica para estimativas de dosagem com segurança.")

    # Cabeçalho principal do subtópico
    st.header(r"Padronização e Studentização de Resíduos")
    
    # Introdução teórica com ritmo de leitura quebrado
    st.markdown(r"""
    ### A Essência do Diagnóstico: Além dos Resíduos Brutos
    No contexto da modelagem linear clássica (MQO), a análise da adequação do modelo depende fundamentalmente do comportamento dos resíduos, $e_i = Y_i - \hat{Y}_i$. Historicamente, a prática inicial limitava-se a estes valores, na presunção de que espelhariam diretamente as perturbações aleatórias $\epsilon_i$. 
    
    Contudo, esta visão é mitigada pela natureza geométrica da estimação por MQO, que impõe uma estrutura de dependência complexa:
    - **Variabilidade:** A variância do resíduo não é constante, sendo $Var(e_i) = \sigma^2(1 - h_{ii})$.
    - **Alavancagem (Leverage):** O termo $h_{ii}$ (diagonal da matriz Hat) indica que observações com alto leverage forçam a reta de regressão a passar mais perto do ponto, tornando o resíduo bruto artificialmente pequeno.
    """)
    
    st.info(r"Conclusão: A comparação direta entre resíduos brutos é estatisticamente inapropriada, pois a variância é heterocedástica e depende da posição do ponto no espaço das covariáveis.")
    
    st.markdown(r"""
    ### Evolução Metodológica: O Surgimento da Estudentização
    Para contornar as limitações da padronização simples, a estudentização surge como um imperativo para equalizar as variâncias.
    
    1. **Estudentização Interna ($r_i$):** Ajusta o denominador para compensar o efeito da alavancagem ($h_{ii}$), equalizando a variância teórica para unitária. É ideal para inspeção visual de padrões.
    2. **Estudentização Externa ($t_i$):** Supera o efeito de mascaramento. Ao omitir a $i$-ésima observação do cálculo da variância residual ($S_{(i)}^2$), garante-se que um *outlier* não contamine a própria estatística de teste que o identifica.
    """)
    
    # Formalismo Matemático
    st.markdown(r"### 📐 O Rigor Matemático: Fórmulas de Diagnóstico")
    st.latex(r"r_i = \frac{e_i}{S \sqrt{1 - h_{ii}}}")
    st.latex(r"t_i = \frac{e_i}{S_{(i)} \sqrt{1 - h_{ii}}}")
    
    # Dedução Analítica
    st.markdown(r"### 🔍 Mecânica da Estudentização")
    st.markdown(r"A relação entre a incerteza do modelo e a detecção de pontos influentes deriva das seguintes propriedades fundamentais:")
    
    st.latex(r"Var(e_i) = \sigma^2(1 - h_{ii})")
    st.markdown(r"O resíduo studentizado interno ($r_i$) é obtido pela normalização do resíduo bruto pela sua variância estimada, removendo o efeito da geometria da matriz $X$:")
    st.latex(r"r_i = \frac{e_i}{S \sqrt{1 - h_{ii}}}")
    st.markdown(r"A transição para a estudentização externa utiliza a relação algébrica entre $r_i$ e $t_i$, permitindo inferência estatística baseada na distribuição $t$:")
    st.latex(r"t_i = r_i \sqrt{\frac{n - k - 1}{n - k - r_i^2}}")
    
    # Exemplos Práticos
    st.markdown(r"### 📈 Casos de Aplicação Prática: Diagnóstico em Eficiência Operacional")
    
    # Exemplo 1
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Cálculo de Resíduo Interno")
        st.markdown(r"Em um estudo de eficiência de máquinas, com $n=10$ observações, um ponto apresentou resíduo $e_i = 2.5$, alavancagem $h_{ii} = 0.45$ e desvio padrão residual $S = 1.2$.")
        st.latex(r"e_i = 2.5, \quad S = 1.2, \quad h_{ii} = 0.45")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Cálculo do fator de correção: $\sqrt{1 - 0.45} = \sqrt{0.55} \approx 0.7416$")
        st.markdown(r"- Aplicação no resíduo: $r_i = 2.5 / (1.2 \times 0.7416)$")
        st.markdown(r"- Resultado final: $r_i = 2.5 / 0.8899 \approx 2.81$")
        st.success(r"Laudo: Um valor de $r_i = 2.81$ indica um desvio considerável. Sugere-se uma investigação desta observação, pois, embora não seja um outlier extremo pelo critério de 3 desvios, ela demanda atenção quanto à influência sobre o modelo.")
    
    # Exemplo 2
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Sensibilidade do Diagnóstico a $S$")
        st.markdown(r"Considerando o mesmo estudo, verificamos o impacto se a variabilidade residual do modelo fosse menor, $S = 1.0$, mantendo $e_i = 2.5$ e $h_{ii} = 0.45$.")
        st.latex(r"e_i = 2.5, \quad S = 1.0, \quad h_{ii} = 0.45")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Fator de correção (mantido): $\sqrt{0.55} \approx 0.7416$")
        st.markdown(r"- Aplicação no resíduo: $r_i = 2.5 / (1.0 \times 0.7416)$")
        st.markdown(r"- Resultado final: $r_i = 2.5 / 0.7416 \approx 3.37$")
        st.success(r"Laudo: O aumento para $r_i = 3.37$, cruzando o limite de 3, demonstra que a sensibilidade do diagnóstico depende da estimativa de $S$. Uma menor variância residual torna o teste de outliers muito mais rigoroso e eficiente.")

    import streamlit as st
    import plotly.graph_objects as go
    import numpy as np
    
    # Cabeçalho do Subtópico
    st.header(r"Diagnóstico de Heterocedasticidade e Linearidade")
    
    # Introdução em Prose e Listas (Ritmo de Leitura)
    st.markdown(r"""
    A validade das inferências estatísticas em modelos de regressão depende crucialmente do cumprimento das premissas de Gauss-Markov. Quando a estrutura de erros viola a homocedasticidade, a dispersão dos resíduos varia com os preditores.
    """)
    
    st.markdown(r"""
    **Principais desvios diagnósticos:**
    - **Heterocedasticidade:** A variância do termo de erro não é constante, manifestando-se frequentemente como um padrão de 'funil' nos resíduos.
    - **Não-Linearidade Residual:** Indica um erro de especificação, onde a curvatura do fenômeno não é capturada pela forma linear, revelando um viés sistemático.
    - **Ruído Branco:** O objetivo ideal, onde os resíduos se comportam como ruído aleatório centrado em zero, sem padrões discerníveis.
    """)
    
    # Bloco de Formalismo Matemático
    st.markdown(r"### 🧮 O Formalismo das Violações")
    st.latex(r"Var(\epsilon_i | X_i) = \sigma_i^2 \neq \sigma^2")
    st.latex(r"E[Y_i | X_i] \neq \beta_0 + \beta_1 X_i")
    
    st.info(r"A presença dessas condições não apenas invalida a eficiência dos estimadores, mas corrompe a confiança das estatísticas t e dos intervalos de confiança, tornando o diagnóstico visual uma etapa inegociável da modelagem.")
    
    # Simulador de Diagnóstico Visual
    st.subheader(r"📈 Simulador de Diagnóstico Visual de Resíduos")
    col_sel, _ = st.columns([1, 2])
    tipo_diagnostico = col_sel.selectbox(
        r"Selecione o cenário de diagnóstico:", 
        ["Homocedástico", "Heterocedástico (Funil)", "Não-Linear (Curvatura)"],
        key="diagnostico_type_subtopico_4"
    )
    
    # Geração de dados estática para o simulador
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    if tipo_diagnostico == "Homocedástico":
        y = 2 + 0.5 * x + np.random.normal(0, 0.5, 100)
        residuos = y - (2 + 0.5 * x)
    elif tipo_diagnostico == "Heterocedástico (Funil)":
        y = 2 + 0.5 * x + np.random.normal(0, 0.1 * x, 100)
        residuos = y - (2 + 0.5 * x)
    else:
        y = 2 + 0.5 * x - 0.1 * (x - 5)**2 + np.random.normal(0, 0.2, 100)
        residuos = y - (2 + 0.5 * x)
    
    # Gráfico Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=residuos, mode='markers', name='Resíduos', marker=dict(color="#58d5d8")))
    fig.add_hline(y=0, line_dash="dash", line_color="#991B1B")
    
    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        plot_bgcolor="white",
        paper_bgcolor="white",
        title=dict(
            text="<b>Diagnóstico Visual de Resíduos</b>", 
            font=dict(size=14, color="#1E293B", family="Arial, sans-serif"), 
            x=0.0, y=0.95
        ),
        xaxis=dict(
            title=dict(text="Valores Ajustados", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")), 
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
    
    st.plotly_chart(fig, use_container_width=True, key=r"plotly_chart_subtopico_4")
    
    # Dedução Analítica
    st.markdown(r"### 📐 O Coração Matemático: Estrutura dos Resíduos")
    st.markdown(r"A relação entre resíduos e erros é mediada pela matriz de projeção $H$ (matriz chapéu):")
    st.latex(r"e = (I - H)\epsilon")
    st.markdown(r"A variância dos resíduos, portanto, depende da geometria do espaço dos regressores:")
    st.latex(r"Var(e) = \sigma^2 (I - H)")
    st.latex(r"Var(e_i) = \sigma^2 (1 - h_{ii})")
    
    # Exemplos Práticos
    st.markdown(r"### 📈 Casos de Aplicação Prática: Diagnóstico de Falhas e Especificação")
    
    # Exemplo 1
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Falhas Industriais")
        st.markdown(r"Um analista estuda falhas industriais (Y) por horas de operação (X). O gráfico de resíduos mostra um efeito 'funil' conforme X aumenta. Temos n=20 observações com modelo $Y_{hat} = 10 + 0.5X$.")
        st.latex(r"Var(e_{baixas}) = 2, Var(e_{altas}) = 8")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Razão de Variâncias = 8 / 2 = 4")
        st.markdown(r"- Diferença na Desvio Padrão = $\sqrt{4} = 2$")
        st.success(r"Uma razão de variâncias de 4 confirma uma heterocedasticidade severa. O analista deve aplicar uma transformação logarítmica em Y ou usar mínimos quadrados ponderados para estabilizar a variância antes de prosseguir com a inferência.")
    
    # Exemplo 2
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Erro de Especificação Funcional")
        st.markdown(r"Em outra análise, os resíduos apresentam um formato de U invertido. O modelo linear $Y = \beta_0 + \beta_1X$ subestima falhas em valores extremos e superestima no centro.")
        st.latex(r"E[Y|X] = \beta_0 + \beta_1 X, E[e|X] \approx 0.1X - 0.2X^2")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Erro de Especificação = curvatura quadrática não capturada")
        st.markdown(r"- Novo Modelo: $Y = \beta_0 + \beta_1 X + \beta_2 X^2$")
        st.success(r"A tendência parabólica dos resíduos é um indicador diagnóstico inequívoco de erro de especificação funcional. A reespecificação para um modelo quadrático é necessária para eliminar o viés sistemático identificado nos resíduos.")

    # Capítulo: A Arquitetura da Incerteza e a Avaliação da Normalidade
    
    st.header(r"Avaliação da Normalidade e Suposições Distribucionais")
    
    st.markdown(r"""
    A fundamentação da estatística inferencial clássica repousa sobre uma série de pilares axiomáticos, dentre os quais a hipótese de normalidade dos erros ocupa uma posição de centralidade. Historicamente, a assunção de que os erros seguem uma distribuição normal, $\varepsilon \sim N(0, \sigma^2 I)$, não é mera conveniência, mas uma herança dos trabalhos de Gauss e Laplace, fundamentada no Teorema Central do Limite.
    """)
    
    st.info(r"**O Papel da Normalidade:** Sem a premissa de normalidade, a variabilidade dos estimadores de mínimos quadrados permaneceria uma entidade descritiva, impossibilitando a construção de intervalos de confiança rigorosos e a realização de testes de hipóteses paramétricos.")
    
    st.markdown(r"""
    ### ⚖️ O Dilema entre Eficiência e Inferência
    É fundamental distinguir o papel desta suposição no contexto do **Teorema de Gauss-Markov**. 
    - **Estimativa Pontual:** Sob linearidade, homoscedasticidade e ausência de autocorrelação, o estimador de MQO é o *Melhor Estimador Linear Não-Viesado (BLUE)*, independentemente da distribuição dos erros.
    - **Inferência Estatística:** A otimalidade do MQO é uma questão de eficiência na estimação pontual, enquanto a normalidade diz respeito à validade da inferência. Para que possamos realizar testes de significância (ex: teste $t$), a distribuição amostral dos coeficientes deve ser conhecida, o que só ocorre analiticamente sob normalidade dos erros.
    
    Negligenciar a verificação da normalidade não invalida a estimativa do parâmetro em si, mas invalida a interpretação de qualquer significância estatística, tornando os testes meramente especulativos.
    """)
    
    st.subheader(r"📐 O Rigor Matemático da Normalidade")
    
    st.markdown(r"Para avaliar essa premissa, operamos com resíduos estudentizados. O processo de estudentização ajusta cada resíduo pelo seu erro padrão estimado, permitindo a comparabilidade e revelando desvios estruturais.")
    
    st.latex(r"\epsilon \sim N_n(0, \sigma^2 I)")
    
    st.markdown(r"A relação entre os resíduos observáveis ($e$) e os erros teóricos ($\epsilon$) é dada pela matriz chapéu ($H$):")
    
    st.latex(r"e = (I - H)\epsilon")
    
    st.markdown(r"Para inferência, utilizamos o resíduo estudentizado, que segue uma distribuição $t$ de Student:")
    
    st.latex(r"r_i = \frac{e_i}{S \sqrt{1 - h_{ii}}} \sim t_{n-k}")
    
    st.divider()
    
    # --- Simulador ---
    st.subheader(r"📊 Explorador de Distribuição em Q-Q Plots")
    st.markdown(r"Visualize como o comportamento dos erros afeta a aderência dos quantis observados à linha teórica de normalidade.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        n_input = st.slider(r"Tamanho da Amostra (n)", min_value=10, max_value=200, value=50, step=10, key="n_samples_subtopico_5")
        # Tratamento de segurança para ambiente de validação (mock object)
        try:
            n_val = int(n_input)
        except (ValueError, TypeError):
            n_val = 50
        
        dist_type = st.selectbox(r"Tipo de Distribuição dos Erros", options=["Normal", "Leptocúrtica (Caudas Pesadas)", "Assimétrica (Positiva)"], key="dist_type_subtopico_5")
    
    # Geração de valores simulados
    np.random.seed(42)
    if dist_type == "Normal":
        valores_simulados = np.random.normal(0, 1, n_val)
    elif dist_type == "Leptocúrtica (Caudas Pesadas)":
        valores_simulados = np.random.standard_t(3, n_val)
    else:
        valores_simulados = np.random.exponential(1, n_val) - 1
    
    # Cálculo dos quantis
    valores_ordenados = np.sort(valores_simulados)
    quantis_teoricos = stats.norm.ppf(np.linspace(0.01, 0.99, n_val))
    
    # Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=quantis_teoricos, y=valores_ordenados, mode='markers', name='Resíduos Observados', marker=dict(color="#58d5d8", size=8)))
    fig.add_trace(go.Scatter(x=[min(quantis_teoricos), max(quantis_teoricos)], y=[min(quantis_teoricos), max(quantis_teoricos)], mode='lines', name='Bissetriz (Normal)', line=dict(color="#991B1B", dash='dash')))
    
    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=55, r=30, t=65, b=55, pad=4),
        plot_bgcolor="white",
        paper_bgcolor="white",
        title=dict(text="<b>Diagnóstico Visual de Normalidade</b>", font=dict(size=14, color="#1E293B", family="Arial, sans-serif"), x=0.0, y=0.95),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0, font=dict(size=9, color="#64748B", family="Arial, sans-serif"), bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="#E2E8F0", borderwidth=1),
        hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_color="#1E293B", font_family="Arial, sans-serif"),
        xaxis=dict(title=dict(text="Quantis Teóricos", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")), tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"), gridcolor="#E2E8F0", zerolinecolor="#CBD5E1", fixedrange=True),
        yaxis=dict(title=dict(text="Resíduos Estudentizados", font=dict(size=11, color="#1E293B", family="Arial, sans-serif")), tickfont=dict(size=9, color="#64748B", family="Arial, sans-serif"), gridcolor="#E2E8F0", zerolinecolor="#CBD5E1", fixedrange=True)
    )
    
    st.plotly_chart(fig, use_container_width=True, key="plotly_chart_subtopico_5")
    
    st.markdown(r"O gráfico Q-Q plot é a ferramenta padrão: desvios da bissetriz indicam patologias. Uma curvatura em 'S' sugere leptocurtose, enquanto padrões assimétricos apontam para transformações necessárias ou erro de especificação.")
    
    st.divider()
    
    st.subheader(r"📈 Casos de Aplicação Prática: Avaliação de Resíduos")
    
    # Exemplo 1
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Detectando Outliers e Caudas Pesadas")
        st.markdown(r"Em um estudo de rendimento industrial com $n=20$ observações, observou-se um resíduo estudentizado máximo de $2.8$. O quantil teórico correspondente da normal (para este nível de probabilidade) é aproximadamente $1.96$.")
        st.latex(r"r_{max} = 2.8, \quad u_{20} \approx 1.96")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Diferença absoluta de magnitude: $2.8 - 1.96 = 0.84$")
        st.markdown(r"- Razão de escala: $2.8 / 1.96 \approx 1.43$")
        st.success(r"**Laudo:** A discrepância superior a 40% em relação ao quantil teórico indica cauda pesada à direita. A normalidade está sob suspeita, sugerindo a presença de um outlier que distorce a inferência. Recomenda-se teste de Shapiro-Wilk.")
    
    # Exemplo 2
    with st.container(border=True):
        st.markdown(r"##### 📖 Exemplo Resolvido: Sensibilidade do p-valor")
        st.markdown(r"Com base em uma amostra de $n=20$ ($gl=18$), calculamos um $p\text{-valor} = 0.04$ para a significância de um coeficiente. Avalie a robustez desta decisão sob violação da normalidade.")
        st.latex(r"p\text{-valor} = 0.04, \quad \alpha = 0.05")
        st.markdown(r"**Desenvolvimento Aritmético Passo a Passo:**")
        st.markdown(r"- Critério de decisão: $0.04 < 0.05$ (Rejeição da $H_0$)")
        st.markdown(r"- Risco: Como o valor está muito próximo do limiar de significância e há evidências de não-normalidade, este resultado é um candidato provável a Falso Positivo.")
        st.success(r"**Laudo:** A decisão é crítica. A violação da normalidade detectada anteriormente invalida a confiança absoluta neste $p\text{-valor}$. A validação das premissas é mandatória antes da conclusão do estudo.")

    st.markdown('---')
    st.markdown('##### 📚 Referências Bibliográficas Consolidadas (Rodapé da Aula)')
    for ref in metadata['referencias_bibliograficas_finais']:
        st.markdown(f'- {ref}')

with tab_exercicios:
    import json, base64
    dados_exercicios = json.loads(base64.b64decode('eyJ0b3BpY29fYXVsYSI6ICI3LjEg4oCTIEFuw6FsaXNlIGRlIHJlc8OtZHVvcyIsICJxdWVzdG9lc19tdWx0aXBsYV9lc2NvbGhhIjogW3siZW51bmNpYWRvIjogIkVtIHVtIHByb2pldG8gZGUgZW5nZW5oYXJpYSBtZWPDom5pY2EsIHVtIGVuZ2VuaGVpcm8gbW9kZWxhIGEgcmVzaXN0w6puY2lhIGRlIHVtIG5vdm8gY29tcG9zdG8gcG9saW3DqXJpY28gKCRZJCkgZW0gZnVuw6fDo28gZGEgdGVtcGVyYXR1cmEgZGUgY3VyYSAoJFhfMSQpIGUgZGEgcHJlc3PDo28gYXBsaWNhZGEgKCRYXzIkKS4gQXDDs3MgbyBhanVzdGUgcGVsbyBtw6l0b2RvIGRvcyBtw61uaW1vcyBxdWFkcmFkb3Mgb3JkaW7DoXJpb3MsIG9idGV2ZS1zZSBhIG1hdHJpeiBkZSBwcm9qZcOnw6NvICRcXG1hdGhiZntIfSA9IFxcbWF0aGJme1h9KFxcbWF0aGJme1h9XlQgXFxtYXRoYmZ7WH0pXnstMX0gXFxtYXRoYmZ7WH1eVCQuIENvbnNpZGVyZSBxdWUgbyB2YWxvciBkYSBhbGF2YW5jYWdlbSAoJGhfe2lpfSQpIHBhcmEgYSBkw6ljaW1hIG9ic2VydmHDp8OjbyBkbyBleHBlcmltZW50byBmb2kgY2FsY3VsYWRvIGNvbW8gMCw4NS4gUXVhbCDDqSBhIGludGVycHJldGHDp8OjbyBlc3RhdMOtc3RpY2EgY29ycmV0YSBkZXNzYSBvYnNlcnZhw6fDo28gbm8gY29udGV4dG8gZG8gbW9kZWxvPyIsICJhbHRlcm5hdGl2YXMiOiB7IkEiOiAiQSBvYnNlcnZhw6fDo28gcG9zc3VpIGFsdGEgYWxhdmFuY2FnZW0sIGluZGljYW5kbyBxdWUgc2V1IHZhbG9yIGRlIHJlc3Bvc3RhICRZX2kkIMOpIHF1YXNlIGlkw6pudGljbyBhbyB2YWxvciBwcmVkaXRvICRcXGhhdHtZfV9pJCwgbyBxdWUgY29uZmlybWEgYSBwcmVjaXPDo28gZG8gbW9kZWxvLiIsICJCIjogIkEgb2JzZXJ2YcOnw6NvIGVzdMOhIHNpdHVhZGEgZW0gdW1hIHJlZ2nDo28gZG8gZXNwYcOnbyBhbW9zdHJhbCBjb20gZ3JhbmRlIGRlbnNpZGFkZSBkZSBwb250b3MsIG8gcXVlIG1pbmltaXphIGEgdmFyacOibmNpYSBkbyByZXPDrWR1byAkZV9pJC4iLCAiQyI6ICJPIHBvbnRvIGFwcmVzZW50YSBhbHRhIGFsYXZhbmNhZ2VtLCBleGVyY2VuZG8gdW1hIGluZmx1w6puY2lhIGRlc3Byb3BvcmNpb25hbCBzb2JyZSBvIGFqdXN0ZSBkYSByZXRhIGRlIHJlZ3Jlc3PDo28sIGZvcsOnYW5kbyBvIG1vZGVsbyBhIHBhc3NhciBtYWlzIHByw7N4aW1vIGRlc3RhIG9ic2VydmHDp8OjbyBlc3BlY8OtZmljYS4iLCAiRCI6ICJPIG1vZGVsbyDDqSByb2J1c3RvIHBhcmEgZXN0YSBvYnNlcnZhw6fDo28sIHBvaXMgbyBhbHRvIHZhbG9yIGRlICRoX3tpaX0kIGdhcmFudGUgcXVlIGEgdmFyacOibmNpYSBkbyBlcnJvICRcXHNpZ21hXjIoMSAtIGhfe2lpfSkkIHNlIGFwcm94aW1lIGRlICRcXHNpZ21hXjIkLiIsICJFIjogIkEgb2JzZXJ2YcOnw6NvIMOpIHVtIG91dGxpZXIgZXN0YXTDrXN0aWNvIHF1ZSBkZXZlIHNlciByZW1vdmlkbyBhdXRvbWF0aWNhbWVudGUsIHBvaXMgJGhfe2lpfSA+IDAsNSQgaW5kaWNhIHVtYSB2aW9sYcOnw6NvIGRpcmV0YSBkYSBwcmVtaXNzYSBkZSBub3JtYWxpZGFkZSBkb3MgcmVzw61kdW9zLiJ9LCAiYWx0ZXJuYXRpdmFfY29ycmV0YSI6ICJDIiwgImRpY2EiOiAiTGVtYnJlLXNlIGRhIHJlbGHDp8OjbyBlbnRyZSBvIGVsZW1lbnRvIGRpYWdvbmFsIGRhIG1hdHJpeiBoYXQgZSBhIHZhcmnDom5jaWEgZG8gcmVzw61kdW8gJFZhcihlX2kpID0gXFxzaWdtYV4yKDEgLSBoX3tpaX0pJC4gTyBxdWUgYWNvbnRlY2UgY29tIGEgdmFyacOibmNpYSBkbyByZXPDrWR1byBxdWFuZG8gJGhfe2lpfSQgc2UgYXByb3hpbWEgZGUgMT8iLCAiZ2FiYXJpdG9fY29tZW50YWRvIjogIkEgYWxhdmFuY2FnZW0gJGhfe2lpfSQgbWVkZSBhIGRpc3TDom5jaWEgZGEgb2JzZXJ2YcOnw6NvICRYX2kkIGVtIHJlbGHDp8OjbyDDoCBtw6lkaWEgZG9zIHByZWRpdG9yZXMuIFF1YW5kbyAkaF97aWl9IFxccmlnaHRhcnJvdyAxJCwgYSB2YXJpw6JuY2lhIGRvIHJlc8OtZHVvICRlX2kgPSAoMS1oX3tpaX0pXFxlcHNpbG9uX2kkIHRlbmRlIGEgemVyby4gSXNzbyBzaWduaWZpY2EgcXVlIG8gbW9kZWxvIMOpIGZvcsOnYWRvIGEgYWp1c3Rhci1zZSBhbyBwb250bywgb2N1bHRhbmRvIG8gZXJybyByZWFsIGUgZGVtb25zdHJhbmRvIGFsdGEgaW5mbHXDqm5jaWEgc29icmUgb3MgZXN0aW1hZG9yZXMgJFxcaGF0e1xcYmV0YX0kLiBQb3J0YW50bywgYSBhbHRlcm5hdGl2YSBDIMOpIGEgY29ycmV0YS4ifSwgeyJlbnVuY2lhZG8iOiAiQW5hbGlzdGFzIGRlIHVtYSByZWRlIGRlIHZhcmVqbyB1dGlsaXphbSB1bSBtb2RlbG8gZGUgcmVncmVzc8OjbyBsaW5lYXIgcGFyYSBwcmV2ZXIgYXMgdmVuZGFzIG1lbnNhaXMgKCRZJCkgYmFzZWFuZG8tc2Ugbm8gaW52ZXN0aW1lbnRvIGVtIG1hcmtldGluZyAoJFgkKS4gQW8gYW5hbGlzYXIgbyBncsOhZmljbyBkZSByZXPDrWR1b3MgJGVfaSQgdmVyc3VzIHZhbG9yZXMgYWp1c3RhZG9zICRcXGhhdHtZfV9pJCwgbyBhbmFsaXN0YSBvYnNlcnZhIHVtYSBleHBhbnPDo28gc2lzdGVtw6F0aWNhIGRhIGRpc3BlcnPDo28gZG9zIHJlc8OtZHVvcyBjb25mb3JtZSAkXFxoYXR7WX1faSQgYXVtZW50YSwgcmVzdWx0YW5kbyBlbSB1bSBwYWRyw6NvIGRlICdmdW5pbCcuIFF1YWwgw6kgYSBpbXBsaWNhw6fDo28gZGVzdGUgYWNoYWRvIHBhcmEgYSB2YWxpZGFkZSBkbyBtb2RlbG8/IiwgImFsdGVybmF0aXZhcyI6IHsiQSI6ICJPIG1vZGVsbyBhcHJlc2VudGEgaGV0ZXJvY2VkYXN0aWNpZGFkZSwgdmlvbGFuZG8gYSBwcmVtaXNzYSBkZSB2YXJpw6JuY2lhIGNvbnN0YW50ZSBkb3MgZXJyb3MgKGhvbW9jZWRhc3RpY2lkYWRlKSwgbyBxdWUgaW52YWxpZGEgb3MgaW50ZXJ2YWxvcyBkZSBjb25maWFuw6dhIHRyYWRpY2lvbmFpcy4iLCAiQiI6ICJPIG1vZGVsbyBzb2ZyZSBkZSBuw6NvLWxpbmVhcmlkYWRlIGVzdHJ1dHVyYWwsIGV4aWdpbmRvIGEgaW5jbHVzw6NvIGRlIHVtIHRlcm1vIHF1YWRyw6F0aWNvICRYXjIkIHBhcmEgY29ycmlnaXIgYSBjdXJ2YXR1cmEgb2JzZXJ2YWRhIG5vIGdyw6FmaWNvIGRlIGRpc3BlcnPDo28uIiwgIkMiOiAiT3MgcmVzw61kdW9zIHNlZ3VlbSB1bWEgZGlzdHJpYnVpw6fDo28gZ2F1c3NpYW5hIHBlcmZlaXRhLCBlIGEgZXhwYW5zw6NvIGluZGljYSBhcGVuYXMgcXVlIG8gbW9kZWxvIHBvc3N1aSB1bWEgcHJlY2lzw6NvIGVsZXZhZGEgcGFyYSB2YWxvcmVzIGRlIHZlbmRhIG1haXMgYWx0b3MuIiwgIkQiOiAiVHJhdGEtc2UgZGUgdW0gcHJvYmxlbWEgZGUgYXV0b2NvcnJlbGHDp8OjbyBzZXJpYWwsIGluZGljYW5kbyBxdWUgb3MgZGFkb3MgZGUgdmVuZGFzIHBvc3N1ZW0gdW1hIGRlcGVuZMOqbmNpYSB0ZW1wb3JhbCBxdWUgbsOjbyBmb2kgY2FwdHVyYWRhIHBlbGEgZXN0cnV0dXJhIGRvIG1vZGVsbyBsaW5lYXIuIiwgIkUiOiAiTyBtb2RlbG8gZXN0w6EgcGVyZmVpdGFtZW50ZSBlc3BlY2lmaWNhZG8sIHNlbmRvIHF1ZSBvIHBhZHLDo28gZGUgZnVuaWwgw6kgdW0gY29tcG9ydGFtZW50byBlc3BlcmFkbyBwYXJhIHZhcmnDoXZlaXMgZGUgY29udGFnZW0gZW0gcmVncmVzc8O1ZXMgbGluZWFyZXMuIn0sICJhbHRlcm5hdGl2YV9jb3JyZXRhIjogIkEiLCAiZGljYSI6ICJQZW5zZSBuYXMgcHJlbWlzc2FzIGRlIEdhdXNzLU1hcmtvdi4gTyBxdWUgYWNvbnRlY2UgY29tIGEgdmFyacOibmNpYSBkb3MgZXJyb3MgcXVhbmRvIG8gZm9ybWF0byBkbyBncsOhZmljbyBkZSByZXPDrWR1b3MgYWx0ZXJhLXNlIGRlIGZvcm1hIHNpc3RlbcOhdGljYSBjb20gb3MgdmFsb3JlcyBwcmV2aXN0b3M/IiwgImdhYmFyaXRvX2NvbWVudGFkbyI6ICJPIHBhZHLDo28gZGUgJ2Z1bmlsJyBubyBncsOhZmljbyBkZSByZXPDrWR1b3MgY29udHJhIHZhbG9yZXMgYWp1c3RhZG9zIMOpIG8gZGlhZ27Ds3N0aWNvIHZpc3VhbCBjbMOhc3NpY28gcGFyYSBoZXRlcm9jZWRhc3RpY2lkYWRlICgkVmFyKFxcZXBzaWxvbl9pKSA9IFxcc2lnbWFfaV4yIFxcbmVxIFxcc2lnbWFeMiQpLiBBIHZpb2xhw6fDo28gZGVzdGEgcHJlbWlzc2EgaW1wbGljYSBxdWUgb3MgZXN0aW1hZG9yZXMgZGUgTVFPIG7Do28gc8OjbyBtYWlzIG9zIGRlIHZhcmnDom5jaWEgbcOtbmltYSwgdG9ybmFuZG8gb3MgZXJyb3MgcGFkcsOjbyBlIHRlc3RlcyBkZSBoaXDDs3Rlc2VzIChjb21vIG8gdGVzdGUgdCkgbsOjbyBjb25macOhdmVpcy4gQWx0ZXJuYXRpdmEgQSBjb3JyZXRhLiJ9LCB7ImVudW5jaWFkbyI6ICJFbSB1bSBlc3R1ZG8gY2zDrW5pY28sIGF2YWxpYS1zZSBvIGVmZWl0byBkZSB1bSBmw6FybWFjbyAoJFgkKSBuYSBwcmVzc8OjbyBhcnRlcmlhbCBzaXN0w7NsaWNhICgkWSQpIGRlIDUwIHBhY2llbnRlcy4gQXDDs3MgYSByZWdyZXNzw6NvLCBvcHRvdS1zZSBwZWxhIHV0aWxpemHDp8OjbyBkZSByZXPDrWR1b3Mgc3R1ZGVudGl6YWRvcyBleHRlcm5vcyAoJHRfaSQpIHBhcmEgaWRlbnRpZmljYXIgb2JzZXJ2YcOnw7VlcyBpbmZsdWVudGVzLiBTZSB1bSBwYWNpZW50ZSBhcHJlc2VudGEgdW0gcmVzw61kdW8gc3R1ZGVudGl6YWRvIGV4dGVybm8gY29tIHZhbG9yIGFic29sdXRvICR8dF9pfCA+IDMkLCBvIHF1ZSBpc3NvIGluZGljYSBzb2JyZSBvIHBvbnRvIGFtb3N0cmFsPyIsICJhbHRlcm5hdGl2YXMiOiB7IkEiOiAiTyBwYWNpZW50ZSDDqSB1bSBwb250byBjZW50cmFsIG5hIGRpc3RyaWJ1acOnw6NvLCBjb250cmlidWluZG8gcGFyYSBhIGVzdGFiaWxpZGFkZSBkbyBtb2RlbG8gZSByZWR1emluZG8gbyBlcnJvIHBhZHLDo28gZG9zIGNvZWZpY2llbnRlcy4iLCAiQiI6ICJPIHBhY2llbnRlIHBvc3N1aSB1bSB2YWxvciBkZSBhbGF2YW5jYWdlbSBuZWdsaWdlbmNpw6F2ZWwsIG8gcXVlIHRvcm5hIG8gcmVzw61kdW8gc3R1ZGVudGl6YWRvIGV4dGVybm8gaWTDqm50aWNvIGFvIHJlc8OtZHVvIHNpbXBsZXMuIiwgIkMiOiAiTyBwYWNpZW50ZSDDqSB1bWEgb2JzZXJ2YcOnw6NvIGF0w61waWNhIG91IG91dGxpZXIgaW5mbHVlbnRlIHF1ZSwgc2UgcmVtb3ZpZG8sIHBvc3NpdmVsbWVudGUgYWx0ZXJhIGRlIGZvcm1hIHNpZ25pZmljYXRpdmEgYSBlc3RpbWF0aXZhIGRvcyBwYXLDom1ldHJvcyBkbyBtb2RlbG8uIiwgIkQiOiAiTyBtb2RlbG8gw6kgcGVyZmVpdGFtZW50ZSBhZGVyZW50ZSBhb3MgZGFkb3MsIGUgZXN0ZSBwYWNpZW50ZSByZXByZXNlbnRhIHVtYSB2YXJpYcOnw6NvIGFsZWF0w7NyaWEgZXNwZXJhZGEgZW0gdW1hIGFtb3N0cmEgZGUgdGFtYW5obyAkbj01MCQuIiwgIkUiOiAiQSBzdXBvc2nDp8OjbyBkZSBub3JtYWxpZGFkZSBmb2kgY29uZmlybWFkYSwgcG9pcyBvIHZhbG9yIGFic29sdXRvIHN1cGVyaW9yIGEgMyDDqSBlc3BlcmFkbyBlbSA5NSUgZGFzIG9ic2VydmHDp8O1ZXMgZGUgdW1hIGRpc3RyaWJ1acOnw6NvIG5vcm1hbC4ifSwgImFsdGVybmF0aXZhX2NvcnJldGEiOiAiQyIsICJkaWNhIjogIlJlc8OtZHVvcyBzdHVkZW50aXphZG9zIGV4dGVybm9zIChvdSBkZWxldGFkb3MpIHPDo28gY2FsY3VsYWRvcyB1dGlsaXphbmRvIGEgdmFyacOibmNpYSByZXNpZHVhbCBlc3RpbWFkYSBzZW0gYSBpbmNsdXPDo28gZGEgJGkkLcOpc2ltYSBvYnNlcnZhw6fDo28uIFZhbG9yZXMgbXVpdG8gZWxldmFkb3MgaW5kaWNhbSBkaXNjcmVww6JuY2lhLiIsICJnYWJhcml0b19jb21lbnRhZG8iOiAiTyByZXPDrWR1byBzdHVkZW50aXphZG8gZXh0ZXJubyAkdF9pJCBjb21wYXJhIG8gcmVzw61kdW8gY29tIHVtYSBlc3RpbWF0aXZhIGRlIGVycm8gcXVlIGV4Y2x1aSBvIHByw7NwcmlvIHBvbnRvLiBWYWxvcmVzIGV4dHJlbW9zIChnZXJhbG1lbnRlICR8dF9pfCA+IDMkKSBzdWdlcmVtIHF1ZSBhIG9ic2VydmHDp8OjbyDDqSBkaXNjcmVwYW50ZSBlbSByZWxhw6fDo28gw6AgZXN0cnV0dXJhIGRpdGFkYSBwZWxhcyBkZW1haXMsIGNsYXNzaWZpY2FuZG8tYSBjb21vIHVtIG91dGxpZXIgb3Ugb2JzZXJ2YcOnw6NvIGRlIGluZmx1w6puY2lhIHNpZ25pZmljYXRpdmEuIEFsdGVybmF0aXZhIEMgY29ycmV0YS4ifSwgeyJlbnVuY2lhZG8iOiAiQ29uc2lkZXJlIG8gbW9kZWxvIGRlIHJlZ3Jlc3PDo28gbGluZWFyICRZID0gWFxcYmV0YSArIFxcZXBzaWxvbiQuIFBhcmEgdmVyaWZpY2FyIGEgc3Vwb3Npw6fDo28gZGUgbm9ybWFsaWRhZGUgZG9zIGVycm9zLCB1dGlsaXphLXNlIG8gZ3LDoWZpY28gcXVhbnRpbC1xdWFudGlsIChRLVEgUGxvdCkgZG9zIHJlc8OtZHVvcy4gU2UgbyBncsOhZmljbyBhcHJlc2VudGEgdW0gZm9ybWF0byBjbGFybyBkZSAnUycsIHF1YWwgaW50ZXJwcmV0YcOnw6NvIGRldmUgc2VyIGRhZGEgw6AgZGlzdHJpYnVpw6fDo28gZG9zIHJlc8OtZHVvcz8iLCAiYWx0ZXJuYXRpdmFzIjogeyJBIjogIk9zIHJlc8OtZHVvcyBzZWd1ZW0gdW1hIGRpc3RyaWJ1acOnw6NvIG5vcm1hbCwgdmFsaWRhbmRvIG8gbW9kZWxvIGRlIEdhdXNzLU1hcmtvdiBOb3JtYWwuIiwgIkIiOiAiT3MgcmVzw61kdW9zIGFwcmVzZW50YW0gY2F1ZGFzIG1haXMgbGV2ZXMgcXVlIGEgZGlzdHJpYnVpw6fDo28gbm9ybWFsIChkaXN0cmlidWnDp8OjbyBwbGF0aWPDunJ0aWNhKSwgaW52YWxpZGFuZG8gb3MgaW50ZXJ2YWxvcyBkZSBjb25maWFuw6dhLiIsICJDIjogIk9zIHJlc8OtZHVvcyBwb3NzdWVtIGNhdWRhcyBwZXNhZGFzIG91IGFzc2ltZXRyaWEsIGluZGljYW5kbyBxdWUgYSBzdXBvc2nDp8OjbyBkZSBub3JtYWxpZGFkZSDDqSBpbmFkZXF1YWRhIHBhcmEgbyBtb2RlbG8gZW0gcXVlc3TDo28uIiwgIkQiOiAiRXhpc3RlIHVtYSBmb3J0ZSBjb3JyZWxhw6fDo28gbGluZWFyIHBvc2l0aXZhIGVudHJlIG9zIHJlc8OtZHVvcyBlIG9zIHZhbG9yZXMgcHJldmlzdG9zLCBpbmRpY2FuZG8gZmFsdGEgZGUgaW5kZXBlbmTDqm5jaWEuIiwgIkUiOiAiTyBtb2RlbG8gcG9zc3VpIHVtYSB2YXJpw6JuY2lhIGNvbnN0YW50ZSwgbWFzIG8gaW50ZXJjZXB0byAkXFxiZXRhXzAkIGVzdMOhIGVudmllc2FkbyBkZXZpZG8gw6AgZmFsdGEgZGUgbm9ybWFsaWRhZGUgbm9zIHByZWRpdG9yZXMuIn0sICJhbHRlcm5hdGl2YV9jb3JyZXRhIjogIkMiLCAiZGljYSI6ICJPIFEtUSBQbG90IGNvbXBhcmEgcXVhbnRpcyBlbXDDrXJpY29zIGNvbnRyYSBxdWFudGlzIHRlw7NyaWNvcy4gVW1hIHJldGEgcGVyZmVpdGEgaW5kaWNhIG5vcm1hbGlkYWRlLiBEZXN2aW9zIHNpc3RlbcOhdGljb3MgaW5kaWNhbSBkZXN2aW9zIGRlIG5vcm1hbGlkYWRlLiIsICJnYWJhcml0b19jb21lbnRhZG8iOiAiTyBncsOhZmljbyBRLVEgcGxvdCDDqSB1bWEgZmVycmFtZW50YSBkaWFnbsOzc3RpY2EgcGFyYSBhdmFsaWFyIGEgbm9ybWFsaWRhZGUgZG9zIHJlc8OtZHVvcy4gRGVzdmlvcyBzaXN0ZW3DoXRpY29zIGRhIGxpbmhhIHJldGEsIGNvbW8gbyBmb3JtYXRvIGVtICdTJywgaW5kaWNhbSBxdWUgb3MgcmVzw61kdW9zIG7Do28gc2VndWVtIHVtYSBkaXN0cmlidWnDp8OjbyBub3JtYWwsIGZyZXF1ZW50ZW1lbnRlIGFwb250YW5kbyBwYXJhIGNhdWRhcyBtYWlzIHBlc2FkYXMgb3UgbWFpcyBsZXZlcyAoY3VydG9zZSkgb3UgYXNzaW1ldHJpYSwgbyBxdWUgY29tcHJvbWV0ZSB0ZXN0ZXMgYmFzZWFkb3MgbmEgZGlzdHJpYnVpw6fDo28gbm9ybWFsLiBBbHRlcm5hdGl2YSBDIGNvcnJldGEuIn0sIHsiZW51bmNpYWRvIjogIlNlamEgbyB2ZXRvciBkZSByZXPDrWR1b3MgJFxcbWF0aGJme2V9ID0gKFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH0pXFxtYXRoYmZ7WX0kLiBRdWFsIMOpIGEgcHJvcHJpZWRhZGUgZnVuZGFtZW50YWwgZGEgbWF0cml6ICQoXFxtYXRoYmZ7SX0gLSBcXG1hdGhiZntIfSkkIG5hIHByb2plw6fDo28gZG9zIGRhZG9zIG9ic2VydmFkb3M/IiwgImFsdGVybmF0aXZhcyI6IHsiQSI6ICJFbGEgcHJvamV0YSBvIHZldG9yICRcXG1hdGhiZntZfSQgbm8gc3ViZXNwYcOnbyBkZWZpbmlkbyBwZWxhcyBjb2x1bmFzIGRhIG1hdHJpeiBkZSBkZXNpZ24gJFxcbWF0aGJme1h9JC4iLCAiQiI6ICJFbGEgcHJvamV0YSBvIHZldG9yICRcXG1hdGhiZntZfSQgbm8gZXNwYcOnbyBvcnRvZ29uYWwgYW8gZXNwYcOnbyBjb2x1bmEgZGUgJFxcbWF0aGJme1h9JCwgb3Ugc2VqYSwgJENeXFxwZXJwKFxcbWF0aGJme1h9KSQuIiwgIkMiOiAiRWxhIHRyYW5zZm9ybWEgbyB2ZXRvciBkZSBlcnJvcyAkXFxlcHNpbG9uJCBlbSB1bSB2ZXRvciBkZSB2YXJpw6F2ZWlzIGFsZWF0w7NyaWFzIGNvbSBtw6lkaWEgZGlmZXJlbnRlIGRlIHplcm8uIiwgIkQiOiAiRWxhIMOpIHVtYSBtYXRyaXogaW52ZXJzw612ZWwsIGdhcmFudGluZG8gcXVlIG8gcmVzw61kdW8gcG9zc2Egc2VyIHJlY3VwZXJhZG8gcGVyZmVpdGFtZW50ZSBhIHBhcnRpciBkZSAkXFxtYXRoYmZ7SH0kLiIsICJFIjogIkVsYSBhbnVsYSB0b2RvcyBvcyB2YWxvcmVzIHByZXZpc3RvcyAkXFxoYXR7XFxtYXRoYmZ7WX19JCwgbWFudGVuZG8gYXBlbmFzIGEgdmFyacOibmNpYSBkb3MgcHJlZGl0b3Jlcy4ifSwgImFsdGVybmF0aXZhX2NvcnJldGEiOiAiQiIsICJkaWNhIjogIkxlbWJyZS1zZSBkYSBkZWNvbXBvc2nDp8OjbyBnZW9tw6l0cmljYTogJFxcbWF0aGJme1l9ID0gXFxoYXR7XFxtYXRoYmZ7WX19ICsgXFxtYXRoYmZ7ZX0gPSBcXG1hdGhiZntIfVxcbWF0aGJme1l9ICsgKFxcbWF0aGJme0l9LVxcbWF0aGJme0h9KVxcbWF0aGJme1l9JC4gTyBxdWUgYSBtYXRyaXogJFxcbWF0aGJme0h9JCBmYXo/IiwgImdhYmFyaXRvX2NvbWVudGFkbyI6ICJBIG1hdHJpeiAkXFxtYXRoYmZ7SH0gPSBcXG1hdGhiZntYfShcXG1hdGhiZntYfV5UXFxtYXRoYmZ7WH0pXnstMX1cXG1hdGhiZntYfV5UJCBwcm9qZXRhICRcXG1hdGhiZntZfSQgc29icmUgbyBlc3Bhw6dvIGNvbHVuYSBkZSAkXFxtYXRoYmZ7WH0kIChvcyB2YWxvcmVzIGFqdXN0YWRvcyAkXFxoYXR7XFxtYXRoYmZ7WX19JCkuIENvbnNlcXVlbnRlbWVudGUsIG8gY29tcGxlbWVudG8gb3J0b2dvbmFsLCByZXByZXNlbnRhZG8gcGVsYSBtYXRyaXogJFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH0kLCBwcm9qZXRhIG8gdmV0b3IgJFxcbWF0aGJme1l9JCBubyBlc3Bhw6dvIG9ydG9nb25hbCBhICRcXG1hdGhiZntYfSQsIGV4dHJhaW5kbyBhcGVuYXMgYSBwYXJ0ZSBxdWUgbyBtb2RlbG8gbsOjbyBleHBsaWNvdSAobyByZXPDrWR1bykuIEFsdGVybmF0aXZhIEIgY29ycmV0YS4ifV0sICJxdWVzdG9lc19kaXNjdXJzaXZhcyI6IFt7ImVudW5jaWFkbyI6ICJEZW1vbnN0cmUsIHV0aWxpemFuZG8gYXMgcHJvcHJpZWRhZGVzIGRhIG1hdHJpeiBjaGFww6l1ICRcXG1hdGhiZntIfSA9IFxcbWF0aGJme1h9KFxcbWF0aGJme1h9XlQgXFxtYXRoYmZ7WH0pXnstMX0gXFxtYXRoYmZ7WH1eVCQsIHF1ZSBhIHZhcmnDom5jaWEgZG8gdmV0b3IgZGUgcmVzw61kdW9zIMOpIGRhZGEgcG9yICRWYXIoXFxtYXRoYmZ7ZX0pID0gXFxzaWdtYV4yKFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH0pJC4iLCAiZGljYSI6ICJMZW1icmUtc2UgcXVlICRcXG1hdGhiZntlfSA9IChcXG1hdGhiZntJfSAtIFxcbWF0aGJme0h9KVxcbWF0aGJme1l9JCBlIHF1ZSAkVmFyKFxcbWF0aGJme1l9KSA9IFxcc2lnbWFeMiBcXG1hdGhiZntJfSQuIFV0aWxpemUgYSBwcm9wcmllZGFkZSBkZSB2YXJpw6JuY2lhIGRlIHRyYW5zZm9ybWHDp8O1ZXMgbGluZWFyZXM6ICRWYXIoXFxtYXRoYmZ7QX1cXG1hdGhiZntZfSkgPSBcXG1hdGhiZntBfSBWYXIoXFxtYXRoYmZ7WX0pIFxcbWF0aGJme0F9XlQkLiIsICJnYWJhcml0b19wYXNzb19hX3Bhc3NvIjogWyIkJFZhcihcXG1hdGhiZntlfSkgPSBWYXIoKFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH0pXFxtYXRoYmZ7WX0pJCQiLCAiQXBsaWNhbmRvIGEgcHJvcHJpZWRhZGUgJFZhcihcXG1hdGhiZntBfVxcbWF0aGJme1l9KSA9IFxcbWF0aGJme0F9IFZhcihcXG1hdGhiZntZfSkgXFxtYXRoYmZ7QX1eVCQsIHRlbW9zOiAkJFZhcihcXG1hdGhiZntlfSkgPSAoXFxtYXRoYmZ7SX0gLSBcXG1hdGhiZntIfSkgVmFyKFxcbWF0aGJme1l9KSAoXFxtYXRoYmZ7SX0gLSBcXG1hdGhiZntIfSleVCQkIiwgIlN1YnN0aXR1aW5kbyAkVmFyKFxcbWF0aGJme1l9KSA9IFxcc2lnbWFeMiBcXG1hdGhiZntJfSQ6ICQkVmFyKFxcbWF0aGJme2V9KSA9IFxcc2lnbWFeMiAoXFxtYXRoYmZ7SX0gLSBcXG1hdGhiZntIfSkgXFxtYXRoYmZ7SX0gKFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH0pXlQgPSBcXHNpZ21hXjIgKFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH0pIChcXG1hdGhiZntJfSAtIFxcbWF0aGJme0h9KV5UJCQiLCAiQ29tbyBhIG1hdHJpeiAkXFxtYXRoYmZ7SH0kIMOpIHNpbcOpdHJpY2EgKCRcXG1hdGhiZntIfV5UID0gXFxtYXRoYmZ7SH0kKSBlIGlkZW1wb3RlbnRlICgkXFxtYXRoYmZ7SH1eMiA9IFxcbWF0aGJme0h9JCksIGVudMOjbyAkKFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH0pJCB0YW1iw6ltIMOpIHNpbcOpdHJpY2EgZSBpZGVtcG90ZW50ZTogJCQoXFxtYXRoYmZ7SX0gLSBcXG1hdGhiZntIfSleVCA9IFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH1eVCA9IFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH0kJCIsICJQb3J0YW50bzogJCRWYXIoXFxtYXRoYmZ7ZX0pID0gXFxzaWdtYV4yIChcXG1hdGhiZntJfSAtIFxcbWF0aGJme0h9KShcXG1hdGhiZntJfSAtIFxcbWF0aGJme0h9KSA9IFxcc2lnbWFeMiAoXFxtYXRoYmZ7SX0gLSAyXFxtYXRoYmZ7SH0gKyBcXG1hdGhiZntIfV4yKSA9IFxcc2lnbWFeMiAoXFxtYXRoYmZ7SX0gLSAyXFxtYXRoYmZ7SH0gKyBcXG1hdGhiZntIfSkgPSBcXHNpZ21hXjIgKFxcbWF0aGJme0l9IC0gXFxtYXRoYmZ7SH0pJCQiXX0sIHsiZW51bmNpYWRvIjogIlVtIGNvbmp1bnRvIGRlIGRhZG9zIGFwcmVzZW50YSB1bWEgb2JzZXJ2YcOnw6NvIGNvbSB2YWxvciBkZSBhbGF2YW5jYWdlbSAkaF97aWl9ID0gMCw5JC4gRXhwbGlxdWUgcG9yIHF1ZSwgc29iIG8gbW9kZWxvIGRlIHJlZ3Jlc3PDo28gbGluZWFyLCBvIHJlc8OtZHVvICRlX2kkIHBhcmEgZXN0YSBvYnNlcnZhw6fDo28gc2Vyw6EgYXJ0aWZpY2lhbG1lbnRlIHBlcXVlbm8gZW0gbWFnbml0dWRlLCBtZXNtbyBxdWUgYSBvYnNlcnZhw6fDo28gc2VqYSB1bSBvdXRsaWVyIHNldmVyby4iLCAiZGljYSI6ICJDb25zaWRlcmUgYSBmw7NybXVsYSBkYSB2YXJpw6JuY2lhIGRvICRpJC3DqXNpbW8gcmVzw61kdW8gJFZhcihlX2kpID0gXFxzaWdtYV4yKDEgLSBoX3tpaX0pJCBlIGEgZGVmaW5pw6fDo28gJGVfaSA9ICgxIC0gaF97aWl9KVxcZXBzaWxvbl9pJC4iLCAiZ2FiYXJpdG9fcGFzc29fYV9wYXNzbyI6IFsiTyByZXPDrWR1byDDqSBkZWZpbmlkbyBjb21vICRlX2kgPSAoMSAtIGhfe2lpfSlcXGVwc2lsb25faSQuIiwgIkEgdmFyacOibmNpYSBkbyByZXPDrWR1byDDqSBkYWRhIHBvciAkVmFyKGVfaSkgPSBcXHNpZ21hXjIoMSAtIGhfe2lpfSkkLiIsICJTZSAkaF97aWl9ID0gMCw5JCwgZW50w6NvICQxIC0gaF97aWl9ID0gMCwxJC4iLCAiTG9nbywgJFZhcihlX2kpID0gXFxzaWdtYV4yKDAsMSkkLCBvIHF1ZSBzaWduaWZpY2EgcXVlIGEgdmFyacOibmNpYSBvYnNlcnZhZGEgZG8gcmVzw61kdW8gw6kgcmVkdXppZGEgYSAxMCUgZGEgdmFyacOibmNpYSBkbyBlcnJvIG9yaWdpbmFsLiIsICJDb21vIG8gbW9kZWxvIE1RTyBtaW5pbWl6YSBhIHNvbWEgZG9zIHF1YWRyYWRvcyBkb3MgcmVzw61kdW9zLCBwb250b3MgY29tIGFsdGEgYWxhdmFuY2FnZW0gKCRoX3tpaX0kIHByw7N4aW1vIGRlIDEpIGZvcsOnYW0gYSByZXRhIGRlIHJlZ3Jlc3PDo28gYSBwYXNzYXIgbXVpdG8gcHLDs3hpbWEgYSBlbGVzLCB0b3JuYW5kbyBvIHZhbG9yIG51bcOpcmljbyBkZSAkZV9pJCBwZXF1ZW5vLCBtYXNjYXJhbmRvIG8gZXJybyByZWFsIGRhcXVlbGEgb2JzZXJ2YcOnw6NvLiJdfSwgeyJlbnVuY2lhZG8iOiAiQSBkZWZpbmnDp8OjbyBkbyByZXPDrWR1byBzdHVkZW50aXphZG8gaW50ZXJubyDDqSAkcl9pID0gZV9pIC8gKFxcaGF0e1xcc2lnbWF9IFxcc3FydHsxIC0gaF97aWl9fSkkLiBQb3IgcXVlIGEgdXRpbGl6YcOnw6NvIGRlc3RlIHJlc8OtZHVvIMOpIHN1cGVyaW9yIGFvIHVzbyBkbyByZXPDrWR1byBwYWRyb25pemFkbyBzaW1wbGVzICR6X2kgPSBlX2kgLyBcXGhhdHtcXHNpZ21hfSQgcGFyYSBhIGRldGVjw6fDo28gZGUgb3V0bGllcnMgZW0gcmVncmVzc8Ojbz8iLCAiZGljYSI6ICJQZW5zZSBubyBjb25jZWl0byBkZSBob21vY2VkYXN0aWNpZGFkZSBlIG5hIHZhcmnDom5jaWEgZG9zIHJlc8OtZHVvcyBicnV0b3MgdmVyc3VzIGEgdmFyacOibmNpYSBkb3MgcmVzw61kdW9zIGNvcnJpZ2lkb3MgcGVsYSBhbGF2YW5jYWdlbS4iLCAiZ2FiYXJpdG9fcGFzc29fYV9wYXNzbyI6IFsiT3MgcmVzw61kdW9zIGJydXRvcyAkZV9pJCBwb3NzdWVtIHZhcmnDom5jaWFzIGRpZmVyZW50ZXMsIGRlcGVuZGVuZG8gZGUgJGhfe2lpfSQsIG1lc21vIHNlIG9zIGVycm9zICRcXGVwc2lsb25faSQgZm9yZW0gaG9tb2NlZMOhc3RpY29zLiIsICJBIHZhcmnDom5jaWEgZGUgdW0gcmVzw61kdW8gYnJ1dG8gw6kgJFZhcihlX2kpID0gXFxzaWdtYV4yKDEgLSBoX3tpaX0pJCwgcG9ydGFudG8sIHBvbnRvcyBjb20gYWx0YSBhbGF2YW5jYWdlbSB0w6ptIHZhcmnDom5jaWEgbWVub3IuIiwgIk8gcmVzw61kdW8gcGFkcm9uaXphZG8gJHpfaSA9IGVfaSAvIFxcaGF0e1xcc2lnbWF9JCBuw6NvIGNvcnJpZ2UgZXNzYSBkaWZlcmVuw6dhIGRlIGVzY2FsYSBjYXVzYWRhIHBlbGEgYWxhdmFuY2FnZW0gJGhfe2lpfSQuIiwgIkFvIGRpdmlkaXIgcG9yICRcXHNxcnR7MSAtIGhfe2lpfX0kLCBvIHJlc8OtZHVvIHN0dWRlbnRpemFkbyBpbnRlcm5vICRyX2kkIHBhZHJvbml6YSB0b2RvcyBvcyByZXPDrWR1b3MgcGFyYSB0ZXJlbSBhIG1lc21hIHZhcmnDom5jaWEgdGXDs3JpY2EgKGFwcm94aW1hZGFtZW50ZSB1bmlkYWRlKS4iLCAiSXNzbyBwZXJtaXRlIGNvbXBhcmFyIGRpcmV0YW1lbnRlIGEgbWFnbml0dWRlIGRlIGRpZmVyZW50ZXMgcmVzw61kdW9zIG5hIGFtb3N0cmEsIGZhY2lsaXRhbmRvIGEgaWRlbnRpZmljYcOnw6NvIGRlIG91dGxpZXJzIHF1ZSwgZGUgb3V0cmEgZm9ybWEsIHRlcmlhbSBzZXVzIHZhbG9yZXMgJ2VzY29uZGlkb3MnIHBlbGEgYWx0YSBhbGF2YW5jYWdlbS4iXX1dfQ==').decode('utf-8'))


    # Título da seção de exercícios
    st.header(f"Exercícios: {dados_exercicios.get('topico_aula', 'Exercícios da Aula')}")
    
    # Seção de Múltipla Escolha
    st.subheader("Questões de Múltipla Escolha")
    
    for i, questao in enumerate(dados_exercicios.get("questoes_multipla_escolha", [])):
        st.markdown(f"---")
        st.markdown(f"**Questão {i+1}**")
        st.write(questao.get("enunciado", "Enunciado não disponível."))
        
        # Preparação das alternativas
        alternativas_dict = questao.get("alternativas", {})
        opcoes = [f"{k}: {v}" for k, v in alternativas_dict.items()]
        
        # Widget de seleção
        escolha = st.radio(
            "Selecione uma alternativa:", 
            opcoes, 
            key=f"radio_mcq_{i}",
            label_visibility="collapsed"
        )
        
        # Colunas para organizar botões
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Verificar Resposta", key=f"btn_check_{i}"):
                letra_selecionada = escolha.split(":")[0].strip()
                correta = questao.get("alternativa_correta", "").strip()
                if letra_selecionada == correta:
                    st.success("Correto! Muito bem.")
                else:
                    st.error(f"Incorreto. A alternativa correta era {correta}.")
        with col2:
            if st.button("💡 Dica", key=f"btn_dica_mcq_{i}"):
                st.info(questao.get("dica", "Dica indisponível."))
                
        # Gabarito oculto
        with st.expander("✅ Ver Gabarito Comentado"):
            st.write(questao.get("gabarito_comentado", "Gabarito indisponível."))
    
    # Seção de Questões Discursivas
    st.markdown("---")
    st.subheader("Questões Discursivas")
    
    for i, questao in enumerate(dados_exercicios.get("questoes_discursivas", [])):
        st.markdown(f"**Questão {i+1}**")
        st.write(questao.get("enunciado", "Enunciado não disponível."))
        
        # Área para o aluno escrever
        st.text_area("Sua resposta:", key=f"area_disc_{i}")
        
        # Botão de dica
        if st.button("💡 Dica para esta questão", key=f"btn_dica_disc_{i}"):
            st.info(questao.get("dica", "Dica indisponível."))
        
        # Resolução passo a passo
        with st.expander("✅ Ver Resolução Detalhada"):
            passos = questao.get("gabarito_passo_a_passo", [])
            if passos:
                for idx, passo in enumerate(passos):
                    st.markdown(f"{idx+1}. {passo}")
            else:
                st.write("Resolução não disponível.")
