import os
import PyPDF2
import firebase_admin
from firebase_admin import credentials, firestore

# Configuração do Firebase
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
if not os.path.exists(cred_path):
    print("Erro: serviceAccountKey.json não encontrado.")
    exit(1)

cred = credentials.Certificate(cred_path)
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

db = firestore.client()

disciplinas_dict = {
    "MAT186": {"nome": "Elementos de Processos Estocásticos", "arquivo": "mat186_elementos_de_processos_estocasticos.pdf"},
    "MAT223": {"nome": "Probabilidade I", "arquivo": "mat223_probabilidade_i.pdf"},
    "MAT224": {"nome": "Probabilidade II", "arquivo": "mat224_probabilidade_ii.pdf"},
    "MAT229": {"nome": "Análise de Regressão", "arquivo": "mat229_analise_de_regressao.pdf"},
    "MATB59": {"nome": "Estatística Básica A", "arquivo": "matb59_estatistica_basica_a.pdf"},
    "MATD38": {"nome": "Estatística Básica B", "arquivo": "matd38_-_estatistica_basica_b.pdf"},
    "MATD39": {"nome": "Análise Descritiva e Exploratória de Dados A", "arquivo": "matd39_analise_descritiva_e_exploratoria_de_dados_a.pdf"},
    "MATD40": {"nome": "Análise de Dados", "arquivo": "matd40_-_analise_de_dados.pdf"},
    "MATD41": {"nome": "Introdução aos Modelos Lineares", "arquivo": "matd41_introducao_aos_modelos_lineares.pdf"},
    "MATD42": {"nome": "Inferência A", "arquivo": "matd42_inferencia_a.pdf"},
    "MATD43": {"nome": "Inferência B", "arquivo": "matd43_inferencia_b.pdf"},
    "MATD44": {"nome": "Amostragem A", "arquivo": "matd44_amostragem_a.pdf"},
    "MATD45": {"nome": "Sistema de Informações e a Profissão do Estatístico", "arquivo": "matd45_-_sistema_de_informacoes_e_a_profissao_do_estatistico.pdf"},
    "MATD46": {"nome": "Estatística Computacional A", "arquivo": "matd46_estatistica_computacional_a.pdf"},
    "MATD47": {"nome": "Métodos Multivariados A", "arquivo": "matd47_metodos_multivariados_a.pdf"},
    "MATD48": {"nome": "Planejamento de Experimentos I", "arquivo": "matd48_planejamento_de_experimentos_i.pdf"},
    "MATD49": {"nome": "Estatística Não Paramétrica", "arquivo": "matd49_estatistica_nao_parametrica.pdf"},
    "MATD50": {"nome": "Modelos Lineares Generalizados A", "arquivo": "matd50_modelos_lineares_generalizados_a.pdf"},
    "MATD51": {"nome": "Análise de Séries Temporais A", "arquivo": "matd51_analise_de_series_temporais_a.pdf"},
}

ementas_dir = os.path.join(os.path.dirname(__file__), "ementas")
total_inseridos = 0

for cod, info in disciplinas_dict.items():
    pdf_path = os.path.join(ementas_dir, info["arquivo"])
    
    if not os.path.exists(pdf_path):
        print(f"[{cod}] Aviso: Arquivo {info['arquivo']} não encontrado. Pulando...")
        continue
    
    print(f"[{cod}] Lendo {info['arquivo']}...")
    texto_extraido = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texto_extraido += text + "\n"
    except Exception as e:
        print(f"Erro ao ler PDF {info['arquivo']}: {e}")
        continue
    
    # Criar objeto para o banco de dados
    disciplina_data = {
        "id_disciplina": cod,
        "nome": info["nome"],
        "departamento": "Departamento de Estatística",
        "ementa_texto": texto_extraido.strip(),
    }

    # Inserir no Firestore
    doc_ref = db.collection("disciplinas").document(cod)
    doc_ref.set(disciplina_data)
    print(f"[{cod}] Sucesso: {info['nome']} injetado no Firestore.")
    total_inseridos += 1

print(f"\nFinalizado! {total_inseridos} ementas de Estatística foram injetadas no banco de dados com sucesso.")
