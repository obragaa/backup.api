import requests, json
from datetime import datetime

# Inicializando o contador de dados
data_counter = 0
# Inicializando o timestamp mais recente
latest_timestamp = None


def fetch_data_from_api(api_name, token, start_date, end_date, all_data):
    global data_counter, latest_timestamp
    # Definindo valor padrão para entrar na lógica de coleta de dados
    qty_atual = 1

    while qty_atual > 0:
        # Substitua a URL da API real e quaisquer parâmetros necessários para fazer a chamada correta
        api_url = f"https://api.tago.io/data?qty=10000"
        headers = {"device-token": f"{token}", "Content-Type": "application/json"}
        parametros = {
            'start_date': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': end_date.strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            response = requests.get(api_url, headers=headers, params=parametros)
            response.raise_for_status()  # Verifica se a resposta tem status de sucesso (200)
            data = response.json()

            # Certifique-se de que a resposta da API esteja num formato adequado para salvar em CSV.
            # Por exemplo, pode retornar uma lista de dicionários com campos específicos.
            formatted_data = format_data_for_csv(data)

            # Quantidade de dados coletados nessa requisição
            print(len(data['result']))
            qty_atual = len(data['result'])

            # Incrementando o contador de dados
            data_counter += qty_atual

            # Pegar último timestamp
            # Converter a ‘string’ para um objeto datetime
            try:
                data_time_str = data['result'][qty_atual - 1]['time']
                end_date = datetime.fromisoformat(data_time_str.replace("Z", ""))

                # Atualizando o timestamp mais recente
                latest_timestamp = end_date

                print(f"Novo: {end_date}")
            except:
                print("End")

            # Verifica se a api_data não é None antes de estender a lista all_data
            if formatted_data is not None:
                all_data.extend(formatted_data)
                print(f"Backup dos dados da API {api_name} concluído.\n")
            else:
                print(f"Erro ao fazer backup dos dados da API {api_name}.\n")

            # Gravando o total de dados coletados, o timestamp mais recente, a data e hora da requisição em um arquivo
            with open('files/request_info.txt', 'w') as f:
                f.writelines(f'Total de dados coletados: {data_counter}\n')
                f.writelines(f'Timestamp mais recente: {latest_timestamp}\n')  # Está com erro de lógica e precisa mudar
                f.writelines(f'Data e hora da requisicao: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                print(f"request_info feito com sucesso!\nCounter: {data_counter}\nTimestamp: {latest_timestamp}")

            if qty_atual == 0:
                return formatted_data, all_data
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a chamada para a API {api_name}: {e}")
            return None


def format_data_for_csv(data):
    # Neste exemplo, vamos supor que a API retorna um JSON com uma lista de dicionários,
    # e queremos manter apenas alguns campos específicos para salvar em CSV.
    # Adaptar essa função conforme o formato de resposta da API.
    formatted_data = []
    for item in data['result']:
        formatted_item = {
            "id": item["id"],
            "time": item["time"],
            "value": item["value"],
            "variable": item["variable"],
            "device": item["device"],
            # Adicione aqui os campos que deseja salvar em CSV.
        }
        formatted_data.append(formatted_item)
    return formatted_data
