import streamlit as st
import pandas as pd
from tmdb_cache_helper import buscar_filme_info_parallel

def recomendar_por_filmes_selecionados(df, filmes_escolhidos, max_recomendacoes=10):
    if not filmes_escolhidos:
        st.warning("Selecione ao menos um filme para receber recomendações.")
        return
    
    # Extrai os gêneros principais dos filmes escolhidos
    generos_escolhidos = df[df['title'].isin(filmes_escolhidos)]['genero_principal'].unique()

    # Filtra filmes do(s) mesmo(s) gênero(s) excluindo os já escolhidos
    df_recomendados = df[
        (df['genero_principal'].isin(generos_escolhidos)) & 
        (~df['title'].isin(filmes_escolhidos))
    ].sort_values(by='rating_imdb', ascending=False).head(max_recomendacoes * 3)

    if df_recomendados.empty:
        st.info("Nenhuma recomendação encontrada para os filmes escolhidos.")
        return
    
    # Busca informações detalhadas no TMDB (com cache e paralelo)
    filmes_com_info = buscar_filme_info_parallel(df_recomendados, max_busca=max_recomendacoes * 5)
    filmes_com_info = filmes_com_info[:max_recomendacoes]  # Limita ao máximo desejado

    if not filmes_com_info:
        st.warning("Nenhum filme com pôster e trailer encontrado para esse gênero.")
        return

    st.subheader("🎯 Recomendações baseadas nos seus filmes selecionados:")

    for filme, info in filmes_com_info:
        st.markdown(f"### {filme['title']} ({int(filme['year']) if pd.notnull(filme['year']) else '?'})")
        st.write(f"Nota IMDb: {filme['rating_imdb']}")
        if info.get("poster_url"):
            st.image(info["poster_url"], width=200)
        sinopse = info.get("overview", "Sinopse indisponível.")
        st.markdown(f"**Sinopse:** {sinopse}")
        trailer = info.get("trailer_url")
        if trailer:
            st.markdown(f"[▶️ Assista ao trailer]({trailer})")
        st.markdown("---")
