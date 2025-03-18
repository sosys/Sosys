import os
import pandas as pd
import pyodbc
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, ttk
from dotenv import dotenv_values

def get_db_connection(db_config):
    """Retorna uma conexão com o banco de dados baseado na configuração usando apenas pyodbc."""
    driver, server, database, user, password = db_config
    
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}",        )
        return conn
    except pyodbc.Error as e:
        messagebox.showerror("Erro", f"Falha ao conectar no banco de dados: {e}")
        return None

def execute_test_queries():
    """Executa as queries nas subpastas de TESTE_Querys e salva os resultados."""
    root = tk.Tk()
    root.withdraw()
    
    config_path = filedialog.askopenfilename(title="Selecione o arquivo de configuração", filetypes=[("Arquivos .env", "*.env")])
    if not config_path:
        messagebox.showwarning("Aviso", "Nenhum arquivo de configuração selecionado.")
        return
    
    client_name = os.path.splitext(os.path.basename(config_path))[0]  # Obtém o nome do cliente a partir do nome do arquivo .env
    config = dotenv_values(config_path)
    base_dir = config.get("DIRETORIO_PADRAO", "C:\\Nanda")  # Obtém o diretório base do arquivo .env
    client_dir = os.path.join(base_dir, client_name)
    
    db_config = [
        config.get("ODBC_DRIVER", ""),
        config.get("IP_BANCO", ""),
        config.get("DATABASE", ""),
        config.get("USUARIO_BANCO", ""),
        config.get("SENHA_BANCO", "")
    ]
    
    test_queries_path = os.path.join(client_dir, "TESTE_Querys")
    parquet_output_path = os.path.join(client_dir, "Arquivos_Parquet")
    csv_output_path = os.path.join(client_dir, "Arquivos_CSV")
    
    if not os.path.exists(f"{base_dir}\\{client_name}"):
        messagebox.showwarning("Aviso", f"O cliente {client_name} não existe. Certifique-se de criá-lo antes de executar as consultas.")
        return
    
    conn = get_db_connection(db_config)
    if not conn:
        return 
    try:
        cursor = conn.cursor()
        files_processed = False
        folders = [folder for folder in os.listdir(test_queries_path) if os.path.isdir(os.path.join(test_queries_path, folder))]
        total_folders = len(folders)
        
        if total_folders == 0:
            messagebox.showwarning("Aviso", "Nenhum arquivo de consulta encontrado para processamento.")
            return
        
        # Criar uma janela para exibir a barra de progresso
        progress_window = tk.Toplevel()
        progress_window.title("Processando consultas")
        progress_window.geometry("400x120")
        
        label = tk.Label(progress_window, text="Processando consultas...", font=("Arial", 12))
        label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
        progress_bar.pack(pady=10)
        
        progress_window.update()
        
        for index, folder in enumerate(folders, start=1):
            folder_path = os.path.join(test_queries_path, folder)
            sql_file = os.path.join(folder_path, f"{folder}.sql")
            if os.path.exists(sql_file):
                with open(sql_file, "r", encoding="utf-8") as f:
                    query = f.read()
                
                cursor.execute(query)
                data = cursor.fetchmany(1000)
                columns = [desc[0].strip() for desc in cursor.description]  # Remove espaços extras dos nomes das colunas
                cleaned_data = [tuple(str(value).strip() for value in row) for row in data]  # Remove espaços dos valores
                
                if data:
                    if all(len(row) == len(columns) for row in cleaned_data):  
                        df = pd.DataFrame(cleaned_data, columns=columns)
                    else:
                        messagebox.showerror("Erro", f"Formato inesperado nos resultados de {folder}.sql")
                        continue  # Pula essa query e segue para a próxima
                    
                    parquet_folder = parquet_output_path
                    
                    if os.path.exists(parquet_folder): 
                        csv_file = os.path.join(csv_output_path, f"{folder}.csv")
                        df.to_csv(csv_file, index=False, sep=";", encoding="utf-8")
                        
                        parquet_file = os.path.join(parquet_folder, f"{folder}.parquet")
                        df.to_parquet(parquet_file, index=False)
                        
                        files_processed = True
            
            # **Atualizar barra de progresso**
            progress_percentage = int((index / total_folders) * 100)
            progress_bar["value"] = progress_percentage
            label.config(text=f"Processando... {progress_percentage}%")
            progress_window.update()
        
        cursor.close()
        conn.close()
        progress_window.destroy()
        
        if files_processed:
            messagebox.showinfo("Sucesso", "Consultas executadas e arquivos gerados com sucesso.")
        else:
            messagebox.showwarning("Aviso", "Nenhum arquivo de consulta encontrado ou processado.")
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar as queries: {e}")