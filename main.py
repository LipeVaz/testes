import tkinter as tk
from tkinter import messagebox
from version import version
from updater import verificar_atualizacao

def checar():
    btn_verificar.config(state="disabled")
    status_label.config(text="Verificando...", fg="blue")
    root.update()

    atualizado, versao_remota, mensagem = verificar_atualizacao()

    status_label.config(text="Pronto.", fg="black")
    btn_verificar.config(state="normal")

    if atualizado:
        messagebox.showinfo("Atualização", mensagem)
    else:
        if versao_remota:
            messagebox.showwarning("Atualização disponível", mensagem)
        else:
            messagebox.showerror("Erro", mensagem)

root = tk.Tk()
root.title("Bellatrix Teste - Atualizador")
root.geometry("350x200")

lbl_versao = tk.Label(root, text=f"Versão atual: {version}", font=("Arial", 12))
lbl_versao.pack(pady=10)

btn_verificar = tk.Button(root, text="Verificar Atualização", command=checar, font=("Arial", 10))
btn_verificar.pack(pady=10)

status_label = tk.Label(root, text="Status: Aguardando ação...", font=("Arial", 10))
status_label.pack(pady=10)

root.mainloop()
