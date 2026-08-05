import streamlit as st
import os
import shutil
import time
import json
import re

# Função auxiliar para garantir carregamento de chave
from gerador_conteudo import carregar_chave_api

def substituir_simbolo(md_content, conceito, novo_simbolo):
    # Regex projetada para casar com: | **Conceito** | old_symbol |
    # e substituir old_symbol por novo_simbolo.
    padrao = rf"(\|\s*\*\*{re.escape(conceito)}\*\*\s*\|)[^|]+(\|)"
    novo_simbolo_escapado = novo_simbolo.replace("\\", "\\\\")
    md_content = re.sub(padrao, rf"\1 {novo_simbolo_escapado} \2", md_content)
    return md_content

def construir_relatorio_prosa_txt(exec_log, teoria_gigante_path, exercicios_path):
    """
    Constrói um relatório descritivo completo em formato TXT contendo todo o passo a passo,
    conteúdos intermediários, prosa expandida e exercícios da geração.
    """
    relatorio = []
    relatorio.append("======================================================================")
    relatorio.append("       RELATÓRIO DE AUDITORIA E HISTÓRICO COMPLETO DA AULA")
    relatorio.append("======================================================================")
    relatorio.append(f"Tema Global: {exec_log.get('tema', 'N/A')}")
    relatorio.append(f"Professor: {exec_log.get('professor', 'N/A')}")
    relatorio.append(f"Disciplina: {exec_log.get('disciplina', 'N/A')}")
    relatorio.append(f"Início da Geração: {exec_log.get('timestamp_inicio', 'N/A')}")
    relatorio.append(f"Fim da Geração: {exec_log.get('timestamp_fim', 'N/A')}")
    relatorio.append(f"Tempo Total: {exec_log.get('tempo_total_segundos', 0.0)} segundos")
    relatorio.append(f"Status Final: {exec_log.get('status', 'N/A').upper()}")
    relatorio.append("======================================================================\n")
    
    # 1. Roteiro e Cronograma
    relatorio.append("----------------------------------------------------------------------")
    relatorio.append("1. CRONOGRAMA E MÉTRICAS DAS ETAPAS DE DESENVOLVIMENTO")
    relatorio.append("----------------------------------------------------------------------")
    etapas = exec_log.get("etapas", {})
    for chave in sorted(etapas.keys()):
        et = etapas[chave]
        relatorio.append(f"- {et.get('descricao', 'Etapa')}:")
        relatorio.append(f"  * Status: {et.get('status', 'N/A')}")
        relatorio.append(f"  * Duração: {et.get('duracao_segundos', 0.0)} segundos")
    relatorio.append("\n")
    
    # 2. Conteúdo de Prosa por Subtópico
    if os.path.exists(teoria_gigante_path):
        try:
            with open(teoria_gigante_path, "r", encoding="utf-8") as f:
                teoria = json.load(f)
                
            relatorio.append("----------------------------------------------------------------------")
            relatorio.append("2. HISTÓRICO DE PRODUÇÃO DOS CONTEÚDOS E PROSA EXPANDIDA")
            relatorio.append("----------------------------------------------------------------------")
            
            subtopicos_log = etapas.get("3_escrita_revisao", {}).get("subtopicos", [])
            subtopicos_dict = {sub.get("titulo", ""): sub for sub in subtopicos_log}
            
            for idx, pagina in enumerate(teoria.get("paginas_conteudo", [])):
                titulo = pagina.get("titulo_subtopico", "Subtópico")
                relatorio.append(f"\n[Subtópico {idx+1}]: {titulo}")
                relatorio.append("-" * 40)
                
                # Exibe métricas de auditoria do revisor para este subtópico se existirem
                sub_info = subtopicos_dict.get(titulo)
                if sub_info:
                    relatorio.append(f"  * Auditoria do Revisor Científico:")
                    relatorio.append(f"    - Tentativas do Escritor: {sub_info.get('tentativas', 1)}")
                    relatorio.append(f"    - Reprovações do Revisor: {sub_info.get('reprovacoes', 0)}")
                    feedbacks = sub_info.get("feedbacks", [])
                    if feedbacks:
                        relatorio.append("    - Histórico de Feedbacks de Correção:")
                        for f_idx, fb in enumerate(feedbacks):
                            relatorio.append(f"      [Tentativa #{f_idx+1}] {fb}")
                
                relatorio.append("\n>>> A) PROSA BASE GERADA:")
                relatorio.append(pagina.get("discussao_teorica_prosa", "N/A"))
                relatorio.append("\n>>> B) FORMALISMO MATEMÁTICO (LaTeX):")
                relatorio.append(pagina.get("formalismo_latex", "N/A"))
                relatorio.append("\n>>> C) PROSA EXPANDIDA FINAL DE LIVRO DIDÁTICO:")
                relatorio.append(pagina.get("prosa_longa_expandida", "N/A"))
                relatorio.append("\n" + "=" * 40)
        except Exception as e:
            relatorio.append(f"[ERRO] Falha ao ler teoria para o relatório: {e}")
    else:
        relatorio.append("[AVISO] Arquivo de teoria não encontrado para detalhamento do conteúdo.")
        
    relatorio.append("\n")
    
    # 3. Exercícios Resolvidos
    if os.path.exists(exercicios_path):
        try:
            with open(exercicios_path, "r", encoding="utf-8") as f:
                exs = json.load(f)
                
            relatorio.append("----------------------------------------------------------------------")
            relatorio.append("3. CADERNO DE EXERCÍCIOS GERADO")
            relatorio.append("----------------------------------------------------------------------")
            
            relatorio.append("\n>>> A) QUESTÕES DE MÚLTIPLA ESCOLHA:")
            for q_idx, q in enumerate(exs.get("questoes_multipla_escolha", [])):
                relatorio.append(f"\nQuestão {q_idx+1}: {q.get('enunciado', 'N/A')}")
                for alt, texto in q.get("alternativas", {}).items():
                    relatorio.append(f"  {alt}) {texto}")
                relatorio.append(f"  * Dica: {q.get('dica', 'N/A')}")
                relatorio.append(f"  * Gabarito Correto: {q.get('alternativa_correta', 'N/A')}")
                relatorio.append(f"  * Justificativa: {q.get('gabarito_comentado', 'N/A')}")
                
            relatorio.append("\n>>> B) QUESTÕES DISCURSIVAS ABERTAS:")
            for q_idx, q in enumerate(exs.get("questoes_discursivas", [])):
                relatorio.append(f"\nQuestão {q_idx+1}: {q.get('enunciado', 'N/A')}")
                relatorio.append(f"  * Dica: {q.get('dica', 'N/A')}")
                relatorio.append("  * Resolução Passo a Passo:")
                for p_idx, passo in enumerate(q.get("gabarito_passo_a_passo", [])):
                    relatorio.append(f"    {p_idx+1}. {passo}")
        except Exception as e:
            relatorio.append(f"[ERRO] Falha ao ler exercícios para o relatório: {e}")
    else:
        relatorio.append("[AVISO] Arquivo de exercícios não encontrado para detalhamento.")
        
    relatorio.append("\n======================================================================")
    relatorio.append("                         FIM DO RELATÓRIO")
    relatorio.append("======================================================================")
    
    return "\n".join(relatorio)

def run_page():
    # Garante a carga da chave de API
    carregar_chave_api()

    # Inicializa estado para notações customizadas
    if "custom_notations" not in st.session_state:
        st.session_state.custom_notations = []

    # Título premium
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #1E3A8A; font-weight: 800; font-size: 2.5rem;">🪄 Painel de Criação de Aulas Acadêmicas</h1>
            <p style="color: #64748B; font-size: 1.1rem; font-style: italic;">
                Gere trilhas de aprendizagem completas de nível universitário premium com RAG pessoal e inteligência artificial
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Bloco informativo premium
    st.info("""
        **🎓 Como funciona a geração de aulas Plataforma 2.0:**
        1. **Alinhamento de Escopo**: O Agente Roteirista analisará a ementa em PDF enviada para desenhar uma trilha perfeitamente alinhada.
        2. **Construção e Revisão Crítica**: Os Agentes Escritor e Revisor redigirão o conteúdo e auditarão as fórmulas matemáticas em LaTeX.
        3. **Refinamento Editorial e Expansão**: O Editor-Chefe removerá repetições e o Construtor de Prosa expandirá a explicação em prosa densa de livro.
        4. **Caderno de Exercícios & Compilação**: Serão criadas 5 questões fechadas e 3 abertas antes do compilador costurar o simulador interativo em Plotly.
    """)

    # Layout de Entradas Principais (Sem st.form para permitir interações dinâmicas fluidas)
    st.markdown("### 📝 Identificação & Tema")
    col1, col2 = st.columns(2)
    with col1:
        nome_professor = st.text_input("Nome do Professor", help="Nome do professor responsável pela disciplina.")
    with col2:
        codigo_disciplina = st.text_input("Código da Disciplina", help="Código identificador da disciplina (ex: MATD38).")

    tema_solicitado = st.text_input("Tema da Aula", help="Tópico estatístico/matemático principal que será abordado na aula.")

    st.markdown("---")
    st.markdown("### 📂 Upload de Documentos")
    
    ementa_file = st.file_uploader(
        "Ementa da Disciplina (PDF) - OBRIGATÓRIO",
        type=["pdf"],
        help="O PDF oficial da ementa que ditará o escopo do que deve ser ensinado."
    )

    materiais_apoio = st.file_uploader(
        "Materiais de Apoio (PDFs) - OPCIONAL",
        type=["pdf"],
        accept_multiple_files=True,
        help="Livros, artigos ou notas de aula do professor para construir o RAG pessoal da disciplina."
    )

    # Seção opcional de customização de diretrizes
    st.markdown("---")
    
    notacoes_interface = {}
    
    with st.expander("📐 Customizar Diretrizes de Notação e Cores (Opcional)", expanded=False):
        st.markdown("""
            Selecione as abas abaixo para alterar símbolos de notação matemática e cores do template.
            Opções não alteradas manterão os padrões rigorosos de livro didático da plataforma.
        """)
        
        tab_d1, tab_d2, tab_d3, tab_d4, tab_d5 = st.tabs([
            "📊 População & Amostra", 
            "🔬 Inferência & Hipóteses", 
            "📈 Regressão & Correlação", 
            "🎲 Distribuições & Funções", 
            "➕ Customizadas"
        ])
        
        with tab_d1:
            st.markdown("##### 📊 Elementos de Amostra e População")
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                notacoes_interface["tamanho_amostral"] = st.text_input("Tamanho Amostral", value=r"$n$")
                notacoes_interface["tamanho_populacional"] = st.text_input("Tamanho Populacional", value=r"$N$")
                notacoes_interface["media_populacional"] = st.text_input("Média Populacional", value=r"$\mu$")
                notacoes_interface["media_amostral"] = st.text_input("Média Amostral", value=r"$\bar{X}$")
            with col_a2:
                notacoes_interface["variancia_populacional"] = st.text_input("Variância Populacional", value=r"$\sigma^2$")
                notacoes_interface["variancia_amostral"] = st.text_input("Variância Amostral", value=r"$S^2$")
                notacoes_interface["desvio_padrao_populacional"] = st.text_input("Desvio Padrão Populacional", value=r"$\sigma$")
                notacoes_interface["desvio_padrao_amostral"] = st.text_input("Desvio Padrão Amostral", value=r"$S$")
            with col_a3:
                notacoes_interface["proporcao_populacional"] = st.text_input("Proporção Populacional", value=r"$p$")
                notacoes_interface["proporcao_amostral"] = st.text_input("Proporção Amostral", value=r"$\hat{p}$")
                notacoes_interface["margem_erro"] = st.text_input("Margem de Erro", value=r"$E$")
                notacoes_interface["intervalo_confianca"] = st.text_input("Intervalo de Confiança", value=r"$IC$")
                notacoes_interface["erro_padrao_media"] = st.text_input("Erro Padrão da Média", value=r"$EP(\bar{X})$")

        with tab_d2:
            st.markdown("##### 🔬 Inferência Estatística & Testes de Hipóteses")
            col_h1, col_h2, col_h3 = st.columns(3)
            with col_h1:
                notacoes_interface["hipotese_nula"] = st.text_input("Hipótese Nula", value=r"$H_0$")
                notacoes_interface["hipotese_alternativa"] = st.text_input("Hipótese Alternativa", value=r"$H_1$")
                notacoes_interface["nivel_significancia"] = st.text_input("Nível de Significância (Alfa)", value=r"$\alpha$")
                notacoes_interface["nivel_confianca"] = st.text_input("Nível de Confiança", value=r"$1 - \alpha$")
                notacoes_interface["erro_tipo_2"] = st.text_input("Erro Tipo II (Beta)", value=r"$\beta$")
                notacoes_interface["poder_teste"] = st.text_input("Poder do Teste", value=r"$1 - \beta$")
            with col_h2:
                notacoes_interface["p_valor"] = st.text_input("P-Valor", value=r"$p\text{-valor}$")
                notacoes_interface["regiao_rejeicao"] = st.text_input("Região Crítica (Rejeição)", value=r"$RC$")
                notacoes_interface["graus_liberdade"] = st.text_input("Graus de Liberdade", value=r"$gl$")
                notacoes_interface["graus_liberdade_num"] = st.text_input("Graus de Liberdade (Numerador)", value=r"$gl_{\text{num}}$")
                notacoes_interface["graus_liberdade_den"] = st.text_input("Graus de Liberdade (Denominador)", value=r"$gl_{\text{den}}$")
            with col_h3:
                notacoes_interface["estatistica_z_calc"] = st.text_input("Estatística Z Calculada", value=r"$Z_{\text{calc}}$")
                notacoes_interface["estatistica_t_calc"] = st.text_input("Estatística t Calculada", value=r"$t_{\text{calc}}$")
                notacoes_interface["estatistica_chi2_calc"] = st.text_input("Estatística Qui-Quadrado Calculada", value=r"$\chi^2_{\text{calc}}$")
                notacoes_interface["estatistica_f_calc"] = st.text_input("Estatística F Calculada", value=r"$F_{\text{calc}}$")
                notacoes_interface["valor_critico_z"] = st.text_input("Valor Crítico Z", value=r"$Z_{\text{crit}}$")
                notacoes_interface["valor_critico_t"] = st.text_input("Valor Crítico t", value=r"$t_{\text{crit}}$")
                notacoes_interface["valor_critico_chi2"] = st.text_input("Valor Crítico Qui-Quadrado", value=r"$\chi^2_{\text{crit}}$")
                notacoes_interface["valor_critico_f"] = st.text_input("Valor Crítico F", value=r"$F_{\text{crit}}$")

        with tab_d3:
            st.markdown("##### 📈 Correlação, Regressão Linear & Somas de Quadrados")
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                notacoes_interface["correlacao_populacional"] = st.text_input("Correlação Populacional (Rho)", value=r"$\rho$")
                notacoes_interface["correlacao_amostral"] = st.text_input("Correlação Amostral (r)", value=r"$r$")
                notacoes_interface["coeficiente_determinacao"] = st.text_input("Coeficiente de Determinação (R²)", value=r"$R^2$")
                notacoes_interface["covariancia_populacional"] = st.text_input("Covariância Populacional", value=r"$\sigma_{XY}$")
                notacoes_interface["covariancia_amostral"] = st.text_input("Covariância Amostral", value=r"$S_{XY}$")
            with col_r2:
                notacoes_interface["intercepto_populacional"] = st.text_input("Intercepto Populacional (Beta 0)", value=r"$\beta_0$")
                notacoes_interface["inclinacao_populacional"] = st.text_input("Inclinação Populacional (Beta 1)", value=r"$\beta_1$")
                notacoes_interface["intercepto_estimado"] = st.text_input("Intercepto Estimado (Beta 0 chapéu)", value=r"$\hat{\beta}_0$")
                notacoes_interface["inclinacao_estimado"] = st.text_input("Inclinação Estimada (Beta 1 chapéu)", value=r"$\hat{\beta}_1$")
                notacoes_interface["residuo_amostral"] = st.text_input("Resíduo Amostral (Erro)", value=r"$e_i$")
            with col_r3:
                notacoes_interface["soma_quadrados_regressao"] = st.text_input("Soma de Quadrados da Regressão (SQR)", value=r"$SQR$")
                notacoes_interface["soma_quadrados_erro"] = st.text_input("Soma de Quadrados do Erro (SQE)", value=r"$SQE$")
                notacoes_interface["soma_quadrados_total"] = st.text_input("Soma de Quadrados Total (SQT)", value=r"$SQT$")

        with tab_d4:
            st.markdown("##### 🎲 Distribuições Teóricas & Notação Matemática de Funções")
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                notacoes_interface["distribuicao_normal"] = st.text_input("Distribuição Normal", value=r"$N(\mu, \sigma^2)$")
                notacoes_interface["distribuicao_normal_padrao"] = st.text_input("Distribuição Normal Padrão", value=r"$N(0, 1)$")
                notacoes_interface["distribuicao_t"] = st.text_input("Distribuição t de Student", value=r"$t(gl)$")
                notacoes_interface["distribuicao_qui_quadrado"] = st.text_input("Distribuição Qui-Quadrado", value=r"$\chi^2(gl)$")
            with col_f2:
                notacoes_interface["distribuicao_f"] = st.text_input("Distribuição F de Snedecor", value=r"$F(gl_{\text{num}}, gl_{\text{den}})$")
                notacoes_interface["distribuicao_binomial"] = st.text_input("Distribuição Binomial", value=r"$Bin(n, p)$")
                notacoes_interface["distribuicao_poisson"] = st.text_input("Distribuição Poisson", value=r"$Poi(\lambda)$")
            with col_f3:
                notacoes_interface["funcao_densidade"] = st.text_input("Função de Densidade / Probabilidade", value=r"$f(x)$")
                notacoes_interface["funcao_acumulada"] = st.text_input("Função de Distribuição Acumulada", value=r"$F(x)$")
                notacoes_interface["somatorio"] = st.text_input("Somatório", value=r"$\sum$")
                notacoes_interface["productorio"] = st.text_input("Produtório", value=r"$\prod$")
                notacoes_interface["integral"] = st.text_input("Integral", value=r"$\int$")

        with tab_d5:
            st.markdown("##### ➕ Adicionar Notações Personalizadas Dinâmicas")
            st.markdown("Adicione regras adicionais de notação matemática e símbolos livres para orientar a geração do professor:")
            
            # Renderiza as linhas de notações customizadas
            novas_remover = []
            for i, item in enumerate(st.session_state.custom_notations):
                col_k, col_v, col_del = st.columns([5, 5, 1])
                with col_k:
                    item["conceito"] = st.text_input(f"Nome do Conceito / Função {i+1}", value=item["conceito"], key=f"custom_k_{i}")
                with col_v:
                    item["simbolo"] = st.text_input(f"Símbolo em LaTeX {i+1}", value=item["simbolo"], key=f"custom_v_{i}")
                with col_del:
                    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("🗑️", key=f"custom_del_{i}"):
                        novas_remover.append(i)
            
            # Remove elementos marcados
            if novas_remover:
                for idx in sorted(novas_remover, reverse=True):
                    st.session_state.custom_notations.pop(idx)
                st.rerun()

            # Botão para adicionar mais uma linha
            if st.button("➕ Adicionar Linha de Notação"):
                st.session_state.custom_notations.append({"conceito": "", "simbolo": ""})
                st.rerun()

        st.markdown("---")
        st.markdown("##### 🎨 Identidade Visual (Cores)")
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        with col_c1:
            cor_principal = st.color_picker("Cor Primária (Identidade)", value="#1E3A8A")
        with col_c2:
            cor_secundaria = st.color_picker("Cor Secundária (Gráficos/Sucesso)", value="#10B981")
        with col_c3:
            cor_alerta = st.color_picker("Cor de Alerta (Aviso/Atenção)", value="#F59E0B")
        with col_c4:
            cor_critica = st.color_picker("Cor Crítica (Erro/Rejeição)", value="#991B1B")

        st.markdown("##### ✍️ Diretrizes de Estilo Livres")
        diretrizes_adicionais = st.text_area(
            "Diretrizes didáticas e regras de estilo adicionais (Texto Livre)",
            placeholder="Ex: Evitar anglicismos, focar em exemplos voltados a ciências biológicas..."
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Botão de Geração Principal (Fora de st.form para compatibilidade total com reruns)
    submit_btn = st.button("🚀 Gerar Aula Acadêmica Premium", type="primary", use_container_width=True)

    # Lógica ao pressionar o botão de gerar
    if submit_btn:
        # Validações estritas
        if not nome_professor.strip():
            st.error("Por favor, preencha o Nome do Professor.")
            return
        if not codigo_disciplina.strip():
            st.error("Por favor, preencha o Código da Disciplina.")
            return
        if not tema_solicitado.strip():
            st.error("Por favor, preencha o Tema da Aula.")
            return
        if not ementa_file:
            st.error("O upload da Ementa da Disciplina em formato PDF é obrigatório.")
            return

        # Executando a lógica de geração com visualizador de status
        t_inicio_geral_completo = time.time()
        
        # Inicializando log de execução
        exec_log = {
            "status": "iniciado",
            "timestamp_inicio": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tema": tema_solicitado,
            "professor": nome_professor,
            "disciplina": codigo_disciplina,
            "tempo_total_segundos": 0.0,
            "etapas": {}
        }
        
        status_box = st.status("Preparando ambiente e processando inputs...", expanded=True)
        
        temp_ementa_path = None
        try:
            # 1. Processamento e Indexação do RAG Pessoal (se houver materiais de apoio)
            nome_professor_clean = nome_professor.lower().strip()
            codigo_disciplina_clean = codigo_disciplina.lower().strip()
            
            t_start_rag = time.time()
            if materiais_apoio:
                status_box.update(label="📂 Indexando materiais de apoio no banco RAG...", state="running")
                temp_materials_dir = f"temp_rag_{nome_professor_clean}_{codigo_disciplina_clean}"
                os.makedirs(temp_materials_dir, exist_ok=True)
                
                for uploaded_file in materiais_apoio:
                    file_path = os.path.join(temp_materials_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Importa e executa a indexação
                from indexador_livros import inicializar_e_indexar
                inicializar_e_indexar(nome_professor_clean, codigo_disciplina_clean, temp_materials_dir)
                
                # Limpeza
                shutil.rmtree(temp_materials_dir, ignore_errors=True)
                status_box.write("✅ RAG pessoal do professor criado/atualizado com sucesso no Google Cloud!")
            else:
                status_box.write("ℹ️ Nenhum material de apoio enviado. Utilizando base global de RAG.")
            t_end_rag = time.time()
            exec_log["etapas"]["1_indexacao_rag"] = {
                "descricao": "Indexação dos Materiais de Apoio (RAG Pessoal)",
                "status": "sucesso" if materiais_apoio else "pulado",
                "duracao_segundos": round(t_end_rag - t_start_rag, 2)
            }

            # 2. Gravação temporária do PDF de ementa
            os.makedirs("cache", exist_ok=True)
            temp_ementa_path = os.path.join("cache", f"ementa_{nome_professor_clean}_{codigo_disciplina_clean}.pdf")
            with open(temp_ementa_path, "wb") as f:
                f.write(ementa_file.getbuffer())

            # 3. Processamento das Diretrizes de Notação e Cores (Substituições Cirúrgicas por Regex)
            diretrizes_texto = ""
            if os.path.exists("diretrizes_padrao.md"):
                with open("diretrizes_padrao.md", "r", encoding="utf-8") as f:
                    diretrizes_texto = f.read()

                # Anexa a tabela extra de funções gerais
                funcoes_adicionais = """
### 1.5 Notações Matemáticas e Funções Gerais
| Conceito | Símbolo Obrigatório (LaTeX) | Descrição |
| :--- | :--- | :--- |
| **Função de Densidade** | $f(x)$ | Função de densidade de probabilidade. |
| **Função de Distribuição Acumulada** | $F(x)$ | Função de probabilidade acumulada. |
| **Somatório** | $\\sum$ | Operador de somatório. |
| **Produtório** | $\\prod$ | Operador de produtório. |
| **Integral** | $\\int$ | Operador de integral. |
"""
                diretrizes_texto += funcoes_adicionais

                # Mapeia os inputs do painel para o texto correspondente do markdown
                notacoes_mapeamento = {
                    "tamanho_amostral": "Tamanho Amostral",
                    "tamanho_populacional": "Tamanho Populacional",
                    "media_populacional": "Média Populacional",
                    "media_amostral": "Média Amostral",
                    "variancia_populacional": "Variância Populacional",
                    "variancia_amostral": "Variância Amostral",
                    "desvio_padrao_populacional": "Desvio Padrão Populacional",
                    "desvio_padrao_amostral": "Desvio Padrão Amostral",
                    "proporcao_populacional": "Proporção Populacional",
                    "proporcao_amostral": "Proporção Amostral",
                    "margem_erro": "Margem de Erro",
                    "intervalo_confianca": "Intervalo de Confiança",
                    "erro_padrao_media": "Erro Padrão da Média",
                    
                    "hipotese_nula": "Hipótese Nula",
                    "hipotese_alternativa": "Hipótese Alternativa",
                    "nivel_significancia": "Nível de Significância",
                    "nivel_confianca": "Nível de Confiança",
                    "erro_tipo_2": "Probabilidade do Erro Tipo II",
                    "poder_teste": "Poder do Teste",
                    "p_valor": "P-Valor",
                    "regiao_rejeicao": "Região de Rejeição",
                    "graus_liberdade": "Graus de Liberdade",
                    "graus_liberdade_num": "Graus de Liberdade (Numerador)",
                    "graus_liberdade_den": "Graus de Liberdade (Denominador)",
                    "estatistica_z_calc": "Estatística Z Calculada",
                    "estatistica_t_calc": "Estatística t Calculada",
                    "estatistica_chi2_calc": "Estatística Qui-Quadrado Calc.",
                    "estatistica_f_calc": "Estatística F Calculada",
                    "valor_critico_z": "Valor Crítico Z",
                    "valor_critico_t": "Valor Crítico t",
                    "valor_critico_chi2": "Valor Crítico Qui-Quadrado",
                    "valor_critico_f": "Valor Crítico F",
                    
                    "distribuicao_normal": "Distribuição Normal",
                    "distribuicao_normal_padrao": "Distribuição Normal Padrão",
                    "distribuicao_t": "Distribuição t de Student",
                    "distribuicao_qui_quadrado": "Distribuição Qui-Quadrado",
                    "distribuicao_f": "Distribuição F de Snedecor",
                    "distribuicao_binomial": "Distribuição Binomial",
                    "distribuicao_poisson": "Distribuição Poisson",
                    
                    "correlacao_populacional": "Correlação Populacional",
                    "correlacao_amostral": "Correlação Amostral",
                    "coeficiente_determinacao": "Coeficiente de Determinação",
                    "covariancia_populacional": "Covariância Populacional",
                    "covariancia_amostral": "Covariância Amostral",
                    "intercepto_populacional": "Intercepto Populacional",
                    "inclinacao_populacional": "Inclinação Populacional",
                    "intercepto_estimado": "Intercepto Estimado",
                    "inclinacao_estimado": "Inclinação Estimada",
                    "residuo_amostral": "Resíduo Amostral",
                    "soma_quadrados_regressao": "Soma de Quadrados da Regressão",
                    "soma_quadrados_erro": "Soma de Quadrados do Erro",
                    "soma_quadrados_total": "Soma de Quadrados Total",

                    "funcao_densidade": "Função de Densidade",
                    "funcao_acumulada": "Função de Distribuição Acumulada",
                    "somatorio": "Somatório",
                    "productorio": "Produtório",
                    "integral": "Integral"
                }

                # Executa substituições
                for key, conceito in notacoes_mapeamento.items():
                    val = notacoes_interface.get(key)
                    if val:
                        diretrizes_texto = substituir_simbolo(diretrizes_texto, conceito, val)

                # Substituições de Cores Hexadecimais
                if cor_principal != "#1E3A8A":
                    diretrizes_texto = diretrizes_texto.replace('"PRIMARY_BLUE": "#1E3A8A"', f'"PRIMARY_BLUE": "{cor_principal}"')
                if cor_secundaria != "#10B981":
                    diretrizes_texto = diretrizes_texto.replace('"SECONDARY_GREEN": "#10B981"', f'"SECONDARY_GREEN": "{cor_secundaria}"')
                if cor_alerta != "#F59E0B":
                    diretrizes_texto = diretrizes_texto.replace('"WARNING_AMBER": "#F59E0B"', f'"WARNING_AMBER": "{cor_alerta}"')
                if cor_critica != "#991B1B":
                    diretrizes_texto = diretrizes_texto.replace('"CRITICAL_RED": "#991B1B"', f'"CRITICAL_RED": "{cor_critica}"')

                # Anexa as diretrizes adicionais livres
                if diretrizes_adicionais.strip():
                    diretrizes_texto += f"\n\n## ✍️ 3. Regras de Estilo e Diretrizes Customizadas Adicionais do Professor\n{diretrizes_adicionais.strip()}\n"

                # Anexa as notações personalizadas criadas dinamicamente
                if st.session_state.custom_notations:
                    custom_table = "\n### 1.6 Notações Personalizadas Adicionais do Professor\n| Conceito | Símbolo Obrigatório (LaTeX) | Descrição |\n| :--- | :--- | :--- |\n"
                    for item in st.session_state.custom_notations:
                        c_conceito = item.get("conceito", "").strip()
                        c_simbolo = item.get("simbolo", "").strip()
                        if c_conceito and c_simbolo:
                            custom_table += f"| **{c_conceito}** | {c_simbolo} | Definição personalizada adicionada dinamicamente pelo professor. |\n"
                    diretrizes_texto += custom_table

            # 4. Geração de Conteúdo da Aula [Agente 1 + 2 + 2.5]
            status_box.update(label="📋 Analisando a ementa e redigindo conteúdo com loop de revisão activa...", state="running")
            from gerador_conteudo import gerar_conteudo_aula
            
            payload_teoria = gerar_conteudo_aula(
                nome_professor=nome_professor,
                codigo_disciplina=codigo_disciplina,
                tema_solicitado=tema_solicitado,
                ementa_pdf_path=temp_ementa_path,
                diretrizes_texto=diretrizes_texto
            )
            
            if not payload_teoria:
                raise Exception("Falha operacional ao gerar o conteúdo teórico com a ementa fornecida.")

            status_box.write("✅ Roteiro pedagógico estruturado e subtopicos validados pelo Revisor!")
            
            # Captura logs internos do gerador
            log_gerador = payload_teoria.get("log_gerador", {})
            exec_log["etapas"]["2_roteirista"] = {
                "descricao": "Agente 1: Roteirista (Alinhamento de Escopo e Trilha)",
                "status": "sucesso",
                "duracao_segundos": log_gerador.get("tempo_roteirista_segundos", 0.0)
            }
            exec_log["etapas"]["3_escrita_revisao"] = {
                "descricao": "Agente 2 + 2.5: Escritor & Revisor (Loop de Revisão Ativa)",
                "status": "sucesso",
                "duracao_segundos": log_gerador.get("tempo_escrita_revisao_segundos", 0.0),
                "subtopicos": log_gerador.get("subtopicos", [])
            }

            # Salvando payload intermediário
            with open(os.path.join("cache", "payload_teoria.json"), "w", encoding="utf-8") as f:
                json.dump(payload_teoria, f, indent=4, ensure_ascii=False)

            # 5. Lapidação Editorial [Agente 3.5]
            status_box.update(label="🔍 Unificando trilha acadêmica e alocando simuladores interativos...", state="running")
            from orquestrador_editorial import lapidar_conteudo_global, expandir_subtopico_para_prosa_livro
            
            t_start_editorial = time.time()
            resultado_editorial = lapidar_conteudo_global(os.path.join("cache", "payload_teoria.json"))
            t_end_editorial = time.time()
            
            if not resultado_editorial:
                raise Exception("Falha crítica no processo editorial de unificação.")
            
            status_box.write("✅ Coerência global estabelecida e referências consolidadas no rodapé!")
            exec_log["etapas"]["4_lapidacao_editorial"] = {
                "descricao": "Agente 3.5: Editor-Chefe (Unificação e Coerência Global)",
                "status": "sucesso",
                "duracao_segundos": round(t_end_editorial - t_start_editorial, 2)
            }

            # 6. Expansão de Prosa Exaustiva [Agente 3.75]
            status_box.update(label="📖 Expandindo conteúdo para prosa exaustiva de livro acadêmico...", state="running")
            t_start_prosa = time.time()
            for idx, pagina in enumerate(resultado_editorial["paginas_conteudo"]):
                status_box.write(f"   -> Redigindo com profundidade o subtópico: *{pagina['titulo_subtopico']}*")
                dados_subtopico = {
                    "titulo_subtopico": pagina["titulo_subtopico"],
                    "discussao_teorica_prosa": pagina["discussao_teorica_prosa"],
                    "formalismo_latex": pagina["formalismo_latex"]
                }
                try:
                    prosa_longa = expandir_subtopico_para_prosa_livro(dados_subtopico)
                    pagina["prosa_longa_expandida"] = prosa_longa
                except Exception as e:
                    status_box.write(f"      [Aviso] Falha de expansão no subtópico, utilizando prosa base. Erro: {e}")
                    pagina["prosa_longa_expandida"] = pagina["discussao_teorica_prosa"]
                
                time.sleep(2) # Pausa de segurança anti-throttling
            t_end_prosa = time.time()
            exec_log["etapas"]["5_expansao_prosa"] = {
                "descricao": "Agente 3.75: Construtor de Prosa (Expansão Exaustiva de Livro)",
                "status": "sucesso",
                "duracao_segundos": round(t_end_prosa - t_start_prosa, 2)
            }

            with open(os.path.join("cache", "payload_teoria_gigante.json"), "w", encoding="utf-8") as f:
                json.dump(resultado_editorial, f, indent=4, ensure_ascii=False)

            # 7. Geração de Exercícios Resolvidos [Agente 3]
            status_box.update(label="📝 Projetando caderno de exercícios com múltipla escolha e discursivas...", state="running")
            from gerador_exercicios import gerar_caderno_exercicios
            
            t_start_exercicios = time.time()
            resultado_exercicios = gerar_caderno_exercicios(os.path.join("cache", "payload_teoria.json"), diretrizes_texto=diretrizes_texto)
            t_end_exercicios = time.time()
            
            if not resultado_exercicios:
                raise Exception("Erro ao gerar o caderno de exercícios.")

            with open(os.path.join("cache", "payload_exercicios.json"), "w", encoding="utf-8") as f:
                json.dump(resultado_exercicios, f, indent=4, ensure_ascii=False)
            
            status_box.write("✅ 5 Questões fechadas e 3 discursivas detalhadas com gabarito passo a passo geradas!")
            exec_log["etapas"]["6_caderno_exercicios"] = {
                "descricao": "Agente 3: Caderno de Exercícios (Questões Fechadas e Abertas)",
                "status": "sucesso",
                "duracao_segundos": round(t_end_exercicios - t_start_exercicios, 2)
            }

            # 8. Compilação da Interface Streamlit [Fase 6]
            status_box.update(label="📐 Compilando e costurando o código Streamlit responsivo final...", state="running")
            from gerador_interface import compilar_aula_completa_por_fatias
            
            t_start_interface = time.time()
            caminho_script_gerado = compilar_aula_completa_por_fatias(
                os.path.join("cache", "payload_teoria_gigante.json"),
                os.path.join("cache", "payload_exercicios.json"),
                motor_grafico="plotly",
                cor_principal=cor_principal,
                cor_critica=cor_critica,
                cor_secundaria=cor_secundaria,
                cor_alerta=cor_alerta
            )
            t_end_interface = time.time()
            
            status_box.write("✅ Arquivo Python executável gerado fisicamente na pasta `/aulas`!")
            exec_log["etapas"]["7_compilacao_interface"] = {
                "descricao": "Fase 6: Compilação de Interface Streamlit",
                "status": "sucesso",
                "duracao_segundos": round(t_end_interface - t_start_interface, 2)
            }

            # 9. Limpeza final e conclusão
            if temp_ementa_path and os.path.exists(temp_ementa_path):
                os.remove(temp_ementa_path)

            exec_log["status"] = "sucesso"
            exec_log["tempo_total_segundos"] = round(time.time() - t_inicio_geral_completo, 2)
            exec_log["timestamp_fim"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Salva o log de última execução para compatibilidade
            with open(os.path.join("cache", "ultimo_log_execucao.json"), "w", encoding="utf-8") as f:
                json.dump(exec_log, f, indent=4, ensure_ascii=False)

            # Salva o log específico associado à aula para persistência no repositório
            if caminho_script_gerado:
                nome_script = os.path.basename(caminho_script_gerado)
                os.makedirs("logdasaulasgeradas", exist_ok=True)
                caminho_log_especifico = os.path.join("logdasaulasgeradas", nome_script.replace(".py", ".log.json"))
                caminho_log_txt = os.path.join("logdasaulasgeradas", nome_script.replace(".py", ".log.txt"))
                
                try:
                    with open(caminho_log_especifico, "w", encoding="utf-8") as f:
                        json.dump(exec_log, f, indent=4, ensure_ascii=False)
                    status_box.write(f"✅ Relatório de auditoria persistido em '{caminho_log_especifico}'!")
                except Exception as log_ex:
                    status_box.write(f"⚠️ Aviso: Não foi possível salvar o log JSON da aula: {log_ex}")
                
                try:
                    teoria_gigante_path = os.path.join("cache", "payload_teoria_gigante.json")
                    exercicios_path = os.path.join("cache", "payload_exercicios.json")
                    relatorio_txt = construir_relatorio_prosa_txt(exec_log, teoria_gigante_path, exercicios_path)
                    
                    with open(caminho_log_txt, "w", encoding="utf-8") as f:
                        f.write(relatorio_txt)
                    status_box.write(f"✅ Relatório descritivo persistido em '{caminho_log_txt}'!")
                except Exception as txt_ex:
                    status_box.write(f"⚠️ Aviso: Não foi possível criar o relatório descritivo txt da aula: {txt_ex}")

                # Envia os arquivos gerados (.py, .log.json e .log.txt) ao repositório do GitHub
                sucesso_py = False
                sucesso_log = False
                sucesso_txt = False
                try:
                    from git_integration import commitar_arquivo_github
                    
                    status_box.write("🚀 Enviando aula gerada ao repositório GitHub...")
                    
                    nome_arquivo_py = os.path.basename(caminho_script_gerado)
                    caminho_repositorio_py = f"aulas/{nome_arquivo_py}"
                    sucesso_py = commitar_arquivo_github(
                        caminho_local=caminho_script_gerado,
                        caminho_repositorio=caminho_repositorio_py,
                        mensagem_commit=f"feat: adiciona aula {caminho_repositorio_py}"
                    )
                    
                    nome_arquivo_log = os.path.basename(caminho_log_especifico)
                    caminho_repositorio_log = f"logdasaulasgeradas/{nome_arquivo_log}"
                    sucesso_log = commitar_arquivo_github(
                        caminho_local=caminho_log_especifico,
                        caminho_repositorio=caminho_repositorio_log,
                        mensagem_commit=f"feat: adiciona log json {caminho_repositorio_log}"
                    )
                    
                    nome_arquivo_txt = os.path.basename(caminho_log_txt)
                    caminho_repositorio_txt = f"logdasaulasgeradas/{nome_arquivo_txt}"
                    sucesso_txt = commitar_arquivo_github(
                        caminho_local=caminho_log_txt,
                        caminho_repositorio=caminho_repositorio_txt,
                        mensagem_commit=f"feat: adiciona log descritivo txt {caminho_repositorio_txt}"
                    )
                    
                    if sucesso_py and sucesso_log and sucesso_txt:
                        status_box.write("✅ Sucesso! Arquivos salvos permanentemente no seu GitHub.")
                    else:
                        status_box.write("⚠️ Aviso: Arquivos gerados localmente, mas nem todos enviados ao GitHub.")
                except Exception as git_ex:
                    status_box.write(f"⚠️ Erro ao tentar salvar no GitHub: {git_ex}")

            status_box.update(label="🎉 Aula Acadêmica Gerada e Compilada com Sucesso!", state="complete")
            st.balloons()
            
            # Alerta explícito de salvamento no Git (solicitado pelo usuário)
            if sucesso_py and sucesso_log and sucesso_txt:
                st.success("✨ A geração foi concluída perfeitamente! Os arquivos da aula, do log JSON e do relatório TXT foram **salvos com sucesso no seu GitHub**.")
            elif sucesso_py:
                st.success("✨ A geração foi concluída perfeitamente! A aula foi salva no GitHub, mas alguns logs adicionais falharam ao commitar.")
            else:
                st.warning("✨ A geração foi concluída localmente! Os arquivos foram gravados na pasta `/aulas`, mas **não puderam ser enviados ao GitHub** (verifique suas credenciais).")
            
            # Força o rerun automático após a conclusão para carregar a nova aula
            st.rerun()

        except Exception as ex:
            # Garante limpeza da ementa temporária
            if temp_ementa_path and os.path.exists(temp_ementa_path):
                os.remove(temp_ementa_path)
            
            exec_log["status"] = "erro"
            exec_log["erro_mensagem"] = str(ex)
            exec_log["tempo_total_segundos"] = round(time.time() - t_inicio_geral_completo, 2)
            exec_log["timestamp_fim"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            with open(os.path.join("cache", "ultimo_log_execucao.json"), "w", encoding="utf-8") as f:
                json.dump(exec_log, f, indent=4, ensure_ascii=False)

            status_box.update(label="❌ Falha crítica no pipeline de geração!", state="error")
            st.error(f"Ocorreu um erro no pipeline de inteligência artificial: {ex}")

    # Seção de Auditoria e Logs Premium no final da página (Exposição Premium no Streamlit)
    opcoes_log = {}
    
    # 1. Adiciona o log de última execução como padrão se existir
    path_ultimo = os.path.join("cache", "ultimo_log_execucao.json")
    if os.path.exists(path_ultimo):
        opcoes_log["Última Execução"] = path_ultimo
        
    # 2. Faz a varredura dinâmica na pasta /logdasaulasgeradas por logs específicos de aulas
    if os.path.exists("logdasaulasgeradas"):
        arquivos_aulas = sorted(os.listdir("logdasaulasgeradas"))
        for f in arquivos_aulas:
            if f.endswith(".log.json"):
                caminho_log = os.path.join("logdasaulasgeradas", f)
                try:
                    with open(caminho_log, "r", encoding="utf-8") as lf:
                        data = json.load(lf)
                        tema = data.get("tema", "Sem Tema")
                        disciplina = data.get("disciplina", "Geral")
                        match = re.match(r'^aula(\d+)', f, flags=re.IGNORECASE)
                        num_str = f"Aula {int(match.group(1)):02d}" if match else "Aula"
                        label_bonito = f"📊 {num_str}: {tema} ({disciplina})"
                        opcoes_log[label_bonito] = caminho_log
                except Exception:
                    pass

    if opcoes_log:
        st.markdown("---")
        st.markdown("""
            <div style="margin-top: 2rem; margin-bottom: 1rem;">
                <h3 style="color: #1E3A8A; font-weight: 700; margin-bottom: 0.2rem;">📊 Relatório de Auditoria e Logs dos Agentes</h3>
                <p style="color: #64748B; font-size: 0.95rem; margin-top: 0px;">
                    Selecione o log de execução de uma aula gerada ou a última execução para detalhamento técnico.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        lista_opcoes = list(opcoes_log.keys())
        log_selecionado_label = st.selectbox("Selecione o Relatório de Auditoria:", options=lista_opcoes, index=0)
        log_path = opcoes_log[log_selecionado_label]
        
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                log_data = json.load(f)
            
            # 1. KPIs
            tempo_total = log_data.get("tempo_total_segundos", 0.0)
            status_exec = log_data.get("status", "desconhecido")
            
            subtopicos_log = log_data.get("etapas", {}).get("3_escrita_revisao", {}).get("subtopicos", [])
            total_tentativas = sum(sub.get("tentativas", 0) for sub in subtopicos_log)
            total_reprovacoes = sum(sub.get("reprovacoes", 0) for sub in subtopicos_log)
            
            # Contagem de erros API
            total_erros_429 = sum(sub.get("erros_api", {}).get("429", 0) for sub in subtopicos_log)
            total_erros_503 = sum(sub.get("erros_api", {}).get("503", 0) for sub in subtopicos_log)
            total_erros_outros = sum(sub.get("erros_api", {}).get("outros", 0) for sub in subtopicos_log)
            total_erros_api = total_erros_429 + total_erros_503 + total_erros_outros
            
            status_color = "#10B981" if status_exec == "sucesso" else "#EF4444"
            status_text = "🟢 SUCESSO" if status_exec == "sucesso" else "🔴 ERRO"
            
            col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
            with col_kpi1:
                st.metric("Status da Execução", status_text)
            with col_kpi2:
                if tempo_total > 60:
                    minutos = int(tempo_total // 60)
                    segundos = int(tempo_total % 60)
                    st.metric("Duração Total", f"{minutos}m {segundos}s", help="Tempo decorrido do início ao fim de todas as etapas.")
                else:
                    st.metric("Duração Total", f"{tempo_total}s", help="Tempo decorrido do início ao fim de todas as etapas.")
            with col_kpi3:
                st.metric("Tentativas do Escritor", f"{total_tentativas} tent.", help="Quantidade de vezes que o Agente Escritor redigiu conteúdo.")
            with col_kpi4:
                st.metric("Reprovações do Revisor", f"{total_reprovacoes} recusas", help="Número de vezes que o Revisor Científico mandou refazer.")
            with col_kpi5:
                st.metric("Falhas de API (429/503)", f"{total_erros_api} erros", help=f"Detalhamento: {total_erros_429} limite de cota (429) | {total_erros_503} indisp. servidor (503) | {total_erros_outros} outros.")
                
            # 2. Abas do painel
            tab_relatorio_txt, tab_duracao, tab_auditoria = st.tabs(["📄 Relatório Completo (TXT)", "⏱️ Cronograma das Etapas", "🤖 Auditoria do Loop de Escrita"])
            
            with tab_relatorio_txt:
                log_txt_path = log_path.replace(".log.json", ".log.txt")
                if os.path.exists(log_txt_path):
                    try:
                        with open(log_txt_path, "r", encoding="utf-8") as tf:
                            conteudo_txt = tf.read()
                        
                        st.markdown("##### 📥 Baixar Relatório Descritivo Completo")
                        st.download_button(
                            label="Download do Relatório (.txt)",
                            data=conteudo_txt,
                            file_name=os.path.basename(log_txt_path),
                            mime="text/plain",
                            use_container_width=True
                        )
                        
                        st.markdown("##### 🔍 Visualização do Histórico e Prosa")
                        st.text_area(
                            "Histórico de Geração e Conteúdo:",
                            value=conteudo_txt,
                            height=500,
                            disabled=True
                        )
                    except Exception as txt_read_err:
                        st.error(f"Erro ao ler arquivo de texto do log: {txt_read_err}")
                else:
                    st.info("O relatório completo em texto (.txt) não está disponível para esta aula (aulas geradas anteriormente não o possuem).")
            
            with tab_duracao:
                st.markdown("##### Duração proporcional por etapa do pipeline:")
                
                etapas = log_data.get("etapas", {})
                chaves_etapas = sorted(etapas.keys())
                
                for chave in chaves_etapas:
                    etapa = etapas[chave]
                    duracao = etapa.get("duracao_segundos", 0.0)
                    desc = etapa.get("descricao", "Etapa")
                    status_etapa = etapa.get("status", "sucesso")
                    
                    porcentagem = (duracao / max(tempo_total, 1.0)) * 100
                    porcentagem = min(porcentagem, 100.0)
                    
                    badge = "✓" if status_etapa == "sucesso" else ("ℹ" if status_etapa == "pulado" else "✗")
                    badge_color = "#10b981" if status_etapa == "sucesso" else ("#64748b" if status_etapa == "pulado" else "#ef4444")
                    
                    st.markdown(f"""
                        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; margin-bottom: 12px; font-family: 'sans-serif';">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <span style="font-weight: 600; color: #1E293B; font-size: 0.95rem;">
                                    <span style="background-color: {badge_color}; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.75rem; margin-right: 6px;">{badge}</span>
                                    {desc}
                                </span>
                                <span style="color: #475569; font-weight: 700; font-size: 0.9rem;">{duracao}s ({porcentagem:.1f}%)</span>
                            </div>
                            <div style="background-color: #E2E8F0; height: 8px; border-radius: 4px; overflow: hidden;">
                                <div style="background-color: #1E3A8A; height: 100%; width: {porcentagem}%;"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
            with tab_auditoria:
                st.markdown("##### Relatório científico de geração e refações por subtópico:")
                
                if not subtopicos_log:
                    st.info("Nenhum detalhe de subtópico disponível nesta execução.")
                else:
                    for i, sub in enumerate(subtopicos_log):
                        titulo_sub = sub.get("titulo", "Subtópico")
                        tentativas_sub = sub.get("tentativas", 1)
                        reprovacoes_sub = sub.get("reprovacoes", 0)
                        tempo_sub = sub.get("tempo_segundos", 0.0)
                        aprovado_sub = sub.get("aprovado", True)
                        
                        sub_erros_429 = sub.get("erros_api", {}).get("429", 0)
                        sub_erros_503 = sub.get("erros_api", {}).get("503", 0)
                        sub_erros_outros = sub.get("erros_api", {}).get("outros", 0)
                        sub_total_erros = sub_erros_429 + sub_erros_503 + sub_erros_outros
                        
                        status_icon = "🟢" if aprovado_sub else "🟡"
                        status_lbl = "Aprovado" if aprovado_sub else "Aprovado via Fallback"
                        
                        header_label = f"{status_icon} Subtópico {i+1}: {titulo_sub} — {tentativas_sub} tent. | {tempo_sub}s"
                        
                        with st.expander(header_label):
                            col_sub1, col_sub2, col_sub3 = st.columns(3)
                            with col_sub1:
                                st.write(f"**Status da Revisão:** {status_lbl}")
                                st.write(f"**Tempo de Processamento:** {tempo_sub}s")
                            with col_sub2:
                                st.write(f"**Tentativas do Escritor:** {tentativas_sub} de 3")
                                st.write(f"**Rejeições do Revisor:** {reprovacoes_sub}")
                            with col_sub3:
                                st.write(f"**Falhas de API enfrentadas:** {sub_total_erros}")
                                st.write(f"└ *429 (Cota): {sub_erros_429} | 503 (Indisp.): {sub_erros_503} | Outros: {sub_erros_outros}*")
                                
                            feedbacks_list = sub.get("feedbacks", [])
                            if feedbacks_list:
                                st.markdown("<div style='margin-top: 10px; font-weight: 600; color: #991B1B;'>❌ Histórico de Rejeições e Feedbacks de Correção:</div>", unsafe_allow_html=True)
                                for f_idx, f_text in enumerate(feedbacks_list):
                                    st.markdown(f"""
                                        <div style="background-color: #FEF2F2; border-left: 4px solid #EF4444; padding: 12px; border-radius: 4px; margin-bottom: 10px;">
                                            <div style="color: #991B1B; font-weight: 700; font-size: 0.85rem; margin-bottom: 4px;">TENTATIVA #{f_idx+1} REPROVADA PELO REVISOR CIENTÍFICO:</div>
                                            <div style="color: #7F1D1D; font-size: 0.9rem; line-height: 1.4; white-space: pre-wrap;">{f_text}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.markdown("<div style='margin-top: 10px; font-weight: 600; color: #065F46;'>✓ Aprovado de primeira tentativa sem correções solicitadas.</div>", unsafe_allow_html=True)
                                
        except Exception as log_err:
            st.warning(f"Não foi possível carregar o log da última execução: {log_err}")

if __name__ == "__main__":
    run_page()
