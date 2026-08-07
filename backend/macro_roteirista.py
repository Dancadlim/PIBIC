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

    def gerar_cronograma(self, ementa_texto: str, instrucoes_personalizadas: str = None, tipo_carga_horaria: str = "padrao_30", permitir_aprofundamento: bool = False, max_aulas: int = 30) -> list:
        
        instrucao_carga = ""
        if tipo_carga_horaria == "padrao_30":
            instrucao_carga = f"O curso DEVE TER EXATAMENTE {max_aulas} aulas no total. Não gere mais nem menos aulas. Aloque toda a ementa de forma balanceada nesse espaço."
        elif tipo_carga_horaria == "auto_ementa":
            instrucao_carga = "O curso deve ter a quantidade de aulas calculada matematicamente a partir da ementa oficial. Leia a ementa, ache a Carga Horária. Se a carga horária for quebrada ou antiga (ex: 72h, 54h), ARREDONDE para a grade universitária oficial mais próxima (30, 45, 60 ou 90 horas). Depois, divida essa carga oficial por ~2.5 horas (150 minutos) para obter a quantidade total de aulas da matéria. Use EXATAMENTE essa quantidade de aulas para estruturar o cronograma."
            
        instrucao_aprofundamento = ""
        if permitir_aprofundamento:
            instrucao_aprofundamento = "VOCÊ TEM PERMISSÃO PARA APROFUNDAR: Você pode criar até 5 aulas ADICIONAIS no final do cronograma contendo temas da fronteira do conhecimento que façam muito sentido com a matéria, mesmo que não estejam na ementa. Marque o campo 'aula_complementar': true em todas elas."
        else:
            instrucao_aprofundamento = "É ESTRITAMENTE PROIBIDO adicionar conteúdos ou aulas sobre tópicos que não constam na ementa. O campo 'aula_complementar' deve ser sempre false."

        prompt = f"""
Por favor, analise a ementa abaixo e crie um cronograma balanceado.

Ementa Oficial:
\"\"\"{ementa_texto}\"\"\"

Instruções Personalizadas do Professor:
\"\"\"{instrucoes_personalizadas or 'Nenhuma.'}\"\"\"

DIRETRIZ DE CARGA HORÁRIA (MANDATÓRIO):
{instrucao_carga}

DIRETRIZ DE APROFUNDAMENTO (MANDATÓRIO):
{instrucao_aprofundamento}

Responda apenas com o Array JSON.
"""
        print(f"[MacroRoteirista] Pensando e fatiando a ementa. (Carga={tipo_carga_horaria}, Aprofundamento={permitir_aprofundamento})...")
        
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
