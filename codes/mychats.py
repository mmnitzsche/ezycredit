#%%
from codes.auth import ollama_key

import openai

openai.api_key = ollama_key

# Função para gerar conversa
def gerar_conversa(prompt_base):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # ou "gpt-4" se preferir
        messages=[
            {"role": "system", "content": "Você é um vendedor experiente atendendo um cliente."},
            {"role": "user", "content": prompt_base}
        ],
        temperature=0.8,
        max_tokens=500
    )
    return response.choices[0].message["content"]

# Prompt de entrada
prompt_base = """
Gere uma conversa fictícia entre um cliente e um vendedor de uma loja de eletrônicos. 
O cliente está procurando um notebook para trabalhar com edição de vídeo. 
Mostre 6 trocas de mensagens entre eles.
"""

print(gerar_conversa(prompt_base))
