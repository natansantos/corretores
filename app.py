import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

# Carregar os dados da planilha
@st.cache_data(show_spinner=False, ttl=0)  # Desativa o cache temporariamente
def load_data():
    df = pd.read_excel("DADOS_ATUALIZADO.xlsx")
    return df

def main():
    st.title("Análise de Corretores por Cidade - Estado BA")

    # Carregar os dados
    data = load_data()

    # Remover cidades que não possuem latitude e longitude
    data = data.dropna(subset=['Latitude', 'Longitude'])

    # Remover as seções de cabeçalho e nomes das colunas
    # Exibir o cabeçalho do arquivo para verificar as colunas
    # st.subheader("Cabeçalho do Arquivo")
    # st.write(data.head())

    # Exibir o cabeçalho do arquivo atualizado para verificar as colunas
    # st.subheader("Cabeçalho do Arquivo Atualizado")
    # st.write(data.head())

    # Exibir os nomes das colunas do DataFrame
    # st.subheader("Nomes das Colunas do Arquivo Atualizado")
    # st.write(data.columns.tolist())

    # Filtrar apenas cidades do estado BA
    data_ba = data[data['UF'] == 'BA']

    # Ajustar o agrupamento para incluir REGULAR e IRREGULAR
    corretores_por_cidade = data_ba[['CIDADE', 'QUANTIDADE', 'REGULAR', 'IRREGULAR', 'Latitude', 'Longitude']].groupby(
        ['CIDADE', 'Latitude', 'Longitude']
    ).sum().reset_index()

    # Exibir o DataFrame
    st.subheader("Pessoa Física")
    st.dataframe(corretores_por_cidade)

    # Filtrar apenas cidades com quantidade mínima de corretores
    quantidade_minima = st.slider("Quantidade mínima de corretores para exibir no mapa", min_value=1, max_value=100, value=10)
    corretores_por_cidade = corretores_por_cidade[corretores_por_cidade['QUANTIDADE'] >= quantidade_minima]

    # Verificar se as colunas de latitude e longitude existem
    if 'Latitude' in data_ba.columns and 'Longitude' in data_ba.columns:
        # Criar o mapa interativo
        st.subheader("Mapa Interativo")
        mapa = folium.Map(location=[-13.5, -41.5], zoom_start=6)  # Coordenadas aproximadas do estado da Bahia

        # Adicionar marcadores para todas as cidades no DataFrame filtrado
        for _, row in corretores_por_cidade.iterrows():
            cidade = row['CIDADE']
            quantidade = row['QUANTIDADE']
            latitude = row['Latitude']
            longitude = row['Longitude']

            folium.Marker(
                location=[latitude, longitude],
                popup=f"{cidade}: {quantidade} corretores<br>Regulares: {row['REGULAR']}<br>Irregulares: {row['IRREGULAR']}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(mapa)

        # Adicionar funcionalidade de tela cheia ao mapa
        Fullscreen().add_to(mapa)

        # Renderizar o mapa no Streamlit
        st_folium(mapa, width=700, height=500)
    else:
        st.error("O arquivo DADOS.xlsx precisa conter as colunas 'Latitude' e 'Longitude' para exibir o mapa corretamente.")

if __name__ == "__main__": 
    main()