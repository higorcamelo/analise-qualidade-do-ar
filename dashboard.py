import streamlit as st
import geopandas as gpd
import folium

def main():
    """
    Este script lê um arquivo geojson contendo dados de qualidade do ar e os exibe em um mapa do Folium.
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

    # Agregação na geometria
    gdf_aggregated = gdf.dissolve(by='geometry', aggfunc='mean').reset_index()

    st.title('Dashboard de dados da qualidade do ar')

    # Criar um mapa Folium centrado em uma localização média
    m = folium.Map(location=[gdf_aggregated['Latitude'].mean(), gdf_aggregated['Longitude'].mean()], zoom_start=5)

    # Adicionar marcadores ao mapa para cada país no GeoDataFrame agregado
    for idx, row in gdf_aggregated.iterrows():
        # Use as informações relevantes ao nível do país
        country_info = f"País: {row['Country']} - Média de Poluição: {row['Value'].mean():.2f} µg/m³"
        folium.Marker([row['Latitude'], row['Longitude']], popup=country_info).add_to(m)
        # Exibir o mapa no Streamlit
        folium_static(m)

if __name__ == '__main__':
    main()
