import os
import gzip
import shutil

def unzip_and_move_database(csv_path):
    arquivo_gz = os.path.join(os.path.expanduser("~"), "Downloads", "world_imdb_movies_top_movies_per_year.csv.gz")

    # Verifica se o arquivo compactado existe
    if not os.path.exists(arquivo_gz):
        print(f"Arquivo .gz não encontrado em: {arquivo_gz}")
        exit()

    # Apaga arquivo CSV antigo, se existir
    if os.path.exists(csv_path):
        try:
            os.remove(csv_path)
            print(f"Arquivo antigo removido: {csv_path}")
        except Exception as e:
            print(f"Erro ao apagar arquivo antigo: {e}")
            exit()

    try:
        # Descompacta o .gz e salva o .csv
        with gzip.open(arquivo_gz, 'rb') as arquivo_compactado:
            with open(csv_path, 'wb') as arquivo_csv:
                shutil.copyfileobj(arquivo_compactado, arquivo_csv)
        print(f"Arquivo descompactado com sucesso em:\n{csv_path}")
        
        # Remove o arquivo .gz
        os.remove(arquivo_gz)
        print("Arquivo compactado removido com sucesso.")

    except Exception as e:
        print(f"Erro ao descompactar ou mover o arquivo: {e}")