import dependency_checker
import sys

def esperar_login():
    print('É necessário realizar o login no site do Mercado Livre para proseguir')
    resposta = dependency_checker.perguntar(f'Após realizar o login digite [Y] para continuar, caso não queira logar digite [N] para fechar o programa \r')
    if not resposta:
        sys.exit(0)
    else:
        return True
