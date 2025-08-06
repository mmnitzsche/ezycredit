# %%
import pandas as pd
import shutil
from pathlib import Path

def create_xlsx_and_move_to_files():
    # Caminho base do script
    base_path = Path(__file__).resolve().parent  # aponta para 'codes/'

    # Caminho do arquivo JSON
    json_path = base_path / "chats_ezycredit.json"

    # Leitura do JSON
    df = pd.read_json(json_path)

    # Salva o DataFrame como Excel temporário na pasta atual
    excel_temp_path = base_path / "ezycredit_chats.xlsx"
    df.to_excel(excel_temp_path, index=False)

    # Caminho final de destino na pasta 'files'
    dest_path = base_path.parent / "files" / "ezycredit_chats.xlsx"
    dest_path.parent.mkdir(parents=True, exist_ok=True)  # Garante que a pasta existe

    # Move o arquivo
    shutil.move(str(excel_temp_path), str(dest_path))

    print(f"Arquivo Excel movido para: {dest_path}")
