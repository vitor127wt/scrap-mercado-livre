
from dependency_checker import verificar_dependencias
verificar_dependencias()
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
from esperar_login import esperar_login
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

def proxima_pagina(navegador, pagina):
    paginador_element = navegador.find_element(By.TAG_NAME, 'nav')
    botao_next = paginador_element.find_element(By.XPATH, '//*[@id="root-app"]/div/div[1]/section/nav/ul/li[12]')
    print('')
    print(f'Passando para a pagina {pagina + 1}')
    botao_next.click()
    

def mostrar_produtos(produtos: list) -> int:
    quantidade = 1
    for produto in produtos:
        print(f'{quantidade} -> {produto['nome']}')
        quantidade += 1
    return quantidade

def iniciar(busca: str, nome: str, paginas: int):
    print('Iniciando Navegador')
    navegador = criar_navegador()
    dormir(2)
    print('Acessando Mercado Livre')
    navegador.get("https://www.mercadolivre.com.br/")
    dormir(randint(1, 3))
    buscar(elemento=busca, navegador=navegador)
    dormir(randint(1, 3))
    
    url_atual = f'{navegador.current_url}'
    
    if 'account-verification' in url_atual:
        while True:
            if esperar_login():
                dormir(5)
                navegador.get("https://www.mercadolivre.com.br/")
                dormir(randint(1, 3))
                buscar(elemento=busca, navegador=navegador)
                dormir(randint(1, 3))
                url_atual = f'{navegador.current_url}'
            if 'account-verification' not in url_atual:
                break
    
    inicio = True
    quantidade_produtos = 0
    for pagina in range(1, paginas + 1):
        print('')
        print(f'Lendo Pagina {pagina}')
        scroll_para_final(navegador=navegador)
        dormir(randint(1, 3))
        produtos = extrair_produtos(navegador=navegador)
        dormir(float(f'0.{randint(1,10)}'))
        data_frame = exportar.criar_data_frame(produtos)
        quantidade_produtos += mostrar_produtos(produtos=produtos)
        if inicio:
            exportar.cria_csv(nome, data_frame)
            inicio = False
            if paginas == 1:
                continue
            proxima_pagina(navegador=navegador, pagina=pagina)
            dormir(randint(2, 6))
            continue
        exportar.adicionar_csv(nome, data_frame)
        if pagina > paginas + 1:
            proxima_pagina(navegador=navegador, pagina=pagina)
        dormir(randint(3, 8))
    print(f'Foram encontrados {quantidade_produtos} itens.')
    dormir(3)
    navegador.quit()

def quantidade_paginas(paginas):
    int_paginas = int(paginas)
    if int_paginas < 1 or int_paginas > 10:
        raise argparse.ArgumentTypeError('O numero de paginas deve estar entre 1 e 10')
    return int_paginas

if __name__ == '__main__':
    # 1. Cria o interpretador de argumentos
    parser = argparse.ArgumentParser(description="Script de Automação de Busca no Mercado Livre")

    # 2. Define os argumentos que o terminal deve receber
    # O 'type=str' garante que o Python leia como texto, e 'help' descreve o argumento
    parser.add_argument("busca", 
                        type=str,
                        nargs='?',
                        default=True,
                        help="O termo ou produto que você deseja buscar. Caso seja mais de uma palavra use aspas ")
    parser.add_argument("--arquivo", '-a',
                        type=str,
                        help="O nome do arquivo CSV de saída (ex: resultado.csv)",
                        default='resultados.csv')
    parser.add_argument("--paginas", '-p',
                        type=quantidade_paginas,
                        help="Quantas paginas deseja que sejam raspadas (Digite somente numeros, o limite é 10 paginas)",
                        default= 1)
    parser.add_argument('--telegram', '-t',
                        action='store_true',
                        help='Inicia o script para responder pelo bot do Telegram')
    
    # 3. Faz o parse (extração) dos argumentos digitados
    args = parser.parse_args()
    print(args.telegram)
    if args.telegram:
        from bot_telegram import iniciar_bot
        iniciar_bot()
    elif args.busca:
        iniciar(busca=args.busca, nome=args.arquivo, paginas=int(args.paginas))
    else:
        parser.print_help()
    # 4. Executa a sua função principal passando os dados coletados do terminal