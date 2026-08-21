# Plataforma Gerador PIBIC - UFBA

Sistema de geração e orquestração de aulas, exercícios e simuladores com Inteligência Artificial para cursos universitários.

---

## 🚀 Alterações da Branch `Luca`

Nesta branch (**`Luca`**), foram implementadas diversas melhorias estruturais no Backend (integração com múltiplos modelos de IA e orquestração de agentes) e no Frontend (melhorias de UI/UX, sanitização de LaTeX e variáveis de ambiente).

### 🛠️ Backend (`/backend`)
* **Utilitário de Modelos de IA (`model_utils.py`)**: Criado módulo para gerenciar a seleção dinâmica de modelos Generative AI (`default_model` vs `gemini-3.5-flash-lite`), tratando especificidades de configuração (como omissão estrita do parâmetro `temperature` para modelos específicos).
* **Parâmetro `modelo_ia` nos Agentes**:
  * `agente_exercicios.py`: Suporte a seleção de modelo na geração de cadernos de exercícios.
  * `agente_simulador.py`: Suporte a seleção de modelo na geração de simuladores interativos em HTML.
  * `gerador_conteudo.py`: Propagação do modelo escolhido na geração de conteúdo bruto das aulas.
  * `macro_roteirista.py`: Suporte ao parâmetro de modelo no planejamento do cronograma do semestre.
  * `orquestrador_editorial.py`: Lapidação global do conteúdo de acordo com o modelo selecionado.
  * `revisor_notacao.py` e `prompts.py`: Atualizações nos fluxos e rotinas de alinhamento e prompting.
* **Endpoints em `main.py`**:
  * Atualizados os schemas (`SemestreRequest`, `SimuladorRequest`, `AulaAvulsaRequest`) para receberem `modelo_ia`.
  * Atualizado o processamento em background para repassar o modelo escolhido para todos os agentes paralelos e subprocessos.

### 🎨 Frontend (`/frontend`)
* **Configuração do Firebase (`lib/firebase.ts`)**: Adicionado suporte a variáveis de ambiente (`process.env.NEXT_PUBLIC_FIREBASE_*`) com fallback seguro para as chaves padrão do projeto.
* **Formatador LaTeX e Exercícios (`lib/latex.ts`)**:
  * Função `processLatex()` para sanitização e adequação dos delimitadores LaTeX (`\[ \]`, `\( \)`) para renderização fluida via ReactMarkdown/KaTeX.
  * Função `getSortedAlternativas()` para normalização e ordenação estrita (A, B, C, D, E) de alternativas de múltipla escolha.
* **Interface do Professor e Aluno**:
  * Atualização das telas de criação inteligente e personalizada de aulas com seletores do modelo de IA a ser utilizado.
  * Melhoria na renderização das aulas, simuladores e exercícios nas visualizações de aluno e professor (`aluno/aula/[id]`, `professor/aula/[id]`).

---

## 📌 Como Executar

### Backend
```bash
cd backend
python -m venv venv
# No Windows Powershell:
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
