import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

# Fluxo principal de decisão de resposta do bot
def chatbot_response(user_text):
    rule = welcome_message(user_text)
    if rule:
        return rule
    return get_answer(user_text)

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
    return "break"

root = tk.Tk()
root.title("Orkut - Chatbot")
root.geometry("950x700")
root.configure(bg="#E5ECF9")

header_frame = tk.Frame(root, bg="#C4D0EB", height=60)
header_frame.pack(fill=tk.X)

logo_label = tk.Label(header_frame, text="orkut", font=("Arial", 28, "bold"), fg="#D0028A", bg="#C4D0EB")
logo_label.pack(side=tk.LEFT, padx=(20, 10), pady=10)

menu_frame = tk.Frame(header_frame, bg="#C4D0EB")
menu_frame.pack(side=tk.LEFT, padx=10, pady=22)
menu_links = ["Início", "Perfil", "Página de recados", "Amigos", "Comunidades"]
for i, link in enumerate(menu_links):
    lbl = tk.Label(menu_frame, text=link, font=("Arial", 10), fg="#0000CC", bg="#C4D0EB", cursor="hand2")
    lbl.pack(side=tk.LEFT, padx=3)
    if i < len(menu_links) - 1:
        tk.Label(menu_frame, text="|", font=("Arial", 10), fg="#666666", bg="#C4D0EB").pack(side=tk.LEFT)

search_frame = tk.Frame(header_frame, bg="#C4D0EB")
search_frame.pack(side=tk.RIGHT, padx=20, pady=20)
tk.Label(search_frame, text="buscar no orkut:", font=("Arial", 9), fg="#333333", bg="#C4D0EB").pack(side=tk.LEFT)
tk.Entry(search_frame, width=20, highlightbackground="#CCCCCC", highlightthickness=1).pack(side=tk.LEFT, padx=5)

body_frame = tk.Frame(root, bg="#E5ECF9")
body_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

sidebar = tk.Frame(body_frame, bg="#FFFFFF", highlightbackground="#A5BBE1", highlightthickness=1, width=220)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
sidebar.pack_propagate(False)

pic_frame = tk.Frame(sidebar, bg="#E5ECF9", width=150, height=180, highlightbackground="#CCCCCC", highlightthickness=1)
pic_frame.pack(pady=15)
pic_frame.pack_propagate(False)
tk.Label(pic_frame, text="Sua Foto\n(Sem Imagem)", bg="#E5ECF9", fg="#666666", font=("Arial", 9)).pack(expand=True)

tk.Label(sidebar, text="Você", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#0000CC").pack()
tk.Label(sidebar, text="masculino\nBrasil", font=("Arial", 9), bg="#FFFFFF", fg="#666666").pack(pady=5)

stats_frame = tk.Frame(sidebar, bg="#F9F9F9", highlightbackground="#E5ECF9", highlightthickness=1)
stats_frame.pack(fill=tk.X, padx=15, pady=15)

tk.Label(stats_frame, text="fãs 🌟 10", font=("Arial", 9), bg="#F9F9F9", fg="#333333").pack(anchor=tk.W, padx=5, pady=2)
tk.Label(stats_frame, text="confiável 🧊🧊🧊", font=("Arial", 9), bg="#F9F9F9", fg="#333333").pack(anchor=tk.W, padx=5, pady=2)
tk.Label(stats_frame, text="legal 😎😎😎", font=("Arial", 9), bg="#F9F9F9", fg="#333333").pack(anchor=tk.W, padx=5, pady=2)
tk.Label(stats_frame, text="Perfli ", font=("Arial", 9), bg="#F9F9F9", fg="#333333").pack(anchor=tk.W, padx=5, pady=2)

main_frame = tk.Frame(body_frame, bg="#FFFFFF", highlightbackground="#A5BBE1", highlightthickness=1)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

title_frame = tk.Frame(main_frame, bg="#D4E6F1", height=35)
title_frame.pack(fill=tk.X)
tk.Label(title_frame, text="Página de recados", font=("Arial", 12, "bold"), fg="#000000", bg="#D4E6F1").pack(side=tk.LEFT, padx=15, pady=5)

chat_window = ScrolledText(main_frame, wrap=tk.WORD, font=("Verdana", 10), bg="#FFFFFF", borderwidth=0, highlightthickness=0)
chat_window.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

chat_window.tag_config("user_name", foreground="#0000CC", font=("Verdana", 10, "bold"))
chat_window.tag_config("bot_name", foreground="#D0028A", font=("Verdana", 10, "bold"))
chat_window.tag_config("meta_text", foreground="#666666", font=("Verdana", 9))
chat_window.tag_config("user_msg", foreground="#333333", font=("Verdana", 10))
chat_window.tag_config("bot_msg", foreground="#333333", font=("Verdana", 10))
chat_window.tag_config("separator", foreground="#E5ECF9", font=("Verdana", 10))

input_frame = tk.Frame(main_frame, bg="#F0F5FA", highlightbackground="#A5BBE1", highlightthickness=1)
input_frame.pack(fill=tk.X, padx=15, pady=15)

tk.Label(input_frame, text="Deixe um scrap para Chatbot:", font=("Arial", 9, "bold"), bg="#F0F5FA", fg="#333333").pack(anchor=tk.W, padx=10, pady=(10, 0))

entry = tk.Text(input_frame, height=4, font=("Verdana", 10), highlightbackground="#CCCCCC", highlightthickness=1)
entry.pack(fill=tk.X, padx=10, pady=5)
entry.bind("<Return>", send_message)

btn_frame = tk.Frame(input_frame, bg="#F0F5FA")
btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

send_button = tk.Button(btn_frame, text="enviar scrap", font=("Arial", 10, "bold"), bg="#E5ECF9", fg="#0000CC", activebackground="#C4D0EB", relief=tk.RAISED, borderwidth=1, command=send_message)
send_button.pack(side=tk.RIGHT, ipadx=10, ipady=3)

chat_window.config(state=tk.NORMAL)
chat_window.insert(tk.END, "Chatbot ", "bot_name")
chat_window.insert(tk.END, "deixou um scrap:\n", "meta_text")
chat_window.insert(tk.END, "Olá! Sou um chatbot especialista em Orkut.\nPergunte qualquer coisa sobre a rede social!\n", "bot_msg")
chat_window.insert(tk.END, "-" * 100 + "\n", "separator")
chat_window.config(state=tk.DISABLED)

root.mainloop()