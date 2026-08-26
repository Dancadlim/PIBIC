/**
 * Sanitizador Universal de LaTeX para a Interface Frontend (Next.js)
 * Enforces 100% valid KaTeX / ReactMarkdown parsing across titles, boxes, and prose.
 */

export function sanitizeLatex(text: string): string {
  if (!text) return "";
  let processed = text;

  // 0. Limpeza determinística de erros de sintaxe do KaTeX gerados por LLM
  processed = processed.replace(/\\boldsymbol\\\{([^}]+)\}/g, '\\boldsymbol{$1}');
  processed = processed.replace(/\\boldsymbol\\\{/g, '\\boldsymbol{');
  processed = processed.replace(/(\t|\\+)hicksim/g, '\\sim');
  processed = processed.replace(/\\nginxed/g, '\\in');
  processed = processed.replace(/\\text\{\s*\\?(hat|bar|tilde|beta|alpha|sigma|theta|nu|mu)\{?([^}]*)\}?\s*\}/g, '\\$1{$2}');
  processed = processed.replace(/\\boldsymbol\{\s*\\text\{([^}]*)\}\s*\}/g, '\\boldsymbol{$1}');
  processed = processed.replace(/\\text\{\s*\\textsigma\s*\}/g, '\\sigma').replace(/\\text\{\s*\\textellipsis\s*\}/g, '\\dots');
  processed = processed.replace(/\\textsigma/g, '\\sigma').replace(/\\textellipsis/g, '\\dots');

  // 0b. Corrigir quebras ou truncamentos de '\right' (ex: ' ight' ou '\r' + 'ight')
  processed = processed.replace(/[\s\r\n\t]+ight([\)\}\]|\\])/g, ' \\right$1');
  processed = processed.replace(/[\s\r\n\t]+ight/g, ' \\right');

  // 1. Corrigir bloco de múltiplas linhas iniciado por '$' único quebrando linha antes de fechar '$'
  processed = processed.replace(/(?<!\$)\$([^$\n]+?\n[^$]+?)\$(?!\$)/g, (match, inner) => {
    return `\n$$\n${inner.trim()}\n$$\n`;
  });

  // 2. Converter delimitadores clássicos LaTeX \[ \] e \( \) para $$ e $
  processed = processed.replace(/\\\[/g, '\n$$\n').replace(/\\\]/g, '\n$$\n');
  processed = processed.replace(/\\\(/g, '$').replace(/\\\)/g, '$');

  // 3. Auto-encapsular linhas soltas que contêm expressões LaTeX matemáticas cruas sem $ ou $$
  const lines = processed.split('\n');
  const processedLines = lines.map(line => {
    const trimmed = line.trim();
    if (!trimmed) return line;

    // Se a linha já tem $$ ou é um título Markdown (#) ou tabela, pula
    if (trimmed.startsWith('$$') || trimmed.startsWith('#') || trimmed.startsWith('|-') || trimmed.startsWith('|')) {
      return line;
    }

    // Se a linha não tem $ mas contém comandos LaTeX típicos
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

  // 4. Garantir que delimitadores $$ fiquem em suas próprias linhas para o remark-math
  processed = processed.replace(/([^\n])\$\$/g, '$1\n$$');
  processed = processed.replace(/\$\$([^\n])/g, '$$\n$1');

  // 5. Remove espaços em branco no INÍCIO de qualquer linha (impede <pre> identado no Markdown)
  processed = processed.replace(/^[ \t]+/gm, '');

  // 6. Arruma espaços acidentais em math inline gerados pela IA (ex: $ k $ -> $k$)
  processed = processed.replace(/\$\s+([^$\n]+?)\s+\$/g, '$$$1$$');

  // 7. Garantir espaço em branco antes e depois de inline math $...$ quando colado em palavras
  processed = processed.replace(/([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])\$([^$\n]+?)\$/g, (m, p1, p2) => `${p1} $${p2}$`);
  processed = processed.replace(/\$([^$\n]+?)\$([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])/g, (m, p1, p2) => `$${p1}$ ${p2}`);

  // 8. Remove quebras de linha excessivas
  return processed.replace(/\n{4,}/g, '\n\n\n');
}
