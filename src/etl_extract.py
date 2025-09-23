import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# Criar pasta "dados" se não existir
# -----------------------------
pasta_dados = "../dados"
os.makedirs(pasta_dados, exist_ok=True)

# Criar pasta para gráficos
pasta_graficos = os.path.join(pasta_dados, "graficos")
os.makedirs(pasta_graficos, exist_ok=True)

# -----------------------------
# Datas de início e fim
# -----------------------------
dataini = "2025-04-01"
datafim = "2025-06-29"

# -----------------------------
# Lista de ativos
# -----------------------------
tickers = {
    "LWSA3": "LWSA3.SA",
    "ELET6": "ELET6.SA",
    "ITSA4": "ITSA4.SA",
    "RENT3": "RENT3.SA",
    "BRFS3": "BRFS3.SA",
    "IBOV": "^BVSP"
}

# -----------------------------
# Baixar dados, padronizar colunas e salvar CSVs
# -----------------------------
dados = {}

for nome, ticker in tickers.items():
    serie = yf.download(ticker, start=dataini, end=datafim)["Close"].dropna()
    
    # Garantir DataFrame com coluna nome do ativo
    if isinstance(serie, pd.Series):
        df = serie.to_frame(name=nome)
    else:
        df = serie.copy()
        df.columns = [nome]
    
    # Salvar CSV individual
    df.to_csv(os.path.join(pasta_dados, f"{nome}.csv"))
    
    # Guardar para consolidado
    dados[nome] = df[nome]
    
    print(f"{nome}: {len(df)} observações")
    
    # -----------------------------
    # Salvar gráfico individual
    # -----------------------------
    plt.figure(figsize=(6, 4))
    plt.plot(df[nome], color="red")
    plt.title(f"Ativo - {nome}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_graficos, f"{nome}.png"))
    plt.close()  # Fecha a figura para não sobrepor

# -----------------------------
# Criar DataFrame consolidado e salvar
# -----------------------------
df_consolidado = pd.DataFrame(dados)
df_consolidado.to_csv(os.path.join(pasta_dados, "precos_consolidados.csv"), index=True)

# -----------------------------
# Gráfico consolidado de todos os ativos
# -----------------------------
plt.figure(figsize=(12, 6))
for nome, serie in dados.items():
    plt.plot(serie, label=nome)
plt.legend()
plt.xticks(rotation=45)
plt.title("Ativos Consolidados")
plt.tight_layout()
plt.savefig(os.path.join(pasta_graficos, "consolidado.png"))
plt.show()
