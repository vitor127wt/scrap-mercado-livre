
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
from random import randint
from extrair_produtos import extrair_produtos
import exportar
import argparse

def dormir(tempo: float | int):
    time.sleep(tempo)


def criar_navegador():
    caminho_absoluto = os.path.abspath('./tmp/chrome_profile')
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={caminho_absoluto}')
    options.add_argument(r"--profile-directory=Default")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless=new")
    navegador = webdriver.Chrome(service=service, options=options)
    return navegador


def buscar(elemento: str, navegador: function) -> None:
    campo_busca = navegador.find_element(By.ID, 'cb1-edit')
    campo_busca.send_keys(f'{elemento}')
    time.sleep(1)
    print(f'Buscando {elemento}')
    campo_busca.send_keys(Keys.ENTER)


def scroll_para_final(navegador):
    for _ in range(30):
        tempo = float(f'0.{randint(1, 8)}')
        navegador.execute_script("window.scrollBy(0, 500);")
        dormir(tempo=tempo)

def proxima_pagina(navegador):
    paginador_element = navegador.find_element(By.TAG_NAME, 'nav')
    botao_next = paginador_element.find_element(By.XPATH, '//*[@id="root-app"]/div/div[1]/section/nav/ul/li[12]')
    botao_next.click()
    

def mostrar_produtos(produtos: list) -> int:
    quantidade = 1
    for produto in produtos:
        print(f'{quantidade} -> {produto['nome']}')
        quantidade += 1
    return quantidade

def iniciar(busca: str, nome: str):
    print('Iniciando Navegador')
    navegador = criar_navegador()
    dormir(2)
    print('Acessando Mercado Livre')
    navegador.get("https://www.mercadolivre.com.br/")
    dormir(randint(1, 3))
    buscar(elemento=busca, navegador=navegador)
    dormir(randint(1, 3))

    inicio = True
    quantidade_produtos = 0
    for _ in range(1, 11):
        print(r'\n')
        print('Lendo Pagina')
        scroll_para_final(navegador=navegador)
        dormir(randint(1, 3))
        produtos = extrair_produtos(navegador=navegador)
        dormir(float(f'0.{randint(1,10)}'))
        data_frame = exportar.criar_data_frame(produtos)
        quantidade_produtos += mostrar_produtos(produtos=produtos)
        if inicio:
            exportar.cria_csv(nome, data_frame)
            inicio = False
            dormir(randint(2, 5))
            proxima_pagina(navegador=navegador)
            continue

        exportar.adicionar_csv(nome, data_frame)
        proxima_pagina(navegador=navegador)
        dormir(randint(3, 8))
    print(f'Foram encontrados {quantidade_produtos}.')
    dormir(3)
    navegador.quit()

if __name__ == '__main__':
    # 1. Cria o interpretador de argumentos
    parser = argparse.ArgumentParser(description="Script de Automação de Busca no Mercado Livre")

    # 2. Define os argumentos que o terminal deve receber
    # O 'type=str' garante que o Python leia como texto, e 'help' descreve o argumento
    parser.add_argument("busca", type=str, help="O termo ou produto que você deseja buscar. Caso seja mais de uma palavra use "" ")
    parser.add_argument("arquivo", type=str, help="O nome do arquivo CSV de saída (ex: resultado.csv)")

    # 3. Faz o parse (extração) dos argumentos digitados
    args = parser.parse_args()

    # 4. Executa a sua função principal passando os dados coletados do terminal
    iniciar(busca=args.busca, nome=args.arquivo)