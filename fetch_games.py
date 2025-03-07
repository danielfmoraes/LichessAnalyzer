import os
import requests
from dotenv import load_dotenv
import time


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do Lichess via variáveis de ambiente
LICHESS_USERNAME = os.getenv("USUARIO")  # Nome de usuário no Lichess
API_TOKEN = os.getenv("API_KEY")  # Token da API Lichess

URL = f"https://lichess.org/api/games/user/{LICHESS_USERNAME}"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept-Encoding": "gzip"
}

LAST_GAME_FILE = "last_game.txt"
DATA_FOLDER = "data"  # Pasta onde as partidas serão armazenadas

# Verifica se a pasta "data" existe, se não, cria
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def get_last_timestamp():
    """Lê o timestamp da última partida baixada."""
    if os.path.exists(LAST_GAME_FILE):
        with open(LAST_GAME_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return None
    return None

def save_last_timestamp(timestamp):
    """Salva o timestamp da última partida baixada."""
    if timestamp:
        with open(LAST_GAME_FILE, "w") as file:
            file.write(str(timestamp))

def fetch_games():
    """Busca novas partidas do usuário no Lichess respeitando limites da API."""
    if not LICHESS_USERNAME or not API_TOKEN:
        print("Erro: Variáveis de ambiente USUARIO ou API_KEY não estão definidas.")
        return

    print("🔄 Carregando partidas do Lichess...")

    params = {
        "max": 500,
        "pgnInJson": False,
        "moves": True,
        "tags": True,
        "clocks": True,
        "evals": True,
        "opening": True
    }

    last_timestamp = get_last_timestamp()
    if last_timestamp:
        params["since"] = last_timestamp

    all_games = []
    total_games = 0
    requests_count = 0  # Contador de requisições feitas
    max_requests = 10   # Limitar o número de requisições para evitar loop infinito
    data = []  # Variável para armazenar as partidas no formato desejado

    while True:
        if requests_count >= max_requests:
            print("⚠️ Limite de requisições alcançado. Parando o processo.")
            break

        print("🔍 Buscando partidas...")
        response = requests.get(URL, params=params, headers=HEADERS)

        if response.status_code == 401:
            print("❌ Erro 401: Token inválido ou permissões insuficientes.")
            return
        elif response.status_code == 429:
            print("⏳ Muitas requisições! Esperando 10 segundos...")
            time.sleep(10)
            continue
        elif response.status_code != 200:
            print(f"⚠️ Erro ao buscar partidas: {response.status_code}")
            return

        games = response.text.strip()
        
        if not games:
            print("✅ Nenhuma nova partida encontrada.")
            break

        partidas_baixadas = games.count("[Event ")
        total_games += partidas_baixadas
        print(f"📥 {partidas_baixadas} novas partidas baixadas...")

        # Adiciona as partidas à variável `data`
        data.append(games)

        new_timestamp = response.headers.get("X-Last-Game-Timestamp")
        if new_timestamp:
            try:
                last_timestamp = int(new_timestamp)
                save_last_timestamp(last_timestamp)
            except ValueError:
                print(f"⚠️ Erro ao converter timestamp: {new_timestamp}")

        requests_count += 1  # Incrementa o contador de requisições
        time.sleep(2)

    if data:
        print(f"✅ {total_games} novas partidas baixadas.")
        # Aqui, você pode fazer algo com os dados armazenados na variável `data`
        # Por exemplo, se quiser, pode exibir ou processar as partidas
        print(f"Partidas armazenadas: {len(data)}")

        # Nome do arquivo onde as partidas serão armazenadas na pasta 'data'
        data_file = os.path.join(DATA_FOLDER, "partidas.pgn")

        # Se quiser continuar a salvar as partidas no arquivo .pgn
        with open(data_file, "a", encoding="utf-8") as f:
            f.write("\n\n".join(data) + "\n\n")
        print(f"Partidas salvas no arquivo: {data_file}")

if __name__ == "__main__":
    fetch_games()
