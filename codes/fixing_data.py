#%%
import json
import pandas as pd

# Abre o arquivo em modo leitura
with open('chats_easycred.json', 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

char_counter = 0                  # começa do 0
for item in dados:
    if item["id"] == 1:           # novo chat detectado
        char_counter += 1
    item["char_id"] = char_counter

# --- 3. (opcional) salva em outro arquivo -----------------------------------
with open("conversas_com_charid.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)


with open('conversas_com_charid.json','r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

df = pd.json_normalize(dados)
df.to_excel("chats.xlsx")