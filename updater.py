import requests
from packaging.version import parse as parse_version
from version import version
import subprocess, sys

VERSION_JSON_URL = "https://raw.githubusercontent.com/intertv-tecnologia/software-versions/refs/heads/main/bellatrix/version.json" # URL do JSON com a versão mais recente


# Verifica se há uma atualização disponível
def verificar_atualizacao():
    try:
        resposta = requests.get(VERSION_JSON_URL, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()

        versao_remota = dados.get("version")
        mensagem = dados.get("message", "")

        
        if not versao_remota:
            return (False, None, "JSON remoto inválido (sem campo 'latest').")

        if parse_version(versao_remota) != parse_version(version):
            subprocess.run([sys.executable, "baixar_zip.py"])
            subprocess.run([sys.executable, "auto_update.py"])

            return (False, versao_remota, f"Nova versão disponível!\n{mensagem}")

        else:
            return (True, versao_remota, f"Bellatrix está atualizada (versão {version}).")

    except Exception as e:
        return (False, None, f"Erro ao verificar atualização: {e}")
