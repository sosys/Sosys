############################################################################
## Script: main.py                                                        ##
## Data: 09/03/2025                                                       ##
## Autor: Sosys                                                           ##
############################################################################
## Função: Gerar a estrutura de pastas para gerenciamento das querys,     ##
## arquivos de configuração, csv e parquet, além de gerar esses arquivos  ##
## de acordo com as especificações do arquivo configurador.               ##
############################################################################

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from Criar_Cliente import on_new
from Executar_Teste import execute_test_queries
from Gerar_Parquet import execute_queries_to_parquet

def on_execute_test():
    """Chama a função de execução de testes."""
    execute_test_queries()

def on_generate_parquet():
    """Gera arquivos Parquet."""
    execute_queries_to_parquet()

def main():
    """Configura e inicia a interface gráfica."""
    root = tk.Tk()
    root.title("Chope")
    root.geometry("400x300")  # Ajuste do tamanho para acomodar imagem e texto
    
    # Definir o ícone
    icon_path = os.path.join(os.path.dirname(__file__), "chope.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    
    # Definir cor de fundo baseada na imagem Chope.png
    bg_color = "#caad8f"  # Cor extraída da imagem Chope.png
    root.configure(bg=bg_color)
    
    frame = tk.Frame(root, padx=20, pady=20, bg=bg_color)
    frame.pack(expand=True)
    
    # Exibir imagem Chope.png
    img_path = os.path.join(os.path.dirname(__file__), "Chope.png")
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img = img.resize((100, 100), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(frame, image=img_tk, bg=bg_color)
        img_label.image = img_tk
        img_label.pack(pady=5)
    
    tk.Label(frame, text="Chope - Ferramenta de Setup IA da Sosys", font=("Arial", 10, "bold"), bg=bg_color).pack(pady=5)
    
    btn_new = tk.Button(frame, text="Novo", command=on_new, width=20)
    btn_new.pack(pady=5)
    
    btn_execute_test = tk.Button(frame, text="Executar Teste", command=on_execute_test, width=20)
    btn_execute_test.pack(pady=5)
    
    btn_generate_parquet = tk.Button(frame, text="Gerar Arquivos Parquet", command=on_generate_parquet, width=20)
    btn_generate_parquet.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
