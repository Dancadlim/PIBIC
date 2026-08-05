import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
import gerador_conteudo
import orquestrador_editorial
from macro_roteirista import MacroRoteirista

# Inicialização do Firebase Admin
try:
    cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(cred)
            
        db = firestore.client()
        print("[OK] Firebase Admin inicializado com sucesso.")
    else:
        print("[AVISO] serviceAccountKey.json não encontrado. Firebase não foi inicializado.")
        db = None
except Exception as e:
    print(f"[ERRO] Falha ao inicializar o Firebase: {e}")
    db = None

app = FastAPI(title="Plataforma de Aulas UFBA - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SemestreRequest(BaseModel):
    id_sala: str
    id_disciplina: str
    modo: str = "inteligente"
    instrucoes_personalizadas: str = ""
    max_aulas: int = 30 # Padrão: Semestre completo (mas aceita travas para teste)

def processar_semestre_background(req: SemestreRequest):
    print(f"[BACKGROUND] Iniciando orquestração do semestre para a sala: {req.id_sala}")
    try:
        # 1. Recuperar ementa do Firestore
        disc_ref = db.collection("disciplinas").document(req.id_disciplina).get()
        if not disc_ref.exists:
            db.collection("classrooms").document(req.id_sala).update({"status": "erro_disciplina_nao_encontrada"})
            return
        
        ementa_texto = disc_ref.to_dict().get("ementa_texto", "")
        nome_disciplina = disc_ref.to_dict().get("nome", req.id_disciplina)
        
        # 2. Agente Macro Roteirista fatia o semestre
        print("[BACKGROUND] Acionando Macro Roteirista...")
        db.collection("classrooms").document(req.id_sala).update({"status": "fatiando_ementa"})
        
        macro = MacroRoteirista()
        cronograma = macro.gerar_cronograma(ementa_texto, req.instrucoes_personalizadas, total_aulas=30)
        
        if not cronograma:
            db.collection("classrooms").document(req.id_sala).update({"status": "erro_macro_roteirista"})
            return
            
        # Salva o cronograma mestre na sala
        db.collection("classrooms").document(req.id_sala).update({
            "cronograma_oficial": cronograma,
            "status": "gerando_aulas",
            "total_aulas": len(cronograma),
            "aulas_geradas": 0
        })
        
        # 3. Loop: Agentes Micro geram as aulas individualmente
        limite = min(req.max_aulas, len(cronograma))
        print(f"[BACKGROUND] Gerando {limite} aulas na fábrica de conteúdo...")
        
        for idx, aula in enumerate(cronograma[:limite]):
            numero = aula.get("numero_aula", idx + 1)
            titulo = aula.get("titulo", "Aula")
            objetivo = aula.get("objetivo_principal", "")
            topicos = ", ".join(aula.get("topicos_abordados", []))
            
            # Constrói o "Tema Global" para a Fábrica
            tema_montado = f"{titulo}. Objetivo: {objetivo}. Tópicos: {topicos}"
            print(f"  -> Processando Aula {numero}: {titulo}...")
            
            # Pipeline de Redação
            diretrizes = f"Foque nestes tópicos: {topicos}. Adapte a profundidade para atingir este objetivo: {objetivo}. Use notação matemática rigorosa e seja didático."
            conteudo_bruto = gerador_conteudo.gerar_conteudo_aula(
                nome_professor="Professor UFBA",
                codigo_disciplina=req.id_disciplina,
                tema_solicitado=tema_montado,
                ementa_texto=ementa_texto,
                diretrizes_texto=diretrizes
            )
            
            if conteudo_bruto:
                conteudo_final = orquestrador_editorial.lapidar_conteudo_global(conteudo_bruto)
                if conteudo_final:
                    # --- NOVO: GERAR EXERCÍCIOS PARA MÉTRICAS ---
                    import agente_exercicios
                    caderno = agente_exercicios.gerar_caderno_exercicios(conteudo_final)
                    if caderno:
                        conteudo_final["exercicios_da_aula"] = caderno

                    # Salva a aula na subcoleção do Firestore
                    db.collection("classrooms").document(req.id_sala).collection("aulas").document(str(numero)).set({
                        "numero_aula": numero,
                        "titulo": titulo,
                        "conteudo_json": conteudo_final
                    })
                    
                    # Atualiza progresso
                    db.collection("classrooms").document(req.id_sala).update({
                        "aulas_geradas": firestore.Increment(1)
                    })
        
        # 4. Finalização
        db.collection("classrooms").document(req.id_sala).update({"status": "pronto"})
        print(f"[BACKGROUND] Semestre {req.id_sala} concluído com sucesso!")
        
    except Exception as e:
        print(f"[ERRO] Exceção no semestre background: {e}")
        if db:
            db.collection("classrooms").document(req.id_sala).update({"status": f"erro: {str(e)}"})

@app.get("/health")
def health_check():
    return {"status": "ok", "firebase": db is not None}

@app.post("/api/gerar_semestre")
def gerar_semestre(req: SemestreRequest, background_tasks: BackgroundTasks):
    if not db:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")
    
    background_tasks.add_task(processar_semestre_background, req)
    
    return {"message": "Semestre em processamento", "sala": req.id_sala}

class SimuladorRequest(BaseModel):
    tema_aula: str
    nome_simulador: str

@app.post("/api/gerar_simulador")
def api_gerar_simulador(req: SimuladorRequest):
    import agente_simulador
    html = agente_simulador.gerar_simulador_html(req.tema_aula, req.nome_simulador)
    if not html:
        raise HTTPException(status_code=500, detail="Erro ao gerar simulador")
    return {"html_code": html}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
