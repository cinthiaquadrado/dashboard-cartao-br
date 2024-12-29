# Importação das bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para extrair dados do Banco Central
def extracao_bcb(codigo, data_inicio, data_fim):
    try:
        url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={data_inicio}&dataFinal={data_fim}'
        df = pd.read_json(url)
        df.set_index('data', inplace=True)
        df.index = pd.to_datetime(df.index, dayfirst=True)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados do código {codigo}: {e}")
        return pd.DataFrame(columns=['data', 'valor']).set_index('data')

# Extração dos dados
dados = {
    "Saldo do Crédito Rotativo": extracao_bcb(20587, '01/01/2010', '31/10/2024'),  # Saldo do crédito rotativo - PF
    "Juros Médios": extracao_bcb(22699, '01/01/2010', '31/10/2024'),  # Juros médios - Cartão de crédito
    "Taxa de Inadimplência (15 a 90 dias)": extracao_bcb(20754, '01/01/2010', '31/10/2024'),  # Inadimplência (15 a 90 dias)
    "Taxa de Inadimplência (>90 dias)": extracao_bcb(20753, '01/01/2010', '31/10/2024'),  # Inadimplência (>90 dias)
    "Volume de Operações": extracao_bcb(20592, '01/01/2010', '31/10/2024'),  # Volume de operações - PF
    "Concessões Pré-Fixadas": extracao_bcb(22356, '01/01/2010', '31/10/2024'),
    "Concessões Pós-Fixadas": extracao_bcb(22357, '01/01/2010', '31/10/2024'),
    "Concessões Flutuantes": extracao_bcb(22358, '01/01/2010', '31/10/2024'),
    "Saldos Consolidados no Mês": extracao_bcb(22359, '01/01/2010', '31/10/2024'),
    "Concessões Consolidadas no Mês": extracao_bcb(22360, '01/01/2010', '31/10/2024'),
    "Carteira de Crédito Rotativo": extracao_bcb(20588, '01/01/2010', '31/10/2024'),
    "Carteira de Crédito Parcelado": extracao_bcb(20589, '01/01/2010', '31/10/2024'),
    "Carteira de Crédito à Vista": extracao_bcb(20590, '01/01/2010', '31/10/2024'),
    "Prazo Médio das Operações": extracao_bcb(22361, '01/01/2010', '31/10/2024'),
}

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
    key: df[(df.index >= pd.Timestamp(data_inicio)) & (df.index <= pd.Timestamp(data_fim))]
    for key, df in dados.items()
}

# Layout do dashboard
tab1, tab2, tab3 = st.tabs(["Indicadores Gerais", "Concessões e Saldos", "Carteiras e Prazo Médio"])

# Indicadores Gerais
with tab1:
    st.subheader("Indicadores Gerais")
    st.line_chart(filtered_data["Saldo do Crédito Rotativo"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Juros Médios"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Taxa de Inadimplência (15 a 90 dias)"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Taxa de Inadimplência (>90 dias)"]["valor"], height=250, use_container_width=True)

# Concessões e Saldos
with tab2:
    st.subheader("Concessões e Saldos")
    st.line_chart(filtered_data["Concessões Pré-Fixadas"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Concessões Pós-Fixadas"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Concessões Flutuantes"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Saldos Consolidados no Mês"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Concessões Consolidadas no Mês"]["valor"], height=250, use_container_width=True)

# Carteiras e Prazo Médio
with tab3:
    st.subheader("Carteiras de Crédito e Prazo Médio")
    st.line_chart(filtered_data["Carteira de Crédito Rotativo"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Carteira de Crédito Parcelado"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Carteira de Crédito à Vista"]["valor"], height=250, use_container_width=True)
    st.line_chart(filtered_data["Prazo Médio das Operações"]["valor"], height=250, use_container_width=True)

# Conclusão
st.write("Este dashboard apresenta uma visão geral do mercado de crédito no Brasil, permitindo a análise de tendências e correlações entre os principais indicadores econômicos relacionados ao crédito.")
