import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    """
    Este script lê um arquivo geojson contendo dados de qualidade do ar e os exibe em um mapa do Streamlit.
    """
    gdf = gpd.read_file('data/processado/geo_data.geojson')
    mapa_subdivisoes = gpd.read_file('data/processado/mapa_subdivisoes.shp')
    mapa_subdivisoes.crs = "EPSG:4326"
    gdf.crs = "EPSG:4326"

    gdf = gdf.to_crs(epsg=4326)
    mapa_subdivisoes = mapa_subdivisoes.to_crs(epsg=4326)

    gdf = gpd.sjoin(gdf, mapa_subdivisoes, how="inner", predicate="intersects")

    st.title('Dashboard de dados da qualidade do ar')

    st.map(gdf, latitude='Latitude', longitude='Longitude')

if __name__ == '__main__':
    main()
