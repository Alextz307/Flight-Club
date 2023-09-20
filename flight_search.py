import requests
import os
from flight_data import FlightData

TEQUILA_ENDPOINT = 'https://api.tequila.kiwi.com'
TEQUILA_API_KEY = os.environ.get('TEQUILA_API_KEY')
FLIGHT_HEADERS = {
    'apikey': TEQUILA_API_KEY
}


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    @staticmethod
    def get_iata_code(city_name):
        flight_params = {
            'term': city_name,
            'location_types': 'city'
        }

        response = requests.get(url=f'{TEQUILA_ENDPOINT}/locations/query', params=flight_params, headers=FLIGHT_HEADERS)
        response.raise_for_status()

        response_data = response.json()

        city_iata_code = response_data['locations'][0]['code']

        return city_iata_code

    @staticmethod
    def check_flights(fly_from, fly_to, date_from, date_to):
        flight_params = {
            'fly_from': fly_from,
            'fly_to': fly_to,
            'date_from': date_from.strftime('%d/%m/%Y'),
            'date_to': date_to.strftime('%d/%m/%Y'),
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'flight_type': 'round',
            'max_stopovers': 0,
            'curr': 'GBP',
            'one_for_city': 1,
        }

        response = requests.get(url=f'{TEQUILA_ENDPOINT}/v2/search', params=flight_params, headers=FLIGHT_HEADERS)

        try:
            flight_data = response.json()['data'][0]
        except IndexError:
            print(f'No direct flights found for {fly_to}.')
            return None
        else:
            flight = FlightData(
                price=flight_data['price'],
                origin_city=flight_data['route'][0]['cityFrom'],
                origin_airport=flight_data['route'][0]['flyFrom'],
                destination_city=flight_data['route'][0]['cityTo'],
                destination_airport=flight_data['route'][0]['flyTo'],
                out_date=flight_data['route'][0]['local_departure'].split('T')[0],
                return_date=flight_data['route'][1]['local_departure'].split('T')[0]
            )

            return flight
