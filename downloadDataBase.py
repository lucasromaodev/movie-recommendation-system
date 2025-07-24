import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def download_database():
    # Caminho onde o Chrome salva os arquivos
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    arquivo_esperado = "world_imdb_movies_top_movies_per_year.csv.gz"

    # Configura o navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    # Acessa a página
    url = "https://basedosdados.org/dataset/6ba4745d-f131-4f8e-9e55-e8416199a6af?table=79de8c5e-9c21-4398-a9fb-bc40e6d6e77f"
    driver.get(url)

    # Fecha modal, se houver
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.chakra-icon.css-onkibi"))
        )
        close_button.click()
        print("Modal fechado com sucesso.")
        time.sleep(3)
    except TimeoutException:
        print("Nenhum modal encontrado.")

    # Clica na aba "Download"
    try:
        download_tab = wait.until(EC.element_to_be_clickable((By.ID, "tabs-56--tab-1")))
        driver.execute_script("arguments[0].scrollIntoView(true);", download_tab)
        time.sleep(1)
        ActionChains(driver).move_to_element(download_tab).click().perform()
        print("Aba 'Download' clicada.")
    except TimeoutException:
        print("Erro ao encontrar a aba de download.")
        driver.quit()
        exit()

    # Clica no botão de download
    try:
        time.sleep(2)
        botao_download = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "css-3ikl5t")))
        botao_download.click()
        print("Botão de download clicado.")
    except TimeoutException:
        print("Erro ao encontrar o botão de download.")
        driver.quit()
        exit()

    # Aguarda o arquivo aparecer na pasta de downloads
    timeout = 30  # segundos
    arquivo_baixado = False
    print("Aguardando download do arquivo...")

    for _ in range(timeout):
        if arquivo_esperado in os.listdir(download_path):
            arquivo_baixado = True
            break
        time.sleep(1)

    driver.quit()

    if arquivo_baixado:
        print(f"Arquivo '{arquivo_esperado}' baixado com sucesso!")
    else:
        print(f"Arquivo '{arquivo_esperado}' **não foi encontrado** após {timeout} segundos.")
