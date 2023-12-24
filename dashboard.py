import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

def plot_dashboard(gdf):
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

    # Gráfico de Pizza
    fig_pizza = px.pie(
        names=poluentes_agrupados.index,
        values=poluentes_agrupados.values,
        title='Principais Poluentes',
        template='seaborn'
    )

    # Gráfico das Top 10 Cidades
    top_cidades = gdf.nlargest(10, 'Value')[['City', 'Value']]
    fig_top_cidades = px.bar(
        top_cidades,
        x='Value',
        y='City',
        orientation='h',
        title='Top 10 Cidades mais Poluídas',
        labels={'Value': 'Índice de Poluição'}
    )

    # Gráfico de Contribuição por País
    contribuicao_pais = gdf.groupby('Country Label')['Value'].mean().reset_index()
    top_paises = contribuicao_pais.nlargest(10, 'Value')

    fig_contribuicao_pais = px.bar(
        top_paises,
        x='Value',
        y='Country Label',
        orientation='h',
        title='Top 10 Países mais Poluídos',
        labels={'Value': 'Índice de Poluição'},
    )

    # Exibir gráficos no layout do dashboard
    st.plotly_chart(fig_pizza, use_container_width=True)
    st.plotly_chart(fig_top_cidades, use_container_width=True)
    st.plotly_chart(fig_contribuicao_pais, use_container_width=True)

    # Novos gráficos adicionados
    # Histograma de Valores
    fig_histograma = px.histogram(
        gdf,
        x='Value',
        nbins=50,
        title='Distribuição de Valores de Poluição',
        labels={'Value': 'Índice de Poluição'}
    )
    st.plotly_chart(fig_histograma, use_container_width=True)

    # Mapa de Calor da Poluição por País
    fig_mapa_calor = px.density_mapbox(
        gdf,
        lat='Latitude',
        lon='Longitude',
        z='Value',
        radius=10,
        title='Mapa de Calor da Poluição por País',
        labels={'Value': 'Índice de Poluição'},
        mapbox_style='open-street-map',
        center={'lat': gdf['Latitude'].mean(), 'lon': gdf['Longitude'].mean()},
        zoom=2
    )
    st.plotly_chart(fig_mapa_calor, use_container_width=True)

def main():
    """
    Este script lê um arquivo geojson contendo dados de qualidade do ar e cria um dashboard com eles.
    """
    gdf = gpd.read_file('data/processado/geo_data.geojson')
    mapa_mundi = gpd.read_file('data/processado/mapa_mundi.shp')
    mapa_mundi.crs = "EPSG:4326"
    gdf.crs = "EPSG:4326"

    gdf = gdf.to_crs(epsg=4326)
    mapa_mundi = mapa_mundi.to_crs(epsg=4326)  # TODO: FAZER MAPA COM OS PAÍSES

    st.title('Análise de dados da qualidade do ar')

    # Adicionando a barra lateral retrátil
    with st.sidebar:
        st.header("Opções de Filtro")
        # Adicionar filtros por país, poluente e unidade
        paises_filtrar_todos = ['Todos'] + list(gdf['Country Label'].unique())
        pais_filtro = st.selectbox("Selecione o País", paises_filtrar_todos)
        poluentes_filtrar_todos = ['Todos'] + list(gdf['Pollutant'].unique())
        poluente_filtro = st.selectbox("Selecione o Poluente", poluentes_filtrar_todos)
        unidades_filtrar_todos = ['Todos'] + list(gdf['Unit'].unique())
        unidade_filtro = st.selectbox("Selecione a Unidade", unidades_filtrar_todos)
        
    # Aplicar filtros apenas se a opção não for "Todos"
    if pais_filtro != 'Todos':
        gdf = gdf[gdf['Country Label'] == pais_filtro]

    if poluente_filtro != 'Todos':
        gdf = gdf[gdf['Pollutant'] == poluente_filtro]

    if unidade_filtro != 'Todos':
        gdf = gdf[gdf['Unit'] == unidade_filtro]


    # Chamar função para plotar o dashboard
    plot_dashboard(gdf)

if __name__ == '__main__':
    main()
