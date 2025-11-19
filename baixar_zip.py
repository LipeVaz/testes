import requests

DOWNLOAD_URL = "http://192.100.0.151:9000/download/latest/"   # ← IP para download do ZIP

def baixar_zip():
    print("📥 Baixando ZIP da atualização...")

    resposta = requests.get(DOWNLOAD_URL, stream=True, timeout=20)
    resposta.raise_for_status()

    with open("testes.zip", "wb") as f:
        for chunk in resposta.iter_content(chunk_size=8192):
            f.write(chunk)

    print("✅ Download concluído! Iniciando atualização automática...")


if __name__ == "__main__":
    baixar_zip()
