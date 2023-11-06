import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    """
    Este script lê um arquivo geojson contendo dados de qualidade do ar e os exibe em um mapa do Streamlit.
    """
    gdf = gpd.read_file('data/processado/geo_data.geojson')

    st.title('Dashboard de dados da qualidade do ar')

    st.map(gdf, latitude='Latitude', longitude='Longitude')

if __name__ == '__main__':
    main()
