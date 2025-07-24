from config import csv_path
from unzipDataBase import unzip_and_move_database
from downloadDataBase import download_database

def main():
    download_database()
    unzip_and_move_database(csv_path)

if __name__ == "__main__":
    main()