/**
 * Sanitizador Universal de LaTeX para a Interface Frontend (Next.js)
 * Enforces 100% valid KaTeX / ReactMarkdown parsing across titles, boxes, and prose.
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

  // 3. Remove cifrões que o modelo possa ter inserido DENTRO de blocos matemáticos
  // (ex: \begin{aligned} ... $theta$ ... \end{aligned})
  c = c.replace(/(?<!\\)\$/g, '');

  // 4. Escapa porcentagem solta dentro do math
  c = c.replace(/(?<!\\)%/g, '\\%');

  // 5. Trunca falhas em \right
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
  
  // Remove cifrões aninhados
  c = c.replace(/(?<!\\)\$/g, '');
  
  // Resolve artefatos onde o LLM insere múltiplas barras antes de comandos gregos
  c = c.replace(/\\\\+/g, '\\');
  
  return c.trim();
}

export function sanitizeLatex(text: string): string {
  if (!text) return "";
  let processed = text.trim();

  // Protege valores monetários (R$ e US$) substituindo temporariamente
  processed = processed.replace(/R\$(?!\$)/g, 'R__DOLLAR__');
  processed = processed.replace(/US\$(?!\$)/g, 'US__DOLLAR__');

  // 1. Normaliza delimitadores clássicos LaTeX
  processed = processed.replace(/\\\[/g, '\n$$\n').replace(/\\\]/g, '\n$$\n');
  processed = processed.replace(/\\\(/g, '$').replace(/\\\)/g, '$');

  // 1.1 Corrige cifrões desbalanceados por parágrafo (evita que texto em português vire math itálico)
  const paragraphs = processed.split('\n\n');
  const balancedParagraphs = paragraphs.map(p => {
    const tempP = p.replace(/\$\$/g, '');
    const matches = tempP.match(/(?<!\\)\$/g);
    const singleDollars = matches ? matches.length : 0;
    if (singleDollars % 2 !== 0) {
      // Há um cifrão ímpar/órfão aberto no parágrafo: fecha no final da linha antes da pontuação/quebra
      return p.replace(/(\$[^$\n]+?)([\.\,\;\:\?\!]|(?=\n)|$)/, '$1$$2');
    }
    return p;
  });
  processed = balancedParagraphs.join('\n\n');

  // 2. Se a string inteira for um bloco com \begin{aligned} ou \begin{...} sem $$, envolve em $$
  if (!processed.includes('$$') && processed.includes('\\begin{')) {
    processed = processed.replace(/(\\begin\{[a-zA-Z*]+\}[\s\S]*?\\end\{[a-zA-Z*]+\})/g, '\n$$\n$1\n$$\n');
  }

  // 3. Divide a string em tokens de Display Math ($$...$$), Inline Math ($...$) e Prosa
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
      // Prosa comum (fora de cifrões)
      let prose = part;
      
      // Auto-wrap para binom solto na prosa (\binom{n}{k} -> $\binom{n}{k}$)
      prose = prose.replace(/(?<!\$)(?<!\\)(\\(?:d?binom|tbinom)\{[^}]+\}\{[^}]+\})(?!\$)/g, ' $$1 ');

      // Símbolos gregos e matemáticos isolados soltos na prosa
      const symbolsToWrap = /(?<!\$)(?<!\\)(\\(?:mu|sigma|alpha|beta|theta|lambda|pi|gamma|delta|epsilon|varepsilon|phi|omega|rho|tau|eta|chi|psi|zeta|Omega|Sigma|Delta|Theta|Gamma|Phi|Psi|Lambda|forall|exists|rightarrow|Rightarrow|infty|partial|mathcal\{[A-Za-z]\}))(?!\$)/g;
      prose = prose.replace(symbolsToWrap, (_, sym) => ` $${sym}$ `);
      resultParts.push(prose);
    }
  }

  processed = resultParts.join('');

  // 4. Anexa pontuações isoladas que ficaram soltas após equações
  processed = processed.replace(/(\$\$[\s\S]*?\$\$)\s*\n+\s*([.,;:!?])/g, '$1$2\n\n');
  processed = processed.replace(/\n+\s*([.,;:!?])\s+(?=[A-Za-z0-9Á-ÿ])/g, '$1 ');
  processed = processed.replace(/\n+\s*([.,;:!?])\s*\n+/g, '$1\n\n');
  processed = processed.replace(/\.{2,}/g, '.');

  // 5. Ajusta o espaçamento ao redor de inline math colado em palavras em português
  processed = processed.replace(/([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])\$([^$\n]+?)\$/g, (_, w, m) => `${w} $${m}$`);
  processed = processed.replace(/\$([^$\n]+?)\$([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])/g, (_, m, w) => `$${m}$ ${w}`);

  // 6. Remove espaços em branco no início de cada linha (evita bloco <pre> identado no Markdown)
  const lines = processed.split('\n');
  const processedLines = lines.map(line => line.replace(/^[ \t]+/, ''));
  processed = processedLines.join('\n');

  // 7. Remove excesso de quebras de linha mantendo no máximo parágrafo duplo
  processed = processed.replace(/\n{3,}/g, '\n\n');

  // 8. Restaura os símbolos monetários devidamente escapados
  processed = processed.replace(/R__DOLLAR__/g, 'R\\$');
  processed = processed.replace(/US__DOLLAR__/g, 'US\\$');

  return processed;
}
