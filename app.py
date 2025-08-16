import re
from datetime import datetime
from collections import defaultdict
from flask import Flask, jsonify
from flask_cors import CORS

# Inicializa a aplicação Flask
app = Flask(__name__)
# Habilita o CORS para permitir que o site acesse a API
CORS(app)

def processar_dados_do_arquivo(caminho_do_arquivo):
    """
    Lê o arquivo de texto, processa os participantes e retorna um dicionário com os dados.
    """
    # Usa defaultdict para contar e armazenar as informações dos participantes
    dados_participantes = defaultdict(
        lambda: {'participacoes': 0, 'primeira_participacao': None, 'ultima_participacao': None}
    )

    try:
        # Abre o arquivo de texto para leitura
        with open(caminho_do_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                # Usa uma expressão regular para extrair o nome e a data/hora
                match = re.search(r'^(.*?),\s*\[(.*?)\]$', linha.strip())
                if match:
                    nome = match.group(1).strip()
                    timestamp_str = match.group(2).strip()
                    data_hora = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

                    # Incrementa a contagem de participações
                    dados_participantes[nome]['participacoes'] += 1

                    # Atualiza a primeira participação se for a primeira vez
                    if dados_participantes[nome]['primeira_participacao'] is None:
                        dados_participantes[nome]['primeira_participacao'] = data_hora
                    
                    # Atualiza a última participação com a data/hora da linha atual
                    dados_participantes[nome]['ultima_participacao'] = data_hora
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_do_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        return None

    # Converte os objetos de data/hora em strings para que o JSON possa ser criado
    dados_para_json = {}
    for nome, dados in dados_participantes.items():
        dados_para_json[nome] = {
            'participacoes': dados['participacoes'],
            'primeira_participacao': dados['primeira_participacao'].isoformat() if dados['primeira_participacao'] else None,
            'ultima_participacao': dados['ultima_participacao'].isoformat() if dados['ultima_participacao'] else None,
        }
    
    return dados_para_json

@app.route('/participantes', methods=['GET'])
def get_participantes():
    """
    Endpoint da API que retorna os dados dos participantes em JSON.
    A URL para acessar este endpoint é http://127.0.0.1:5000/participantes.
    """
    caminho_do_arquivo = 'participantes.txt'
    dados = processar_dados_do_arquivo(caminho_do_arquivo)
    
    if dados is None:
        return jsonify({'erro': 'Não foi possível processar o arquivo de participantes.'}), 500
    
    return jsonify(dados)

if __name__ == '__main__':
    # Roda a API no modo de desenvolvimento, tornando-a acessível na porta 5000
    app.run(debug=True)