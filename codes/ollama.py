#%%
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd 


base_data = datetime(2024, 10, 27, 10, 0)
conversas = []


TIPOS = [
    "pedido de crédito",
    "pedido de crédito",
    "pedido de crédito",
    "pedido de crédito",
    "pedido de crédito",
    "pedido de crédito",
    "pedido de crédito",
    "cancelamento",
    "cancelamento",
    "cancelamento",
    "pedido de refinanciamento",
    "pedido de refinanciamento",
    "pedido de refinanciamento",
    "ajuste de parcelas",
    "ajuste de parcelas",
    "solicitação de segunda via de boleto",
    "informação sobre taxas",
    "informação sobre taxas",
    "atendimento helpdesk (app travando)",
    "atendimento helpdesk (app travando)",
    "mudança de dados cadastrais",
    "mudança de dados cadastrais",
    "portabilidade de crédito",
    "reclamação sobre atendimento"
]


for i, tipo in enumerate(TIPOS, 1):
    prompt = f"""
Gere uma conversa fictícia de texto entre um cliente (C:) e um atendente (V:) da EasyCred, 
sobre o seguinte tipo de chamado: **{tipo}**. 
A conversa deve ter entre 6 a 16 mensagens, com alternância entre cliente e atendente.

Formato:
[
  {{
    "agente":"humano" ou "bot"
    "cliente_nome":"João da Sivlva"
    "id": 1,
    "data": "2024-10-27 10:00:00",
    "tipo": "{tipo}",
    "conteudo": "C: Olá, ..."
  }},
  ...
]

Responda SOMENTE com o conteúdo JSON dentro de um bloco ```json.
"""

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma3", "prompt": prompt, "stream": False}
    )

    raw = r.json()["response"]

    # Extração de JSON da resposta
    import re
    match = re.search(r"```json\s*(\[\s*{.*?}\s*])\s*```", raw, re.DOTALL)
    if match:
        try:
            chat = json.loads(match.group(1))
            conversas.extend(chat)
        except Exception as e:
            print(f"⚠️ Erro ao parsear JSON do chat {i}: {e}")
    else:
        print(f"⚠️ Nenhum JSON válido encontrado para o tipo {tipo}")

# Salvar resultado final
with open("chats_easycred.json", "w", encoding="utf-8") as f:
    json.dump(conversas, f, ensure_ascii=False, indent=2)

print("✅ Arquivo gerado com sucesso: chats_easycred.json")


chat_df = pd.json_normalize(conversas)
chat_df