import pandas as pd
import requests
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Função para buscar coordenadas usando a API Nominatim com tratamento de erros
def get_coordinates_nominatim(city, state):
    geolocator = Nominatim(user_agent="creci_itinerante_app")
    try:
        location = geolocator.geocode(f"{city}, {state}, Brazil", timeout=10)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        print(f"Tempo esgotado para a cidade: {city}, {state}")
    except GeocoderServiceError as e:
        print(f"Erro no serviço de geocodificação: {e}")
    return None, None

# Carregar o arquivo Excel
data = pd.read_excel("DADOS.xlsx")

# Adicionar colunas de latitude e longitude usando Nominatim
latitudes = []
longitudes = []

for _, row in data.iterrows():
    city = row['CIDADE']
    state = row['UF']
    lat, lng = get_coordinates_nominatim(city, state)
    latitudes.append(lat)
    longitudes.append(lng)
    time.sleep(1)  # Respeitar o limite de requisições por segundo da API

data['Latitude'] = latitudes
data['Longitude'] = longitudes

# Salvar o arquivo atualizado
data.to_excel("DADOS_ATUALIZADO.xlsx", index=False)
print("Arquivo atualizado com coordenadas salvo como 'DADOS_ATUALIZADO.xlsx'.")