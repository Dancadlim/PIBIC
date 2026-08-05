import os
import sys
from dotenv import load_dotenv
import json
import orquestrador_editorial

load_dotenv()

with open('aula_1.json', encoding='utf-8') as f:
    data = json.load(f)

payload_bruto = {
    'tema': 'Teste',
    'conteudo_paginas': data['conteudo_json']['conteudo_paginas']
}

print('Calling lapidar_conteudo_global...', flush=True)
try:
    res = orquestrador_editorial.lapidar_conteudo_global(payload_bruto)
    if "paginas_conteudo" in res:
        print('SUCCESS!')
    else:
        print('FAILED! IT RETURNED PAYLOAD BRUTO INSTEAD OF LAPIDADO!')
except Exception as e:
    print('ERROR:', str(e))
