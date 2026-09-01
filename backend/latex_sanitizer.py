import re

def sanitize_display_math(content: str) -> str:
    """Sanitiza o conteúdo interno de um bloco de Display Math ($$...$$)."""
    c = content
    # 1. Converte ambientes incompatíveis com o rehype-katex
    c = re.sub(r'\\begin\{(align\*?|equation\*?|gather\*?)\}', r'\\begin{aligned}', c)
    c = re.sub(r'\\end\{(align\*?|equation\*?|gather\*?)\}', r'\\end{aligned}', c)
    
    # 2. Converte macros incompatíveis e limpa chaves escapadas
    c = re.sub(r'\\bm\{', r'\\boldsymbol{', c)
    c = re.sub(r'\\bold\{', r'\\mathbf{', c)
    c = re.sub(r'\\+boldsymbol\\+\{([^}]+)\}', r'\\boldsymbol{\1}', c)
    c = re.sub(r'\\+boldsymbol\\+\{', r'\\boldsymbol{', c)
    c = re.sub(r'\\+mathbf\\+\{', r'\\mathbf{', c)
    c = re.sub(r'(\t|\\+)hicksim', r'\\sim', c)
    c = re.sub(r'\\+nginxed', r'\\in', c)
    
    # 3. Remove cifrões que o modelo possa ter inserido DENTRO de blocos matemáticos
    c = re.sub(r'(?<!\\)\$', '', c)

    # 4. Escapa porcentagem solta dentro do math
    c = re.sub(r'(?<!\\)%', r'\\%', c)
    
    # 5. Trunca falhas em \right
    c = re.sub(r'[\s\r\n\t]+ight([\)\}\]|\\])', r' \\right\1', c)
    c = re.sub(r'[\s\r\n\t]+ight', r' \\right', c)
    
    return c.strip()

def sanitize_inline_math(content: str) -> str:
    """Sanitiza o conteúdo interno de um bloco de Inline Math ($...$)."""
    c = content
    c = re.sub(r'\\bm\{', r'\\boldsymbol{', c)
    c = re.sub(r'\\bold\{', r'\\mathbf{', c)
    c = re.sub(r'\\+boldsymbol\\+\{([^}]+)\}', r'\\boldsymbol{\1}', c)
    c = re.sub(r'\\+boldsymbol\\+\{', r'\\boldsymbol{', c)
    c = re.sub(r'\\+nginxed', r'\\in', c)
    c = re.sub(r'(?<!\\)%', r'\\%', c)
    c = re.sub(r'(?<!\\)\$', '', c)
    return c.strip()

def sanitize_latex_string(text: str) -> str:
    """
    Sanitiza e normaliza deterministicamente qualquer string contendo notações LaTeX
    usando uma abordagem de tokenização por Árvore de Blocos (Context-Aware).
    """
    if not isinstance(text, str) or not text.strip():
        return text

    processed = text.strip()

    # Protege valores monetários (R$ e US$)
    processed = re.sub(r'R\$(?!\$)', 'R__DOLLAR__', processed)
    processed = re.sub(r'US\$(?!\$)', 'US__DOLLAR__', processed)

    # 1. Normaliza delimitadores clássicos LaTeX
    processed = processed.replace(r'\[', '\n$$\n').replace(r'\]', '\n$$\n')
    processed = processed.replace(r'\(', '$').replace(r'\)', '$')

    # 1.1 Corrige cifrões desbalanceados por parágrafo (evita que texto em português vire math itálico)
    paragraphs = processed.split('\n\n')
    balanced_paragraphs = []
    for p in paragraphs:
        # Conta cifrões não-escapados (excluindo display math $$)
        temp_p = p.replace('$$', '')
        single_dollars = len(re.findall(r'(?<!\\)\$', temp_p))
        if single_dollars % 2 != 0:
            # Há um cifrão ímpar/órfão aberto no parágrafo: fecha no final da linha antes da pontuação/quebra
            p = re.sub(r'(\$[^$\n]+?)([\.\,\;\:\?\!]|(?=\n)|$)', r'\1$\2', p, count=1)
        balanced_paragraphs.append(p)
    processed = '\n\n'.join(balanced_paragraphs)

    # 2. Se a string contiver \begin{aligned} ou \begin{...} sem $$, envolve em $$
    if '$$' not in processed and r'\begin{' in processed:
        processed = re.sub(r'(\\begin\{[a-zA-Z*]+\}[\s\S]*?\\end\{[a-zA-Z*]+\})', r'\n$$\n\1\n$$\n', processed)

    # 3. Divide a string em tokens de Display Math ($$...$$), Inline Math ($...$) e Prosa
    pattern = r'(?<!\\)(\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\$(?:[^\$\n]|\\\$)+?(?<!\\)\$)'
    parts = re.split(pattern, processed, flags=re.DOTALL)
    
    result_parts = []
    for part in parts:
        if not part:
            continue
            
        if part.startswith('$$') and part.endswith('$$') and len(part) >= 4:
            inner = part[2:-2]
            sanitized_inner = sanitize_display_math(inner)
            result_parts.append(f"\n$$\n{sanitized_inner}\n$$\n")
        elif part.startswith('$') and part.endswith('$') and len(part) >= 2 and '\n' not in part:
            inner = part[1:-1]
            sanitized_inner = sanitize_inline_math(inner)
            result_parts.append(f"${sanitized_inner}$")
        else:
            # Prosa comum (fora de cifrões)
            prose = part
            # Auto-wrap para binom solto na prosa (\binom{n}{k} -> $\binom{n}{k}$)
            prose = re.sub(r'(?<!\$)(?<!\\)(\\(?:d?binom|tbinom)\{[^}]+\}\{[^}]+\})(?!\$)', r' $\1$ ', prose)
            
            # Símbolos gregos e matemáticos isolados soltos na prosa
            symbols_to_wrap = r'\\(?:mu|sigma|alpha|beta|theta|lambda|pi|gamma|delta|epsilon|varepsilon|phi|omega|rho|tau|eta|chi|psi|zeta|Omega|Sigma|Delta|Theta|Gamma|Phi|Psi|Lambda|forall|exists|rightarrow|Rightarrow|infty|partial|mathcal\{[A-Za-z]\})'
            prose = re.sub(r'(?<!\$)(?<!\\)(' + symbols_to_wrap + r')(?!\$)', r' $\1$ ', prose)
            result_parts.append(prose)

    processed = "".join(result_parts)

    # 4. Anexa pontuações isoladas
    processed = re.sub(r'(\$\$[\s\S]*?\$\$)\s*\n+\s*([.,;:!?])', r'\1\2\n\n', processed)
    processed = re.sub(r'\n+\s*([.,;:!?])\s+(?=[A-Za-z0-9Á-ÿ])', r'\1 ', processed)
    processed = re.sub(r'\n+\s*([.,;:!?])\s*\n+', r'\1\n\n', processed)
    processed = re.sub(r'\.{2,}', '.', processed)

    # 5. Ajusta o espaçamento ao redor de inline math colado em palavras em português
    processed = re.sub(r'([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])\$([^$\n]+?)\$', r'\1 $\2$', processed)
    processed = re.sub(r'\$([^$\n]+?)\$([a-zA-Z0-9áàâãéèêíóòôõúçÁÀÂÃÉÈÊÍÓÒÔÕÚÇ])', r'$\1$ \2', processed)

    # 6. Remove espaços em branco no início de cada linha
    lines = processed.split('\n')
    processed_lines = [line.lstrip(' \t') for line in lines]
    processed = '\n'.join(processed_lines)

    # 7. Remove excesso de quebras de linha múltiplas mantendo no máximo parágrafo duplo (\n\n)
    processed = re.sub(r'\n{3,}', '\n\n', processed)

    # 8. Restaura símbolos monetários
    processed = processed.replace('R__DOLLAR__', r'R\$')
    processed = processed.replace('US__DOLLAR__', r'US\$')

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
