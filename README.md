# Análise de Qualidade do Ar

Este projeto realiza uma análise abrangente da qualidade do ar em diferentes partes do mundo. Os dados são visualizados em um dashboard interativo e informativo, destacando os principais poluentes, as cidades mais poluídas e os países com maiores índices de poluição.

## Dashboard

O dashboard inclui os seguintes elementos:

1. **Principais Poluentes:** Um gráfico de pizza que mostra a distribuição percentual dos principais poluentes, destacando aqueles que contribuem significativamente para a poluição do ar.

2. **Top 10 Cidades mais Poluídas:** Um gráfico de barras horizontais que apresenta as 10 cidades com os maiores índices de poluição, permitindo uma visão rápida das áreas mais afetadas.

3. **Top 10 Países mais Poluídos:** Um gráfico de barras horizontais que destaca os 10 países com os maiores índices de poluição, proporcionando insights sobre padrões globais.

4. **Distribuição de Valores de Poluição:** Um histograma que mostra a distribuição dos índices de poluição, ajudando a identificar tendências e outliers.

5. **Mapa de Calor da Poluição por País:** Um mapa de calor interativo que ilustra a distribuição geográfica da poluição, destacando regiões com maiores concentrações.

## Tratamento de Dados

Os dados brutos são tratados para garantir sua qualidade e consistência. Isso inclui a remoção de valores nulos, a correção de coordenadas geográficas e a identificação e tratamento de outliers. Os valores discrepantes são substituídos pela mediana dos respectivos países.

## Bibliotecas Utilizadas

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [GeoPandas](https://geopandas.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)

## Dados

Os dados utilizados neste projeto foram obtidos do [Kaggle]([inserir-link-fonte-dados](https://www.kaggle.com/datasets/imtkaggleteam/world-air-quality)https://www.kaggle.com/datasets/imtkaggleteam/world-air-quality).

---
 
