import os
import zipfile
import shutil
import subprocess
import sys

ZIP_NAME = "testes.zip"

PASTAS_PROTEGIDAS = {"venv", "__pycache__", "update_temp"}
ARQUIVOS_PROTEGIDOS = {"auto_update.py", "baixar_zip.py"}

def extrair_zip():
    print("📦 Extraindo ZIP...")

    if not os.path.exists(ZIP_NAME):
        print(f"❌ Arquivo {ZIP_NAME} não encontrado! Execute baixar_zip.py primeiro.")
        return False

    if os.path.exists("update_temp"):
        shutil.rmtree("update_temp")

    os.mkdir("update_temp")

    with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
        zip_ref.extractall("update_temp")

    return True


def substituir_arquivos():
    print("🔄 Atualizando arquivos...")

    origem = "update_temp"

    for root, dirs, files in os.walk(origem):
        relative_path = os.path.relpath(root, origem)

        if relative_path.split(os.sep)[0] in PASTAS_PROTEGIDAS:
            continue

        destino = os.path.join(os.getcwd(), relative_path)

        if not os.path.exists(destino):
            os.makedirs(destino, exist_ok=True)

        for file in files:

            if file in ARQUIVOS_PROTEGIDOS:
                continue

            caminho_origem = os.path.join(root, file)
            caminho_destino = os.path.join(destino, file)

            shutil.copy2(caminho_origem, caminho_destino)
            print(f"📁 Atualizado → {caminho_destino}")


def main():
    print("📥 Iniciando atualização com base no ZIP baixado...")

    if not extrair_zip():
        return

    substituir_arquivos()

    print("\n✅ Atualização concluída com sucesso!")
    print("🚀 Reiniciando a nova versão...")

    # Apaga o zip baixado (opcional)
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)

    # Executa novamente o main.py atualizado
    python_exe = sys.executable
    subprocess.Popen([python_exe, "main.py"])

    # Fecha o processo atual
    os._exit(0)


if __name__ == "__main__":
    main()
