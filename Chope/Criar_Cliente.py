import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from dotenv import dotenv_values, set_key

def get_best_odbc_driver(user_driver):
    """Substitui o driver informado pelo usuário pelo melhor ODBC disponível."""
    drivers = {
        "MSSQL": "{ODBC Driver 17 for SQL Server}",
        "PostgreSQL": "{PostgreSQL Unicode}",
        "MySQL": "{MySQL ODBC 8.0 Unicode Driver}",
        "MariaDB": "{MariaDB ODBC 3.1 Driver}",
        "Oracle": "{Oracle in OraDB12Home1}",
        "SQLite": "{SQLite3 ODBC Driver}",
        "DB2": "{IBM DB2 ODBC DRIVER}",
        "Firebird": "{Firebird ODBC Driver}",
        "Sybase": "{Sybase ASE ODBC Driver}",
        "Snowflake": "{SnowflakeDSIIDriver}"
    }
    
    for db, driver_info in drivers.items():
        if db.lower() in user_driver.lower():
            if isinstance(driver_info, dict):  # Caso seja um banco com múltiplas versões
                for version, driver in driver_info.items():
                    if version in user_driver:
                        return driver
                return list(driver_info.values())[-1]  # Se não especificar versão, usa a mais recente
            return driver_info
    return user_driver  # Retorna o que foi informado se não houver correspondência

def load_config(config_path):
    """Carrega as configurações do arquivo .env fornecido pelo usuário."""
    config = dotenv_values(config_path)
    base_dir = config.get("DIRETORIO_PADRAO", "C:\\Nanda")
    folders = config.get("PASTAS").split(';')
    subfolders = config.get("SUB_PASTAS").split(';')
    files = config.get("ARQUIVOS").split(';')
    
    return base_dir, folders, subfolders, files, config_path

def create_client_structure(base_dir, client_name, folders, subfolders, files, config_path):
    """Cria a estrutura de diretórios para o cliente."""
    client_path = os.path.join(base_dir, client_name)
    
    try:
        os.makedirs(client_path, exist_ok=True)
        
        for folder in folders:
            folder_path = os.path.join(client_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            for subfolder in subfolders:
                os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)
        
        for file_folder in files:
            file_folder_path = os.path.join(client_path, file_folder)
            os.makedirs(file_folder_path, exist_ok=True)
        
        # Copiar o arquivo de configuração para a pasta base
        env_file_path = shutil.copy(config_path, os.path.join(client_path, client_name + '.env')) 
        env_file_path = os.path.join(client_path, f"{client_name}.env")
        
        # Solicitar informações do banco de dados
        db_driver = simpledialog.askstring("Configuração do Banco", "Informe o ODBC DRIVER:")
        db_driver = get_best_odbc_driver(db_driver)  # Substitui pelo melhor driver disponível
        db_ip = simpledialog.askstring("Configuração do Banco", "Informe o IP do banco de dados:")
        db_name = simpledialog.askstring("Configuração do Banco", "Informe o nome do DATABASE:")
        db_user = simpledialog.askstring("Configuração do Banco", "Informe o USUÁRIO do banco de dados:")
        db_password = simpledialog.askstring("Configuração do Banco", "Informe a SENHA do banco de dados:")
        
        # Gravar informações no arquivo .env
        set_key(env_file_path, "ODBC_DRIVER", db_driver)
        set_key(env_file_path, "IP_BANCO", db_ip)
        set_key(env_file_path, "DATABASE", db_name)
        set_key(env_file_path, "USUARIO_BANCO", db_user)
        set_key(env_file_path, "SENHA_BANCO", db_password)
        
        messagebox.showinfo("Sucesso", f"Estrutura criada para {client_name} em {client_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar estrutura: {e}")

def on_new():
    """Solicita o nome do cliente e o arquivo de configuração, depois cria a estrutura."""
    config_path = filedialog.askopenfilename(title="Selecione o arquivo de configuração", filetypes=[("Arquivos .env", "*.env")])
    
    if not config_path:
        messagebox.showwarning("Aviso", "Nenhum arquivo de configuração selecionado.")
        return
    
    base_dir, folders, subfolders, files, config_path = load_config(config_path)
    client_name = simpledialog.askstring("Nome do Cliente", "Digite o nome do cliente:")
    
    if client_name:
        create_client_structure(base_dir, client_name, folders, subfolders, files, config_path)
    else:
        messagebox.showwarning("Aviso", "Nome do cliente não pode ser vazio.")
