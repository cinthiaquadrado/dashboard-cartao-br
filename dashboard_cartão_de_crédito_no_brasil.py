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

# Função para exibir os indicadores
def exibir_indicador(titulo, indicador, unidade):
    # Exibe o título do indicador
    st.subheader(titulo)
    
    # Exibe o gráfico do indicador
    st.line_chart(indicador)
    
    # Verifica se o indicador não está vazio e pega o último valor
    if not indicador.empty:
        ultimo_valor = indicador.iloc[-1]  # Acessa o último valor da Series
        
        # Verifica se o último valor é NaN
        if pd.isna(ultimo_valor):
            st.markdown(f"Último valor: Não disponível ({unidade})")
        else:
            st.markdown(f"Último valor: {ultimo_valor:.2f} {unidade}")
    else:
        st.markdown(f"Dados não disponíveis para {titulo} ({unidade})")

# Layout do dashboard
st.title("📊 Panorama do Uso de Cartões de Crédito no Brasil")

# Texto inicial explicativo
st.markdown("""
    Este dashboard apresenta uma análise sobre o uso de cartões de crédito por pessoas físicas no Brasil, 
    com o objetivo de fornecer informações atualizadas sobre a evolução do crédito rotativo, inadimplência, 
    as carteiras de crédito e as operações realizadas. Ele permite entender os principais indicadores do mercado de 
    crédito, auxiliando na análise de tendências e na tomada de decisões estratégicas.
""")

# Seção de Visão Geral
st.subheader("📈 Visão Geral do Mercado de Cartões de Crédito")
st.markdown("""
    Os cartões de crédito são um dos principais meios de pagamento no Brasil. A análise a seguir mostra o panorama geral 
    sobre o número de cartões emitidos e ativos, além das transações realizadas.
""")

# Indicadores da visão geral
indicadores_visao_geral = [
    ("Número de Cartões de Crédito Emitidos", dados["Número de Cartões de Crédito Emitidos"], "unidades (milhões)"),
    ("Número de Cartões de Crédito Ativos", dados["Número de Cartões de Crédito Ativos"], "unidades (milhões)"),
    ("Valor Total das Transações com Cartões de Crédito", dados["Valor Total das Transações com Cartões de Crédito"], "R$ milhões")
]

for titulo, indicador, unidade in indicadores_visao_geral:
    exibir_indicador(titulo, indicador, unidade)

# Seção de Carteira de Crédito
st.subheader("💳 Carteira de Crédito com Cartões de Crédito")
st.markdown("""
    A carteira de crédito reflete o saldo total que os consumidores possuem em seus cartões. A seguir, mostramos a 
    divisão entre crédito parcelado e à vista.
""")

# Indicadores da carteira de crédito
indicadores_carteira_credito = [
    ("Saldo da Carteira - Cartão de Crédito Total", dados["Saldo da Carteira - Cartão de Crédito Total"], "R$ milhões"),
    ("Saldo da Carteira - Cartão de Crédito à Vista", dados["Saldo da Carteira - Cartão de Crédito à Vista"], "R$ milhões"),
    ("Saldo da Carteira - Cartão de Crédito Parcelado", dados["Saldo da Carteira - Cartão de Crédito Parcelado"], "R$ milhões")
]

for titulo, indicador, unidade in indicadores_carteira_credito:
    exibir_indicador(titulo, indicador, unidade)

# Seção de Juros e Inadimplência
st.subheader("💡 Juros e Inadimplência no Crédito")
st.markdown("""
    A seguir, apresentamos as taxas médias de juros e a inadimplência, que refletem o comportamento dos consumidores 
    no uso do crédito e as dificuldades financeiras associadas.
""")

# Indicadores de juros e inadimplência
indicadores_juros_inadimplencia = [
    ("Taxa média de juros - Cartão de crédito total", dados["Taxa média de juros - Cartão de crédito total"], "% a.a."),
    ("Inadimplência - Cartão de Crédito Total", dados["Inadimplência - Cartão de Crédito Total"], "%"),
    ("Inadimplência - Cartão de Crédito Rotativo", dados["Inadimplência - Cartão de Crédito Rotativo"], "%"),
    ("Inadimplência - Cartão de Crédito Parcelado", dados["Inadimplência - Cartão de Crédito Parcelado"], "%")
]

for titulo, indicador, unidade in indicadores_juros_inadimplencia:
    exibir_indicador(titulo, indicador, unidade)

