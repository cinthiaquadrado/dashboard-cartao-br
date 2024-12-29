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
    "Valor Total das Transações com Cartões de Crédito": extracao_bcb(25229, '31/12/2010', '28/12/2024'),
    "Inadimplência - Cartão de Crédito Rotativo": extracao_bcb(21127, '01/03/2011', '28/12/2024'),
    "Inadimplência - Cartão de Crédito Parcelado": extracao_bcb(21128, '01/03/2011', '28/12/2024'),
    "Inadimplência - Cartão de Crédito Total": extracao_bcb(21129, '01/03/2011', '28/12/2024'),
    "Saldo do Crédito Rotativo": extracao_bcb(20587, '01/03/2007', '28/12/2024'),
    "Número de Cartões de Crédito Emitidos": extracao_bcb(25147, '31/12/2010', '28/12/2024'),
    "Número de Cartões de Crédito Ativos": extracao_bcb(25149, '31/12/2010', '28/12/2024'),
    "Taxa média de juros - Cartão de crédito total": extracao_bcb(22024, '01/03/2007', '28/12/2024'),
    "Saldo da Carteira - Cartão de Crédito Parcelado": extracao_bcb(20588, '01/03/2007', '28/12/2024'),
    "Saldo da Carteira - Cartão de Crédito à Vista": extracao_bcb(20589, '01/03/2007', '28/12/2024'),
    "Saldo da Carteira - Cartão de Crédito Total": extracao_bcb(20590, '01/03/2007', '28/12/2024')
}

# Layout do dashboard
st.title("📊 Panorama do Uso de Cartões de Crédito no Brasil")

# Texto inicial explicativo
st.markdown("""
    Este dashboard apresenta uma análise sobre o uso de cartões de crédito por pessoas físicas no Brasil, 
    com o objetivo de fornecer informações atualizadas sobre a evolução do crédito rotativo, inadimplência, 
    as carteiras de crédito e as operações realizadas. Ele permite entender os principais indicadores do mercado de 
    crédito, auxiliando na análise de tendências e na tomada de decisões estratégicas.
""")

# Função para exibir gráficos e tabelas com unidades e títulos
def exibir_indicador(titulo, dados, unidade):
    st.subheader(titulo)
    st.markdown(f"**Unidade:** {unidade}")
    if dados.empty:
        st.warning(f"Não há dados disponíveis para o indicador: {titulo}")
    else:
        st.line_chart(dados['valor'], height=250, use_container_width=True)
        st.write(dados.tail(5))  # Exibe os 5 dados mais recentes

# Ordem lógica de indicadores
indicadores = [
    ("Número de Cartões de Crédito Emitidos", dados["Número de Cartões de Crédito Emitidos"], "unidades (milhões)"),
    ("Número de Cartões de Crédito Ativos", dados["Número de Cartões de Crédito Ativos"], "unidades (milhões)"),
    ("Valor Total das Transações com Cartões de Crédito", dados["Valor Total das Transações com Cartões de Crédito"], "R$ milhões"),
    ("Saldo da Carteira - Cartão de Crédito Total", dados["Saldo da Carteira - Cartão de Crédito Total"], "R$ milhões"),
    ("Saldo da Carteira - Cartão de Crédito à Vista", dados["Saldo da Carteira - Cartão de Crédito à Vista"], "R$ milhões"),
    ("Saldo da Carteira - Cartão de Crédito Parcelado", dados["Saldo da Carteira - Cartão de Crédito Parcelado"], "R$ milhões"),
    ("Taxa média de juros - Cartão de crédito total", dados["Taxa média de juros - Cartão de crédito total"], "% a.a."),
    ("Inadimplência - Cartão de Crédito Total", dados["Inadimplência - Cartão de Crédito Total"], "%"),
    ("Inadimplência - Cartão de Crédito Rotativo", dados["Inadimplência - Cartão de Crédito Rotativo"], "%"),
    ("Inadimplência - Cartão de Crédito Parcelado", dados["Inadimplência - Cartão de Crédito Parcelado"], "%")
]

# Exibindo indicadores na ordem lógica
for titulo, indicador, unidade in indicadores:
    exibir_indicador(titulo, indicador, unidade)
