import re

def sanitize_latex_string(text: str) -> str:
    """
    Sanitiza e normaliza deterministicamente qualquer string contendo notações LaTeX
    para garantir 100% de compilação sem erros no KaTeX / ReactMarkdown.
    """
    if not isinstance(text, str) or not text.strip():
        return text

    processed = text

    # 0a. Substituir ambientes LaTeX que o KaTeX não suporta diretamente em rehype-katex inline
    processed = re.sub(r'\\begin\{(align\*?|equation\*?|gather\*?)\}', r'\\begin{aligned}', processed)
    processed = re.sub(r'\\end\{(align\*?|equation\*?|gather\*?)\}', r'\\end{aligned}', processed)

    # 0b. Substituir comandos não suportados pelo KaTeX
    processed = re.sub(r'\\bm\{', r'\\boldsymbol{', processed)
    processed = re.sub(r'\\bold\{', r'\\mathbf{', processed)
    processed = re.sub(r'\\+boldsymbol\\+\{([^}]+)\}', r'\\boldsymbol{\1}', processed)
    processed = re.sub(r'\\+boldsymbol\\+\{', r'\\boldsymbol{', processed)
    processed = re.sub(r'(\t|\\+)hicksim', r'\\sim', processed)
    processed = re.sub(r'\\+nginxed', r'\\in', processed)
    
    # 0c. Limpar comandos de equação dentro de \text{...}
    processed = re.sub(r'\\+text\{\s*\\+?(hat|bar|tilde|beta|alpha|sigma|theta|nu|mu|lambda|pi|gamma|delta|epsilon|phi)\{?([^}]*)\}?\s*\}', r'\\\1{\2}', processed)
    processed = re.sub(r'\\+boldsymbol\{\s*\\+text\{([^}]*)\}\s*\}', r'\\boldsymbol{\1}', processed)
    processed = re.sub(r'\\+text\{\s*\\+textsigma\s*\}', r'\\sigma', processed)
    processed = re.sub(r'\\+text\{\s*\\+textellipsis\s*\}', r'\\dots', processed)
    processed = re.sub(r'\\+textsigma', r'\\sigma', processed)
    processed = re.sub(r'\\+textellipsis', r'\\dots', processed)

    # 1. Corrigir truncamentos de \right (ex: ' ight' ou '\r' + 'ight')
    processed = re.sub(r'[\s\r\n\t]+ight([\)\}\]|\\])', r' \\right\1', processed)
    processed = re.sub(r'[\s\r\n\t]+ight', r' \\right', processed)

    # 2. Corrigir blocos multilinhas iniciados com cifrão único '$' (Cifrão único NÃO pode conter \n ou \\)
    def fix_multiline_single_dollar(match):
        inner = match.group(1)
        if '\n' in inner or '\\\\' in inner or '\\quad' in inner:
            return f"\n$$\n{inner.strip()}\n$$\n"
        return match.group(0)

    processed = re.sub(r'(?<!\$)\$([^$\n]+?\n[^$]+?)\$(?!\$)', fix_multiline_single_dollar, processed)

    # 3. Converter delimitadores clássicos LaTeX \[ \] e \( \) para $$ e $
    processed = processed.replace(r'\[', '\n$$\n').replace(r'\]', '\n$$\n')
    processed = processed.replace(r'\(', '$').replace(r'\)', '$')

    # 4. Corrigir chaves de conjunto numérico sem barra de escape em ambiente matemático (ex: { \omega } -> \{ \omega \})
    def escape_set_braces(math_str):
        math_str = re.sub(r'(?<!\\)\{\s*(\\omega|\\in|\\forall|\\exists|x|y|i|a|b)', r'\\{\1', math_str)
        math_str = re.sub(r'(\\text\{[^}]+\}\s*)\}(?!\s*\\)', r'\1\\}', math_str)
        return math_str

    # Processar dentro dos blocos $$...$$
    def process_display_math(match):
        content = escape_set_braces(match.group(1))
        return f"\n$$\n{content.strip()}\n$$\n"

    processed = re.sub(r'\$\$(.*?)\$\$', process_display_math, processed, flags=re.DOTALL)

    # 5. Detectar linhas soltas que contêm expressões LaTeX matemáticas cruas sem $ ou $$
    lines = processed.split('\n')
    processed_lines = []
    for line in lines:
        trimmed = line.strip()
        if not trimmed:
            processed_lines.append(line)
            continue

        if trimmed.startswith('$$') or trimmed.startswith('#') or trimmed.startswith('|-') or trimmed.startswith('|'):
            processed_lines.append(line)
            continue

        has_latex_cmd = bool(re.search(r'\\[a-zA-Z]+|\^\{|_\{', trimmed))
        has_dollar = '$' in trimmed

        if has_latex_cmd and not has_dollar:
            palavras_prosa = re.findall(r'[a-zA-ZáàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ]{4,}', trimmed)
            if len(palavras_prosa) <= 3 or ('=' in trimmed and ('\\' in trimmed or '^' in trimmed or '_' in trimmed)):
                processed_lines.append(f"\n$$\n{trimmed}\n$$\n")
                continue
            else:
                wrapped_line = re.sub(
                    r'(?<!\$)(?<!\\)(\\[a-zA-Z]+(?:\{[^}]*\}|_[a-zA-Z0-9{}]+|\^[a-zA-Z0-9{}]+)*|(?:[a-zA-Z0-9_]+\^\{[^}]*\}|[a-zA-Z0-9_]+_\{[^}]*\}|\b[a-zA-Z]_\{[0-9a-zA-Z,]+\}))(?!\$)',
                    r' $\1$ ',
                    line
                )
                processed_lines.append(wrapped_line)
                continue

        processed_lines.append(line)

    processed = '\n'.join(processed_lines)

    # 6. Envolver comandos matemáticos LaTeX soltos em prosa que não estão dentro de $...$
    symbols_to_wrap = r'(?:\\mu|\\sigma|\\alpha|\\beta|\\theta|\\lambda|\\pi|\\gamma|\\delta|\\epsilon|\\phi|\\omega|\\rho|\\tau|\\eta|\\chi|\\psi|\\zeta|\\in|\\forall|\\exists|\\rightarrow|\\Rightarrow|\\infty|\\partial)'
    processed = re.sub(r'(?<!\$)(?<!\\)\b(' + symbols_to_wrap + r')\b(?!\$)', r'$\1$', processed)

    # 7. Garantir espaço em branco ao redor de inline math $...$ quando colado em palavras
    processed = re.sub(r'([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])\$([^$\n]+?)\$', r'\1 $\2$', processed)
    processed = re.sub(r'\$([^$\n]+?)\$([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])', r'$\1$ \2', processed)

    # 8. Remover quebras de linha quadruplas
    processed = re.sub(r'\n{4,}', '\n\n\n', processed)

    return processed

def sanitize_json_recursively(obj):
    """
    Percorre recursivamente um dicionário ou lista JSON e aplica sanitize_latex_string em cada campo de texto.
    """
    if isinstance(obj, str):
        return sanitize_latex_string(obj)
    elif isinstance(obj, dict):
        return {k: sanitize_json_recursively(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_json_recursively(elem) for elem in obj]
    return obj
