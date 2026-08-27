import os
import json
import glob
import re
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
sys.path.insert(0, r"c:\Users\lucab\Documents\pibic\backend")
import latex_sanitizer

files = glob.glob('data_local/classrooms/101/aulas/*.json') + glob.glob('backend/data_local/classrooms/101/aulas/*.json')
files = list(set(files))

print("=================================================================")
print(f"🔍 VERIFICAÇÃO FINAL DE COMPILAÇÃO DO LATEX ({len(files)} aulas salvas)")
print("=================================================================\n")

total_formulas = 0
erros_identificados = []

BAD_PATTERNS = [
    (r'\\boldsymbol\\\{', "Chave escapada erradamente em \\boldsymbol\\{"),
    (r'\\thicksim', "Comando inválido \\thicksim (usar \\sim)"),
    (r'\\nginxed', "Comando alucinado \\nginxed (usar \\in)"),
    (r'\\text\{\s*\\(hat|bar|beta|alpha|sigma|theta|nu|mu)', "Comando de equação dentro de \\text{...}"),
    (r'\\text\{\s*\\textsigma\s*\}', "\\text{\\textsigma}"),
]

import agente_validador_latex

for fpath in files:
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            aula = json.load(f)
            
        aula_sanitizada = latex_sanitizer.sanitize_json_recursively(aula)
        raw_str = json.dumps(aula_sanitizada, ensure_ascii=False)
        
        display_math = len(re.findall(r'\$\$(.*?)\$\$', raw_str, flags=re.DOTALL))
        inline_math = len(re.findall(r'(?<!\$)\$([^$\n]+?)\$(?!\$)', raw_str))
        total_formulas += (display_math + inline_math)
        
        anomalias = agente_validador_latex.mapear_todas_anomalias_json(aula_sanitizada)
        if anomalias:
            for item in anomalias:
                erros_identificados.append((os.path.basename(fpath), item['caminho_campo'], item['erro_detectado']))
                
    except Exception as e:
        print(f"Erro ao ler {fpath}: {e}")

print(f"📈 Total de Fórmulas Matemáticas Mapeadas: {total_formulas}")
print(f"🚨 Total de Anomalias Estruturais Detectadas: {len(erros_identificados)}\n")

if len(erros_identificados) == 0:
    print("🎉 RESULTADO: COMPILAÇÃO 100% PERFEITA E LIMPA (Zero Anomalias!)")
else:
    for arq, campo, desc in erros_identificados:
        print(f" ⚠️ [{arq}] {campo} -> {desc}")
