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

# Definir filtros para a barra lateral
st.sidebar.header("Filtros de Visualização")

# Filtro de seleção de indicadores
indicador_selecionado = st.sidebar.selectbox(
    "Selecione o Indicador",
    ["Saldo do Crédito Rotativo", "Taxa de Inadimplência (15 a 90 dias)", "Taxa de Inadimplência (>90 dias)",
     "Saldo da carteira - Cartão de crédito parcelado", "Saldo da carteira - Cartão de crédito à vista",
     "Saldo da carteira - Cartão de crédito total", "Número de Cartões de Crédito Emitidos",
     "Número de Cartões de Crédito Ativos", "Valor total das transações com cartões de crédito",
     "Taxa de Juros do Cartão de Crédito"]
)

# Filtro de intervalo de datas
data_inicio = st.sidebar.date_input("Data de Início", pd.to_datetime("2020-01-01"))
data_fim = st.sidebar.date_input("Data de Fim", pd.to_datetime("2024-12-28"))

# Função para filtrar dados com base nas datas selecionadas
def filtrar_dados(df, data_inicio, data_fim):
    return df[(df.index >= data_inicio) & (df.index <= data_fim)]

# Extração dos dados
dados = {
    "Saldo do Crédito Rotativo": extracao_bcb(20587, '01/03/2007', '28/12/2024'),  # Saldo do crédito rotativo - PF
    "Taxa de Inadimplência (15 a 90 dias)": extracao_bcb(7912, '30/06/2000', '31/12/2012'),  # Inadimplência (15 a 90 dias)
    "Taxa de Inadimplência (>90 dias)": extracao_bcb(7934, '30/06/20001', '31/12/2012'),  # Inadimplência (>90 dias)
    "Saldo da carteira - Cartão de crédito parcelado": extracao_bcb(20588, '01/03/2007', '28/12/2024'),
    "Saldo da carteira - Cartão de crédito à vista": extracao_bcb(20589, '01/03/2007', '28/12/2024'),
    "Saldo da carteira - Cartão de crédito total": extracao_bcb(20590, '01/03/2007', '28/12/2024'),
    "Número de Cartões de Crédito Emitidos": extracao_bcb(25147, '31/12/2010', '28/12/2024'),  # Número de cartões emitidos
    "Número de Cartões de Crédito Ativos": extracao_bcb(25149, '31/12/2010', '28/12/2024'),  # Número de cartões ativos
    "Valor total das transações com cartões de crédito": extracao_bcb(25229, '31/12/2010', '28/12/2024'),
    "Taxa de Juros do Cartão de Crédito": extracao_bcb(20751, '01/03/2007', '28/12/2024'),  # Taxa de juros do cartão
}

# Filtragem de dados com base na seleção do indicador e intervalo de datas
df_selecionado = dados[indicador_selecionado]
df_filtrado = filtrar_dados(df_selecionado, data_inicio, data_fim)

# Layout do dashboard
tab1, tab2, tab3, tab4 = st.tabs(["Indicadores Gerais", "Carteiras de Crédito", "Operações de Cartão", "Conclusão"])

# Texto inicial explicativo
st.markdown("""
    # Dashboard: Panorama do Uso de Cartões de Crédito no Brasil
    Este dashboard apresenta uma análise detalhada sobre o uso de cartões de crédito por pessoas físicas no Brasil, 
    com o objetivo de fornecer informações atualizadas sobre a evolução do crédito rotativo, inadimplência, 
    as carteiras de crédito e as operações realizadas. Ele permite entender os principais indicadores do mercado de 
    crédito, auxiliando na análise de tendências e na tomada de decisões estratégicas.
""")

# Indicadores Gerais
with tab1:
    st.subheader("Indicadores Gerais")
    st.markdown(f"**{indicador_selecionado} (em R$ ou %)**")
    st.line_chart(df_filtrado["valor"], height=250, use_container_width=True)

# Carteiras de Crédito
with tab2:
    st.subheader("Carteiras de Crédito")
    st.markdown(f"**{indicador_selecionado} (em R$ ou %)**")
    st.line_chart(df_filtrado["valor"], height=250, use_container_width=True)

# Operações de Cartão de Crédito
with tab3:
    st.subheader("Operações de Cartão de Crédito")
    st.markdown(f"**{indicador_selecionado} (em R$ ou %)**")
    st.line_chart(df_filtrado["valor"], height=250, use_container_width=True)

# Conclusão
with tab4:
    st.subheader("Conclusão")
    st.write("""
    Este dashboard proporciona uma visão abrangente do uso de cartões de crédito no Brasil, destacando os principais 
    indicadores relacionados ao crédito rotativo, inadimplência, tipos de crédito (parcelado e à vista) e transações realizadas. 
    Esses dados permitem avaliar o panorama do crédito e as condições do mercado, proporcionando insights valiosos sobre os comportamentos 
    de consumo e os desafios enfrentados pelos consumidores brasileiros.
    """)
