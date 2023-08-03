# main.py

import json
from api.api_utils import fetch_data_from_api
from output.save_to_csv import save_data_to_csv

def main():
    # Carrega os tokens a partir do arquivo tokens.json
    with open("api/tokens.json") as f:
        tokens = json.load(f)

    # Lista para armazenar todos os dados coletados
    all_data = []

    # Loop sobre as APIs e tokens para fazer backup dos dados
    for api_name, api_info in tokens.items():
        token = api_info["token"]
        print(f"Fazendo backup dos dados da API: {api_name}...")
        
        # Chama a função para puxar os dados da API usando o token específico
        api_data = fetch_data_from_api(api_name, token)

        # Salva os dados coletados na lista all_data
        all_data.extend(api_data)

        print(f"Backup dos dados da API {api_name} concluído.\n")

    # Salva os dados coletados em um arquivo CSV
    save_data_to_csv(all_data, "dados_coletados.csv")

    print("Backup concluído com sucesso!")

if __name__ == "__main__":
    main()
