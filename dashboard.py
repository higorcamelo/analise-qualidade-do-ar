import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go


def plot_pizza_chart(poluentes_agrupados):
    fig = px.pie(
        names=poluentes_agrupados.index,
        values=poluentes_agrupados.values,
        title='Principais Poluentes',
        template='seaborn'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_top_cidades(gdf):
    top_cidades = gdf.nlargest(10, 'Value')[['City', 'Value']]
    fig = px.bar(
        top_cidades,
        x='Value',
        y='City',
        orientation='h',
        title='Top 10 Cidades mais Poluídas',
        labels={'Value': 'Índice de Poluição'}
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_contribuicao_pais(gdf):
    contribuicao_pais = gdf.groupby(['Country Label', 'Pollutant']).mean().reset_index()
    fig = px.bar(
        contribuicao_pais,
        x='Value',
        y='Country Label',
        color='Pollutant',
        orientation='h',
        title='Contribuição de Cada País para a Poluição',
        labels={'Value': 'Índice de Poluição'}
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    """
    Este script lê um arquivo geojson contendo dados de qualidade do ar e cria um dashboard com eles.
    """
    gdf = gpd.read_file('data/processado/geo_data.geojson')
    mapa_mundi = gpd.read_file('data/processado/mapa_mundi.shp')
    mapa_mundi.crs = "EPSG:4326"
    gdf.crs = "EPSG:4326"

    gdf = gdf.to_crs(epsg=4326)
    mapa_mundi = mapa_mundi.to_crs(epsg=4326) # TODO: FAZER MAPA COM OS PAÍSES

    st.title('Dashboard de dados da qualidade do ar')

    # Calcular a frequência de cada poluente
    poluentes_frequentes = gdf['Pollutant'].value_counts(normalize=True)

    # Agrupar poluentes com menos de 5% em um grupo chamado "Outros"
    threshold = 0.05
    poluentes_agrupados = poluentes_frequentes.copy()
    poluentes_agrupados[poluentes_agrupados < threshold] = 'Outros'

    # Mapear descrições dos poluentes
    descricao_poluentes = {
        'PM10': 'Material particulado fino (partículas com diâmetro menor que 10 micrômetros)',
        'NO': 'Óxido nítrico',
        'PM2.5': 'Material particulado fino (partículas com diâmetro menor que 2.5 micrômetros)',
        'O3': 'Ozônio',
        'CO': 'Monóxido de carbono',
        'NO2': 'Dióxido de nitrogênio'
    }

    # Ordenar o ranking de cidades mais poluídas
    gdf = gdf.sort_values(by='Value', ascending=False)

    # Adicionando seletor para escolher o tipo de gráfico
    opcao_grafico = st.selectbox('Escolha um gráfico:', ['Principais Poluentes', 'Top 10 Cidades', 'Contribuição por País'])

    # Plotar os gráficos conforme a escolha
    if opcao_grafico == "Principais Poluentes":
        plot_pizza_chart(poluentes_agrupados)
    elif opcao_grafico == "Top 10 Cidades":
        plot_top_cidades(gdf)
    elif opcao_grafico == "Contribuição por País":
        plot_contribuicao_pais(gdf)


if __name__ == '__main__':
    main()
