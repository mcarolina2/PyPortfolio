import streamlit as st
import pandas as pd
import os

# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(page_title="Análise de Ativos", layout="wide")

# -----------------------------
# Diretórios
# -----------------------------
pasta_dados = "dados"
pasta_graficos = os.path.join(pasta_dados, "graficos")

# -----------------------------
# Ler CSV consolidado
# -----------------------------
consolidado_path = os.path.join(pasta_dados, "precos_consolidados.csv")

if not os.path.exists(consolidado_path):
    st.error("Arquivo consolidado não encontrado. Execute primeiro o etl_extract.py")
    st.stop()

df_consolidado = pd.read_csv(consolidado_path, index_col=0, parse_dates=True)

# -----------------------------
# Criar abas
# -----------------------------
aba_contexto, aba_graficos, aba_dados = st.tabs(["Contextualização", "Gráficos", "Dados"])

# -----------------------------
# Aba 1: Contextualização
# -----------------------------
with aba_contexto:
    st.header("📖 Contextualização")
    st.markdown("""
                
    Imagine um investidor conservador, avesso ao risco. Ele deseja montar sua carteira de investimentos, mas sua principal preocupação é minimizar a exposição às incertezas do mercado. A questão é: como encontrar a melhor combinação de ativos que ofereça o menor risco possível, sem abrir mão de um retorno desejado?
 
        ➡️O desafio: qual é a melhor proporção de cada ativo para alcançar esse equilíbrio?"
                
    Neste projeto, exploramos esse dilema clássico da teoria de portfólios. A partir de uma carteira composta por 5 ativos, utilizamos técnicas de otimização para identificar a alocação que posiciona o investidor no ponto ideal da fronteira eficiente: onde o risco é minimizado para um nível de retorno previamente estabelecido.

    Este aplicativo permite analisar ativos financeiros selecionados, utilizando dados históricos de fechamento.
    
    **Funcionalidades:**
    - Visualizar gráficos individuais de cada ativo.
    - Comparar todos os ativos em um gráfico consolidado.
    - Consultar a tabela com preços históricos.
    
    **Observações:**
    - Os dados são atualizados pelo script `etl_extract.py`.
    - Os gráficos salvos podem ser acessados na pasta `dados/graficos`.
    """)

# -----------------------------
# Aba 2: Gráficos
# -----------------------------
with aba_graficos:
    st.header("📈 Gráficos")
    
    # Sidebar para seleção de ativos
    ativos_disponiveis = df_consolidado.columns.tolist()
    ativos_selecionados = st.multiselect(
        "Selecione os ativos:",
        options=ativos_disponiveis,
        default=ativos_disponiveis
    )

    # Exibir gráficos individuais
    for ativo in ativos_selecionados:
        caminho_grafico = os.path.join(pasta_graficos, f"{ativo}.png")
        if os.path.exists(caminho_grafico):
            st.subheader(ativo)
            st.image(caminho_grafico, use_container_width=True)
        else:
            st.warning(f"Gráfico do ativo {ativo} não encontrado.")

# -----------------------------
# Aba 3: Dados
# -----------------------------
with aba_dados:
    st.header("📊 Tabela de Preços Consolidados")
    df_filtrado = df_consolidado[ativos_selecionados]
    st.dataframe(df_filtrado)
