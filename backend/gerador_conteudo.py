import os
import sys
import json
import re
import time
import concurrent.futures
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# Importando os schemas estruturados que criamos no arquivo anterior
from schemas import SubtopicoValidado, FonteRDetalhada, SubtopicoRoteiro, RoteiroCompletoAula
# Importamos a função do revisor local para auditoria
from revisor_notacao import auditar_subtopico_local
import latex_sanitizer

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
        
    # Tenta ler do secrets.toml da pasta local
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

# Inicializa o carregamento da chave de API
carregar_chave_api()

# ==============================================================================
# FUNÇÃO PRINCIPAL DE ORQUESTRAÇÃO DE CONTEÚDO
# ==============================================================================
def gerar_conteudo_aula(nome_professor: str, codigo_disciplina: str, tema_solicitado: str, ementa_texto: str = None, diretrizes_texto: str = None, logger=None, modelo_llm: str = "2.5"):
    t_inicio_roteirista = 0.0
    t_fim_roteirista = 0.0
    t_inicio_escrita = 0.0
    t_fim_escrita = 0.0
    log_subtopicos = []
    if logger:
        logger.update_agent("gerador_bruto", "rodando")
        logger.log("Gerador de Conteúdo: Iniciando elaboração do macro roteiro...", "info")
    
    try:
        os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "vertex-key.json")
        client = genai.Client(vertexai=True, location="us-central1")
        modelo_roteirista = "gemini-2.5-pro"
        modelo_escritor = "gemini-2.5-pro" if str(modelo_llm) == "pro" else "gemini-2.5-flash"

    except Exception as e:
        if logger:
            logger.update_agent("gerador_bruto", "erro")
            logger.log(f"Gerador de Conteúdo: Erro crítico - {str(e)}", "error")
        raise e

    # 1. Recupera as Stores do professor e de livros globais para busca híbrida simultânea
    NOME_STORE = f"store-{nome_professor.lower().strip()}-{codigo_disciplina.lower().strip()}"
    NOME_STORE_FALLBACK = "plataforma-estatistica-db"
    store_names = []
    
    try:
        stores_disponiveis = list(client.file_search_stores.list())
        for store in stores_disponiveis:
            if store.display_name == NOME_STORE:
                store_names.append(store.name)
                print(f"[RAG] RAG especifico do professor ativado! Usando a Store: {store.display_name}")
                
        for store in stores_disponiveis:
            if store.display_name == NOME_STORE_FALLBACK:
                store_names.append(store.name)
                print(f"[RAG] RAG global de livros ativado! Usando a Store: {store.display_name}")
    except Exception as e:
        print(f"[ALERTA] Alerta ao buscar stores no Google Cloud: {e}")
            
    if not store_names:
        print(f"[AVISO] Nenhuma base de dados RAG ('{NOME_STORE}' ou '{NOME_STORE_FALLBACK}') foi encontrada. Continuando em modo sem RAG...")

    # 2. Carrega a ementa (texto puro via API FastAPI)
    if not ementa_texto:
        raise ValueError("O texto da ementa é obrigatório.")
    
    print(f"[EMENTA] Utilizando ementa de {len(ementa_texto)} caracteres para alinhamento de escopo...")

    # 3. Valida as diretrizes de notação e design enviadas pelo Streamlit
    if not diretrizes_texto or not diretrizes_texto.strip():
        raise ValueError("As diretrizes de notação e estilo são obrigatórias e devem ser fornecidas pelo Streamlit.")

    # ==============================================================================
    # FASE 1: AGENTE 1 - O ROTEIRISTA DA EMENTA (Gemini 2.5 Pro)
    # ==============================================================================
    t_inicio_roteirista = time.time()
    print("\n[Agente 1 - Roteirista (gemini-2.5-pro)] Analisando a ementa e estruturando a trilha pedagógica da aula...")
    
    prompt_roteirista = f"""
Você é um Designer Instrucional Especialista em Ensino Superior Universitário de Matemática e Estatística, com foco em modelagem de currículos acadêmicos de graduação.

### CONTEXTO E MISSÃO
Você receberá a [EMENTA] oficial completa de uma disciplina universitária e um [TÓPICO_SOLICITADO] (o tema de uma aula específica).
Sua missão é atuar como arquiteto pedagógico: você deve analisar o contexto e a maturidade da disciplina a partir da ementa e estruturar uma sequência equilibrada e coesa de subtópicos conceituais para a aula, preenchendo a estrutura 'RoteiroCompletoAula'.

---

### DIRETRIZES DE CALIBRAÇÃO PEDAGÓGICA (MANDATÓRIO)
1. Calibração pelo Nível da Disciplina no Currículo Universitário:
   - Analise a [EMENTA] global para inferir o momento da disciplina no curso (ex: Disciplina Introdutória de primeiros semestres vs Disciplina de Formação Profissionalizante ou Tópicos Avançados de Bacharelado).
   - Ajuste a profundidade para ser didática e alinhada ao nível da disciplina. Não force teoremas puramente abstratos ou assintóticos em disciplinas introdutórias, e não simplifique em excesso em matérias de formação avançada.
2. Delimitação Estrita da Ementa: Cubra o [TÓPICO_SOLICITADO] com rigor e clareza, mas NUNCA antecipe ou invada tópicos listados em outras aulas da ementa.
3. Granularidade Equilibrada: Estruture uma sequência pedagógica fluida e natural (geralmente entre 4 a 6 subtópicos balanceados, sem divisões artificiais ou excesso desnecessário). Cada subtópico deve ter foco claro.
4. Formalismo Teórico e Didática: O foco deve ser intuição conceitual, rigor matemático adequado ao nível da disciplina e aplicações ricas. É TERMINANTEMENTE PROIBIDO incluir sintaxe de código de programação (R, Python, SAS).

---

### INSTRUÇÕES PARA PREENCHIMENTO DO SCHEMA DE RETORNO

1. 'nivel_estimado_disciplina' (string):
   - Descreva o contexto universitário inferido da ementa (ex: "Graduação - Ciclo Introdutório (Primeiros Semestres)", "Graduação - Ciclo Profissionalizante", "Graduação - Formação Avançada / Bacharelado").

2. 'topico_principal' (string): 
   - Nomeie o tema da aula de forma fluida, elegante e contextualizada. 
   - Exemplo: "Fundamentos Teóricos e Aplicações da Regressão Linear Simples".

3. 'esquema_paginas' (lista de SubtopicoRoteiro):
   Cada item representa um subtópico da aula e deve conter:
   
   - 'titulo' (string): Título científico claro, convidativo e de boa sonoridade acadêmica.
     * Exemplo: "Interpretação Geométrica dos Mínimos Quadrados Ordinários e Decomposição da Variância"
     
   - 'conceitos_chave_rag' (lista de strings): 3 a 5 termos técnicos precisos associados ao conceito para busca vetorial em livros-texto (ex: ["estimadores de MQO", "resíduos ordinários", "mínimos quadrados ordinários", "Gauss-Markov"]).

---

### ENTRADAS DO USUÁRIO
- [EMENTA]: {ementa_texto}
- [TÓPICO_SOLICITADO]: {tema_solicitado}
- [DIRETRIZES_DO_PROFESSOR]: {diretrizes_texto}
"""
    
    contents_roteirista = []
    if ementa_texto:
        contents_roteirista.append(f"Esta é a ementa oficial:\n{ementa_texto}")
    contents_roteirista.append(prompt_roteirista)

    try:
        resposta_roteiro = client.models.generate_content(
            model=modelo_roteirista,
            contents=contents_roteirista,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RoteiroCompletoAula
            )
        )
        
        # O Pydantic realiza o parsing nativo garantindo o objeto tipado
        roteiro_pedagogico = RoteiroCompletoAula.model_validate_json(resposta_roteiro.text)
        if logger:
            logger.init_subtopics(len(roteiro_pedagogico.esquema_paginas))
            logger.update_agent("gerador_bruto", "concluido", resposta=resposta_roteiro.text)
            logger.log(f"Roteirista: Roteiro macro concluído com {len(roteiro_pedagogico.esquema_paginas)} subtópicos.", "success")
        t_fim_roteirista = time.time()
        print(f"[OK] Roteiro gerado com sucesso! {len(roteiro_pedagogico.esquema_paginas)} subtópicos mapeados.")
    except Exception as e:
        if logger:
            logger.update_agent("gerador_bruto", "erro")
            logger.log(f"Gerador de Conteúdo: Erro crítico - {str(e)}", "error")
        raise e

    # ==============================================================================
    # FASE 2: AGENTE 2 + 2.5 - O ESCRITOR COM LOOP DE REVISÃO ATIVA
    # ==============================================================================
    t_inicio_escrita = time.time()
    print("\n[Agente 2 + 2.5] Iniciando laço de escrita com loop de revisão ativa EM PARALELO...")
    
    # Função isolada para processar um único subtópico
    def processar_subtopico(idx, sub):
        t_inicio_sub = time.time()
        print(f"\n   -> Iniciando Processamento Subtópico [{idx+1}/{len(roteiro_pedagogico.esquema_paginas)}]: {sub.titulo}")
        
        termos_busca = " ".join(sub.conceitos_chave_rag)
        query_rag = f"{tema_solicitado} - {sub.titulo} - {termos_busca}"
        
        tentativa = 0
        bloco_aprovado = False
        comentario_feedback_llm = "Nenhum. Esta é a primeira tentativa de escrita do bloco."
        subtopico_atual_dados = None
        dados_escritor_dict = None
        
        feedbacks = []
        erros_429 = 0
        erros_503 = 0
        erros_outros = 0
        MAX_TENTATIVAS_REVISAO = 3

        while tentativa < MAX_TENTATIVAS_REVISAO and not bloco_aprovado:
            tentativa += 1
            print(f"      [Topico {idx+1} | Tentativa {tentativa}/{MAX_TENTATIVAS_REVISAO}] Enviando para o Escritor...")

            if store_names:
                diretriz_veracidade = "Baseie-se estritamente e exclusivamente nas informações contidas nos documentos do RAG e nos materiais do professor fornecidos pelo File Search. É terminantemente proibido inventar teoremas, deduzir propriedades sem fundamentação teórica nas fontes recuperadas, ou citar livros que não constem de fato nas referências obtidas."
                contexto_rag_descricao = "os documentos recuperados da base RAG (File Search)"
                tools_config = [
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=store_names,
                            metadata_filter=f'discipline="{codigo_disciplina.upper().strip()}"',
                            top_k=45
                        )
                    )
                ]
            else:
                diretriz_veracidade = "Como não há base RAG de apoio disponível, baseie-se no conhecimento estatístico consolidado da literatura acadêmica padrão (ex: Bussab & Morettin, Morettin & Singer, etc.). É terminantemente proibido inventar teoremas ou deduzir propriedades errôneas. Cite obras e páginas reais e verossímeis nas referências bibliográficas do retorno."
                contexto_rag_descricao = "o conhecimento estatístico consolidado da literatura acadêmica padrão"
                tools_config = None

            from prompts import REGRAS_MESTRE_ESCRITOR
            prompt_escritor = f"""
Você é um Professor Titular de Estatística e co-autor de livros didáticos clássicos e rigorosos de nível universitário.

### CONTEXTO E MISSÃO
Você receberá as Diretrizes de Notação e Design do professor, {contexto_rag_descricao} e um [SUBTÓPICO_ALVO] que integra o [TÓPICO_DA_AULA].
Sua missão é atuar como o produtor científico principal do conteúdo teórico: você deve redigir a teoria acadêmica e formalismo matemático de forma extremamente completa para o [SUBTÓPICO_ALVO], preenchendo rigorosamente a estrutura 'SubtopicoValidado'.

---

### DIRETRIZES DE ESCOPO E EXAUSTIVIDADE (MANDATÓRIO)
1. Escrita Didática de Livro: Você tem um limite de saída alto. USE ESTE ESPAÇO PARA SER O MÁXIMO POSSÍVEL DIDÁTICO E CLARO. É OBRIGATÓRIO escrever o texto, explicações e detalhes analíticos para que o aluno compreenda plenamente o assunto. Proibido simplificar demais a ponto de perder o rigor matemático.
2. Regra de Ouro de Veracidade: {diretriz_veracidade}
3. Rigor Científico e LaTeX: Toda notação matemática formal, hipóteses, variabilidades, distribuições e deduções devem ser apresentadas com rigor absoluto em LaTeX estruturado ($$ para destaque centralizado ou $ para linha).

{REGRAS_MESTRE_ESCRITOR}

---

### INSTRUÇÕES PARA PREENCHIMENTO DO SCHEMA DE RETORNO

1. 'titulo_subtopico' (string):
   - Deve conter o título exato do subtópico: '{sub.titulo}'.

2. 'conteudo' (objeto ConteudoSubtopico):
   - 'tipo_bloco' (string): Deve ser preenchido estritamente como 'teorico'.
   - 'conceito_intuitivo' (string): Texto longo e aprofundado, de no mínimo 3 a 4 parágrafos densos (separe-os obrigatoriamente com DUAS quebras de linha \n\n). Explique a motivação histórica, o problema prático que impulsionou o conceito e analogias do mundo real. Adote o tom, linguagem e termos do professor fornecidos no override. ATENÇÃO: Proibido inserir qualquer notação LaTeX matemática ($ ou $$) neste campo. Mantenha o foco puramente na prosa qualitativa.
   - 'conceito_formal' (string ou null): Apresente o enunciado matemático formal em LaTeX ($$ ou $). Se o subtópico for histórico/qualitativo/conceitual (sem fórmulas próprias), RETORNE ESTRITAMENTE null.
   - 'propriedades_do_conceito' (lista de strings ou null): Mapeie leis, teoremas e propriedades deduzidas diretamente desse conceito (ou null se for subtópico qualitativo).
   - 'pre_requisitos_e_auxiliares' (lista de strings ou null): Ferramentas matemáticas necessárias (ou null se não houver).
   - 'condicoes_de_contorno' (lista de strings ou null): Premissas e suposições fundamentais para a validade do modelo (ou null se não aplicável).
   - 'simuladores_interativos_recomendados' (lista de strings ou null): Lista contendo uma ou mais propostas de simulações/visualizações interativas com Plotly e controles dinâmicos/sliders (ex: ['Reta OLS com sliders de tamanho amostral n e ruído sigma', 'Gráfico de dispersão de resíduos']). PRIORIZE SEMPRE A INTERATIVIDADE. Se não for necessário gráfico neste subtópico, retorne null.
   - 'deducao_formal_passo_a_passo' (lista de strings ou null): Demonstração matemática completa em LaTeX ($$), cada string representando um passo contíguo. Se for subtópico conceitual/histórico/qualitativo sem demonstração algébrica, RETORNE ESTRITAMENTE null.
   - 'interpretacao_geometrica_grafica' (string ou null): Explique como visualizar o conceito espacialmente ou graficamente (ou null se não aplicável).
   - 'exemplo_canonico' (objeto EstruturaExemplo ou null):
     * 'enunciado' (string): Problema contextualizado (podendo ser clássico como moedas/dados para intuição ou aplicado à indústria).
     * 'passo_a_passo_solucao' (lista de strings): Cálculos detalhados em LaTeX ($$).
     * 'resultado_final' (string): Resultado aritmético seguido de interpretação prática.

3. 'fontes_rag' (lista de FonteRDetalhada):
   Cada item representa uma fonte bibliográfica e deve conter:
   - 'livro_autor' (string): Sobrenome dos autores e título clássico do livro.
   - 'capitulo' (string): Capítulo e seção consultada.
   - 'paginas_utilizadas' (string): O número exato da página ou intervalo de páginas consultadas (ex: "p. 142" ou "pp. 210-214"). Se não houver RAG, preencher com referências padrão consolidadas.

---

### ENTRADAS DO USUÁRIO
- [TÓPICO_DA_AULA]: {tema_solicitado}
- [SUBTÓPICO_ALVO]: {sub.titulo}
- [DIRETRIZES_DE_ESTILO]:
{diretrizes_texto}
- [FEEDBACKS_REVISAO]: {comentario_feedback_llm}
"""

            config_escritor = types.GenerateContentConfig(
                tools=tools_config,
                response_mime_type="application/json",
                response_schema=SubtopicoValidado
            )

            try:
                if logger:
                    logger.update_agent(f"gerador_bruto_{idx+1}", "rodando", prompt=prompt_escritor)
                    logger.log(f"Gerador de Conteúdo: Redigindo tópico {idx+1} (Tentativa {tentativa})...", "info")
                resposta_escritor = client.models.generate_content(
                    model=modelo_escritor,
                    contents=[query_rag, prompt_escritor],
                    config=config_escritor
                )
                if logger:
                    logger.update_agent(f"gerador_bruto_{idx+1}", "rodando", resposta=resposta_escritor.text)
                if logger:
                    logger.log(f"gerador_{idx+1}_{tentativa} terminou", "info")
                
                
                
                dados_escritor_dict = json.loads(resposta_escritor.text)
                dados_escritor_dict = latex_sanitizer.sanitize_json_recursively(dados_escritor_dict)
                
                print(f"      [REVISOR] Analisando tópico {idx+1}...")
                laudo_revisao = auditar_subtopico_local(dados_escritor_dict, diretrizes_texto, logger=logger, sub_idx=idx+1, sub_tentativa=tentativa)
                
                if laudo_revisao.aprovado:
                    print(f"      [OK] Bloco {idx+1} APROVADO pelo revisor!")
                    if logger:
                        logger.log(f"Revisor (Crítico): Tópico {idx+1} aprovado!", "success")
                    bloco_aprovado = True
                    
                    if laudo_revisao.conteudo_corrigido:
                        subtopico_atual_dados = laudo_revisao.conteudo_corrigido
                    else:
                        subtopico_atual_dados = SubtopicoValidado(**dados_escritor_dict)
                    
                    fontes_capturadas = []
                    if hasattr(resposta_escritor, "grounding_metadata") and resposta_escritor.grounding_metadata:
                        chunks = resposta_escritor.grounding_metadata.grounding_chunks
                        if chunks:
                            for chunk in chunks:
                                if hasattr(chunk, "retrieved_context") and chunk.retrieved_context:
                                    ctx = chunk.retrieved_context
                                    title = getattr(ctx, "title", "Livro Ingerido")
                                    page = str(getattr(ctx, "page_number", "S/N"))
                                    fontes_capturadas.append(
                                        FonteRDetalhada(
                                            livro_autor=title,
                                            capitulo="N/A (Grounding)",
                                            paginas_utilizadas=f"p. {page}" if page != "S/N" else "p. não especificada"
                                        )
                                    )
                    if fontes_capturadas:
                        vistas = set()
                        fontes_unicas = []
                        for f in fontes_capturadas:
                            chave = (f.livro_autor, f.paginas_utilizadas)
                            if chave not in vistas:
                                vistas.add(chave)
                                fontes_unicas.append(f)
                        subtopico_atual_dados.fontes_rag = fontes_unicas
                else:
                    print(f"      [REPROVADO] Bloco {idx+1} REPROVADO! Motivo: {laudo_revisao.comentario_correcao}")
                    if logger:
                        logger.log(f"Revisor (Crítico): Tópico {idx+1} reprovado. Devolvendo ao gerador...", "warning")
                    comentario_feedback_llm = f"ALERTA DE ERRO NA TENTATIVA ANTERIOR: Seu bloco foi reprovado pelo revisor com o seguinte comentário: {laudo_revisao.comentario_correcao}. Por favor, refaça o trabalho corrigindo este problema."
                    feedbacks.append(laudo_revisao.comentario_correcao)
                    
            except Exception as e:
                erro_str = str(e)
                if "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
                    erros_429 += 1
                    print(f"      [AVISO 429] Limite de cota excedido no tópico {idx+1}. Propagando erro para gerenciador de pool...")
                    raise Exception("429_TOO_MANY_REQUESTS")
                elif "503" in erro_str or "UNAVAILABLE" in erro_str:
                    erros_503 += 1
                    print(f"      [AVISO 503] Servidor ocupado no tópico {idx+1}. Retentando rapidamente em 2s...")
                    time.sleep(2)
                else:
                    erros_outros += 1
                    print(f"      [ERRO] Falha genérica no tópico {idx+1}. Retentando em 5s... Erro: {e}")
                    time.sleep(5)
                
        if not subtopico_atual_dados and dados_escritor_dict:
            subtopico_atual_dados = SubtopicoValidado(**dados_escritor_dict)
            subtopico_atual_dados.fontes_rag = [
                FonteRDetalhada(
                    livro_autor="Fonte nao mapeada",
                    capitulo="Falhas na revisao",
                    paginas_utilizadas="p. S/N"
                )
            ]
            
        t_fim_sub = time.time()
        log_data = {
            "titulo": sub.titulo,
            "tentativas": tentativa,
            "reprovacoes": len(feedbacks),
            "feedbacks": feedbacks,
            "erros_api": {
                "429": erros_429,
                "503": erros_503,
                "outros": erros_outros
            },
            "tempo_segundos": round(t_fim_sub - t_inicio_sub, 2),
            "aprovado": bloco_aprovado
        }
        
        if logger:
            logger.update_agent(f"gerador_bruto_{idx+1}", "concluido")
            logger.update_agent(f"revisor_{idx+1}", "concluido")
        return (idx, subtopico_atual_dados, log_data)


    # Controle de Pool de Execução
    aulas_conteudo_final = [None] * len(roteiro_pedagogico.esquema_paginas)
    log_subtopicos = [None] * len(roteiro_pedagogico.esquema_paginas)
    
    tarefas_pendentes = list(enumerate(roteiro_pedagogico.esquema_paginas))
    max_workers_atuais = 5
    cooldowns_executados = 0
    MAX_COOLDOWNS = 3
    
    while tarefas_pendentes:
        print(f"\n[POOL] Iniciando pool com {max_workers_atuais} workers para {len(tarefas_pendentes)} tópicos pendentes.")
        ocorreu_429 = False
        tarefas_falhadas_429 = []
        
        # O ThreadPoolExecutor será cancelado nativamente no Python 3.9+ usando cancel_futures=True se houver erro
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers_atuais)
        
        # Submete as tarefas
        futuros = {}
        for item in tarefas_pendentes:
            fut = executor.submit(processar_subtopico, item[0], item[1])
            futuros[fut] = item
            
        tarefas_pendentes = [] # Limpa a lista para o caso de precisarmos reabastecer com as falhas
        
        try:
            for futuro in concurrent.futures.as_completed(futuros):
                item = futuros[futuro]
                idx_orig, sub_orig = item
                try:
                    res_idx, res_dados, res_log = futuro.result()
                    aulas_conteudo_final[res_idx] = res_dados
                    log_subtopicos[res_idx] = res_log
                    print(f"   -> [CONCLUÍDO] Tópico {res_idx+1} gerado com sucesso!")
                except Exception as e:
                    if "429_TOO_MANY_REQUESTS" in str(e):
                        if not ocorreu_429:
                            print("\n[ERRO CRÍTICO 429] Detectado limite de requisições! Iniciando protocolo de cancelamento e cooldown...")
                            ocorreu_429 = True
                        tarefas_falhadas_429.append(item)
                    else:
                        print(f"\n[ERRO FATAL] O tópico {idx_orig+1} falhou e não pode ser recuperado: {e}")
                        aulas_conteudo_final[idx_orig] = "FALHA"
                        
        finally:
            # Encerra o pool atual. Em Python 3.9+, cancel_futures=True cancela as tarefas que ainda estão na fila de espera
            # Para manter compatibilidade com versões antigas, cancelamos manualmente as pendentes que não completaram.
            executor.shutdown(wait=False, cancel_futures=True) if hasattr(executor, 'shutdown') and 'cancel_futures' in executor.shutdown.__code__.co_varnames else executor.shutdown(wait=False)
            
            # As tarefas canceladas não retornarão result(), então elas não foram colocadas em aulas_conteudo_final
            # Precisamos re-adicionar todas as tarefas que ainda não estão prontas na lista pendente
            tarefas_pendentes = []
            for i, sub in enumerate(roteiro_pedagogico.esquema_paginas):
                if aulas_conteudo_final[i] is None:
                    tarefas_pendentes.append((i, sub))
        
        if ocorreu_429 and tarefas_pendentes:
            cooldowns_executados += 1
            if cooldowns_executados > MAX_COOLDOWNS:
                raise Exception(f"Abortando após {MAX_COOLDOWNS} tentativas falhas de cooldown para erros 429. Verifique sua cota da API.")
            print(f"[COOLDOWN {cooldowns_executados}/{MAX_COOLDOWNS}] Aguardando 60 segundos antes de tentar novamente...")
            time.sleep(60)
            max_workers_atuais = 3
            print("[COOLDOWN] Reduzindo paralelismo para 3 workers para evitar novos erros 429.")
            
    # Remove eventuais Nones caso algum tópico tenha falhado irreversivelmente
    aulas_conteudo_final = [x for x in aulas_conteudo_final if x is not None and x != "FALHA"]
    
    t_fim_escrita = time.time()
    if logger:
        for i in range(1, len(roteiro_pedagogico.esquema_paginas) + 1):
            logger.update_agent(f"gerador_bruto_{i}", "concluido")
            logger.update_agent(f"revisor_{i}", "concluido")
        logger.update_agent("revisor", "concluido")
        logger.log("Conteúdo bruto e revisão finalizados.", "success")

    return {
        "tema": tema_solicitado,
        "conteudo_paginas": [p.model_dump() for p in aulas_conteudo_final],
        "log_gerador": {
            "tempo_roteirista_segundos": round(t_fim_roteirista - t_inicio_roteirista, 2),
            "tempo_escrita_revisao_segundos": round(t_fim_escrita - t_inicio_escrita, 2),
            "subtopicos": log_subtopicos
        }
    }

if __name__ == "__main__":
    print("[AVISO] A geração de conteúdo deve ser executada a partir da interface do Streamlit.")
    print("Por favor, execute o comando: streamlit run app.py")
