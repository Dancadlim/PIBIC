import os
import json
from google import genai
from google.genai import types
from prompts import PROMPT_MACRO_ROTEIRISTA

class MacroRoteirista:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não configurada no ambiente.")
        
        # Novo cliente do google-genai
        self.client = genai.Client(vertexai=True, api_key=self.api_key)
        
        self.system_instruction = PROMPT_MACRO_ROTEIRISTA

    def gerar_cronograma(self, ementa_texto: str, instrucoes_personalizadas: str = None, total_aulas: int = 30) -> list:
        prompt = f"""
Por favor, analise a ementa abaixo e crie um cronograma balanceado para {total_aulas} encontros letivos.

Ementa Oficial:
\"\"\"{ementa_texto}\"\"\"

Instruções Personalizadas do Professor (Caso existam, priorize estas instruções na alocação de tempo e foco. Senão, ignore):
\"\"\"{instrucoes_personalizadas or 'Nenhuma.'}\"\"\"

Responda apenas com o Array JSON.
"""
        print(f"[MacroRoteirista] Pensando e fatiando a ementa em {total_aulas} aulas...")
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    response_mime_type="application/json",
                    temperature=0.4
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[Erro no MacroRoteirista JSON] {e}")
            return []
