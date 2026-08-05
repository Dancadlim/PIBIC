import os
import firebase_admin
from firebase_admin import credentials, firestore

# Configuração do Firebase
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
if not os.path.exists(cred_path):
    print("Erro: serviceAccountKey.json não encontrado.")
    exit(1)

cred = credentials.Certificate(cred_path)
try:
    # Se já foi inicializado (caso estejamos importando algo), não inicializa de novo
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Dados da disciplina Estatística
ementa_estatistica = """
EMENTA MATB59 - ESTATÍSTICA BÁSICA

1. Introdução à Estatística: População e amostra. Variáveis quantitativas e qualitativas.
2. Estatística Descritiva: Distribuição de frequência. Medidas de tendência central (Média, Mediana, Moda). Medidas de dispersão (Variância, Desvio Padrão, Coeficiente de Variação).
3. Probabilidade: Espaço amostral e eventos. Operações com eventos. Definição clássica e frequencial de probabilidade. Probabilidade condicional e Teorema de Bayes.
4. Variáveis Aleatórias Discretas: Função de probabilidade. Esperança e variância. Modelos: Bernoulli, Binomial, Poisson.
5. Variáveis Aleatórias Contínuas: Função densidade de probabilidade. Esperança e variância. Modelo Normal.
6. Inferência Estatística: Estimação pontual e por intervalo. Intervalos de confiança para a média e proporção.
7. Testes de Hipóteses: Conceitos básicos (erros do tipo I e II, nível de significância). Testes para a média e para a proporção populacional.
8. Correlação e Regressão Linear Simples: Diagrama de dispersão. Coeficiente de correlação de Pearson. Ajuste da reta de regressão (Método dos Mínimos Quadrados).
"""

disciplina = {
    "id_disciplina": "MATB59",
    "nome": "Estatística Básica",
    "departamento": "Estatística",
    "ementa_texto": ementa_estatistica.strip(),
    "referencias_basicas": [
        "Bussab, W. O., & Morettin, P. A. (2010). Estatística Básica (6ª ed.). Saraiva.",
        "Morettin, P. A., & Singer, J. M. (2022). Estatística e Ciência de Dados. LTC."
    ]
}

# Inserindo no Firestore
doc_ref = db.collection("disciplinas").document(disciplina["id_disciplina"])
doc_ref.set(disciplina)

print(f"Disciplina {disciplina['id_disciplina']} inserida com sucesso no Firestore!")
