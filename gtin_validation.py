import pandas as pd
from pathlib import Path
from src.normalize_function import normalized_gtin

def fill_14(gtin: str, lenght: int) -> str:
    if lenght != 14:
        normalized_gtin = gtin.zfill(14)
        return normalized_gtin
    else:
        return gtin
    
def valid_prefix(gtin: str, prefix_list: list[str]) -> bool:
    length = len(gtin)
    normalized_gtin = fill_14(gtin, length)

    if normalized_gtin[:6] == "000000":
        prefix = normalized_gtin[6:9]
        if prefix not in prefix_list:
            return False
        else:
            return True
    else:
        prefix = normalized_gtin[1:4]
        if prefix not in prefix_list:
            return False
        else:
            return True

def get_valid_prefix(path: Path) -> list[str]:
    df = pd.read_excel(path, sheet_name="Prefixo GS1")
    prefix_list = []
    for _, row in df.iterrows():
        inicio = row['fxPrefixIni']
        fim = row['fxPrefixFim']
        
        if pd.notna(inicio) and pd.notna(fim) and inicio <= fim:
            prefix_list.extend(range(int(inicio), int(fim) + 1))
    
    formatted_prefix_list = [str(value).zfill(3) for value in prefix_list]

    return formatted_prefix_list

def is_valid_gtin(gtin: str) -> bool:
    real_gtin = normalized_gtin(gtin)
    length = len(gtin)
    zero_verif = "0"*length

    if length not in [8, 12, 13, 14]:
        return False
    
    if gtin == zero_verif:
        return False
    
    if length == 14 and gtin[0] == "0":
        return False

    if not gtin.isdigit():
        return False

    normalize_gtin = fill_14(gtin, length)
    lenght_normalized = len(normalize_gtin)

    check_digit = int(normalize_gtin[-1])
    total = 0

    for i in range(lenght_normalized - 1):
        digit = int(normalize_gtin[i])
        if (lenght_normalized - i) % 2 == 0:
            total += digit * 3
        else:
            total += digit

    calculated_check_digit = (10 - (total % 10)) % 10

    return check_digit == calculated_check_digit

file_prefix_path = Path.cwd() / "resources" / "Tabela_Prefixo_GS1.xlsx"
valid_prefix_list = get_valid_prefix(file_prefix_path)

def main(gtin) -> bool:
    val_gtin = is_valid_gtin(gtin)
    val_prefix = valid_prefix(gtin, valid_prefix_list)
    if val_gtin == True and val_prefix == True:
        return True
    else:
        return False
