import plotly.express as px
import streamlit as st

def plot_media_notas(df):
    media_notas = df.groupby('genero_principal')['rating_imdb'].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(media_notas, x='genero_principal', y='rating_imdb',
                 color='rating_imdb', color_continuous_scale='Blues',
                 labels={'genero_principal': 'Gênero', 'rating_imdb': 'Nota Média'},
                 title="Média das Notas IMDb")
    st.plotly_chart(fig, use_container_width=True)

def plot_arrecadacao(df):
    arrecadacao = df.groupby('genero_principal')['gross_world_wide'].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(arrecadacao, x='genero_principal', y='gross_world_wide',
                 color='gross_world_wide', color_continuous_scale='Greens',
                 labels={'genero_principal': 'Gênero', 'gross_world_wide': 'Arrecadação Mundial ($)'},
                 title="Soma da Arrecadação Mundial por Gênero")
    st.plotly_chart(fig, use_container_width=True)
    return arrecadacao
