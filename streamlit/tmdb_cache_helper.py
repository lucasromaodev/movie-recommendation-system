import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from tmdb_helper import get_tmdb_movie_data

CACHE_FILE = "tmdb_cache.json"

def carregar_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

cache_tmdb = carregar_cache()

def get_tmdb_data_cache(title, year):
    key = f"{title}_{year}"
    if key in cache_tmdb:
        return cache_tmdb[key]
    result = get_tmdb_movie_data(title, year)
    cache_tmdb[key] = result
    salvar_cache(cache_tmdb)
    return result

def buscar_filme_info_parallel(df_filmes, max_busca=30, max_workers=5):
    filmes = df_filmes.head(max_busca)
    resultados = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                get_tmdb_data_cache,
                filme['title'],
                int(filme['year']) if pd.notnull(filme['year']) else None
            ): filme
            for _, filme in filmes.iterrows()
        }
        for future in as_completed(futures):
            filme = futures[future]
            try:
                info = future.result()
                if info and info.get("poster_url") and info.get("trailer_url"):
                    resultados.append((filme, info))
            except Exception as e:
                print(f"Erro ao buscar {filme['title']}: {e}")

    return resultados
