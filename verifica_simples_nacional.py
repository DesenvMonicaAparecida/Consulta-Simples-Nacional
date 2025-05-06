import tkinter as tk
import tkinter.ttk as ttk
import requests
import re

def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj in (cnpj[0] * 14 for _ in range(10)):
        return False

    def calc_dv(digits, weights):
        soma = sum(int(d) * w for d, w in zip(digits, weights))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    dv1 = calc_dv(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    dv2 = calc_dv(cnpj[:12] + dv1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    return cnpj[-2:] == dv1 + dv2

def check_simples_nacional(cnpj):
    url = f"https://open.cnpja.com/office/{cnpj}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('company', {}).get('simples', {}).get('optant'):
                return "Optante pelo Simples Nacional"
            else:
                return "Não optante pelo Simples Nacional"
        else:
            return f"Erro ao consultar o CNPJ: Código {response.status_code}"
    except requests.RequestException as e:
        return f"Erro de conexão: {str(e)}"
    except ValueError:
        return "Erro ao processar a resposta da API"

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Verificador de Simples Nacional")

    # Aumentando o tamanho da janela
    root.geometry("600x400")  # Largura e altura ajustadas (dobro)


    style = ttk.Style()
    style.configure('TFrame', background='#295C77')  # Azul escuro
    style.configure('TLabel', background='#063970', foreground='white', font=("Arial", 14))
    style.configure('Title.TLabel', background='#063970', foreground='white', font=("Arial", 18))
    style.configure('TEntry', fieldbackground='#e8da65', foreground='black', font=("Arial", 14))  # CNPJ com fundo bege
    style.configure('TButton', background='#87cefa', foreground='black', font=("Arial", 14))  # Botão azul céu com texto preto

    main_frame = ttk.Frame(root, style='TFrame')
    main_frame.pack(fill='both', expand=True)

    title_label = ttk.Label(main_frame, text="Verificador de Simples Nacional", style='Title.TLabel')
    title_label.pack(pady=20)

    cnpj_label = ttk.Label(main_frame, text="Insira o número do CNPJ:", style='TLabel')
    cnpj_label.pack(pady=10)

    entry = ttk.Entry(main_frame, style='TEntry', width=20)
    entry.pack(pady=10)
    entry.focus()

    result_label = ttk.Label(main_frame, text="", style='TLabel')
    result_label.pack(pady=10)

    def verificar():
        cnpj = entry.get()
        if not validar_cnpj(cnpj):
            result_label.config(text="CNPJ inválido.")
        else:
            cnpj_digits = ''.join(filter(str.isdigit, cnpj))
            result = check_simples_nacional(cnpj_digits)
            result_label.config(text=result)

    button = ttk.Button(main_frame, text="Verificar", command=verificar, style='TButton')
    button.pack(pady=10)

    root.mainloop()
