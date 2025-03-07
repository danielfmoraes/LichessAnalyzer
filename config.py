# config.py

# Caminho para o arquivo CSV com os dados das partidas
CSV_FILE = "data/games.csv"

# Configurações de visualização
FIGURE_SIZE = (8, 5)  # Tamanho padrão dos gráficos
PALETTE = "pastel"  # Paleta de cores para os gráficos

# Configurações de análise
TOP_OPENINGS_COUNT = 10  # Número de aberturas mais jogadas para exibição
TOP_OPPONENTS_COUNT = 10  # Número de adversários mais enfrentados

# Configurações para API do Lichess
LICHESS_API_URL = "https://lichess.org/api/games/user/"
USERNAME = os.getenv("USUARIO")  # Alterar para seu username no Lichess
TOKEN = os.getenv("API_KEY")  # Substituir pelo seu token de API
MAX_GAMES = 100  # Número máximo de partidas a baixar

