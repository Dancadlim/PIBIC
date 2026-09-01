/**
 * Sanitizador Universal de LaTeX para a Interface Frontend (Next.js)
 * Enforces 100% valid KaTeX / ReactMarkdown parsing across titles, boxes, and prose
 * using Context-Aware Block Tokenization.
 */

function sanitizeDisplayMath(content: string): string {
  let c = content;
  // 1. Converte ambientes incompatíveis com o rehype-katex
  c = c.replace(/\\begin\{(align\*?|equation\*?|gather\*?)\}/g, '\\begin{aligned}');
  c = c.replace(/\\end\{(align\*?|equation\*?|gather\*?)\}/g, '\\end{aligned}');

  // 2. Converte macros incompatíveis e limpa chaves escapadas
  c = c.replace(/\\bm\{/g, '\\boldsymbol{');
  c = c.replace(/\\bold\{/g, '\\mathbf{');
  c = c.replace(/\\+boldsymbol\\+\{([^}]+)\}/g, '\\boldsymbol{$1}');
  c = c.replace(/\\+boldsymbol\\+\{/g, '\\boldsymbol{');
  c = c.replace(/\\+mathbf\\+\{/g, '\\mathbf{');
  c = c.replace(/(\t|\\+)hicksim/g, '\\sim');
  c = c.replace(/\\+nginxed/g, '\\in');

  // 3. Escapa porcentagem solta dentro do math
  c = c.replace(/(?<!\\)%/g, '\\%');

  // 4. Trunca falhas em \right
  c = c.replace(/[\s\r\n\t]+ight([\)\}\]|\\])/g, ' \\right$1');
  c = c.replace(/[\s\r\n\t]+ight/g, ' \\right');

  return c.trim();
}

function sanitizeInlineMath(content: string): string {
  let c = content;
  c = c.replace(/\\bm\{/g, '\\boldsymbol{');
  c = c.replace(/\\bold\{/g, '\\mathbf{');
  c = c.replace(/\\+boldsymbol\\+\{([^}]+)\}/g, '\\boldsymbol{$1}');
  c = c.replace(/\\+boldsymbol\\+\{/g, '\\boldsymbol{');
  c = c.replace(/\\+nginxed/g, '\\in');
  c = c.replace(/(?<!\\)%/g, '\\%');
  
  // Resolve artefatos onde o LLM insere múltiplas barras antes de comandos gregos, ex: \\\\mu -> \\mu
  c = c.replace(/\\\\+/g, '\\');
  
  return c.trim();
}

export function sanitizeLatex(text: string): string {
  if (!text) return "";
  let processed = text;

  // Protege valores monetários (R$ e US$) substituindo temporariamente para que o tokenizador não os engula
  processed = processed.replace(/R\$(?!\$)/g, 'R__DOLLAR__');
  processed = processed.replace(/US\$(?!\$)/g, 'US__DOLLAR__');

  // 1. Normaliza delimitadores clássicos LaTeX
  processed = processed.replace(/\\\[/g, '\n$$\n').replace(/\\\]/g, '\n$$\n');
  processed = processed.replace(/\\\(/g, '$').replace(/\\\)/g, '$');

  // 2. Divide a string em tokens de Display Math ($$...$$), Inline Math ($...$) e Prosa
  // O lookbehind (?<!\\) impede que um \$ (cifrão escapado) inicie ou termine um bloco matemático.
  const pattern = /(?<!\\)(\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\$(?:[^\$\n]|\\\$)+?(?<!\\)\$)/g;
  const parts = processed.split(pattern);

  const resultParts: string[] = [];
  for (const part of parts) {
    if (!part) continue;

    if (part.startsWith('$$') && part.endsWith('$$') && part.length >= 4) {
      const inner = part.slice(2, -2);
      const sanitizedInner = sanitizeDisplayMath(inner);
      resultParts.push(`\n$$\n${sanitizedInner}\n$$\n`);
    } else if (part.startsWith('$') && part.endsWith('$') && part.length >= 2 && !part.includes('\n')) {
      const inner = part.slice(1, -1);
      const sanitizedInner = sanitizeInlineMath(inner);
      resultParts.push(`$${sanitizedInner}$`);
    } else {
      // É prosa comum (fora de cifrões)
      let prose = part;
      
      // Auto-envelopa expressões matemáticas óbvias soltas na prosa (ex: P(A \text{ vence}) \times ... = R$ 48.000 ou \beta_1 = 3.5)
      // Identifica linhas ou segmentos contendo comandos como \times, \frac, \text, \sum, \hat, \sqrt sem $
      const mathLinePattern = /(?:(?:[A-Z]\([^\)]+\)|\\(?:text|times|frac|sum|prod|int|hat|bar|sqrt|boldsymbol|mathbf|pm|approx|leq|geq|neq|sim|cdot))[^$\n]*?(?:=|\+|-|\*|\/|\\times|\approx)[^$\n]*)/g;
      
      prose = prose.replace(mathLinePattern, (match) => {
        // Se já tiver $, não mexe
        if (match.includes('$')) return match;
        // Limpa espaços extras nas pontas e envelopa em $
        const trimmed = match.trim();
        if (trimmed.length > 3) {
          return ` $${trimmed}$ `;
        }
        return match;
      });

      // Símbolos gregos e matemáticos isolados soltos na prosa
      const symbolsToWrap = /(?<!\$)(?<!\\)(\\(?:mu|sigma|alpha|beta|theta|lambda|pi|gamma|delta|epsilon|phi|omega|rho|tau|eta|chi|psi|zeta|Omega|Sigma|Delta|Theta|Gamma|Phi|Psi|Lambda|in|forall|exists|rightarrow|Rightarrow|infty|partial|mathcal\{[A-Za-z]\}))(?!\$)/g;
      prose = prose.replace(symbolsToWrap, (_, sym) => ` $${sym}$ `);
      resultParts.push(prose);
    }
  }

  processed = resultParts.join('');

  // 3. Corrige cifrões duplicados ou aninhados criados acidentalmente ($ $...$ $)
  processed = processed.replace(/\$\s*\$([^\$]+?)\$\s*\$/g, '$$$1$$');

  // 3. Anexa pontuações isoladas que ficaram soltas após equações ou quebras de linha
  processed = processed.replace(/(\$\$[\s\S]*?\$\$)\s*\n+\s*([.,;:!?])/g, '$1$2\n\n');
  processed = processed.replace(/\n+\s*([.,;:!?])\s+(?=[A-Za-z0-9Á-ÿ])/g, '$1 ');
  processed = processed.replace(/\n+\s*([.,;:!?])\s*\n+/g, '$1\n\n');
  processed = processed.replace(/\.{2,}/g, '.');

  // 4. Ajusta o espaçamento ao redor de inline math colado em palavras em português
  processed = processed.replace(/([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])\$([^$\n]+?)\$/g, (_, w, m) => `${w} $${m}$`);
  processed = processed.replace(/\$([^$\n]+?)\$([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])/g, (_, m, w) => `$${m}$ ${w}`);

  // 5. Remove espaços em branco no início de cada linha (evita bloco <pre> identado no Markdown)
  const lines = processed.split('\n');
  const processedLines = lines.map(line => line.replace(/^[ \t]+/, ''));
  processed = processedLines.join('\n');

  // 6. Remove excesso de quebras de linha mantendo no máximo parágrafo duplo
  processed = processed.replace(/\n{3,}/g, '\n\n');

  // 7. Restaura os símbolos monetários devidamente escapados
  processed = processed.replace(/R__DOLLAR__/g, 'R\\$');
  processed = processed.replace(/US__DOLLAR__/g, 'US\\$');

  return processed;
}
