#%%
from gtts import gTTS
import os

# Lista de textos
textos = [
    "Olá, este é o primeiro texto.",
    "Este é o segundo texto que será convertido.",
    "Mais um exemplo para transformar em áudio."
]

# Diretório de saída
output_dir = "audios"
os.makedirs(output_dir, exist_ok=True)

# Loop para converter
for i, texto in enumerate(textos, start=1):
    tts = gTTS(text=texto, lang='pt-br')
    filename = os.path.join(output_dir, f"audio_{i}.mp3")
    tts.save(filename)
    print(f"Salvo: {filename}")
