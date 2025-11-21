import os
import zipfile
import shutil
import subprocess
import sys

ZIP_NAME = "testes.zip"

PASTA_DESTINO = r"C:\Bellatrix"

PASTAS_PROTEGIDAS = {"configs"} # <- Adicionar futuramente pasta de logs
ARQUIVOS_PROTEGIDOS = {} # <- Adicionar futuramente banco de dados.


def garantir_pasta_destino():
    if not os.path.exists(PASTA_DESTINO):
        os.makedirs(PASTA_DESTINO)
        print(f"📁 Pasta criada: {PASTA_DESTINO}")
    else:
        print(f"📁 Pasta já existe: {PASTA_DESTINO}")

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
    print("🔄 Movendo arquivos atualizados para C:\\Bellatrix ...")

    origem = "update_temp"

    for root, dirs, files in os.walk(origem):
        relative_path = os.path.relpath(root, origem)

        # Ignorar pastas protegidas
        if relative_path.split(os.sep)[0] in PASTAS_PROTEGIDAS:
            continue

        destino = os.path.join(PASTA_DESTINO, relative_path)

        if not os.path.exists(destino):
            os.makedirs(destino, exist_ok=True)

        for file in files:

            if file in ARQUIVOS_PROTEGIDOS:
                continue

            caminho_origem = os.path.join(root, file)
            caminho_destino = os.path.join(destino, file)

            # Se já existir, apaga antes de substituir
            if os.path.exists(caminho_destino):
                os.remove(caminho_destino)

            shutil.copy2(caminho_origem, caminho_destino)
            print(f"📁 Atualizado → {caminho_destino}")


def main():
    print("📥 Iniciando atualização com base no ZIP baixado...")

    garantir_pasta_destino()

    if not extrair_zip():
        return

    substituir_arquivos()

    print("\n✅ Atualização concluída com sucesso!")
    print("🚀 Reiniciando a nova versão...")

    # Apaga o zip baixado
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)

    # Reinicia o sistema rodando o main.py agora dentro de C:\Bellatrix
    python_exe = sys.executable
    main_py = os.path.join(PASTA_DESTINO, "main.py")

    if os.path.exists(main_py):
        subprocess.Popen([python_exe, main_py])
    else:
        print("⚠ main.py não encontrado em C:\\Bellatrix")

    os._exit(0)


if __name__ == "__main__":
    main()
