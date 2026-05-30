import json
import os
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

# ==========================================
# CARREGAMENTO DINÂMICO DOS ARQUIVOS JSON
# ==========================================
knowledge_base = []
fact_categories = {}

def load_knowledge_base():
    global knowledge_base, fact_categories
    knowledge_base = []
    fact_categories = {}
    
    json_files = ["orkut_cultura.json", "orkut_historia.json", "orkut_tecnico.json"]
    for file_name in json_files:
        if os.path.exists(file_name):
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    category = data.get("categoria", "geral")
                    dados = data.get("dados", [])
                    for item in dados:
                        knowledge_base.append(item)
                        fact_categories[item] = category
            except Exception as e:
                print(f"Erro ao carregar {file_name}: {e}")
                
    # Fallback se nenhum arquivo for carregado
    if not knowledge_base:
        knowledge_base = [
            "Orkut foi uma rede social criada em 2004 por Orkut Büyükkökten.",
            "O Orkut era muito popular no Brasil e na Índia.",
            "O Orkut tinha comunidades onde usuários podiam discutir interesses em comum.",
            "O Orkut foi descontinuado pelo Google em 2014.",
            "O Orkut permitia depoimentos públicos que os amigos podiam escrever no seu perfil.",
            "O Orkut tinha scraps, depoimentos e comunidades."
        ]
        for item in knowledge_base:
            fact_categories[item] = "geral"

# Inicializa a base
load_knowledge_base()
print(f"Base de conhecimento carregada com {len(knowledge_base)} fatos.")

# ==========================================
# REGRAS E PROCESSAMENTO NLP
# ==========================================
welcome_inputs = ["hi", "hello", "hey", "oi", "olá", "bom dia", "boa tarde", "boa noite"]
welcome_outputs = ["Olá! Seja bem-vindo ao Orkut!", "Oi! Como posso te ajudar hoje?", "Hey! Tudo tranquilo por aí?", "Olá! Pode perguntar sobre o Orkut :)"]

def welcome_message(text):
    # Divide o texto em palavras limpas
    words = re.sub(r'[^a-zA-Záéíóúãõâêôç ]', '', text.lower()).split()
    for word in welcome_inputs:
        if word in words:
            return random.choice(welcome_outputs)
    # Suporta saudações compostas
    text_clean = re.sub(r'[^a-zA-Záéíóúãõâêôç ]', '', text.lower())
    for phrase in ["bom dia", "boa tarde", "boa noite"]:
        if phrase in text_clean:
            return random.choice(welcome_outputs)
    return None

stem_mapping = {
    "criar": "criar", "criou": "criar", "criaram": "criar", "criando": "criar", 
    "criador": "criar", "criadores": "criar", "criado": "criar", "criada": "criar", 
    "criadas": "criar", "criados": "criar", "criação": "criar", "criou-se": "criar",
    "comunidade": "comunidade", "comunidades": "comunidade",
    "amigo": "amigo", "amigos": "amigo", "amiga": "amigo", "amigas": "amigo", 
    "amizade": "amigo", "amizades": "amigo",
    "scrap": "scrap", "scraps": "scrap", "scrapbook": "scrap",
    "foto": "foto", "fotos": "foto", "fotografia": "foto", "fotografias": "foto",
    "popular": "popular", "popularização": "popular", "popularizou": "popular", 
    "popularizado": "popular", "popularidade": "popular"
}

def simple_portuguese_stemmer(word):
    word = word.lower()
    if word in stem_mapping:
        return stem_mapping[word]
    if len(word) > 4:
        if word.endswith("s"):
            word = word[:-1]
    return word

def preprocess(sentence):
    sentence = sentence.lower()
    sentence = re.sub(r'[^a-zA-Záéíóúãõâêôç ]', '', sentence)
    tokens = sentence.split()
    stemmed = [simple_portuguese_stemmer(t) for t in tokens]
    return " ".join(stemmed)

# Helper para formatar a capitalização da primeira letra de frases conectadas
def format_sentence(sentence):
    if not sentence:
        return ""
    words = sentence.split()
    if not words:
        return sentence
    first_word = words[0]
    # Se for uma palavra reservada/nome próprio, não altera
    if first_word in ["Orkut", "Brasil", "Índia", "Google", "HTML", "Java", "OpenSocial", "Takeout", "MySpace", "Facebook"]:
        return sentence
    return sentence[0].lower() + sentence[1:]

# Motor de Busca NLP: similaridade de cossenos para respostas abrangentes
def get_answer(user_text, threshold=0.12):
    if not knowledge_base:
        return None

    cleaned_base = [preprocess(s) for s in knowledge_base]
    user_text_clean = preprocess(user_text)

    # Adiciona o texto do usuário ao final para vetorizar
    corpus = cleaned_base + [user_text_clean]

    try:
        tfidf = TfidfVectorizer()
        matrix = tfidf.fit_transform(corpus)
    except Exception as e:
        print(f"Erro na vetorização: {e}")
        return None

    # Calcula a similaridade da pergunta contra a base local
    similarity = cosine_similarity(matrix[-1], matrix)[0]
    scores = similarity[:-1] # Remove a auto-similaridade da pergunta

    # Encontra correspondências acima do limite (threshold)
    matching_indices = [i for i, score in enumerate(scores) if score >= threshold]

    if not matching_indices:
        return None

    # Ordena por relevância (score decrescente)
    sorted_matches = sorted(matching_indices, key=lambda x: scores[x], reverse=True)

    # Pega até os 3 principais resultados para compor uma resposta abrangente
    top_matches = sorted_matches[:3]
    responses = [knowledge_base[idx] for idx in top_matches]

    # Constrói o parágrafo enriquecido usando conectores
    if len(responses) == 1:
        answer = responses[0]
    elif len(responses) == 2:
        answer = f"{responses[0]} Além disso, {format_sentence(responses[1])}"
    else:
        answer = f"{responses[0]} Além disso, {format_sentence(responses[1])} Também vale ressaltar que {format_sentence(responses[2])}"

    return answer

# Fallback: Pesquisa dinâmica na Wikipédia em português
def buscar_no_wikipedia(query):
    try:
        wikipedia.set_lang("pt")
        # Busca pelos tópicos relacionados
        results = wikipedia.search(query)
        if results:
            for result in results[:3]: # Tenta os primeiros resultados para evitar erros de desambiguação
                try:
                    summary = wikipedia.summary(result, sentences=2)
                    return f"Não encontrei isso na base local do Orkut, mas pesquisei no Wikipédia e descobri o seguinte:\n\n\"{summary}\""
                except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
                    continue
    except Exception as e:
        print(f"Erro ao buscar no Wikipedia: {e}")
    return None

# ==========================================
# ANÁLISE DE SENTIMENTO E IDIOMA
# ==========================================
def check_language(text):
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "pt"

def get_sentiment_intervention(text):
    try:
        # Traduz para inglês para maior precisão do TextBlob
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        blob = TextBlob(translated)
        polarity = blob.sentiment.polarity
        
        if polarity <= -0.3:
            return "Notei que você parece um pouco chateado. O Orkut era justamente um lugar para relaxar e fazer amigos! Mas, sobre o que você perguntou: "
    except Exception:
        pass
    return ""

# ==========================================
# FLUXO PRINCIPAL DO CHATBOT
# ==========================================
def chatbot_response(user_text):
    # 1. Verifica idioma
    lang = check_language(user_text)
    if lang != 'pt' and len(user_text.split()) > 2:
        return "Desculpe, meu banco de dados é focado no Orkut em português. Por favor, pergunte em português."
        
    # 2. Verifica regras / saudações
    rule = welcome_message(user_text)
    if rule:
        return rule
        
    # 3. Intervenção de humor (sentimento)
    intervention = get_sentiment_intervention(user_text)
    
    # 4. Busca base local (híbrido cossenos)
    answer = get_answer(user_text)
    
    # 5. Fallback para o Wikipedia
    if not answer:
        answer = buscar_no_wikipedia(user_text)
        
    # 6. Fallback final se nada der certo
    if not answer:
        answer = "Desculpe, não encontrei uma resposta abrangente sobre isso na base do Orkut e nem no Wikipédia."
        
    return intervention + answer if intervention else answer

# ==========================================
# SINTETIZADOR DE VOZ (SOM / TTS)
# ==========================================
def speak_response(text):
    try:
        engine = pyttsx3.init()
        # Ajusta a velocidade de fala um pouco mais suave
        engine.setProperty('rate', 150)
        # Fala o texto
        # Para evitar ler blocos longos com citações complicadas da Wikipedia por voz, vamos ler apenas o primeiro parágrafo
        speak_text = text.split('\n')[0]
        engine.say(speak_text)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro no TTS: {e}")

# ==========================================
# INTERFACE GRÁFICA TKINTER (ORKUT)
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Orkut - Chatbot")
    root.geometry("950x750")
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
    # JANELA DO CHAT (SCROLLEDTEXT)
    # --------------------------
    chat_window = ScrolledText(
        root, wrap=tk.WORD,
        width=110, height=26,
        font=("Arial", 11),
        bg="#FFFFFF"
    )
    chat_window.pack(pady=20)

    # Configuração de estilos clássicos Orkut (Recados / Scraps)
    chat_window.tag_config("user_name", foreground="#0000CC", font=("Arial", 11, "bold"))
    chat_window.tag_config("meta_text", foreground="#666666", font=("Arial", 9, "italic"))
    chat_window.tag_config("user_msg", foreground="#333333", font=("Arial", 11))
    chat_window.tag_config("bot_name", foreground="#D0028A", font=("Arial", 11, "bold"))
    chat_window.tag_config("bot_msg", foreground="#000000", font=("Arial", 11))
    chat_window.tag_config("separator", foreground="#CCCCCC", font=("Arial", 9))
    chat_window.tag_config("info_tag", foreground="#888888", font=("Arial", 10, "italic"))

    chat_window.insert(tk.END, "Bem-vindo ao Chatbot do Orkut! Deixe um scrap abaixo para interagir com o bot.\n", "info_tag")
    chat_window.insert(tk.END, "="*85 + "\n", "separator")
    chat_window.configure(state="disabled")

    # --------------------------
    # CONTROLES DE ENTRADA
    # --------------------------
    input_frame = tk.Frame(root, bg="#E5ECF9")
    input_frame.pack(pady=10)

    entrada = tk.Entry(input_frame, width=70, font=("Arial", 12))
    entrada.pack(side=tk.LEFT, padx=10)

    # Função para enviar mensagens
    def send_message(event=None):
        user_text = entrada.get().strip()
        if user_text == "":
            return "break"
        
        chat_window.config(state=tk.NORMAL)
        
        # Adiciona a mensagem do Usuário como Scrap
        chat_window.insert(tk.END, "Você ", "user_name")
        chat_window.insert(tk.END, "deixou um scrap:\n", "meta_text")
        chat_window.insert(tk.END, user_text + "\n", "user_msg")
        chat_window.insert(tk.END, "-" * 105 + "\n", "separator")
        
        # Obtém resposta abrangente do chatbot
        response = chatbot_response(user_text)
        
        # Adiciona a resposta do Bot como Scrap
        chat_window.insert(tk.END, "Chatbot do Orkut ", "bot_name")
        chat_window.insert(tk.END, "deixou um scrap:\n", "meta_text")
        chat_window.insert(tk.END, response + "\n", "bot_msg")
        chat_window.insert(tk.END, "-" * 105 + "\n", "separator")
        
        chat_window.see(tk.END)
        chat_window.config(state=tk.DISABLED)
        
        # Limpa campo
        entrada.delete(0, tk.END)
        
        # Inicia a fala em segundo plano
        threading.Thread(target=speak_response, args=(response,), daemon=True).start()
        
        return "break" # Evita que a tecla Enter insira uma quebra de linha indesejada

    # Vincula a tecla Enter e o botão para enviar
    entrada.bind("<Return>", send_message)

    btn = tk.Button(input_frame, text="Enviar Scrap",
                    command=send_message,
                    font=("Arial", 11, "bold"),
                    fg="#FFFFFF", bg="#D0028A",
                    activebackground="#A0016B", activeforeground="#FFFFFF",
                    cursor="hand2", borderwidth=0, padx=15, pady=5)
    btn.pack(side=tk.LEFT, padx=5)

    root.mainloop()
