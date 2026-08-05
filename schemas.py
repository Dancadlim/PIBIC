from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

# ==========================================
# SUB-OBJETOS AUXILIARES
# ==========================================

class EstruturaExemplo(BaseModel):
    enunciado: str = Field(description="O problema proposto com contextualização acadêmica detalhada.")
    passo_a_passo_solucao: List[str] = Field(description="Lista contendo os passos lógicos e cálculos intermediários em LaTeX.")
    resultado_final: str = Field(description="A conclusão direta e interpretação prática do problema.")

class ExemploResolvidoRico(BaseModel):
    contexto_e_enunciado: str = Field(
        description="Enunciado longo e contextualizado em um cenário real (mínimo 2 parágrafos). Deve descrever o problema prático, a origem dos dados e os objetivos da análise."
    )
    dados_brutos_sumarizados: str = Field(
        description="Exibição clara e organizada dos dados descritivos em LaTeX (ex: sum_x, sum_y, n, barras) necessários para o cálculo."
    )
    desenvolvimento_aritmético_passo_a_passo: List[str] = Field(
        description="Lista exaustiva mostrando a substituição numérica em cada fórmula. Proibido pular etapas de cálculo ou jogar resultados diretos."
    )
    conclusao_e_laudo_comercial: str = Field(
        description="Interpretação prática e qualitativa do resultado final para o tomador de decisão (mínimo 1 parágrafo denso)."
    )

class FonteRDetalhada(BaseModel):
    livro_autor: str = Field(description="Nome do livro e sobrenome do autor (ex: Bussab & Morettin, Wooldridge).")
    capitulo: str = Field(description="Capítulo específico consultado no documento RAG.")
    paginas_utilizadas: str = Field(description="Número exato da página ou intervalo de páginas de onde o conteúdo foi extraído (ex: p. 234, pp. 112-115). Obrigatório.")

# ==========================================
# SCHEMAS DO AGENTE 2 (ESCRITOR TEÓRICO)
# ==========================================

class ConteudoSubtopico(BaseModel):
    """
    Modelo unificado e determinístico de conteúdo do subtópico.
    Evita o uso de Union (anyOf/oneOf) que gera erros de compatibilidade na API do Gemini (Structured Outputs).
    """
    tipo_bloco: Literal["teorico"] = Field(
        default="teorico",
        description="O tipo do bloco: sempre 'teorico'."
    )
    
    # ----------------------------------------------------
    # CAMPOS COMUNS
    # ----------------------------------------------------
    conceito_intuitivo: str = Field(description="Explicação profunda do conceito em linguagem natural e fluida, sem formalismo matemático ainda.")
    conceito_formal: str = Field(description="Definição matemática precisa ou enunciado acadêmico formal do conceito em LaTeX.")
    propriedades_do_conceito: List[str] = Field(description="Lista de regras, teoremas ou leis que este conceito sempre segue.")
    pre_requisitos_e_auxiliares: List[str] = Field(description="Mapeamento de ferramentas matemáticas ou aulas passadas necessárias aqui.")
    condicoes_de_contorno: List[str] = Field(description="Suposições obrigatórias para que a teoria seja válida. Se não houver, responda 'N/A'.")
    
    # --- O NOVO CAMPO ACIONADOR DE INTERATIVIDADE ---
    simulador_interativo_recomendado: Optional[str] = Field(
        default=None, 
        description="Se o subtópico se beneficiar de um gráfico parametrizado por sliders, descreva detalhadamente qual simulação deve ser renderizada aqui (Ex: 'Plotar curva gaussiana bicaudal onde o slider altera alfa'). Se não precisar, deixe None."
    )
    
    # ----------------------------------------------------
    # CAMPOS ESPECÍFICOS DE CONTEÚDO TEÓRICO
    # ----------------------------------------------------
    deducao_formal_passo_a_passo: Optional[List[str]] = Field(
        default=None,
        description="O passo a passo detalhado da derivação matemática das fórmulas em LaTeX."
    )
    interpretacao_geometrica_grafica: Optional[str] = Field(
        default=None,
        description="A descrição de como visualizar esse teorema espacialmente ou em gráficos."
    )
    
    # ----------------------------------------------------
    # EXEMPLO CANÔNICO
    # ----------------------------------------------------
    exemplo_canonico: Optional[EstruturaExemplo] = Field(
        default=None,
        description="O exemplo (clássico ou prático) estruturado ou None."
    )

class SubtopicoValidado(BaseModel):
    titulo_subtopico: str
    conteudo: ConteudoSubtopico = Field(description="O conteúdo do subtópico estruturado (teórico).")
    fontes_rag: List[FonteRDetalhada] = Field(description="Lista de fontes bibliográficas detalhadas extraídas estritamente do RAG.")

# ==========================================
# SCHEMAS DO AGENTE 3 (CRIADOR DE EXERCÍCIOS)
# ==========================================

class AlternativasFechadas(BaseModel):
    A: str = Field(description="Opção alternativa A.")
    B: str = Field(description="Opção alternativa B.")
    C: str = Field(description="Opção alternativa C.")
    D: str = Field(description="Opção alternativa D.")
    E: Optional[str] = Field(default=None, description="Opção alternativa E (opcional).")

class QuestaoFechada(BaseModel):
    enunciado: str = Field(description="O problema prático com uma situação estatística clara.")
    alternativas: AlternativasFechadas = Field(description="As alternativas estruturadas contendo exatamente de A a D (e opcionalmente E).")
    alternativa_correta: str = Field(description="A letra da alternativa correta (Ex: 'A', 'B', 'C', 'D' ou 'E').")
    dica: str = Field(description="Orientação sutil para o aluno pensar, sem dar a resposta direta.")
    gabarito_comentado: str = Field(description="Explicação detalhada do porquê aquela alternativa é a correta.")

class QuestaoAberta(BaseModel):
    enunciado: str = Field(description="Pergunta discursiva ou problema de cálculo estatístico detalhado.")
    dica: str = Field(description="Diretriz conceitual ou fórmula que o aluno deve lembrar para resolver.")
    gabarito_passo_a_passo: List[str] = Field(description="Passo a passo matemático para se chegar à resolução completa.")

class CadernoExerciciosValidado(BaseModel):
    topico_aula: str
    questoes_multipla_escolha: List[QuestaoFechada] = Field(
        description="Lista contendo obrigatoriamente pelo menos 5 questões de múltipla escolha complexas."
    )
    questoes_discursivas: List[QuestaoAberta] = Field(
        description="Lista contendo obrigatoriamente pelo menos 3 questões discursivas/cálculos complexas."
    )

class PaginaLapidada(BaseModel):
    titulo_subtopico: str
    discussao_teorica_prosa: str = Field(description="Texto longo e denso em prosa acadêmica sem bullets. O conteúdo deve se conectar fluentemente com o subtópico anterior.")
    prosa_longa_expandida: Optional[str] = Field(default=None, description="Texto extremamente longo, denso e exaustivo em prosa fluida gerado pelo Construtor de Prosa.")
    formalismo_latex: str = Field(description="Bloco de fórmulas em LaTeX ($$) sem repetições de equações que já apareceram na aula.")
    
    # Mudança de String para List para forçar a abertura de todas as linhas matemáticas
    deducao_analitica_linhas: List[str] = Field(
        description="A derivação matemática completa dividida linha por linha em LaTeX ($$). Cada item da lista deve ser uma equação que se desdobra logicamente da anterior."
    )
    
    # Transformado em lista obrigatória para garantir volume de conteúdo prático
    exemplos_praticos_ricos: List[ExemploResolvidoRico] = Field(
        description="Lista contendo obrigatoriamente de 2 a 3 exemplos práticos e resolvidos de alta complexidade sobre o subtópico."
    )

class MapeamentoSimulador(BaseModel):
    indice_pagina: str = Field(description="O índice da página (ex: '1', '2', '3') onde o simulador interativo deve ser carregado.")
    nome_simulador: str = Field(description="O nome descritivo do simulador interativo correspondente (ex: 'Visualizador de Erros').")

class AulaUnificadaELapidada(BaseModel):
    tema_global: str
    paginas_conteudo: List[PaginaLapidada] = Field(description="A sequência de páginas da aula, livre de repetições textuais ou conceituais.")
    # --- MAPEAMENTO CENTRALIZADO DE SIMULADORES (Acaba com gráficos repetidos) ---
    simuladores_da_aula: List[MapeamentoSimulador] = Field(
        description="Lista contendo o mapeamento de onde os gráficos devem entrar. Atribua gráficos apenas onde for vital, garantindo que nenhum gráfico seja igual ao outro."
    )
    # --- O RODAPÉ EXIGIDO PELO PROFESSOR ---
    referencias_bibliograficas_finais: List[str] = Field(description="Lista consolidada e unificada de livros e páginas reais utilizadas em toda a extensão da aula (sem duplicatas).")
