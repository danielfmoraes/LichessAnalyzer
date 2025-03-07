import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Carregar os dados
CSV_FILE = "data/games.csv"
df = pd.read_csv(CSV_FILE)

# Converter a coluna de data para datetime
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

# Contagem de vitórias, derrotas e empates
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="Resultado", palette="pastel")
plt.title("Distribuição de Resultados")
plt.xlabel("Resultado")
plt.ylabel("Quantidade de Partidas")
plt.show()

# Aberturas mais jogadas
top_openings = df["Abertura"].value_counts().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=top_openings.values, y=top_openings.index, palette="muted")
plt.title("Top 10 Aberturas Mais Jogadas")
plt.xlabel("Quantidade de Partidas")
plt.ylabel("Abertura")
plt.show()

# Evolução da performance ao longo do tempo
df_sorted = df.sort_values("Data")
df_sorted["Vitória"] = df_sorted["Resultado"].apply(lambda x: 1 if x == "1-0" else (-1 if x == "0-1" else 0))
df_sorted["Performance Acumulada"] = df_sorted["Vitória"].cumsum()

plt.figure(figsize=(10, 5))
plt.plot(df_sorted["Data"], df_sorted["Performance Acumulada"], marker="o", linestyle="-", color="blue")
plt.title("Evolução da Performance ao Longo do Tempo")
plt.xlabel("Data")
plt.ylabel("Performance Acumulada")
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Tempo médio por jogada (se houver dados de tempo)
if "Clocks" in df.columns:
    df["Tempo Médio por Jogada"] = df["Clocks"].apply(lambda x: sum(map(int, str(x).split())) / len(str(x).split()) if pd.notna(x) else None)
    plt.figure(figsize=(6, 4))
    sns.histplot(df["Tempo Médio por Jogada"].dropna(), bins=20, kde=True, color="green")
    plt.title("Distribuição do Tempo Médio por Jogada")
    plt.xlabel("Segundos por Jogada")
    plt.ylabel("Frequência")
    plt.show()

# Desempenho contra adversários recorrentes
if "Adversario" in df.columns:
    adversary_stats = df.groupby("Adversario")["Vitória"].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=adversary_stats.values, y=adversary_stats.index, palette="coolwarm")
    plt.title("Top 10 Adversários Mais Enfrentados e Vitórias Acumuladas")
    plt.xlabel("Vitórias Acumuladas")
    plt.ylabel("Adversário")
    plt.show()

# Mapa de calor das casas mais utilizadas (se houver dados de lances)
if "Lances" in df.columns:
    all_moves = [move for game in df["Lances"].dropna() for move in game.split()]
    unique_squares = sorted(set(all_moves))
    square_counts = {sq: all_moves.count(sq) for sq in unique_squares}
    
    board_matrix = np.zeros((8, 8))
    files = "abcdefgh"
    
    for square, count in square_counts.items():
        if len(square) == 2 and square[0] in files and square[1].isdigit():
            file_index = files.index(square[0])
            rank_index = 8 - int(square[1])
            board_matrix[rank_index, file_index] = count
    
    plt.figure(figsize=(6, 6))
    sns.heatmap(board_matrix, annot=True, cmap="Reds", linewidths=0.5, xticklabels=list(files), yticklabels=range(8, 0, -1))
    plt.title("Mapa de Calor das Casas Mais Utilizadas")
    plt.xlabel("Coluna")
    plt.ylabel("Linha")
    plt.show()