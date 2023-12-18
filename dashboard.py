import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
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
    mapa_mundi = mapa_mundi.to_crs(epsg=4326)

    # Criar uma máscara booleana para os pontos que intersectam com o mapa_mundi
    mask = gdf.geometry.intersects(mapa_mundi.unary_union)

    # Aplicar a máscara ao GeoDataFrame
    gdf = gdf[mask]

    # Agregação na geometria por país
    gdf_aggregated = gdf.dissolve(by='Country Label', aggfunc='mean').reset_index()

    st.title('Dashboard de dados da qualidade do ar')

    # Criar gráfico de pizza com os principais poluentes
    poluentes_frequentes = gdf['Pollutant'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(poluentes_frequentes, labels=poluentes_frequentes.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Assegura que o gráfico seja desenhado como um círculo.

    st.pyplot(fig)
    
if __name__ == '__main__':
    main()
