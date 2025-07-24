import streamlit as st
import pandas as pd
from tmdb_cache_helper import buscar_filme_info_parallel

def recomendar_filmes(df, genero_escolhido, num_sugestoes):
    df_filmes_genero = (
        df[df['genero_principal'] == genero_escolhido]
        .sort_values(by='rating_imdb', ascending=False)
        .dropna(subset=['rating_imdb'])
    )

    max_busca = min(num_sugestoes * 2, 30)

    with st.spinner("Carregando sugestões..."):
        filmes_com_info = buscar_filme_info_parallel(df_filmes_genero, max_busca=max_busca)

    if not filmes_com_info:
        st.warning("Nenhum filme com pôster e trailer encontrado para esse gênero.")
        return

    filmes_com_info = filmes_com_info[:num_sugestoes]  # garante a qtd desejada

    for filme, info in filmes_com_info:
        st.subheader(filme['title'])
        st.write(f"Ano: {int(filme['year']) if pd.notnull(filme['year']) else '?'}")
        st.write(f"Nota IMDb: {filme['rating_imdb']}")
        st.image(info.get("poster_url", ""), width=200)
        st.markdown(f"**Sinopse:** {info.get('overview', 'Sinopse indisponível.')}")
        trailer = info.get("trailer_url")
        if trailer:
            st.markdown(f"[Assista ao trailer]({trailer})")
        st.markdown("---")
