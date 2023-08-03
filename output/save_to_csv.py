# output/save_to_csv.py

import csv

def save_data_to_csv(data, filename):
    # data é uma lista de dicionários com os dados coletados.
    # filename é o nome do arquivo CSV que você deseja salvar.

    # Defina os nomes das colunas do CSV. 
    # Certifique-se de que os nomes das colunas correspondam às chaves dos dicionários em "data".
    fieldnames = ["api_name", "data"]

    # Escreve os dados no arquivo CSV.
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Dados salvos com sucesso no arquivo {filename}")
