import streamlit as st
from data_loader import carregar_dados
from analysis import plot_media_notas, plot_arrecadacao
from recommendations import recomendar_filmes
from catalog import recomendar_por_filmes_selecionados


CAMINHO_CSV = r"C:\Users\luckh\Desktop\Automações\Projetos Pessoais\filmes\world_imdb_movies_top_movies_per_year.csv"

st.set_page_config(page_title="Análise e Descoberta de Filmes", layout="wide")
st.title("🎥 Análise e Descoberta de Filmes IMDb")

with st.spinner('Carregando dados...'):
    df = carregar_dados(CAMINHO_CSV)

aba_analise, aba_recomendacao, aba_catalogo = st.tabs([
    "📊 Análise de Gêneros",
    "🎬 Descubra Filmes",
    "📚 Catálogo Interativo"
])


with aba_analise:
    st.header("📊 Análise Comparativa por Gênero")
    qtd = st.slider("Quantidade de filmes na amostragem:", 10, 1000, 100)
    generos_disponiveis = sorted(df['genero_principal'].unique())
    generos_selecionados = st.multiselect("Selecione gêneros para análise:", generos_disponiveis,
                                          default=["Drama", "Comedy", "Horror", "Action"])
    min_ano, max_ano = int(df['year'].min()), int(df['year'].max())
    anos = st.slider("Filtrar por ano de lançamento:", min_ano, max_ano, (2000, 2020))

    df_filtrado = df[
        df['genero_principal'].isin(generos_selecionados) &
        df['year'].between(anos[0], anos[1])
    ]
    df_amostrado = df_filtrado.sample(n=min(qtd, len(df_filtrado)), random_state=42)

    st.subheader("🎯 Amostragem de Filmes")
    with st.expander("🔍 Ver dados da amostra"):
        st.dataframe(df_amostrado[['title', 'year', 'rating_imdb', 'gross_world_wide', 'genero_principal']],
                     use_container_width=True)

    st.subheader("⭐ Nota Média IMDb por Gênero")
    plot_media_notas(df_amostrado)

    st.markdown("""
    🎭 **Por que filmes de Drama têm notas mais altas?**  
    Narrativas complexas, foco em emoções e atuações fortes são valorizados por público e crítica.
    """)

    st.subheader("💰 Arrecadação Mundial por Gênero")
    arrecadacao = plot_arrecadacao(df_amostrado)

    if not arrecadacao.empty:
        genero_top = arrecadacao.iloc[0]['genero_principal']
        valor_top = arrecadacao.iloc[0]['gross_world_wide']
        st.markdown(f"""
        💡 **Curiosidade:**  
        O gênero mais rentável na amostragem atual é **{genero_top}**, com arrecadação de **${valor_top:,.2f}**.
        """)

    with st.expander("📚 Explicações e Insights por Gênero"):
        st.markdown("""
        - 🎭 **Drama**: Narrativas profundas, forte impacto emocional.
        - 🎬 **Action**: Grandes franquias e blockbusters.
        - 😱 **Horror**: Baixo custo, alto retorno.
        - 🤡 **Comedy**: Popular e acessível, nem sempre com notas altas.
        - Outros gêneros podem ser explorados também.
        """)

with aba_recomendacao:
    st.header("🎯 Descubra Filmes para Assistir por Gênero")
    generos_recomendacao = sorted(df['genero_principal'].dropna().unique())
    genero_escolhido = st.selectbox("Escolha um gênero:", generos_recomendacao)
    num_sugestoes = st.slider("Quantos filmes deseja ver?", 3, 15, 5)

    recomendar_filmes(df, genero_escolhido, num_sugestoes)
    
    
with aba_catalogo:
    st.header("📚 Catálogo Interativo de Filmes")
    st.markdown("Selecione filmes do catálogo e clique em **Recomendar** para receber sugestões baseadas neles.")

    filmes_disponiveis = df_filtrado['title'].tolist()
    filmes_selecionados = st.multiselect("Selecione os filmes:", filmes_disponiveis)

    if st.button("Recomendar"):
        recomendar_por_filmes_selecionados(df, filmes_selecionados, max_recomendacoes=10)
