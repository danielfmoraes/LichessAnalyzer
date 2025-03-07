import os
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do usuário
LICHESS_USERNAME = os.getenv("USUARIO")  # Nome de usuário no Lichess
API_TOKEN = os.getenv("API_KEY")  # Token da API Lichess

# Verifique se as variáveis foram carregadas corretamente
if not LICHESS_USERNAME or not API_TOKEN:
    print("Erro: As variáveis de ambiente não foram carregadas corretamente.")
    exit(1)

# URL da API do Lichess para exportar partidas
url = f"https://lichess.org/api/games/user/{LICHESS_USERNAME}"

# Parâmetros da requisição
params = {
    "max": 500,  # Número máximo de partidas por requisição (ajustável)
    "pgnInJson": False,  # Certifique-se de que não é JSON, apenas PGN
    "moves": True,  # Incluir movimentos
    "tags": True,  # Incluir tags
    "clocks": True,  # Incluir tempo gasto por lance
    "evals": True,  # Incluir avaliações do Stockfish (se disponível)
    "opening": True,  # Incluir informações da abertura
}

# Cabeçalhos com o token de autenticação
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
}

# Fazer a requisição à API
response = requests.get(url, params=params, headers=headers)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    with open("data/games.pgn", "w", encoding="utf-8") as f:
        f.write(response.text)  # Salvar o arquivo PGN sem imagens
    print("Partidas salvas no arquivo 'games.pgn'")
else:
    print(f"Erro na requisição: {response.status_code} - {response.text}")
