
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def extrair_produtos(navegador: function) -> list:
    grid = extrair_grid(navegador=navegador)
    cards = extrair_cards(grid=grid)
    produtos = [
        extrair_produto(card=card) for card in cards
    ]
    return produtos


def extrair_grid(navegador: function):
    grid = navegador.find_element(By.XPATH, '//*[@id="root-app"]/div/div[1]/section/ol')
    return grid

def extrair_cards(grid):
    cards = grid.find_elements(By.CLASS_NAME, 'poly-card__content')
    return cards

def extrair_produto(card) -> dict:
    parcelamento = extrair_parcelamento(card=card)
    frete = extrair_frete(card=card)
    produto = {
        'nome' : extrair_nome(card=card),
        'preço' : extrair_valor(card=card),
        'desconto' : extrair_desconto(card=card),
        'parcelamento_vezes' : parcelamento['vezes'],
        'parcelamento_sem_juros' : parcelamento['sem_juros'],
        'frete_gratis' : frete['frete'],
        'frete_full' : frete['full'],
        'condicao' : extrair_condicao(card=card),
        'link' : extrair_link(card=card)
        
    }
    return produto

def extrair_nome(card) -> str:
    titulo = card.find_element(By.CLASS_NAME, 'poly-component__title-wrapper')
    return titulo.text

def extrair_valor(card) -> float:
    reais = converter_reais(card=card)
    centavos = converter_centavos(card=card)
    
    valor = float(f'{reais}.{centavos}')
    return valor


def converter_reais(card):
    reais = card.find_element(By.CSS_SELECTOR, 'span.andes-money-amount__fraction')
    reais_str = reais.text
    new_reais = ''
    for char in reais_str:
        if char.isdigit():
            new_reais += char
    return new_reais


def converter_centavos(card):
    try:
        centavos = card.find_element(By.CSS_SELECTOR, 'span.andes-money-amount__cents.andes-money-amount__cents--superscript-24')
    except NoSuchElementException:
        centavos = '00'
    if centavos != '00':
        return centavos.text
    return centavos

def extrair_desconto(card) -> bool | str:
    try:
        desconto_element = card.find_element(By.CLASS_NAME, 'poly-price__disc_label')
    except NoSuchElementException, ValueError:
        return 0
    desconto_str = f'{desconto_element.text}'
    desconto_dig = '0'
    for char in desconto_str:
        if char.isdigit():
            desconto_dig += char
    if desconto_dig == '0':
        return 0
    return int(desconto_dig)

def extrair_parcelamento(card):
    try:
        parcelamento_element = card.find_element(By.CLASS_NAME, 'poly-price__installments')
    except NoSuchElementException:
        return {'vezes' : 0,
                'sem_juros' : False}
    parcelamento_str = f'{parcelamento_element.text}'
    parcelamento_vezes = ''
    parcelamento_sem_juros = False
    for char in parcelamento_str:
        if char == 'x':
            break
        if char.isdigit():
            parcelamento_vezes += char
    if 'sem juros' in parcelamento_str:
        parcelamento_sem_juros = True
    if int(parcelamento_vezes) > 24:
        parcelamento_vezes = 0
    
    return {'vezes' : parcelamento_vezes,
            'sem_juros' : parcelamento_sem_juros}


def extrair_frete(card):
    try:
        frete_element = card.find_element(By.CLASS_NAME, 'poly-shipping-v2__item')
    except NoSuchElementException:
        return {'frete': False,
            'full': False}
    try:
        frete_gratis_element = frete_element.find_element(By.TAG_NAME, 'span')
        frete_gratis_str = f'{frete_gratis_element.text}'
    except:
        frete_gratis_str = f'Sem Frete Gratis'
    try:
        frete_full_element = frete_element.find_element(By.TAG_NAME, 'svg')
    except NoSuchElementException:
        frete_full_element = False
    if frete_full_element:
        frete_full_text = frete_full_element.get_attribute('aria-label')
        return {'frete' : frete_gratis_str,
                'full': frete_full_text}
    return {'frete': frete_gratis_str,
            'full': frete_full_element}
    
def extrair_condicao(card):
    try:
        usado_element = card.find_element(By.CLASS_NAME, 'poly-component__item-condition')
    except NoSuchElementException:
        usado = False
        return usado
    usado_str = f'{usado_element.text}'
    if 'usado' in usado_str:
        usado = True
        return usado
    return False

def extrair_link(card):
    titulo = card.find_element(By.CLASS_NAME, 'poly-component__title-wrapper')
    link_element = titulo.find_element(By.TAG_NAME, 'a')
    link = link_element.get_attribute('href')
    return link