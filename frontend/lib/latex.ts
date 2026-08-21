/**
 * Sanitiza e prepara strings contendo marcações LaTeX/Markdown
 * para renderização limpa e confiável no ReactMarkdown + KaTeX.
 */
export function processLatex(text: string): string {
  if (!text) return "";
  let processed = text;

  // 1. Converter delimitadores clássicos LaTeX \[ \] e \( \) para $$ e $
  processed = processed.replace(/\\\[/g, '\n\n$$\n\n').replace(/\\\]/g, '\n\n$$\n\n');
  processed = processed.replace(/\\\(/g, '$').replace(/\\\)/g, '$');

  // 2. Garantir que delimitadores $$ fiquem isolados com quebras de linha duplas
  processed = processed.replace(/([^\n])\$\$/g, '$1\n\n$$');
  processed = processed.replace(/\$\$([^\n])/g, '$$\n\n$1');
  
  // 3. Remove espaços em branco no INÍCIO de qualquer linha (impede blocos <pre> acidentais no Markdown)
  processed = processed.replace(/^[ \t]+/gm, '');

  // 4. Arruma espaços acidentais em math inline gerados pela IA (ex: $ k $ -> $k$)
  processed = processed.replace(/\$\s+([^$\n]+?)\s+\$/g, '$$$1$$');

  // 5. Garantir espaço adequado antes e depois de inline math $...$ quando colado em palavras ou pontuações como ($R^2$)
  processed = processed.replace(/([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ(])\$([^$\n]+?)\$/g, '$1 $$$2$$');
  processed = processed.replace(/\$([^$\n]+?)\$([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ)])/g, '$$$1$$ $2');

  // 6. Remove quebras de linha excessivas
  return processed.replace(/\n{4,}/g, '\n\n\n');
}

/**
 * Normaliza e ordena rigorosamente as alternativas de múltipla escolha
 * garantindo a ordem alfabética estrita (A, B, C, D, E).
 */
export function getSortedAlternativas(alternativas: any): Array<{ letra: string; texto: string }> {
  if (!alternativas) return [];

  let items: Array<{ letra: string; texto: string }> = [];

  if (Array.isArray(alternativas)) {
    alternativas.forEach((item: any, idx: number) => {
      if (typeof item === 'string') {
        const match = item.match(/^([A-Ea-e])[\s):.-]+(.*)/);
        if (match) {
          items.push({ letra: match[1].toUpperCase(), texto: match[2] });
        } else {
          const defaultLetter = String.fromCharCode(65 + idx);
          items.push({ letra: defaultLetter, texto: item });
        }
      } else if (typeof item === 'object' && item !== null) {
        if (item.letra && item.texto) {
          items.push({ letra: String(item.letra).toUpperCase(), texto: String(item.texto) });
        } else {
          const entries = Object.entries(item);
          if (entries.length > 0) {
            const [k, v] = entries[0];
            const cleanKey = k.replace(/[^a-zA-Z]/g, '').toUpperCase() || String.fromCharCode(65 + idx);
            items.push({ letra: cleanKey, texto: String(v) });
          }
        }
      }
    });
  } else if (typeof alternativas === 'object' && alternativas !== null) {
    Object.entries(alternativas).forEach(([k, v]) => {
      if (v === null || v === undefined || v === "") return;
      const cleanKey = k.replace(/[^a-zA-Z]/g, '').toUpperCase();
      const letra = cleanKey.length > 0 ? cleanKey.slice(-1) : k.toUpperCase();
      items.push({ letra, texto: String(v) });
    });
  }

  const orderMap: Record<string, number> = { A: 1, B: 2, C: 3, D: 4, E: 5, F: 6 };
  items.sort((a, b) => {
    const orderA = orderMap[a.letra] || a.letra.charCodeAt(0);
    const orderB = orderMap[b.letra] || b.letra.charCodeAt(0);
    return orderA - orderB;
  });

  return items;
}
