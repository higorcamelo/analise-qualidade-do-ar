import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import folium

def main():
    """
    Este script lê um arquivo geojson contendo dados de qualidade do ar e cria um dashboard com eles.
    """
    gdf = gpd.read_file('data/processado/geo_data.geojson')
    mapa_mundi = gpd.read_file('data/processado/mapa_mundi.shp')
    mapa_mundi.crs = "EPSG:4326"
    gdf.crs = "EPSG:4326"

    gdf = gdf.to_crs(epsg=4326)
    mapa_mundi = mapa_mundi.to_crs(epsg=4326) #TODO: FAZER MAPA COM OS PAÍSES

    st.title('Dashboard de dados da qualidade do ar')

    # Calcular a frequência de cada poluente
    poluentes_frequentes = gdf['Pollutant'].value_counts(normalize=True)

    # Agrupar poluentes com menos de 5% em um grupo chamado "Outros"
    threshold = 0.05
    poluentes_agrupados = poluentes_frequentes.copy()
    poluentes_agrupados[poluentes_agrupados < threshold] = 'Outros'

    # Criar o gráfico de pizza com Plotly Express
    fig = px.pie(names=poluentes_agrupados.index, values=poluentes_agrupados.values, title='Principais Poluentes')
    st.plotly_chart(fig)
    
if __name__ == '__main__':
    main()
