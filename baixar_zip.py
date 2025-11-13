import os
import requests

# ======================================================
# 🔧 CONFIGURAÇÕES INICIAIS
# ======================================================

# Seu usuário e repositório privado no GitHub
usuario = "LipeVaz"
repositorio = "versaoteste_privado"

# Lê o token de acesso do ambiente (precisa ter permissões de "repo" e "read:packages")
# Você pode definir antes de rodar:
# PowerShell → $env:GITHUB_TOKEN = "seu_token_aqui"
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise EnvironmentError("❌ Variável de ambiente GITHUB_TOKEN não encontrada!")

# ======================================================
# 📦 BUSCA A ÚLTIMA RELEASE
# ======================================================

url_release = f"https://api.github.com/repos/{usuario}/{repositorio}/releases/latest"

# Faz a requisição autenticada pedindo o JSON completo da release
resposta = requests.get(
    url_release,
    headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"  # <-- ESSENCIAL para receber os 'assets'
    },
    timeout=15
)

# Verifica o código de status HTTP
if resposta.status_code != 200:
    print(f"❌ Erro ao acessar a API do GitHub ({resposta.status_code})")
    print(resposta.text)
    exit()

# Converte a resposta para dicionário Python
dados = resposta.json()

# ======================================================
# 📁 OBTÉM O LINK DO PRIMEIRO ASSET (ZIP)
# ======================================================

assets = dados.get("assets", [])
if not assets:
    print("❌ Nenhum asset encontrado na release.")
    exit()

# Normalmente só há um arquivo (o ZIP da release)
link_download = assets[0]["url"]  # URL interna (API)
nome_arquivo = assets[0]["name"]

# ======================================================
# ⬇️ FAZ O DOWNLOAD AUTENTICADO DO ASSET
# ======================================================

res = requests.get(
    link_download,
    headers={
        "Authorization": f"token {token}",
        "Accept": "application/octet-stream"  # Dizemos que queremos o ARQUIVO, não o JSON
    },
    timeout=60
)

if res.status_code != 200:
    print(f"❌ Falha ao baixar o asset ({res.status_code})")
    print(res.text)
    exit()

# ======================================================
# 💾 SALVA O ARQUIVO LOCALMENTE
# ======================================================

with open(nome_arquivo, "wb") as f:
    f.write(res.content)

print(f"✅ Download concluído! Arquivo salvo como {nome_arquivo}")
