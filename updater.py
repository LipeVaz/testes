import requests
from packaging.version import parse as parse_version
from version import version
import subprocess, sys

# URL pública do seu JSON (repositório público criado no GitHub)
VERSION_JSON_URL = "https://raw.githubusercontent.com/LipeVaz/versaoteste/refs/heads/main/version2.json"

def verificar_atualizacao():
    """
    Verifica a versão atual comparando com o JSON remoto.
    Retorna uma tupla: (atualizado, versao_remota, mensagem)
    """
    try:
        resposta = requests.get(VERSION_JSON_URL, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()

        versao_remota = dados.get("latest")
        mensagem = dados.get("message", "")
        
        if not versao_remota:
            return (False, None, "JSON remoto inválido (sem campo 'latest').")
        
        # Comparar versões usando 'packaging' (mais seguro)
        if parse_version(versao_remota) != parse_version(version):
            subprocess.run([sys.executable, "baixar_zip.py"])
            return (False, versao_remota, f"Nova versão disponível!\n{mensagem}. Iniciando atualização...")
            
        else:
            return (True, versao_remota, f"Bellatrix está atualizada (versão {version}).")

    except Exception as e:
        return (False, None, f"Erro ao verificar atualização: {e}")
