import os
import base64
import requests
import re

def extrair_repo_git_local():
    """Tenta ler a URL do remote origin no arquivo .git/config e extrair o path 'dono/repo'."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_config = os.path.join(base_dir, ".git", "config")
        
        if not os.path.exists(caminho_config):
            caminho_config = os.path.join(os.getcwd(), ".git", "config")
            
        if os.path.exists(caminho_config):
            with open(caminho_config, "r", encoding="utf-8") as f:
                conteudo = f.read()
            # Regex para casar com URLs HTTPS ou SSH do GitHub
            match = re.search(r'url\s*=\s*(?:https://github\.com/|git@github\.com:)([^/\s]+/[^/\s\.]+?)(?:\.git)?\s*$', conteudo, re.MULTILINE | re.IGNORECASE)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"[GITHUB] Erro ao tentar extrair repositório local do .git/config: {e}")
    return None

def salvar_credencial_github(token: str, repo: str, branch: str = "main"):
    """Salva as credenciais do GitHub no arquivo .streamlit/secrets.toml local do projeto."""
    try:
        diretorio_streamlit = os.path.join(os.getcwd(), ".streamlit")
        os.makedirs(diretorio_streamlit, exist_ok=True)
        caminho_secrets = os.path.join(diretorio_streamlit, "secrets.toml")
        
        secrets_atuais = {}
        if os.path.exists(caminho_secrets):
            with open(caminho_secrets, "r", encoding="utf-8") as f:
                for linha in f:
                    linha_limpa = linha.strip()
                    if linha_limpa and "=" in linha_limpa and not linha_limpa.startswith("#"):
                        parts = linha_limpa.split("=", 1)
                        k = parts[0].strip()
                        v = parts[1].strip().strip('"').strip("'")
                        secrets_atuais[k] = v
        
        # Atualiza segredos
        if token:
            secrets_atuais["GITHUB_PAT"] = token
        if repo:
            secrets_atuais["GITHUB_REPO"] = repo
        if branch:
            secrets_atuais["GITHUB_BRANCH"] = branch
            
        # Grava de volta
        with open(caminho_secrets, "w", encoding="utf-8") as f:
            for k, v in secrets_atuais.items():
                f.write(f'{k} = "{v}"\n')
        return True
    except Exception as e:
        print(f"[GITHUB] Erro ao salvar credenciais em secrets.toml: {e}")
        return False

def obter_credencial_github():
    """Recupera as credenciais do GitHub a partir do ambiente, do st.secrets (incluindo seção [Git]) ou do st.session_state."""
    token = os.environ.get("GITHUB_PAT") or os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    branch = os.environ.get("GITHUB_BRANCH", "main")
    
    try:
        import streamlit as st
        # 1. Tenta carregar do st.session_state
        if not token and "GITHUB_PAT" in st.session_state:
            token = st.session_state["GITHUB_PAT"]
        if not repo and "GITHUB_REPO" in st.session_state:
            repo = st.session_state["GITHUB_REPO"]
        if branch == "main" and "GITHUB_BRANCH" in st.session_state:
            branch = st.session_state["GITHUB_BRANCH"]
            
        # 2. Tenta carregar do st.secrets raiz
        if not token and "GITHUB_PAT" in st.secrets:
            token = st.secrets["GITHUB_PAT"]
        if not token and "GITHUB_TOKEN" in st.secrets:
            token = st.secrets["GITHUB_TOKEN"]
        if not repo and "GITHUB_REPO" in st.secrets:
            repo = st.secrets["GITHUB_REPO"]
        if branch == "main" and "GITHUB_BRANCH" in st.secrets:
            branch = st.secrets["GITHUB_BRANCH"]

        # 3. Tenta carregar de dentro da seção [Git] do st.secrets (conforme configurado no Streamlit Cloud)
        if "Git" in st.secrets:
            git_sec = st.secrets["Git"]
            if not token and "GITHUB_PAT" in git_sec:
                token = git_sec["GITHUB_PAT"]
            if not token and "GITHUB_TOKEN" in git_sec:
                token = git_sec["GITHUB_TOKEN"]
            if not repo and "GITHUB_REPO" in git_sec:
                repo = git_sec["GITHUB_REPO"]
            if branch == "main" and "GITHUB_BRANCH" in git_sec:
                branch = git_sec["GITHUB_BRANCH"]
    except Exception:
        pass
        
    # 4. Se repositório ainda não foi definido, tenta autodetectar a partir do .git/config local
    if not repo:
        repo = extrair_repo_git_local()
        
    return token, repo, branch

def commitar_arquivo_github(caminho_local: str, caminho_repositorio: str, mensagem_commit: str):
    """
    Envia um arquivo local diretamente para o repositório do GitHub do usuário via API REST.
    """
    token, repo, branch = obter_credencial_github()
    
    if not token or not repo:
        print("[GITHUB] Integração com GitHub pulada: GITHUB_PAT ou GITHUB_REPO não configurados.")
        return False
        
    # Garante formatação correta do caminho
    caminho_repositorio = caminho_repositorio.replace("\\", "/")
    
    try:
        if not os.path.exists(caminho_local):
            print(f"[GITHUB] Arquivo local não encontrado: {caminho_local}")
            return False
            
        with open(caminho_local, "rb") as f:
            conteudo_binario = f.read()
            
        conteudo_base64 = base64.b64encode(conteudo_binario).decode("utf-8")
        
        # URL da API do GitHub para criar/atualizar conteúdo
        url = f"https://api.github.com/repos/{repo}/contents/{caminho_repositorio}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        # 1. Verifica se o arquivo já existe para obter o SHA
        sha = None
        params = {"ref": branch}
        res_get = requests.get(url, headers=headers, params=params)
        if res_get.status_code == 200:
            sha = res_get.json().get("sha")
            
        # 2. Prepara o payload
        payload = {
            "message": mensagem_commit,
            "content": conteudo_base64,
            "branch": branch
        }
        if sha:
            payload["sha"] = sha
            
        # 3. Executa a escrita
        res_put = requests.put(url, headers=headers, json=payload)
        
        if res_put.status_code in [200, 201]:
            print(f"[GITHUB] Sucesso ao commitar '{caminho_repositorio}' no GitHub!")
            return True
        else:
            print(f"[GITHUB] Erro ao commitar (HTTP {res_put.status_code}): {res_put.text}")
            return False
            
    except Exception as e:
        print(f"[GITHUB] Falha operacional ao tentar commitar: {e}")
        return False
