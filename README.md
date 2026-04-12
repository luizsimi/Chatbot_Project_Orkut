Chatbot sobre Orkut

Este projeto é um chatbot simples desenvolvido em Python com foco em responder perguntas sobre o Orkut. Ele utiliza técnicas básicas de processamento de linguagem natural para encontrar respostas a partir de uma base de conhecimento.

O chatbot é do tipo híbrido, combinando respostas por regras (para saudações) e similaridade de texto (TF-IDF com cosseno) para responder perguntas do usuário.

Tecnologias utilizadas
Python 3
Tkinter
Scikit-learn
Como executar
Clone o repositório ou baixe os arquivos:

git clone <repo_url>
cd projeto_processamento

(Opcional) Crie um ambiente virtual:

python3 -m venv venv
source venv/bin/activate

Instale as dependências:

pip install scikit-learn

Execute o programa:

python app.py

Como usar

Ao rodar o programa, uma janela será aberta.

Digite uma pergunta no campo de texto e clique em "Enviar". O chatbot irá responder com base nas informações disponíveis sobre o Orkut.

Exemplos de perguntas:

quem criou o orkut
quando o orkut acabou
o que eram scraps
para que serviam as comunidades
Interface com Tkinter

A interface foi feita utilizando Tkinter, que já vem com o Python.

Elementos principais:

janela principal criada com Tk()
área de chat com ScrolledText
campo de entrada com Text
botão de envio com Button
Funcionamento

O chatbot funciona da seguinte forma:

Verifica se a mensagem é uma saudação e responde com uma frase pronta
Caso contrário, processa o texto e compara com a base de conhecimento
Utiliza TF-IDF e similaridade de cossenos para encontrar a resposta mais próxima
Observações
O chatbot responde apenas com base no conteúdo da base de dados
Perguntas fora do tema podem não ter resposta adequada
O projeto tem objetivo educacional
