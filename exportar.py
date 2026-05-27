import pandas

def criar_data_frame(dados: list) -> pandas.DataFrame:
    df = pandas.DataFrame(dados)
    return df

def cria_csv(nome: str, data: pandas.DataFrame):
    data.to_csv(f'{nome}', index=False, sep=';', encoding='utf-8-sig')
    
def adicionar_csv(nome: str, data: pandas.DataFrame):
    data.to_csv(
        nome,
        mode='a', 
        index=False, 
        sep=";", 
        encoding="utf-8-sig", 
        header=False
    )