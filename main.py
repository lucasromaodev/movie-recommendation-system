from config import destino_csv
from unzipDataBase import unzip_and_move_database
from downloadDataBase import download_database

def main():
    download_database()
    unzip_and_move_database(destino_csv)

if __name__ == "__main__":
    main()