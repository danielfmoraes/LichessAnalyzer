import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Criar pasta para salvar as imagens, caso não exista
os.makedirs("imagens", exist_ok=True)

# Carregar os dados
CSV_FILE = "data/games.csv"
df = pd.read_csv(CSV_FILE)

# Converter a coluna de data para datetime
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

# Relatório - Estatísticas gerais
relatorio_html = """
<html>
<head>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        h1, h2 {
            color: #2c3e50;
            text-align: center;
        }
        .container {
            width: 90%;
            margin: 0 auto;
            padding: 20px;
        }
        .chart {
            margin: 40px 0;
            text-align: center;
        }
        .table {
            margin-top: 20px;
            border-collapse: collapse;
            width: 100%;
        }
        .table, .table th, .table td {
            border: 1px solid #ddd;
        }
        .table th, .table td {
            padding: 10px;
            text-align: left;
        }
        .table th {
            background-color: #2c3e50;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Relatório de Jogos</h1>
"""

# Contagem de vitórias, derrotas e empates
resultado_count = df["Resultado"].value_counts()
relatorio_html += f"<h2>Distribuição de Resultados</h2><table class='table'>{resultado_count.to_frame().to_html(index=False)}</table>"

# Aberturas mais jogadas
top_openings = df["Abertura"].value_counts().head(10)
relatorio_html += f"<h2>Top 10 Aberturas Mais Jogadas</h2><table class='table'>{top_openings.to_frame().to_html(index=False)}</table>"

# Evolução da performance ao longo do tempo
df_sorted = df.sort_values("Data")
df_sorted["Vitória"] = df_sorted["Resultado"].apply(lambda x: 1 if x == "1-0" else (-1 if x == "0-1" else 0))
df_sorted["Performance Acumulada"] = df_sorted["Vitória"].cumsum()
performance_evolucao = df_sorted[["Data", "Performance Acumulada"]].tail(10)  # Últimos 10 pontos da performance acumulada
relatorio_html += f"<h2>Evolução da Performance (Últimos 10 jogos)</h2><table class='table'>{performance_evolucao.to_html(index=False)}</table>"

# Tempo médio por jogada (se houver dados de tempo)
if "Clocks" in df.columns:
    df["Tempo Médio por Jogada"] = df["Clocks"].apply(lambda x: sum(map(int, str(x).split())) / len(str(x).split()) if pd.notna(x) else None)
    tempo_medio = df["Tempo Médio por Jogada"].dropna().mean()
    relatorio_html += f"<h2>Tempo Médio por Jogada (média)</h2><p style='text-align: center;'>{tempo_medio:.2f} segundos</p>"

# Desempenho contra adversários recorrentes
if "Adversario" in df.columns:
    adversary_stats = df.groupby("Adversario")["Vitória"].sum().sort_values(ascending=False).head(10)
    relatorio_html += f"<h2>Top 10 Adversários Mais Enfrentados e Vitórias Acumuladas</h2><table class='table'>{adversary_stats.to_frame().to_html(index=False)}</table>"

# Gerar e salvar as visualizações como imagens

# Contagem de vitórias, derrotas e empates
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="Resultado", palette="Set2")
plt.title("Distribuição de Resultados", fontsize=16, color="#2c3e50")
plt.xlabel("Resultado", fontsize=12)
plt.ylabel("Quantidade de Partidas", fontsize=12)
plt.tight_layout()
plt.savefig("imagens/distribuicao_resultados.png")
relatorio_html += f"<div class='chart'><h2>Distribuição de Resultados</h2><img src='imagens/distribuicao_resultados.png' alt='Distribuição de Resultados'/></div>"

# Aberturas mais jogadas
top_openings = df["Abertura"].value_counts().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=top_openings.values, y=top_openings.index, palette="Blues_d")
plt.title("Top 10 Aberturas Mais Jogadas", fontsize=16, color="#2c3e50")
plt.xlabel("Quantidade de Partidas", fontsize=12)
plt.ylabel("Abertura", fontsize=12)
plt.tight_layout()
plt.savefig("imagens/top_aberturas.png")
relatorio_html += f"<div class='chart'><h2>Top 10 Aberturas Mais Jogadas</h2><img src='imagens/top_aberturas.png' alt='Top 10 Aberturas Mais Jogadas'/></div>"

# Evolução da performance ao longo do tempo
plt.figure(figsize=(10, 5))
plt.plot(df_sorted["Data"], df_sorted["Performance Acumulada"], marker="o", linestyle="-", color="#2980b9")
plt.title("Evolução da Performance ao Longo do Tempo", fontsize=16, color="#2c3e50")
plt.xlabel("Data", fontsize=12)
plt.ylabel("Performance Acumulada", fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("imagens/evolucao_performance.png")
relatorio_html += f"<div class='chart'><h2>Evolução da Performance ao Longo do Tempo</h2><img src='imagens/evolucao_performance.png' alt='Evolução da Performance'/></div>"

# Desempenho contra adversários recorrentes
if "Adversario" in df.columns:
    adversary_stats = df.groupby("Adversario")["Vitória"].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=adversary_stats.values, y=adversary_stats.index, palette="coolwarm")
    plt.title("Top 10 Adversários Mais Enfrentados e Vitórias Acumuladas", fontsize=16, color="#2c3e50")
    plt.xlabel("Vitórias Acumuladas", fontsize=12)
    plt.ylabel("Adversário", fontsize=12)
    plt.tight_layout()
    plt.savefig("imagens/adversarios.png")
    relatorio_html += f"<div class='chart'><h2>Top 10 Adversários Mais Enfrentados e Vitórias Acumuladas</h2><img src='imagens/adversarios.png' alt='Adversários Mais Enfrentados'/></div>"

# Finalizar o HTML
relatorio_html += """
    </div>
</body>
</html>
"""

# Salvar o relatório HTML
with open("relatorio.html", "w", encoding="utf-8") as f:
    f.write(relatorio_html)

print("Relatório gerado com sucesso! Confira o arquivo 'relatorio.html' com as imagens.")
