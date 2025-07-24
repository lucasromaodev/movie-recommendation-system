import requests
import streamlit as st
from config import API_KEY


BASE_URL = "https://api.themoviedb.org/3"


@st.cache_data(show_spinner=False)
def get_tmdb_movie_data(title, year=None):
    """
    Busca dados do filme na TMDB: pôster, trailer (YouTube) e sinopse.
    """
    try:
        # Buscar filme por título e ano
        search_url = f"{BASE_URL}/search/movie"
        params = {"api_key": API_KEY, "query": title}
        if year:
            params["year"] = year

        res = requests.get(search_url, params=params)
        res.raise_for_status()
        data = res.json()

        if not data["results"]:
            return {"poster_url": None, "trailer_url": None, "overview": "Sinopse não disponível."}

        movie = data["results"][0]
        movie_id = movie["id"]
        poster_path = movie.get("poster_path")
        overview = movie.get("overview", "Sinopse não disponível.")

        # Buscar trailer
        video_url = f"{BASE_URL}/movie/{movie_id}/videos"
        video_res = requests.get(video_url, params={"api_key": API_KEY})
        video_res.raise_for_status()
        video_data = video_res.json()

        trailer_key = next(
            (video["key"] for video in video_data.get("results", [])
             if video["type"] == "Trailer" and video["site"] == "YouTube"),
            None
        )

        return {
            "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
            "trailer_url": f"https://www.youtube.com/watch?v={trailer_key}" if trailer_key else None,
            "overview": overview
        }

    except requests.RequestException as e:
        st.warning(f"Erro ao acessar TMDB: {e}")
        return {
            "poster_url": None,
            "trailer_url": None,
            "overview": "Sinopse não disponível."
        }
