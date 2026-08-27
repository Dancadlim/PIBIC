import os
import json
import glob
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, r"c:\Users\lucab\Documents\pibic\backend")
import latex_sanitizer

files = glob.glob("data_local/classrooms/*/aulas/*.json") + glob.glob("data_local/aulas_geradas/*.json")
if not files:
    files = glob.glob("backend/data_local/classrooms/*/aulas/*.json") + glob.glob("backend/data_local/aulas_geradas/*.json")

cleaned = 0
for fpath in files:
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        sanitized = latex_sanitizer.sanitize_json_recursively(data)
        
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(sanitized, f, ensure_ascii=False, indent=2)
        cleaned += 1
    except Exception as e:
        print(f"Erro em {fpath}: {e}")

print(f"✅ {cleaned} arquivos de aula armazenados em disco foram limpos e sanitizados deterministicamente!")
