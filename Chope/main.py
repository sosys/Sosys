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
from Criar_Cliente import on_new
from Executar_Teste import execute_test_queries

def on_execute_test():
    """Chama a função de execução de testes."""
    execute_test_queries()

def on_generate_parquet():
    """Gera arquivos Parquet (placeholder)."""
    print("TESTE")
    messagebox.showinfo("Gerar Arquivos Parquet", "TESTE")

def main():
    """Configura e inicia a interface gráfica."""
    root = tk.Tk()
    root.title("Gerenciador de Estruturas")
    root.geometry("300x200")
    
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)
    
    btn_new = tk.Button(frame, text="Novo", command=on_new, width=20)
    btn_new.pack(pady=5)
    
    btn_execute_test = tk.Button(frame, text="Executar Teste", command=on_execute_test, width=20)
    btn_execute_test.pack(pady=5)
    
    btn_generate_parquet = tk.Button(frame, text="Gerar Arquivos Parquet", command=on_generate_parquet, width=20)
    btn_generate_parquet.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
