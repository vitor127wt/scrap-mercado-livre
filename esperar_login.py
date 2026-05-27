import dependency_checker
import sys

def esperar_login():
    print('É necessário realizar o login no site do Mercado Livre para proseguir')
    print('Após realizar o login digite [Y] para continuar, caso não queira logar digite [N] para fechar o programa')
    resposta = dependency_checker.perguntar('Após realizar o login digite [Y] para continuar, caso não queira logar digite [N] para fechar o programa')
    if not resposta:
        sys.exit(0)
    else:
        return True
