import json
import wikipedia
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect, LangDetectException
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pyttsx3
import threading


# Base de conhecimento do chatbot
knowledge_base = [
    "Orkut foi uma rede social criada em 2004 por Orkut Büyükkökten.",
    "O Orkut era muito popular no Brasil e na Índia.",
    "O Orkut tinha comunidades onde usuários podiam discutir interesses em comum.",
    "O Orkut foi descontinuado pelo Google em 2014.",
    "O Orkut permitia depoimentos públicos que os amigos podiam escrever no seu perfil.",
    "O Orkut tinha recursos como scraps, depoimentos e comunidades.",
    "O criador da rede social Orkut foi Orkut Büyükkökten, um engenheiro turco.",
    "O Orkut era conhecido pela forte cultura de comunidades brasileiras.",
    "O Google encerrou o Orkut para focar em outras redes, como o Google+.",
    "O Orkut possuía perfis personalizáveis com foto, descrição e lista de amigos.",

    "O Brasil se tornou o maior país do Orkut, ultrapassando os Estados Unidos rapidamente.",
    "A Índia era o segundo país mais ativo dentro da plataforma.",
    "As comunidades eram o coração do Orkut, reunindo pessoas com os mais variados interesses.",
    "Algumas comunidades tinham milhões de membros.",
    "Os usuários do Orkut podiam avaliar seus amigos como 'confiável', 'legal' e 'sexy'.",
    "A página inicial mostrava os recados recentes enviados no scrapbook.",
    "Os scraps eram mensagens públicas, visíveis para qualquer visitante do perfil.",
    "Depoimentos eram mensagens privadas que, ao serem aceitas, ficavam públicas no perfil.",
    "O Orkut permitia deixar recados coloridos usando HTML simples.",
    "Era comum personalizar scraps com glitter, gifs e textos animados.",

    "O Orkut tinha um limite de 1000 amigos por usuário.",
    "Havia um contador de visitas ao perfil, mas nem sempre funcionava de forma precisa.",
    "A função de comunidades recomendadas ajudava usuários a descobrir interesses parecidos.",
    "Existiam comunidades de humor, memes, fandoms e até coisas bizarras.",
    "O Orkut tinha um feed chamado 'Atualizações', que mostrava mudanças no perfil dos amigos.",
    "Era comum usuários competirem pela maior quantidade de depoimentos.",
    "O Orkut suportava fotos, mas o limite inicial era de apenas 12 imagens.",
    "Mais tarde, o número de fotos por álbum aumentou significativamente.",
    "O Orkut teve suporte a vídeos embutidos apenas nos seus últimos anos.",
    "O design original era azul, mas depois mudou para tons de rosa e roxo.",

    "O nome Orkut vem do sobrenome do criador, Orkut Büyükkökten.",
    "A rede social foi desenvolvida inicialmente como um projeto experimental dentro do Google.",
    "O Orkut tinha a filosofia de aproximar pessoas e formar novas amizades.",
    "O Orkut exibiu mensagens comemorativas em datas especiais, como Páscoa e Natal.",
    "Havia uma seção chamada 'Coisas que eu odeio' no perfil dos usuários.",
    "Era possível indicar se você estava solteiro, namorando ou em um relacionamento sério.",
    "O Orkut tinha uma das primeiras implementações de 'scraps em massa', usados em correntes.",
    "Existiam comunidades dedicadas a stalkear perfis, apelidadas de 'detetives do Orkut'.",
    "Algumas comunidades viraram fandoms importantes no Brasil.",
    "Os moderadores das comunidades tinham o poder de controlar discussões e banir membros.",

    "O Orkut teve problemas sérios com spam e perfis falsos em sua fase final.",
    "No auge, mais de 70% do tráfego mundial do Orkut vinha do Brasil.",
    "O Orkut ganhou uma versão móvel simples antes de ser encerrado.",
    "O Google criou o Google+ e passou a focar nele, o que acelerou o fim do Orkut.",
    "Quando o Orkut acabou, o Google permitiu baixar fotos e dados pelo Google Takeout.",
    "O Orkut tinha uma página de estatísticas mostrando número de amigos, scraps e visitas.",
    "Algumas comunidades ficaram famosas, como 'Eu Odeio Acordar Cedo'.",
    "O Orkut influenciou profundamente a cultura da internet brasileira dos anos 2000.",
    "Muitas amizades e relacionamentos começaram através das comunidades do Orkut.",
    "O Orkut possuía um sistema de karma social baseado nas classificações dadas pelos amigos.", 

    "Alguns usuários usavam HTML para criar recados com bordas, brilhos e fontes personalizadas.",
    "O Orkut tinha um sistema de 'fans', onde você podia se declarar fã de alguém.",
    "A ferramenta de busca de comunidades permitia filtrar temas por popularidade.",
    "O Orkut chegou a ter mais de 300 milhões de usuários ao longo de sua existência.",
    "Havia comunidades dedicadas a professores, escolas, cantores e até bairros inteiros.",
    "O termo 'miguxês' viralizou em parte por causa das comunidades do Orkut.",
    "Muitos memes brasileiros surgiram originalmente no Orkut.",
    "Existiam perfis fakes populares que se tornavam celebridades dentro da plataforma.",
    "O Orkut teve problemas recorrentes de instabilidade nos seus primeiros anos.",
    "A opção de 'modo visitante' permitia ver perfis anonimamente durante algum tempo.",

    "Comunidades como 'Eu Confesso' funcionavam como confessionários públicos.",
    "Algumas comunidades serviam como fóruns de suporte emocional entre usuários.",
    "A barra lateral mostrava aniversários dos amigos no dia.",
    "O Orkut organizava eventos oficiais em alguns países.",
    "Havia concursos informais de fotos dentro das comunidades.",
    "As pessoas usavam o perfil para expor frases filosóficas famosas.",
    "Algumas comunidades tinham regras muito rígidas, como gramaticais e de conteúdo.",
    "O Orkut exibia quais comunidades você havia acabado de entrar.",
    "Era comum adicionar desconhecidos apenas por terem gostos parecidos em comunidades.",
    "O Orkut permitia enviar scraps com vídeos do YouTube nos seus últimos anos.",

    "Existia uma comunidade famosa chamada 'Não sou obrigado a nada'.",
    "A comunidade 'Eu Odeio Gente Falsa' foi uma das maiores do site.",
    "Muitas pessoas usavam o Orkut para divulgar blogs pessoais.",
    "A aba de fotos tinha um botão de zoom primitivo.",
    "Os usuários podiam escolher até seis fotos favoritas para destacar no perfil.",
    "Havia um sistema de mensagens privadas chamado 'mensagens diretas'.",
    "Alguns jogos casuais chegaram ao Orkut antes de migrar para o Facebook.",
    "O Orkut possuía páginas oficiais de artistas e bandas.",
    "As discussões em comunidades podiam durar anos sem serem apagadas.",
    "Os moderadores podiam fixar tópicos importantes no topo da comunidade.",

    "O Orkut teve versões em mais de 10 idiomas.",
    "A busca interna do Orkut nunca foi totalmente precisa.",
    "Perfis com muitos fãs viravam celebridades dentro da rede.",
    "O Orkut tinha suporte parcial para fotos em alta resolução.",
    "A aba 'vídeos' permitia favoritar vídeos de outros usuários.",
    "Algumas escolas e empresas bloqueavam o Orkut para evitar distrações.",
    "O Orkut possuía temas comemorativos, como em datas de aniversário do site.",
    "O Orkut permitia indicar quem eram seus 'melhores amigos' no perfil.",
    "Alguns usuários usavam o Orkut como currículo informal.",
    "O Orkut marcou época como uma das maiores redes sociais já usadas no Brasil."
]

# Sistema de regras: Verifica se o usuário enviou uma saudação
welcome_inputs = ["hi", "hello", "hey", "oi", "olá"]
welcome_outputs = ["Olá!", "Oi! Como posso ajudar?", "Hey! Tudo certo?", "Olá! Pode perguntar :)"]

def welcome_message(text):
    for word in text.lower().split():
        if word in welcome_inputs:
            return random.choice(welcome_outputs)
    return None


# Pré-processamento: Padroniza o texto removendo pontuações e números
def preprocess(sentence):
    sentence = sentence.lower()
    sentence = re.sub(r'[^a-zA-Záéíóúãõâêôç ]', '', sentence)
    tokens = sentence.split()
    return " ".join(tokens)

# Motor de Busca NLP: Calcula a Similaridade de Cossenos usando TF-IDF
def get_answer(user_text, threshold=0.01):
    cleaned_base = [preprocess(s) for s in knowledge_base]
    user_text_clean = preprocess(user_text)

    corpus = cleaned_base + [user_text_clean]

    tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform(corpus)

    similarity = cosine_similarity(matrix[-1], matrix)
    index = similarity.argsort()[0][-2]
    value = similarity[0][index]

    if value < threshold:
        return "Desculpe, não encontrei uma resposta sobre isso."
    else:
        return knowledge_base[index]

# Analisador de Sentimento e Idioma
def check_language(text):
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "pt" # Fallback

def get_sentiment_intervention(text):
    try:
        # Traduz para inglês para usar TextBlob de forma mais precisa
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        blob = TextBlob(translated)
        polarity = blob.sentiment.polarity
        
        if polarity <= -0.3:
            return "Notei que você parece um pouco chateado. O Orkut era justamente um lugar para relaxar e fazer amigos! Mas, sobre o que você perguntou: "
    except Exception:
        pass
    return ""

# Fluxo principal de decisão de resposta do bot
def chatbot_response(user_text):
    # Verifica idioma
    lang = check_language(user_text)
    if lang != 'pt' and len(user_text.split()) > 2: # Evitar falsos positivos em saudações curtas
        return "Desculpe, meu banco de dados é focado no Orkut em português. Por favor, pergunte em português."
        
    rule = welcome_message(user_text)
    if rule:
        return rule
        
    # Análise de sentimento (intervenção)
    intervention = get_sentiment_intervention(user_text)
    
    # Resposta padrão
    answer = get_answer(user_text)
    
    return intervention + answer if intervention else answer

def speak_response(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro no TTS: {e}")

# Função executada ao enviar um texto: Atualiza a interface gráfica com as mensagens
def send_message(event=None):
    user_text = entry.get("1.0", tk.END).strip()
    if user_text == "":
        return
    
    chat_window.config(state=tk.NORMAL)
    # Scrap do usuário
    chat_window.insert(tk.END, "Você ", "user_name")
    chat_window.insert(tk.END, "deixou um scrap:\n", "meta_text")
    chat_window.insert(tk.END, user_text + "\n", "user_msg")
    chat_window.insert(tk.END, "-" * 100 + "\n", "separator")

    response = chatbot_response(user_text)
    # Scrap do bot
    chat_window.insert(tk.END, "Chatbot ", "bot_name")
    chat_window.insert(tk.END, "deixou um scrap:\n", "meta_text")
    chat_window.insert(tk.END, response + "\n", "bot_msg")
    chat_window.insert(tk.END, "-" * 100 + "\n", "separator")

    chat_window.see(tk.END)
    chat_window.config(state=tk.DISABLED)
    entry.delete("1.0", tk.END)
    
    # Inicia a fala em uma thread separada para não travar a interface
    threading.Thread(target=speak_response, args=(response,), daemon=True).start()
    
    return "break"

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
