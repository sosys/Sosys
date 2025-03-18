import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from dotenv import dotenv_values, set_key

def load_config(config_path):
    """Carrega as configurações do arquivo .env fornecido pelo usuário."""
    config = dotenv_values(config_path)
    base_dir = config.get("DIRETORIO_PADRAO", "C:\\Nanda")
    subfolders = config.get("PASTAS").split(';')
    query_subfolders = config.get("SUB_PASTAS").split(';')
    
    return base_dir, subfolders, query_subfolders, config_path

def create_client_structure(base_dir, client_name, subfolders, query_subfolders, config_path):
    """Cria a estrutura de diretórios para o cliente."""
    client_path = os.path.join(base_dir, client_name)
    
    try:
        os.makedirs(client_path, exist_ok=True)
        
        for folder in subfolders:
            folder_path = os.path.join(client_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            
            if folder in subfolders:
                for subfolder in query_subfolders:
                    os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)
        
        # Copiar o arquivo de configuração para a pasta base
        env_file_path = shutil.copy(config_path, os.path.join(client_path, client_name + '.env')) 
        env_file_path = os.path.join(client_path, f"{client_name}.env")
        
        # Solicitar informações do banco de dados
        db_driver = simpledialog.askstring("Configuração do Banco", "Informe o ODBC DRIVER:")
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
    
    base_dir, subfolders, query_subfolders, config_path = load_config(config_path)
    client_name = simpledialog.askstring("Nome do Cliente", "Digite o nome do cliente:")
    
    if client_name:
        create_client_structure(base_dir, client_name, subfolders, query_subfolders, config_path)
    else:
        messagebox.showwarning("Aviso", "Nome do cliente não pode ser vazio.")
