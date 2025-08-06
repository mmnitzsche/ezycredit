#%%
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import re


def generate_chats():

    # saída
    output_file = "chats_ezycredit.json"

    # Data base
    base_data = datetime(2024, 10, 27, 10, 0)
    conversas = []

    # Tipos de chamados
    TIPOS = [
        "pedido de crédito", "pedido de crédito", "pedido de crédito",
        "cancelamento", "cancelamento",
        "pedido de refinanciamento", "pedido de refinanciamento",
        "ajuste de parcelas", "solicitação de segunda via de boleto",
        "informação sobre taxas", "atendimento helpdesk (app travando)",
        "mudança de dados cadastrais", "portabilidade de crédito",
        "reclamação sobre atendimento"
    ]


    # Loop principal
    for i, tipo in enumerate(TIPOS, 1):
        prompt = f"""
    Gere uma conversa fictícia de texto entre um cliente (C:) e um atendente (V:) da EasyCred, 
    sobre o seguinte tipo de chamado: **{tipo}**. 
    A conversa deve ter entre 6 a 16 mensagens, com alternância entre cliente e atendente.

    Formato:
    [
    {{
        "agente":"humano" ou "bot",
        "cliente_nome":"João da Silva",
        "id": 1,
        "data": {base_data},
        "tipo": "{tipo}",
        "conteudo": "C: Olá, ..."
    }},
    ...
    ]

    Responda SOMENTE com o conteúdo JSON dentro de um bloco ```json.
    """

        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "gemma3", "prompt": prompt, "stream": True}
            )

            # Acumula todas as linhas da resposta
            full_response = ""
            for line in r.iter_lines(decode_unicode=True):
                if line:
                    json_data = json.loads(line)
                    full_response += json_data.get("response", "")

            # Extrai conteúdo JSON da resposta completa
            match = re.search(r"```json\s*(\[\s*{.*?}\s*])\s*```", full_response, re.DOTALL)
            if match:
                try:
                    chat = json.loads(match.group(1))
                    conversas.extend(chat)
                except Exception as e:
                    print(f"⚠️ Erro ao parsear JSON do chat {i}: {e}")
            else:
                print(f"⚠️ Nenhum JSON válido encontrado para o tipo '{tipo}'")

        except Exception as e:
            print(f"❌ Erro na requisição para o tipo '{tipo}': {e}")

    # Salvar resultado final
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(conversas, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Arquivo gerado com sucesso: {output_file}")


