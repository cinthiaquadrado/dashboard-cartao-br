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
    "Taxa de Inadimplência (>90 dias)": extracao_bcb(7934, '30/06/2000', '31/12/2012'),  # Inadimplência (>90 dias)
    "Saldo da carteira - Cartão de crédito parcelado": extracao_bcb(20588, '01/03/2007', '28/12/2024'),
    "Saldo da carteira - Cartão de crédito à vista": extracao_bcb(20589, '01/03/2007', '28/12/2024'),
    "Saldo da carteira - Cartão de crédito total": extracao_bcb(20590, '01/03/2007', '28/12/2024'),
    "Número de Cartões de Crédito Emitidos": extracao_bcb(25147, '31/12/2010', '28/12/2024'),  # Número de cartões emitidos
    "Número de Cartões de Crédito Ativos": extracao_bcb(25149, '31/12/2010', '28/12/2024'),  # Número de cartões ativos
    "Valor total das transações com cartões de crédito": extracao_bcb(25229, '31/12/2010', '28/12/2024'),
    "Taxa média de juros - Cartão de crédito total": extracao_bcb(22024, '01/03/2007', '28/12/2024'),  # Taxa de juros do cartão
}

# Layout do dashboard
st.title("Dashboard: Panorama do Uso de Cartões de Crédito no Brasil")

# Texto inicial explicativo
st.markdown("""
    Este dashboard apresenta uma análise detalhada sobre o uso de cartões de crédito por pessoas físicas no Brasil, 
    com o objetivo de fornecer informações atualizadas sobre a evolução do crédito rotativo, inadimplência, 
    as carteiras de crédito e as operações realizadas. Ele permite entender os principais indicadores do mercado de 
    crédito, auxiliando na análise de tendências e na tomada de decisões estratégicas.
""")

# Filtros para interatividade (se necessário, com base nas suas preferências)
data_inicio = st.date_input("Data de Início", pd.to_datetime('2010-01-01'))
data_fim = st.date_input("Data de Fim", pd.to_datetime('2024-12-28'))

# Função para exibir gráficos e tabelas com unidades e títulos
def exibir_indicador(titulo, dados, unidade):
    st.subheader(titulo)
    st.markdown(f"**Unidade:** {unidade}")
    if dados.empty:
        st.warning(f"Não há dados disponíveis para o indicador: {titulo}")
    else:
        st.line_chart(dados['valor'], height=250, use_container_width=True)
        st.write(dados.head())

# Títulos e Unidades para cada indicador
indicadores = [
    ("Saldo do Crédito Rotativo", dados["Saldo do Crédito Rotativo"], "R$ milhões"),
    ("Taxa de Inadimplência (15 a 90 dias)", dados["Taxa de Inadimplência (15 a 90 dias)"], "%"),
    ("Taxa de Inadimplência (>90 dias)", dados["Taxa de Inadimplência (>90 dias)"], "%"),
    ("Saldo da Carteira - Cartão de Crédito Parcelado", dados["Saldo da carteira - Cartão de crédito parcelado"], "R$ milhões"),
    ("Saldo da Carteira - Cartão de Crédito à Vista", dados["Saldo da carteira - Cartão de crédito à vista"], "R$ milhões"),
    ("Saldo da Carteira - Cartão de Crédito Total", dados["Saldo da carteira - Cartão de crédito total"], "R$ milhões"),
    ("Número de Cartões de Crédito Emitidos", dados["Número de Cartões de Crédito Emitidos"], "unidades (milhões)"),
    ("Número de Cartões de Crédito Ativos", dados["Número de Cartões de Crédito Ativos"], "unidades (milhões)"),
    ("Valor Total das Transações com Cartões de Crédito", dados["Valor total das transações com cartões de crédito"], "R$ milhões"),
    ("Taxa média de juros - Cartão de crédito total", dados["Taxa de Juros do Cartão de Crédito"], "% a.a.")
]

# Exibindo indicadores
for titulo, indicador, unidade in indicadores:
    exibir_indicador(titulo, indicador, unidade)

# Resumo final
st.markdown("## Resumo Final")
st.write("""
    O painel proporciona uma visão abrangente do uso de cartões de crédito no Brasil, destacando os principais 
    indicadores relacionados ao crédito rotativo, inadimplência, tipos de crédito (parcelado e à vista) e transações realizadas. 
    Esses dados permitem avaliar o panorama do crédito e as condições do mercado, proporcionando insights valiosos sobre os comportamentos 
    de consumo e os desafios enfrentados pelos consumidores brasileiros.
""")

# Exibir dados mais atuais (últimos valores)
st.markdown("### Dados Mais Recentes")
for titulo, indicador, unidade in indicadores:
    st.markdown(f"**{titulo}**: {indicador['valor'].iloc[-1]:.2f} {unidade}")
