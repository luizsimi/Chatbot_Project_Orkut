import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Base de dados da silva 

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

# Saudacao da gentileza

welcome_inputs = ["hi", "hello", "hey", "oi", "olá"]
welcome_outputs = ["Olá!", "Oi! Como posso ajudar?", "Hey! Tudo certo?", "Olá! Pode perguntar :)"]

def welcome_message(text):
    for word in text.lower().split():
        if word in welcome_inputs:
            return random.choice(welcome_outputs)
    return None


# Pré processamento (tava usando nltk, mas tava dando bug, então fiz um pré processamento direto)
def preprocess(sentence):
    sentence = sentence.lower()
    sentence = re.sub(r'[^a-zA-Záéíóúãõâêôç ]', '', sentence)
    tokens = sentence.split()
    return " ".join(tokens)

# Resposta via parametro de similaridade
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

# -----------------------------
# BOT
# -----------------------------
def chatbot_response(user_text):
    rule = welcome_message(user_text)
    if rule:
        return rule
    return get_answer(user_text)

# -----------------------------
# INTERFACE
# -----------------------------
def send_message():
    user_text = entry.get("1.0", tk.END).strip()
    if user_text == "":
        return
    
    chat_window.insert(tk.END, "Você: " + user_text + "\n")

    response = chatbot_response(user_text)
    chat_window.insert(tk.END, "Chatbot: " + response + "\n\n")

    entry.delete("1.0", tk.END)
    chat_window.see(tk.END)

root = tk.Tk()
root.title("Chatbot Especialista em Orkut")

chat_window = ScrolledText(root, wrap=tk.WORD, width=70, height=25, font=("Arial", 11))
chat_window.pack(padx=10, pady=10)

entry = tk.Text(root, height=1, width=60, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=10, pady=10)

send_button = tk.Button(root, text="Enviar", width=10, command=send_message)
send_button.pack(side=tk.LEFT)

chat_window.insert(tk.END, "Chatbot: Olá! Sou um chatbot especialista em Orkut.\nPergunte qualquer coisa!\n\n")

root.mainloop()