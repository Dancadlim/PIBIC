import os
import sys
import time
import unicodedata
from google import genai
from google.genai import types

def print_safe(*args, **kwargs):
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    file = kwargs.get('file', sys.stdout)
    text = sep.join(str(arg) for arg in args) + end
    encoding = getattr(file, 'encoding', 'utf-8') or 'utf-8'
    try:
        file.write(text)
    except UnicodeEncodeError:
        safe_text = text.encode(encoding, errors='replace').decode(encoding)
        file.write(safe_text)
    file.flush()

print = print_safe

def remover_acentos(texto):
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def inicializar_e_indexar(nome_professor: str, codigo_disciplina: str, pasta_livros: str):
    client = genai.Client()
    
    # Gerando o nome da Store (usa plataforma-estatistica-db se for 'global', caso contrário cria Store específica)
    if nome_professor.lower().strip() == "global":
        NOME_STORE = "plataforma-estatistica-db"
    else:
        NOME_STORE = f"store-{nome_professor.lower().strip()}-{codigo_disciplina.lower().strip()}"
    print(f"📦 Inicializando verificação para a Store: {NOME_STORE}")
    
    store_alvo = None
    try:
        for store in client.file_search_stores.list():
            if store.display_name == NOME_STORE:
                store_alvo = store
                print(f"✅ Store encontrada no servidor do Google: {store_alvo.name}")
                break
    except Exception as e:
        raise RuntimeError(f"Erro ao listar stores: {e}")
        
    if not store_alvo:
        print(f"⚠️ Store não existente. Criando nova store corporativa...")
        store_alvo = client.file_search_stores.create(
            config={
                'display_name': NOME_STORE
            }
        )
        print(f"🎉 Store criada com sucesso: {store_alvo.name}")

    if not os.path.exists(pasta_livros):
        print(f"Erro: A pasta local '{pasta_livros}' não existe.")
        return

    arquivos_locais = [f for f in os.listdir(pasta_livros) if f.endswith(".pdf")]
    if not arquivos_locais:
        print(f"ℹ️ Nenhum arquivo PDF novo para indexar na pasta '{pasta_livros}'.")
        return

    for arquivo in arquivos_locais:
        caminho_completo = os.path.join(pasta_livros, arquivo)
        print(f"\n🚀 Enviando '{arquivo}' para processamento vetorial (RAG)...")
        
        # Remove acentos do nome do arquivo para evitar problemas de codificação no Windows
        arquivo_seguro = remover_acentos(arquivo)
        caminho_seguro = os.path.join(pasta_livros, arquivo_seguro)
        if caminho_completo != caminho_seguro:
            os.rename(caminho_completo, caminho_seguro)
        
        try:
            # 1. Faz o upload temporário do arquivo usando Files API
            file_obj = client.files.upload(file=caminho_seguro)
            
            # 2. Importa o arquivo para a Store do RAG com os metadados customizados de disciplina
            operation = client.file_search_stores.import_file(
                file_search_store_name=store_alvo.name,
                file_name=file_obj.name,
                config={
                    'customMetadata': [
                        {'key': 'discipline', 'stringValue': codigo_disciplina.upper().strip()}
                    ]
                }
            )
            print(f"📤 Upload concluído. Operação iniciada: {operation.name}")
            
            # LOOP DE POLLING: Bloqueia o terminal local até o status da operação ser concluída no Google
            print("⏳ Aguardando indexação e geração de embeddings no servidor do Google RAG...")
            while not operation.done:
                time.sleep(5)
                # Requisita o status atualizado da operação
                operation = client.operations.get(operation)
                print("   Processando e gerando embeddings...")
                
            print(f"💪 Sucesso! '{arquivo}' está 100% pronto e indexado na store para buscas estatísticas.")
                
        except Exception as e:
            print(f"❌ Falha operacional ao processar arquivo {arquivo}: {e}")
