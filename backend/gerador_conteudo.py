import os
import sys
import json
import re
import time
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# Importando os schemas estruturados que criamos no arquivo anterior
from schemas import SubtopicoValidado, FonteRDetalhada
# Importamos a função do revisor local para auditoria
from revisor_notacao import auditar_subtopico_local

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
# SCHEMA AUXILIAR APENAS PARA O AGENTE 1 (ROTEIRISTA)
# ==============================================================================
class SubtopicoRoteiro(BaseModel):
    titulo: str = Field(description="Título curto e direto do sub-tópico conceitual.")
    conceitos_chave_rag: List[str] = Field(description="Lista de 3 a 5 termos estatísticos específicos e exatos para guiar a busca vetorial.")

class RoteiroCompletoAula(BaseModel):
    topico_principal: str
    esquema_paginas: List[SubtopicoRoteiro]

# ==============================================================================
# FUNÇÃO PRINCIPAL DE ORQUESTRAÇÃO DE CONTEÚDO
# ==============================================================================
def gerar_conteudo_aula(nome_professor: str, codigo_disciplina: str, tema_solicitado: str, ementa_texto: str = None, diretrizes_texto: str = None):
    t_inicio_roteirista = 0.0
    t_fim_roteirista = 0.0
    t_inicio_escrita = 0.0
    t_fim_escrita = 0.0
    log_subtopicos = []
    
    # Garante que temos a chave configurada
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("Chave de API 'GEMINI_API_KEY' não configurada. Configure a chave nos Secrets do Streamlit ou no ambiente.")

    try:
        client = genai.Client(vertexai=True, api_key=os.environ.get("GEMINI_API_KEY"))
    except Exception as e:
        print(f"[ERRO] Erro ao inicializar o cliente do Google GenAI: {e}")
        return None
    
    # 1. Recupera as Stores do professor e de livros globais para busca híbrida simultânea
    NOME_STORE = f"store-{nome_professor.lower().strip()}-{codigo_disciplina.lower().strip()}"
    NOME_STORE_FALLBACK = "plataforma-estatistica-db"
    store_names = []
    
    try:
        # Faz uma busca por ambas as stores
        stores_disponiveis = list(client.file_search_stores.list())
        
        # 1. Tenta achar a store específica do professor
        for store in stores_disponiveis:
            if store.display_name == NOME_STORE:
                store_names.append(store.name)
                print(f"[RAG] RAG especifico do professor ativado! Usando a Store: {store.display_name}")
                
        # 2. Tenta achar a store global plataforma-estatistica-db que contem os livros
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
    # FASE 1: AGENTE 1 - O ROTEIRISTA DA EMENTA
    # ==============================================================================
    t_inicio_roteirista = time.time()
    print("\n[Agente 1] Analisando a ementa e estruturando a trilha pedagógica da aula...")
    
    prompt_roteirista = f"""
Você é um Designer Instrucional Especialista em Ensino Superior de Matemática e Estatística, com foco em modelagem de currículos acadêmicos rigorosos.

### CONTEXTO E MISSÃO
Você receberá a [EMENTA] de uma disciplina universitária (anexada em PDF) e um [TÓPICO_SOLICITADO] (um recorte extraído dessa ementa). 
Sua missão é atuar como um arquiteto de conteúdo: você deve quebrar o [TÓPICO_SOLICITADO] em uma sequência lógica, 
linear e exaustiva de subtópicos teóricos, preenchendo rigorosamente a estrutura 'RoteiroCompletoAula'.

---

### DIRETRIZES DE ESCOPO E COBERTURA (MANDATÓRIO)
1. Delimitação Estrita da Ementa: Analise a [EMENTA] global para entender o nível de maturidade da disciplina. 
Cubra o [TÓPICO_SOLICITADO] com profundidade matemática adequada, mas NUNCA antecipe ou invada tópicos que estão listados em outras partes da ementa.
2. Granularidade Didática: Não economize subtópicos. Se o tema for complexo, 
fracione-o de forma robusta (geralmente entre 5 a 8 subtópicos, ou mais se necessário). 
Cada item da lista deve focar intensamente em um único conceito específico, garantindo uma progressão pedagógica fluida.
3. Formalismo Teórico Exclusivo: O foco deve ser a intuição conceitual, o formalismo matemático e as deduções analíticas. 
É TERMINANTEMENTE PROIBIDO incluir, sugerir ou criar componentes de programação, sintaxe de código ou laboratórios computacionais 
(como R, Python, SAS ou Julia).

---

### INSTRUÇÕES PARA PREENCHIMENTO DO SCHEMA DE RETORNO

1. 'topico_principal' (string): 
   - Nomeie o tema da aula de forma fluida, clara e contextualizada. 
   - Exemplo: "Fundamentos Teóricos e Aplicações da Regressão Linear Simples".

2. 'esquema_paginas' (lista de SubtopicoRoteiro):
   Cada item representa um subtópico que se tornará uma página teórica e deve conter:
   
   - 'titulo' (string): Título científico elegante, imersivo e de alta sonoridade acadêmica. Evite nomes curtos, genéricos ou informais.
     * Exemplo Ruim: "Introdução ao Teste t"
     * Exemplo Ideal: "A Engenharia Inferencial: Testes de Hipóteses e Distribuição t de Student"
     
   - 'conceitos_chave_rag' (lista de strings): Forneça de 3 a 5 palavras-chave cirúrgicas e termos técnicos exatos associados ao conceito (em português ou inglês). 
     * IMPORTANTE: Esses termos serão usados por um Agente Escritor para busca vetorial (RAG) em livros-texto. Use jargões estatísticos precisos, notações ou nomes de teoremas/estimadores (ex: ["estimadores de MQO", "resíduos ordinários", "mínimos quadrados ordinários", "Gauss-Markov theorem"]).

---

### ENTRADAS DO USUÁRIO
- [EMENTA]: {ementa_texto}
- [TÓPICO_SOLICITADO]: {tema_solicitado}
"""
    
    contents_roteirista = []
    if ementa_texto:
        contents_roteirista.append(f"Esta é a ementa oficial:\n{ementa_texto}")
    contents_roteirista.append(prompt_roteirista)

    try:
        # Usando gemini-3.1-flash-lite com capacidade máxima de raciocínio profundo
        resposta_roteiro = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents_roteirista,
            config=types.GenerateContentConfig(
                temperature=1.0,
                response_mime_type="application/json",
                response_schema=RoteiroCompletoAula
            )
        )
        
        # O Pydantic realiza o parsing nativo garantindo o objeto tipado
        roteiro_pedagogico = RoteiroCompletoAula.model_validate_json(resposta_roteiro.text)
        t_fim_roteirista = time.time()
        print(f"[OK] Roteiro gerado com sucesso! {len(roteiro_pedagogico.esquema_paginas)} subtópicos mapeados.")
    except Exception as e:
        print(f"[ERRO] Erro crítico ao gerar roteiro pedagógico: {e}")
        return None

    # ==============================================================================
    # FASE 2: AGENTE 2 + 2.5 - O ESCRITOR COM LOOP DE REVISÃO ATIVA
    # ==============================================================================
    t_inicio_escrita = time.time()
    print("\n[Agente 2 + 2.5] Iniciando laço de escrita com loop de revisão ativa...")
    aulas_conteudo_final = []
    MAX_TENTATIVAS_REVISAO = 3

    for idx, sub in enumerate(roteiro_pedagogico.esquema_paginas):
        t_inicio_sub = time.time()
        # Pausa preventiva de 5 segundos entre subtópicos para evitar estouro de limite de cota (Rate Limits / 429)
        if idx > 0:
            print("[INFO] Pausa de 5 segundos para respeitar limites de cota (Rate Limit)...")
            time.sleep(5)
            
        print(f"\n   -> Processando Subtópico [{idx+1}/{len(roteiro_pedagogico.esquema_paginas)}]: {sub.titulo}")
        
        # Criação da Query Contextualizada e Hierárquica para o RAG
        termos_busca = " ".join(sub.conceitos_chave_rag)
        query_rag = f"{tema_solicitado} - {sub.titulo} - {termos_busca}"
        
        # Variáveis de controle do loop de refação
        tentativa = 0
        bloco_aprovado = False
        comentario_feedback_llm = "Nenhum. Esta é a primeira tentativa de escrita do bloco."
        subtopico_atual_dados = None
        dados_escritor_dict = None  # CORREÇÃO: Evita vazamento de escopo e duplicação em caso de erro
        
        feedbacks = []
        erros_429 = 0
        erros_503 = 0
        erros_outros = 0

        while tentativa < MAX_TENTATIVAS_REVISAO and not bloco_aprovado:
            tentativa += 1
            print(f"      [Tentativa {tentativa}/{MAX_TENTATIVAS_REVISAO}] Enviando para o Escritor...")

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
Sua missão é atuar como o produtor científico principal do conteúdo teórico: você deve redigir a teoria acadêmica e formalismo matemático de forma extremamente completa e exaustiva para o [SUBTÓPICO_ALVO], preenchendo rigorosamente a estrutura 'SubtopicoValidado'.

---

### DIRETRIZES DE ESCOPO E EXAUSTIVIDADE (MANDATÓRIO)
1. Escrita Exaustiva de Livro: Você tem um limite de saída de 65.000 tokens. USE ESTE ESPAÇO PARA SER O MÁXIMO POSSÍVEL EXAUSTIVO. É OBRIGATÓRIO escrever o máximo de texto, explicações e detalhes analíticos possíveis. Proibido resumir, simplificar ou abreviar em nenhuma hipótese.
2. Regra de Ouro de Veracidade: {diretriz_veracidade}
3. Rigor Científico e LaTeX: Toda notação matemática formal, hipóteses, variabilidades, distribuições e deduções devem ser apresentadas com rigor absoluto em LaTeX estruturado ($$ para destaque centralizado ou $ para linha).

{REGRAS_MESTRE_ESCRITOR}

---

### INSTRUÇÕES PARA PREENCHIMENTO DO SCHEMA DE RETORNO

1. 'titulo_subtopico' (string):
   - Deve conter o título exato do subtópico: '{sub.titulo}'.

2. 'conteudo' (objeto ConteudoSubtopico):
   - 'tipo_bloco' (string): Deve ser preenchido estritamente como 'teorico'.
   - 'conceito_intuitivo' (string): Texto longo e aprofundado, de no mínimo 3 a 4 parágrafos densos. Explique a motivação histórica, o problema prático que impulsionou o conceito e analogias do mundo real. ATENÇÃO: Proibido inserir qualquer notação LaTeX matemática ($ ou $$) neste campo. Mantenha o foco puramente na prosa qualitativa.
   - 'conceito_formal' (string): Apresente o enunciado matemático definitivo do conceito ou teorema. Defina o espaço amostral, os parâmetros e as variáveis com rigor matemático absoluto utilizando LaTeX estruturado ($$ ou $).
   - 'propriedades_do_conceito' (lista de strings): Mapeie de forma exaustiva e rigorosa todas as leis, teoremas e propriedades matemáticas deduzidas diretamente desse conceito.
   - 'pre_requisitos_e_auxiliares' (lista de strings): Liste os pré-requisitos conceituais e ferramentas de cálculo necessários para compreender este subtópico.
   - 'condicoes_de_contorno' (lista de strings): Descreva todas as premissas matemáticas e suposições fundamentais para a validade do modelo (ex: homocedasticidade, independência dos erros, normalidade). Se não houver, preencha 'N/A'.
   - 'simulador_interativo_recomendado' (string): Proponha uma simulação interativa baseada em Plotly que auxilie a visualizar este conceito (ex: reta OLS com sliders de tamanho amostral $n$ e ruído $\sigma$). Detalhe as variáveis e os limites dos sliders para o frontend do Streamlit.
   - 'deducao_formal_passo_a_passo' (lista de strings): Forneça a demonstração matemática completa. Cada string deve representar um único passo ou equação matemática em LaTeX ($$), organizados de forma logicamente contígua e sem saltar passagens algébricas cruciais. Lembre-se que QUALQUER BLOCO DE MULTIPLAS LINHAS DEVE ESTAR ENVOLVIDO POR $$ DUPLO.
   - 'interpretacao_geometrica_grafica' (string): Explique de forma clara como visualizar esse conceito graficamente ou espacialmente (ex: inclinação da reta, áreas de probabilidade sob curvas, vetores de erro).
   - 'exemplo_canonico' (objeto EstruturaExemplo):
     * 'enunciado' (string): Enunciado realista e complexo sobre o mundo real (controle de qualidade, ensaios clínicos, IoT), evitando problemas puramente abstratos.
     * 'passo_a_passo_solucao' (lista de strings): As passagens e etapas de cálculo detalhadas em LaTeX ($$), mostrando numericamente a substituição de valores nas fórmulas.
     * 'resultado_final' (string): O resultado aritmético final seguido da respectiva interpretação prática/comercial conclusiva.

3. 'fontes_rag' (lista de FonteRDetalhada):
   Cada item representa uma fonte bibliográfica e deve conter:
   - 'livro_autor' (string): Sobrenome dos autores e título clássico do livro.
   - 'capitulo' (string): Capítulo e seção consultada.
   - 'paginas_utilizadas' (string): O número exato da página ou intervalo de páginas consultadas (ex: "p. 142" ou "pp. 210-214"). ATENÇÃO: A ausência de páginas exatas é motivo de reprovação pelo Revisor.

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
                temperature=1.0,
                response_mime_type="application/json",
                response_schema=SubtopicoValidado
            )

            try:
                resposta_escritor = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[query_rag, prompt_escritor],
                    config=config_escritor
                )
                
                # Parsing temporário do que o escritor acabou de gerar
                dados_escritor_dict = json.loads(resposta_escritor.text)
                
                # ACIONA O AGENTE 2.5 (REVISOR DE CONTEÚDO) IMEDIATAMENTE
                print("      [REVISOR] Analisando rigor matemático e profundidade...")
                laudo_revisao = auditar_subtopico_local(dados_escritor_dict, diretrizes_texto)
                
                if laudo_revisao.aprovado:
                    print("      [OK] Bloco APROVADO pelo revisor científico!")
                    bloco_aprovado = True
                    
                    # Usa o conteúdo revisado se fornecido, senão cria do dict bruto
                    if laudo_revisao.conteudo_corrigido:
                        subtopico_atual_dados = laudo_revisao.conteudo_corrigido
                    else:
                        subtopico_atual_dados = SubtopicoValidado(**dados_escritor_dict)
                    
                    # Captura os metadados do grounding normais do RAG
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
                        # Remove duplicatas
                        vistas = set()
                        fontes_unicas = []
                        for f in fontes_capturadas:
                            chave = (f.livro_autor, f.paginas_utilizadas)
                            if chave not in vistas:
                                vistas.add(chave)
                                fontes_unicas.append(f)
                        subtopico_atual_dados.fontes_rag = fontes_unicas
                else:
                    # Se reprovado, o laudo vira o prompt da próxima iteração do laço while!
                    print(f"      [REPROVADO] Bloco REPROVADO! Motivo: {laudo_revisao.comentario_correcao}")
                    comentario_feedback_llm = f"ALERTA DE ERRO NA TENTATIVA ANTERIOR: Seu bloco foi reprovado pelo revisor com o seguinte comentário: {laudo_revisao.comentario_correcao}. Por favor, refaça o trabalho corrigindo este problema."
                    feedbacks.append(laudo_revisao.comentario_correcao)
                    
            except Exception as e:
                # CORREÇÃO INTELIGENTE (Recomendação do Usuário):
                # Distingue erro 429 (cota esgotada: exige espera longa de 15s) de erro 503 (servidor ocupado: retentativa rápida de 2s)
                erro_str = str(e)
                if "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
                    erros_429 += 1
                    print(f"      [AVISO] Limite de cota excedido (429). Aguardando 15 segundos para renovar a cota... Erro: {e}")
                    time.sleep(15)
                elif "503" in erro_str or "UNAVAILABLE" in erro_str:
                    erros_503 += 1
                    print(f"      [AVISO] Servidor da Google ocupado (503). Retentando rapidamente em 2 segundos...")
                    time.sleep(2)
                else:
                    erros_outros += 1
                    print(f"      [ERRO] Falha de comunicação genérica. Retentando em 5 segundos... Erro: {e}")
                    time.sleep(5)
                
        # Se estourar os retries e não aprovar, salva o último gerado para não travar o pipeline
        if not subtopico_atual_dados and dados_escritor_dict:
            subtopico_atual_dados = SubtopicoValidado(**dados_escritor_dict)
            subtopico_atual_dados.fontes_rag = [
                FonteRDetalhada(
                    livro_autor="Fonte nao mapeada",
                    capitulo="Falhas na revisao",
                    paginas_utilizadas="p. S/N"
                )
            ]
            
        if subtopico_atual_dados:
            aulas_conteudo_final.append(subtopico_atual_dados)
            
        t_fim_sub = time.time()
        log_subtopicos.append({
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
        })

    t_fim_escrita = time.time()

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
