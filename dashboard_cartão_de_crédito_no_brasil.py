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
    st.markdown("""
        **1. Saldo do Crédito Rotativo (em R$)**
        Este indicador mostra o saldo total da utilização do crédito rotativo em cartões de crédito por pessoas físicas no Brasil.
    """)
    if "Saldo do Crédito Rotativo" in dados:
        st.line_chart(dados["Saldo do Crédito Rotativo"]["valor"], height=250, use_container_width=True)

    st.markdown("""
        **2. Taxa de Inadimplência (15 a 90 dias)**
        A taxa de inadimplência é a porcentagem de crédito que está em atraso de 15 a 90 dias.
    """)
    if "Taxa de Inadimplência (15 a 90 dias)" in dados:
        st.line_chart(dados["Taxa de Inadimplência (15 a 90 dias)"]["valor"], height=250, use_container_width=True)

    st.markdown("""
        **3. Taxa de Inadimplência (>90 dias)**
        A taxa de inadimplência superior a 90 dias indica o percentual de crédito vencido por mais de 90 dias.
    """)
    if "Taxa de Inadimplência (>90 dias)" in dados:
        st.line_chart(dados["Taxa de Inadimplência (>90 dias)"]["valor"], height=250, use_container_width=True)

# Carteiras de Crédito
with tab2:
    st.subheader("Carteiras de Crédito")
    st.markdown("""
        **1. Saldo da Carteira - Cartão de Crédito Parcelado (em R$)**
        Este indicador mostra o saldo da carteira de crédito relacionada ao pagamento parcelado dos cartões de crédito.
    """)
    if "Saldo da carteira - Cartão de crédito parcelado" in dados:
        st.line_chart(dados["Saldo da carteira - Cartão de crédito parcelado"]["valor"], height=250, use_container_width=True)

    st.markdown("""
        **2. Saldo da Carteira - Cartão de Crédito à Vista (em R$)**
        Refere-se ao saldo da carteira de crédito para transações realizadas à vista com o cartão de crédito.
    """)
    if "Saldo da carteira - Cartão de crédito à vista" in dados:
        st.line_chart(dados["Saldo da carteira - Cartão de crédito à vista"]["valor"], height=250, use_container_width=True)

    st.markdown("""
        **3. Saldo da Carteira - Cartão de Crédito Total (em R$)**
        Este indicador soma o saldo total da carteira de crédito dos cartões de crédito, considerando tanto as transações à vista quanto as parceladas.
    """)
    if "Saldo da carteira - Cartão de crédito total" in dados:
        st.line_chart(dados["Saldo da carteira - Cartão de crédito total"]["valor"], height=250, use_container_width=True)

# Operações de Cartão de Crédito
with tab3:
    st.subheader("Operações de Cartão de Crédito")
    st.markdown("""
        **1. Valor Total das Transações com Cartões de Crédito (em R$)**
        Mostra o valor total movimentado nas transações realizadas com cartões de crédito em determinado período.
    """)
    if "Valor total das transações com cartões de crédito" in dados:
        st.line_chart(dados["Valor total das transações com cartões de crédito"]["valor"], height=250, use_container_width=True)

    st.markdown("""
        **2. Taxa de Juros do Cartão de Crédito (%)**
        A taxa de juros média aplicada nas transações de cartão de crédito no Brasil, afetando tanto as compras à vista quanto parceladas.
    """)
    if "Taxa de Juros do Cartão de Crédito" in dados:
        st.line_chart(dados["Taxa de Juros do Cartão de Crédito"]["valor"], height=250, use_container_width=True)

# Conclusão
with tab4:
    st.subheader("Conclusão")
    st.write("""
    Este dashboard proporciona uma visão abrangente do uso de cartões de crédito no Brasil, destacando os principais 
    indicadores relacionados ao crédito rotativo, inadimplência, tipos de crédito (parcelado e à vista) e transações realizadas. 
    Esses dados permitem avaliar o panorama do crédito e as condições do mercado, proporcionando insights valiosos sobre os comportamentos 
    de consumo e os desafios enfrentados pelos consumidores brasileiros.
    """)
