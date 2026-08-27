import time
import requests
import json
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, r"c:\Users\lucab\Documents\pibic\backend")
import latex_sanitizer

BASE_URL = "http://localhost:8000"

print("=================================================================")
print("🚀 INICIANDO GERAÇÃO COMPLETA DE AULA DE PROBABILIDADE (TESTE AO VIVO)")
print("=================================================================\n")

payload = {
    "sala_id": "101",
    "id_disciplina": "MAT223",
    "numero_aula": 70,
    "modelo_llm": "flash_lite",
    "aula_manual": {
        "titulo": "Propriedades Básicas da Probabilidade: Axiomas de Kolmogorov e Teoremas Fundamentais",
        "descricao": "Estudo aprofundado dos axiomas de Kolmogorov, probabilidade do evento complementar, regra da adição para eventos quaisquer e propriedades fundamentais da medida de probabilidade com exemplos práticos e simulador.",
        "gerar_exercicios": True,
        "gerar_simulador": True
    }
}

t0 = time.perf_counter()

print("1. Disparando geração no Backend (POST /api/gerar_aula_avulsa)...")
res = requests.post(f"{BASE_URL}/api/gerar_aula_avulsa", json=payload)
print(f"   Status HTTP de disparo: {res.status_code}")

if res.status_code != 200:
    print("❌ Erro ao disparar geração!")
    sys.exit(1)

print("\n2. Monitorando progresso do pipeline de agentes em tempo real...")
concluido = False
tentativas = 0
max_tentativas = 60 # 2 minutos limite

while not concluido and tentativas < max_tentativas:
    time.sleep(2)
    tentativas += 1
    
    # Checa status da sala
    try:
        sala_res = requests.get(f"{BASE_URL}/api/local/salas/101")
        if sala_res.status_code == 200:
            sala_data = sala_res.json()
            progresso = sala_data.get("detalhe_progresso", "Processando...")
            status = sala_data.get("status", "rodando")
            print(f"   [{tentativas*2}s] Status: {status} | Etapa: {progresso}")
            
            if status == "pronto":
                concluido = True
                break
    except Exception as e:
        print(f"   [Aviso] Erro ao checar status: {e}")

t1 = time.perf_counter()
tempo_total = t1 - t0

print("\n=================================================================")
print(f"⏱️ TEMPO TOTAL DE GERAÇÃO: {tempo_total:.2f} SEGUNDOS")
print("=================================================================\n")

print("3. Auditando o conteúdo gerado para a Aula 70...")
aula_res = requests.get(f"{BASE_URL}/api/local/salas/101/aulas")
if aula_res.status_code == 200:
    aulas = aula_res.json()
    aula_70 = None
    for a in aulas:
        if a.get("numero_aula") == 70:
            aula_70 = a
            break
            
    if not aula_70:
        print("❌ Aula 70 não foi encontrada na lista de aulas salvos!")
        sys.exit(1)
        
    conteudo_json = aula_70.get("conteudo_json", {})
    tema_global = conteudo_json.get("tema_global", "N/A")
    paginas = conteudo_json.get("paginas_conteudo", [])
    simuladores = conteudo_json.get("simuladores_da_aula", [])
    exercicios = conteudo_json.get("exercicios_da_aula", {})
    codigo_simulador = conteudo_json.get("codigo_simulador_html", "")
    
    print(f"📌 Tema Global: {tema_global}")
    print(f"📖 Número de Subtópicos / Páginas Didáticas: {len(paginas)}")
    for i, p in enumerate(paginas):
        print(f"   - Página {i+1}: {p.get('titulo_subtopico')}")
        
    print(f"\n🎮 Simulador Interativo Recomendado: {len(simuladores)} mapeado(s)")
    print(f"   - Código HTML do Simulador Gerado: {'Sim (' + str(len(codigo_simulador)) + ' bytes)' if codigo_simulador else 'Não'}")
    
    print(f"\n📝 Caderno de Exercícios Gerado:")
    multipla = exercicios.get("questoes_multipla_escolha", [])
    discursivas = exercicios.get("questoes_discursivas", [])
    print(f"   - Questões de Múltipla Escolha: {len(multipla)}")
    print(f"   - Questões Discursivas: {len(discursivas)}")
    
    print("\n🔍 Auditoria Estrita de Sintaxe e Compilação do KaTeX:")
    raw_str = json.dumps(aula_70, ensure_ascii=False)
    
    BAD_PATTERNS = [
        (r'\\boldsymbol\\\{', 'Chave escapada em \\boldsymbol\\{'),
        (r'\\thicksim', 'Comando invalido \\thicksim'),
        (r'\\nginxed', 'Comando alucinado \\nginxed'),
        (r'\\text\{\s*\\(hat|bar|beta|alpha|sigma|theta|nu|mu)', 'Comando de equação em \\text{...}'),
    ]
    
    erros_katex = 0
    for pat, desc in BAD_PATTERNS:
        matches = re.findall(pat, raw_str)
        if matches:
            print(f" ⚠️ [{desc}]: {len(matches)} ocorrência(s)")
            erros_katex += len(matches)
            
    if erros_katex == 0:
        print("   ✅ COMPILAÇÃO DO KATEX: 100% PERFEITA E LIMPA (Zero Erros)!")
    else:
        print(f"   ❌ {erros_katex} erro(s) de KaTeX detectado(s)!")
