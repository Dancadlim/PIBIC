/**
 * Sanitizador Universal de LaTeX para a Interface Frontend (Next.js)
 * Enforces 100% valid KaTeX / ReactMarkdown parsing across titles, boxes, and prose.
 */

export function sanitizeLatex(text: string): string {
  if (!text) return "";
  let processed = text;

  // 0a. Substituir ambientes LaTeX que o KaTeX não suporta diretamente no rehype-katex
  processed = processed.replace(/\\begin\{(align\*?|equation\*?|gather\*?)\}/g, '\\begin{aligned}');
  processed = processed.replace(/\\end\{(align\*?|equation\*?|gather\*?)\}/g, '\\end{aligned}');

  // 0b. Substituir comandos não suportados pelo KaTeX
  processed = processed.replace(/\\bm\{/g, '\\boldsymbol{');
  processed = processed.replace(/\\bold\{/g, '\\mathbf{');
  processed = processed.replace(/\\+boldsymbol\\+\{([^}]+)\}/g, '\\boldsymbol{$1}');
  processed = processed.replace(/\\+boldsymbol\\+\{/g, '\\boldsymbol{');
  processed = processed.replace(/(\t|\\+)hicksim/g, '\\sim');
  processed = processed.replace(/\\+nginxed/g, '\\in');

  // 0c. Limpar comandos de equação dentro de \text{...}
  processed = processed.replace(/\\+text\{\s*\\+?(hat|bar|tilde|beta|alpha|sigma|theta|nu|mu|lambda|pi|gamma|delta|epsilon|phi)\{?([^}]*)\}?\s*\}/g, '\\$1{$2}');
  processed = processed.replace(/\\+boldsymbol\{\s*\\+text\{([^}]*)\}\s*\}/g, '\\boldsymbol{$1}');
  processed = processed.replace(/\\+text\{\s*\\+textsigma\s*\}/g, '\\sigma').replace(/\\+text\{\s*\\+textellipsis\s*\}/g, '\\dots');
  processed = processed.replace(/\\+textsigma/g, '\\sigma').replace(/\\+textellipsis/g, '\\dots');

  // 1. Corrigir quebras ou truncamentos de '\right' (ex: ' ight' ou '\r' + 'ight')
  processed = processed.replace(/[\s\r\n\t]+ight([\)\}\]|\\])/g, ' \\right$1');
  processed = processed.replace(/[\s\r\n\t]+ight/g, ' \\right');

  // 2. Corrigir bloco de múltiplas linhas iniciado por '$' único quebrando linha antes de fechar '$'
  processed = processed.replace(/(?<!\$)\$([^$\n]+?\n[^$]+?)\$(?!\$)/g, (match, inner) => {
    return `\n$$\n${inner.trim()}\n$$\n`;
  });

  // 3. Converter delimitadores clássicos LaTeX \[ \] e \( \) para $$ e $
  processed = processed.replace(/\\\[/g, '\n$$\n').replace(/\\\]/g, '\n$$\n');
  processed = processed.replace(/\\\(/g, '$').replace(/\\\)/g, '$');

  // 4. Auto-encapsular linhas soltas que contêm expressões LaTeX matemáticas cruas sem $ ou $$
  const lines = processed.split('\n');
  const processedLines = lines.map(line => {
    const trimmed = line.trim();
    if (!trimmed) return line;

    if (trimmed.startsWith('$$') || trimmed.startsWith('#') || trimmed.startsWith('|-') || trimmed.startsWith('|')) {
      return line;
    }

    const hasLatexCmd = /\\[a-zA-Z]+|\^\{|_\{/.test(trimmed);
    const hasDollar = trimmed.includes('$');

    if (hasLatexCmd && !hasDollar) {
      if (trimmed.startsWith('\\') || (trimmed.includes('=') && (trimmed.includes('\\') || trimmed.includes('^') || trimmed.includes('_')))) {
        return `\n$$\n${trimmed}\n$$\n`;
      }
    }
    return line;
  });
  processed = processedLines.join('\n');

  // 5. Envolver comandos matemáticos LaTeX soltos em prosa que não estão dentro de $...$
  const symbolsToWrap = /(?<!\$)(?<!\\)\b(\\mu|\\sigma|\\alpha|\\beta|\\theta|\\lambda|\\pi|\\gamma|\\delta|\\epsilon|\\phi|\\omega|\\rho|\\tau|\\eta|\\chi|\\psi|\\zeta|\\in|\\forall|\\exists|\\rightarrow|\\Rightarrow|\\infty|\\partial)\b(?!\$)/g;
  processed = processed.replace(symbolsToWrap, '$$1$');

  // 6. Garantir que delimitadores $$ fiquem em suas próprias linhas para o remark-math
  processed = processed.replace(/([^\n])\$\$/g, '$1\n$$');
  processed = processed.replace(/\$\$([^\n])/g, '$$\n$1');

  // 7. Remove espaços em branco no INÍCIO de qualquer linha (impede <pre> identado no Markdown)
  processed = processed.replace(/^[ \t]+/gm, '');

  // 8. Arruma espaços acidentais em math inline gerados pela IA (ex: $ k $ -> $k$)
  processed = processed.replace(/\$\s+([^$\n]+?)\s+\$/g, '$$$1$$');

  // 9. Garantir espaço em branco antes e depois de inline math $...$ quando colado em palavras
  processed = processed.replace(/([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])\$([^$\n]+?)\$/g, (m, p1, p2) => `${p1} $${p2}$`);
  processed = processed.replace(/\$([^$\n]+?)\$([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])/g, (m, p1, p2) => `$${p1}$ ${p2}`);

  // 10. Remove quebras de linha excessivas
  return processed.replace(/\n{4,}/g, '\n\n\n');
}

