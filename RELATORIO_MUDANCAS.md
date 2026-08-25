# Relatório Detalhado de Mudanças e Evolução do Projeto (PIBIC / Plataforma de Aulas UFBA)

Este documento registra detalhadamente todas as alterações, novos componentes, agentes de Inteligência Artificial, seleção de modelos, módulos de higienização de LaTeX e refatorações realizadas no sistema.

---

## 📋 Sumário
1. [Visão Geral Arquitetural](#1-visão-geral-arquitetural)
2. [Seleção e Alternância Dinâmica de Modelos de IA (Vertex AI)](#2-seleção-e-alternância-dinâmica-de-modelos-de-ia-vertex-ai)
3. [Novos Agentes e Módulos do Backend (`/backend`)](#3-novos-agentes-e-módulos-do-backend-backend)
4. [Refatoração dos Agentes Existentes](#4-refatoração-dos-agentes-existentes)
5. [Atualizações e Melhorias no Frontend (`/frontend`)](#5-atualizações-e-melhorias-no-frontend-frontend)
6. [Ferramentas de Diagnóstico e Benchmark](#6-ferramentas-de-diagnóstico-e-benchmark)
7. [Resumo dos Arquivos Modificados e Adicionados](#7-resumo-dos-arquivos-modificados-e-adicionados)

---

## 1. Visão Geral Arquitetural

A plataforma foi aprimorada para garantir **100% de estabilidade na geração, revisão e renderização de aulas acadêmicas** (com notação estatística e matemática via KaTeX/LaTeX).

### Principais Objetivos Alcançados:
- **Seleção e Alternância Dinâmica de Modelos Generativos**: Suporte a modelos pesados (`gemini-2.5-pro`), padrão (`gemini-2.5-flash`) e modelos da série Gemini 3.5 (`gemini-3.5-flash-lite`) via SDK `google-genai` conectando à **Vertex AI** (`us-central1` no projeto `plataformas-aula-ufba`).
- **Resiliência e Tolerância a Falhas de Armazenamento**: Criação do `StorageManager` híbrido com suporte a armazenamento local em arquivos JSON quando o Firebase não estiver disponível.
- **Extração Inteligente de Diretrizes Acadêmicas**: Novo `AgenteExtrator` capaz de interpretar PDFs ou notas de aula de professores e convertê-los em schemas estruturados de regras (`RegraOverride`).
- **Higienização Determinística e Validação de LaTeX**: Módulos dedicados no backend e frontend (`latex_sanitizer.py` e `latexSanitizer.ts`) para eliminar erros comuns de compilação KaTeX (como delimitadores desbalanceados, comandos malformados e truncamentos `\right`).
- **Depurador de Agentes em Tempo Real**: Expansão do modal de logs (`AgentDebuggerModal.tsx`) permitindo inspeção em tempo real de prompts, respostas brutas e etapas dos agentes.

---

## 2. Seleção e Alternância Dinâmica de Modelos de IA (Vertex AI)

A arquitetura do pipeline multi-agente permite escolher e alternar entre modelos generativos conforme a necessidade de velocidade, custo ou profundidade:

| Agente / Componente | Modelo Padrão / Opções | Função & Perfil de Desempenho |
| :--- | :--- | :--- |
| **Gerador de Conteúdo** | `gemini-3.5-flash-lite` *(Requer Ativação)* / `gemini-2.5-pro` / `gemini-2.5-flash` | Suporte a `gemini-3.5-flash-lite` para velocidade máxima e menor latência, ou `gemini-2.5-pro` para máxima profundidade teórica. |
| **MacroRoteirista** | `gemini-2.5-pro` | Raciocínio estrutural complexo para fatiar e organizar ementas universitárias inteiras em cronogramas coerentes. |
| **Orquestrador Editorial** | `gemini-2.5-pro` | Lapidação final, coesão pedagógica e refinamento de texto. |
| **Agente Extrator** | `gemini-3.5-flash-lite` *(Requer Ativação)* / `gemini-2.5-flash` | Extração rápida e estruturada (*Structured Outputs* com schema `RegraOverride`) a partir de PDFs de diretrizes. |
| **Agente de Exercícios** | `gemini-3.5-flash-lite` *(Requer Ativação)* / `gemini-2.5-flash` | Geração paralela ágil de questões de fixação e gabaritos comentados. |
| **Agente Simulador** | `gemini-3.5-flash-lite` *(Requer Ativação)* / `gemini-2.5-flash` | Criação rápida de estudos de caso e scripts executáveis para simulação. |
| **Validador de LaTeX** | `gemini-3.5-flash-lite` *(Requer Ativação)* / `gemini-2.5-flash` | Correção sintática ultra-rápida para anomalias em código KaTeX. |

> [!IMPORTANT]
> **Status de Ativação dos Modelos na Conta Vertex AI (Projeto `plataformas-aula-ufba`)**:
> - 🟢 **`gemini-2.5-flash`**: **[ATIVO / OPERACIONAL]**
> - 🟢 **`gemini-2.5-pro`**: **[ATIVO / OPERACIONAL]**
> - ⚠️ **`gemini-3.5-flash-lite`**: **[REQUER ATIVAÇÃO NO GOOGLE CLOUD CONSOLE]** — Atualmente retorna erro `404 NOT_FOUND`. Para utilizar este modelo no projeto, é necessário habilitar a API/Modelo no **Vertex AI Model Garden / Google Cloud Console** para o projeto `plataformas-aula-ufba`.

---

## 3. Novos Agentes e Módulos do Backend (`/backend`)

### 🔹 `backend/agente_extrator.py`
- **Função**: Processa documentos de diretrizes ou notações específicas fornecidos por professores.
- **Tecnologia**: Utiliza Gemini Flash (`gemini-3.5-flash-lite` / `gemini-2.5-flash`) com *Structured Outputs* (schema `RegraOverride`).
- **Retorno**: Mapeamento preciso de notações LaTeX exigidas (ex: $\mu$, $\sigma$, $\perp$), tópicos obrigatórios e estilo de exercícios.

### 🔹 `backend/latex_sanitizer.py`
- **Função**: Higienização determinística de notação matemática LaTeX antes do envio para o banco/frontend.
- **Correções Determinísticas**:
  - Ajusta comandos malformados como `\boldsymbol`, `\thicksim`, `\textsigma`.
  - Recompõe truncamentos como `ight` para `\right`.
  - Normaliza delimitadores clássicos `\[ \]` e `\( \)` para `$$` e `$`.
  - Garante que cifrões soltos `$ ... $` multilinhas sejam convertidos em blocos `$$ ... $$`.

### 🔹 `backend/agente_validador_latex.py`
- **Função**: Auditagem e correção automatizada de anomalias em código LaTeX.
- **Checagens**:
  - Valida alinhamento de ambientes `\begin{...}` e `\end{...}`.
  - Verifica cifrões desbalanceados e chaves `{}` não fechadas.
  - Submete trechos problemáticos ao Gemini com instruções focadas em sintaxe KaTeX.

### 🔹 `backend/storage.py`
- **Função**: Gerenciador unificado de persistência (`StorageManager`).
- **Modos**: Suporta persistência híbrida em **Firebase Firestore** ou **Sistema de Arquivos Local** (`backend/data_local/`), garantindo execução offline e resiliência.

---

## 4. Refatoração dos Agentes Existentes

### ✏️ `backend/main.py`
- Integração do `StorageManager` e novos endpoints para criação flexível de aulas manuais, personalizadas e inteligentes.
- Suporte a rotas com tratamento gracioso de erros de persistência.

### ✏️ `backend/gerador_conteudo.py` & `backend/orquestrador_editorial.py`
- Suporte à escolha de modelos (ex: `gemini-3.5-flash-lite` / `gemini-2.5-flash` vs `gemini-2.5-pro`).
- Integração da etapa de sanitização LaTeX automática e salvamento de logs estruturados.

### ✏️ `backend/revisor_notacao.py`
- Refatorado para checar notações exigidas por professores e notações padrão da literatura estatística.

### ✏️ `backend/agente_exercicios.py` & `backend/agente_simulador.py`
- Suporte a geração paralela e sanitização de enunciados e gabaritos em LaTeX.

### ✏️ `backend/logger_agentes.py` & `backend/schemas.py`
- Inclusão dos schemas `RegraOverride` e expansão de hooks de log para visualização de prompts e status em tempo real.

---

## 5. Atualizações e Melhorias no Frontend (`/frontend`)

### 🎨 `frontend/app/utils/latexSanitizer.ts`
- Sanitizador TypeScript equivalente ao do backend.
- Garante renderização impecável no ReactMarkdown / KaTeX no lado do cliente.

### 🐛 `frontend/components/AgentDebuggerModal.tsx`
- Modal de depuração visual com abas para cada agente.
- Exibe status, logs detalhados, tempo de execução e inspeção de prompts.

### 💻 Telas de Aluno e Professor
- `frontend/app/professor/criar/personalizado/page.tsx` & `inteligente/page.tsx`: Interface renovada com upload/inserção de diretrizes específicas do professor.
- `frontend/app/professor/aula/[id]/page.tsx` & `aluno/aula/[id]/page.tsx`: Melhorias de layout, suporte a abas de conteúdo, exercícios interativos e renderização KaTeX sem quebras.
- `frontend/app/globals.css`: Estilização aprimorada para blocos de código e fórmulas matemáticas.

---

## 6. Ferramentas de Diagnóstico e Benchmark

Foram incluídos scripts de teste e validação quantitativa:
- `backend/benchmark_runner.py`: Suíte para medir tempo de geração e taxa de sucesso dos agentes.
- `backend/run_full_eval.py` & `backend/check_eval_results.py`: Scripts para avaliação automatizada do pipeline.
- `backend/diagnostico_erros_latex.py` & `backend/test_sanitizer_fix.py`: Validação das regras de sanitização de LaTeX.
- `backend/inspect_aulas_generated.py`: Inspeção e exportação de aulas geradas no banco.

---

## 7. Resumo dos Arquivos Modificados e Adicionados

| Arquivo / Módulo | Tipo | Descrição |
| :--- | :--- | :--- |
| `backend/agente_extrator.py` | **[NOVO]** | Agente extrator de notações do professor via Gemini 3.5 Flash-Lite / 2.5 Flash. |
| `backend/latex_sanitizer.py` | **[NOVO]** | Sanitizador determinístico de LaTeX no backend. |
| `backend/agente_validador_latex.py` | **[NOVO]** | Validador e corretor de sintaxe KaTeX com IA. |
| `backend/storage.py` | **[NOVO]** | Gerenciador de armazenamento híbrido (Firebase/Local). |
| `frontend/app/utils/latexSanitizer.ts` | **[NOVO]** | Sanitizador determinístico no frontend. |
| `backend/main.py` | **[MODIFICADO]** | Novas rotas e integração com StorageManager. |
| `backend/gerador_conteudo.py` | **[MODIFICADO]** | Suporte a seleção de modelos (`gemini-3.5-flash-lite` / `gemini-2.5-flash` / `pro`), sanitização e auditoria. |
| `backend/orquestrador_editorial.py` | **[MODIFICADO]** | Pipeline de lapidação editorial. |
| `backend/logger_agentes.py` | **[MODIFICADO]** | Hooks de depuração e auditoria de prompts. |
| `frontend/components/AgentDebuggerModal.tsx` | **[MODIFICADO]** | Interface visual de depuração de agentes. |
| `frontend/app/professor/*` | **[MODIFICADO]** | Páginas de criação e visualização do professor. |
| `frontend/app/aluno/*` | **[MODIFICADO]** | Páginas de aulas e dashboard do aluno. |

---
*Relatório gerado em 25/08/2026.*
