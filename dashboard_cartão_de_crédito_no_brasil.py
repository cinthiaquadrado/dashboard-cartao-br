# Importação das bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para extrair dados do Banco Central
def extracao_bcb(codigo, data_inicio, data_fim):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={data_inicio}&dataFinal={data_fim}'
    df = pd.read_json(url)
    df.set_index('data', inplace=True)
    df.index = pd.to_datetime(df.index, dayfirst=True)
    return df

# Extração dos dados
saldo_cartao_rotativo = extracao_bcb(20587, '01/01/2010', '31/10/2024')  # Saldo do crédito rotativo - PF
juros_medio = extracao_bcb(22699, '01/01/2010', '31/10/2024')  # Juros médios - Cartão de crédito
inadimplencia = extracao_bcb(20753, '01/01/2010', '31/10/2024')  # Taxa de inadimplência - PF
volume_operacoes = extracao_bcb(20592, '01/01/2010', '31/10/2024')  # Volume de operações - PF

# Configuração do Streamlit
st.set_page_config(page_title="Dashboard - Mercado de Crédito no Brasil", layout="wide")

# Título
st.title("📊 Dashboard - Mercado de Crédito no Brasil")
st.write("Dados extraídos do Banco Central (https://www.bcb.gov.br)")

# Filtro de data
st.sidebar.header("Filtros")
data_inicio = st.sidebar.date_input("Data Inicial", value=pd.Timestamp('2010-01-01'))
data_fim = st.sidebar.date_input("Data Final", value=pd.Timestamp('2024-10-31'))

# Aplicar filtro
filtered_data = {
    "Saldo do Crédito Rotativo": saldo_cartao_rotativo[(saldo_cartao_rotativo.index >= pd.Timestamp(data_inicio)) & (saldo_cartao_rotativo.index <= pd.Timestamp(data_fim))],
    "Juros Médios": juros_medio[(juros_medio.index >= pd.Timestamp(data_inicio)) & (juros_medio.index <= pd.Timestamp(data_fim))],
    "Taxa de Inadimplência": inadimplencia[(inadimplencia.index >= pd.Timestamp(data_inicio)) & (inadimplencia.index <= pd.Timestamp(data_fim))],
    "Volume de Operações": volume_operacoes[(volume_operacoes.index >= pd.Timestamp(data_inicio)) & (volume_operacoes.index <= pd.Timestamp(data_fim))],
}

# Layout do dashboard
col1, col2 = st.columns(2)

# Saldo do Crédito Rotativo
col1.subheader("Saldo do Crédito Rotativo (PF)")
col1.line_chart(filtered_data["Saldo do Crédito Rotativo"]["valor"])

# Juros Médios
col2.subheader("Juros Médios do Crédito Rotativo")
col2.line_chart(filtered_data["Juros Médios"]["valor"])

# Taxa de Inadimplência
col1.subheader("Taxa de Inadimplência (PF)")
col1.line_chart(filtered_data["Taxa de Inadimplência"]["valor"])

# Volume de Operações
col2.subheader("Volume de Operações (PF)")
col2.line_chart(filtered_data["Volume de Operações"]["valor"])

# Análise Resumida
st.header("📈 Análise Resumida")
saldo_atual = filtered_data["Saldo do Crédito Rotativo"]["valor"].iloc[-1]
juros_atual = filtered_data["Juros Médios"]["valor"].iloc[-1]
inadimplencia_atual = filtered_data["Taxa de Inadimplência"]["valor"].iloc[-1]
volume_atual = filtered_data["Volume de Operações"]["valor"].iloc[-1]

st.write(f"**Saldo Atual (R$):** {saldo_atual:,.2f}")
st.write(f"**Juros Médios (%):** {juros_atual:.2f}")
st.write(f"**Taxa de Inadimplência (%):** {inadimplencia_atual:.2f}")
st.write(f"**Volume de Operações (R$):** {volume_atual:,.2f}")

# Conclusão
st.write("Este dashboard apresenta uma visão geral do mercado de crédito no Brasil, permitindo a análise de tendências e correlações entre os principais indicadores econômicos relacionados ao crédito.")

