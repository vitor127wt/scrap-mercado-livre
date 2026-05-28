import sys
import subprocess
import time

def verificar_dependencias():
    DEPENDENCIAS = ['selenium', 'webdriver-manager', 'pandas', 'python-telegram-bot']
    for dependencia in DEPENDENCIAS:
        nome_pacote = dependencia
        try:
            __import__(nome_pacote)
        except ModuleNotFoundError:
            print(f'Pacote: {nome_pacote}, não encontrado. Deseja instalar ?')
            if perguntar():
                instalar_pacote(nome_pacote)
                continue
            else:
                print('Encerrando processo')
                time.sleep(1)
                sys.exit(0)
            


def instalar_pacote(pacote):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pacote])
        print(f'Pacote {pacote}, instalado com sucesso')
    except Exception as e:
        print(f'Erro ao instalar {pacote}: {e}')
        time.sleep(1)
        sys.exit(1)

def perguntar(pergunta: str = '[Y] Para instalar. [N] Para sair.') -> bool:
    resposta = input(pergunta)
    resposta = resposta.upper()
    if not validar_resposta(resposta):
        print('Entrada invalida.')
        perguntar(pergunta)
    return True if resposta == 'Y' else False

def validar_resposta(resposta) -> bool:
    if len(resposta) != 1:
        return False
    if resposta not in 'YN':
        return False
    return True