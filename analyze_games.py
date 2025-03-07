import chess.pgn
import pandas as pd

# Caminho do arquivo PGN
PGN_FILE = "data/partidas.pgn"

# Lista para armazenar os dados das partidas
game_data = []

# Lendo o arquivo PGN
with open(PGN_FILE, encoding="utf-8") as pgn_file:
    while True:
        game = chess.pgn.read_game(pgn_file)
        if game is None:
            break
        
        # Extraindo informações principais
        headers = game.headers
        game_data.append({
            "Data": headers.get("Date", "N/A"),
            "Evento": headers.get("Event", "N/A"),
            "Brancas": headers.get("White", "N/A"),
            "Pretas": headers.get("Black", "N/A"),
            "Resultado": headers.get("Result", "N/A"),
            "Abertura": headers.get("Opening", "N/A"),
            "Eco": headers.get("ECO", "N/A"),
        })

# Criando um DataFrame
df = pd.DataFrame(game_data)

# Salvando em CSV para análises futuras
df.to_csv("data/games.csv", index=False)
print("Análise concluída! Dados salvos em data/games.csv")

# Estatísticas gerais
print("\nEstatísticas das suas partidas:")
print(df["Resultado"].value_counts())
print("\nAberturas mais jogadas:")
print(df["Abertura"].value_counts().head(10))