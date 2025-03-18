import os
import pandas as pd
import pyodbc
import tkinter as tk
from tkinter import filedialog, messagebox
from dotenv import dotenv_values, set_key

def get_db_connection(db_config):
    """Retorna uma conexão com o banco de dados baseado na configuração usando pyodbc."""
    driver, server, database, user, password = db_config
    
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}"
        )
        return conn
    except pyodbc.Error as e:
        messagebox.showerror("Erro", f"Falha ao conectar no banco de dados: {e}")
        return None

def execute_queries_to_parquet():
    """Executa as queries e salva os resultados completos em arquivos Parquet e CSV com sufixo _PRD."""
    root = tk.Tk()
    root.withdraw()
    
    config_path = filedialog.askopenfilename(title="Selecione o arquivo de configuração", filetypes=[("Arquivos .env", "*.env")])
    if not config_path:
        messagebox.showwarning("Aviso", "Nenhum arquivo de configuração selecionado.")
        return
    
    config = dotenv_values(config_path)
    if config.get("TESTE") != "OK":
        messagebox.showerror("Erro", "O teste não foi realizado com sucesso. Execute o teste antes de gerar os arquivos Parquet.")
        return
    
    client_name = os.path.splitext(os.path.basename(config_path))[0]
    base_dir = config.get("DIRETORIO_PADRAO", "C:\\Nanda")
    client_dir = os.path.join(base_dir, client_name)
    
    db_config = [
        config.get("ODBC_DRIVER", ""),
        config.get("IP_BANCO", ""),
        config.get("DATABASE", ""),
        config.get("USUARIO_BANCO", ""),
        config.get("SENHA_BANCO", "")
    ]
    
    queries_path = os.path.join(client_dir, "Querys")
    parquet_output_path = os.path.join(client_dir, "Arquivos_Parquet")
    csv_output_path = os.path.join(client_dir, "Arquivos_CSV")
    
    if not os.path.exists(client_dir):
        messagebox.showwarning("Aviso", f"O cliente {client_name} não existe. Certifique-se de criá-lo antes de executar as consultas.")
        return
    
    conn = get_db_connection(db_config)
    if not conn:
        return 
    
    try:
        cursor = conn.cursor()
        files_processed = False
        
        for root_dir, sub_dirs, files in os.walk(queries_path):
            for file in files:
                if file.endswith(".sql"):
                    sql_file_path = os.path.join(root_dir, file)
                    with open(sql_file_path, "r", encoding="utf-8") as f:
                        query = f.read()
                    
                    cursor.execute(query)
                    data = cursor.fetchall()
                    columns = [desc[0].strip() for desc in cursor.description]
                    cleaned_data = [tuple(str(value).strip() for value in row) for row in data]  # Limpeza dos valores
                    
                    if data and all(len(row) == len(columns) for row in cleaned_data):
                        df = pd.DataFrame(cleaned_data, columns=columns)
                        
                        base_filename = os.path.splitext(file)[0] + "_PRD"
                        df.to_csv(os.path.join(csv_output_path, f"{base_filename}.csv"), index=False, sep=";", encoding="utf-8")
                        df.to_parquet(os.path.join(parquet_output_path, f"{base_filename}.parquet"), index=False)
                        files_processed = True
        
        cursor.close()
        conn.close()
        
        if files_processed:
            messagebox.showinfo("Sucesso", "Consultas executadas e arquivos Parquet e CSV gerados com sucesso.")
        else:
            messagebox.showwarning("Aviso", "Nenhum arquivo de consulta encontrado ou processado.")
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar as queries: {e}")
