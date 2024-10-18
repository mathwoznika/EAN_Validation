#Completar de zeros a esquerda ate 8 digitos:
def fill_8(gtin: str) -> str:
    return gtin.zfill(8)

#Completar de zeros a esquerda ate 12 digitos:
def fill_13(gtin: str) -> str:
    return gtin.zfill(13)

#Extrair apenas os digitos de uma string
def extrair_numeros(text) -> str:
    return ''.join(char for char in text if char.isdigit())

#Retirar zeros a esquerda
def raw_gtin(gtin: str) -> str:
    gtin_od = extrair_numeros(gtin)
    return gtin_od.lstrip('0')

#Normalizar o gtin completando de zeros a esquerda
def normalized_gtin(gtin: str) -> str:
    gtin_od = raw_gtin(gtin)
    lenght = len(gtin_od)
    if lenght <= 8:
        return fill_8(gtin_od)
    elif lenght < 13:
        return fill_13(gtin_od)
    else:
        return gtin_od