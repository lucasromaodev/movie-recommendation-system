import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)
def carregar_dados(caminho_csv):
    def extrair_genero_principal(generos):
        principais = ["Horror", "Drama", "Comedy", "Action"]
        for g in principais:
            if g.lower() in str(generos).lower():
                return g
        return str(generos).split(",")[0].strip() if pd.notnull(generos) else None

    df = pd.read_csv(caminho_csv)
    df['genero_principal'] = df['genre'].apply(extrair_genero_principal)
    df['rating_imdb'] = pd.to_numeric(df['rating_imdb'], errors='coerce')
    df['gross_world_wide'] = pd.to_numeric(df['gross_world_wide'], errors='coerce')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    return df[df['genero_principal'].notnull()]
