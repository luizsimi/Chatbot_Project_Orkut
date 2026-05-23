import json
import wikipedia
import tkinter as tk
from tkinter import scrolledtext
from langdetect import detect
from deep_translator import GoogleTranslator 
from textblob import TextBlob


# --------------------------
# CARREGAR BASE
# --------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

historia = load_json("orkut_historia.json")["dados"]
cultura = load_json("orkut_cultura.json")["dados"]
tecnico = load_json("orkut_tecnico.json")["dados"]

knowledge_base = historia + cultura + tecnico


# --------------------------
# DETECÇÃO
# --------------------------
def detectar_idioma(texto):
    try:
        return detect(texto)
    except:
        return "pt"


def analisar_sentimento(texto):
    try:
        texto_en = GoogleTranslator(source="pt", target="en").translate(texto)
        p = TextBlob(texto_en).sentiment.polarity

        print("DEBUG ORIGINAL:", texto)
        print("DEBUG TRADUZIDO:", texto_en)
        print("DEBUG POLARITY:", p)

        if p > 0.2:
            return "positivo"
        elif p < -0.2:
            return "negativo"
        return "neutro"

    except Exception as e:
        print("ERRO SENTIMENTO:", e)
        return "neutro"
# --------------------------
# BUSCA INTELIGENTE NA BASE
# --------------------------
def buscar_na_base(pergunta, base):
    pergunta = pergunta.lower()
    palavras = set(pergunta.split())

    resultados = []

    for fato in base:
        fato_lower = fato.lower()

        score = sum(1 for p in palavras if p in fato_lower)

        if score > 2:
            resultados.append((score, fato))

    resultados.sort(reverse=True, key=lambda x: x[0])

    return [f[1] for f in resultados[:3]] if resultados else None


# --------------------------
# SÍNTESE DE RESPOSTA (COM SENTIMENTO USADO)
# --------------------------
def sintetizar_resposta(pergunta, fatos, sentimento):
    if not fatos:
        return None

    base = fatos[0]

    pergunta = pergunta.lower()

    # estilo por sentimento
    if sentimento == "positivo":
        tom_inicio = "Legal! 😊 "
        tom_meio = "Isso é interessante porque "

    elif sentimento == "negativo":
        tom_inicio = "Entendo. "
        tom_meio = "De forma mais clara, "

    else:
        tom_inicio = ""
        tom_meio = ""

    # respostas mais naturais (sem depender de keywords frágeis)
    if len(fatos) == 1:
        return f"{tom_inicio}{tom_meio}{base}"

    # junta múltiplos fatos de forma fluida
    return (
        f"{tom_inicio}{tom_meio}"
        f"{fatos[0]} Além disso, {fatos[1]}."
    )
# --------------------------
# WIKIPEDIA CONTROLADO
# --------------------------
def buscar_no_wikipedia(pergunta):
    try:
        resultados = wikipedia.search(pergunta)
        if not resultados:
            return None

        for r in resultados[:3]:
            try:
                resumo = wikipedia.summary(r, sentences=2)

                if any(k in resumo.lower() for k in ["orkut", "google", "rede social"]):
                    return resumo

            except:
                continue

        return None

    except:
        return None


# --------------------------
# RESPOSTA FINAL
# --------------------------
def responder(pergunta):
    print("RESPONDER FOI CHAMADO")
    detectar_idioma(pergunta)

    sentimento = analisar_sentimento(pergunta)

    fatos = buscar_na_base(pergunta, knowledge_base)

    resposta = sintetizar_resposta(pergunta, fatos, sentimento)

    if not resposta:
        resposta = buscar_no_wikipedia(pergunta)

    if not resposta:
        return "Não encontrei nada relacionado ao Orkut sobre isso."

    return resposta


# --------------------------
# TKINTER (INTACTO)
# --------------------------
root = tk.Tk()
root.title("Orkut - Chatbot")
root.geometry("950x700")
root.configure(bg="#E5ECF9")

header_frame = tk.Frame(root, bg="#C4D0EB", height=60)
header_frame.pack(fill=tk.X)

logo_label = tk.Label(header_frame, text="orkut",
                      font=("Arial", 28, "bold"),
                      fg="#D0028A", bg="#C4D0EB")
logo_label.pack(side=tk.LEFT, padx=(20, 10), pady=10)

menu_frame = tk.Frame(header_frame, bg="#C4D0EB")
menu_frame.pack(side=tk.LEFT, padx=10, pady=22)

menu_links = ["Início", "Perfil", "Página de recados", "Amigos", "Comunidades"]

for i, link in enumerate(menu_links):
    lbl = tk.Label(menu_frame, text=link,
                   font=("Arial", 10),
                   fg="#0000CC", bg="#C4D0EB",
                   cursor="hand2")
    lbl.pack(side=tk.LEFT, padx=3)

    if i < len(menu_links) - 1:
        tk.Label(menu_frame, text="|",
                 font=("Arial", 10),
                 fg="#666666", bg="#C4D0EB").pack(side=tk.LEFT)

search_frame = tk.Frame(header_frame, bg="#C4D0EB")
search_frame.pack(side=tk.RIGHT, padx=20, pady=20)

tk.Label(search_frame, text="buscar no orkut:",
         font=("Arial", 9),
         fg="#333333", bg="#C4D0EB").pack(side=tk.LEFT)

tk.Entry(search_frame, width=20,
         highlightbackground="#CCCCCC",
         highlightthickness=1).pack(side=tk.LEFT, padx=5)


# --------------------------
# CHAT
# --------------------------
chat_window = scrolledtext.ScrolledText(
    root, wrap=tk.WORD,
    width=110, height=25,
    font=("Arial", 11),
    bg="#FFFFFF"
)

chat_window.pack(pady=20)
chat_window.insert(tk.END, "Bot do Orkut iniciado!\n")
chat_window.configure(state="disabled")


# --------------------------
# INPUT
# --------------------------
input_frame = tk.Frame(root, bg="#E5ECF9")
input_frame.pack(pady=10)

entrada = tk.Entry(input_frame, width=70, font=("Arial", 12))
entrada.pack(side=tk.LEFT, padx=10)


def enviar():
    pergunta = entrada.get().strip()

    if not pergunta:
        return

    chat_window.configure(state="normal")
    chat_window.insert(tk.END, f"\nVocê: {pergunta}\n")

    resposta = responder(pergunta)

    chat_window.insert(tk.END, f"Bot: {resposta}\n")

    chat_window.configure(state="disabled")
    entrada.delete(0, tk.END)


btn = tk.Button(input_frame, text="Enviar",
                command=enviar,
                font=("Arial", 12),
                bg="#C4D0EB")

btn.pack(side=tk.LEFT, padx=5)

root.mainloop()
