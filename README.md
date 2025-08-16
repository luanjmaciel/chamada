A aplicação foi construída com uma arquitetura cliente-servidor, onde a API atua como o servidor (back-end) e o site como o cliente (front-end). A comunicação entre eles é feita através de requisições HTTP.

A API foi desenvolvida em Python utilizando o framework Flask. O seu papel principal é processar os dados do back-end, sem se preocupar com a interface visual. Ela foi projetada com uma rota específica (/participantes) que, ao ser acessada via método GET, executa a seguinte sequência de ações:

Leitura e Parsing do arquivo: A API lê um arquivo de texto (participantes.txt) que contém os nomes e horários de participação.

Processamento dos Dados: Utiliza a biblioteca datetime para converter os horários em objetos de data e hora, e defaultdict para contar e armazenar o número de participações, além da primeira e última ocorrência de cada participante.

Serialização para JSON: Os dados processados são convertidos para o formato JSON (JavaScript Object Notation), um padrão leve e universal para troca de dados na web.

Para permitir que o site acesse a API, foi configurado o CORS (Cross-Origin Resource Sharing) com a extensão Flask-CORS, prevenindo bloqueios de segurança do navegador.
