const text1 = '$$ E[\\mathbf{X}] = \\begin{pmatrix} E[X_1] \\\\ E[X_2] \\end{pmatrix} $';
const text2 = '$ E[\\mathbf{X}] = \\begin{pmatrix} E[X_1] \\\\ E[X_2] \\end{pmatrix} $';
const text3 = '$$ E[\\mathbf{X}] = \\begin{pmatrix} E[X_1] \\\\ E[X_2] \\end{pmatrix} $$';
const text4 = 'prefix $$ E[\\mathbf{X}] = \\begin{pmatrix} E[X_1] \\\\ E[X_2] \\end{pmatrix} $ suffix';

let processLatex = (text) => {
  if (!text) return "";
  let processed = text;
  
  // 1. Corrige bloco $$ ... $ 
  processed = processed.replace(/(^|[^$])\$\$([^$]*?)\$(?!\$)/g, (_, prefix, math) => prefix + '$$' + math + '$$');

  // 2. Corrige bloco $ ... $$
  processed = processed.replace(/(^|[^$])\$([^$]*?)\$\$(?!\$)/g, (_, prefix, math) => prefix + '$$' + math + '$$');

  // 3. Converte $ \begin{...} ... \end{...} $ para $$ ... $$
  processed = processed.replace(/(^|[^$])\$([^$]*?\\begin\{[^}]+\}[^$]*?\\end\{[^}]+\}[^$]*?)\$(?!\$)/g, (_, prefix, math) => prefix + '$$' + math + '$$');

  // 4. Converte \[ ... \] para $$ ... $$
  processed = processed.replace(/\\\[([\s\S]*?)\\\]/g, (_, math) => '$$' + math + '$$');

  // 5. Garante as quebras de linha para todos os blocos $$
  processed = processed.replace(/\$\$/g, () => '\n\n$$\n\n');

  // Remove quebras de linha em excesso
  processed = processed.replace(/\n{4,}/g, '\n\n\n');

  return processed;
};

console.log('1:', processLatex(text1));
console.log('2:', processLatex(text2));
console.log('3:', processLatex(text3));
console.log('4:', processLatex(text4));
