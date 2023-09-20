import requests
import os
from notification_manager import NotificationManager

PRICES_SHEET_GET_ENDPOINT = os.environ.get('PRICES_SHEET_GET_ENDPOINT')
PRICES_SHEET_PUT_ENDPOINT = os.environ.get('PRICES_SHEET_PUT_ENDPOINT')
USERS_SHEET_GET_ENDPOINT = os.environ.get('USERS_SHEET_GET_ENDPOINT')
USERS_SHEET_POST_ENDPOINT = os.environ.get('USERS_SHEET_POST_ENDPOINT')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
SHEET_HEADERS = {
    'Authorization': BEARER_TOKEN
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheet_data = {}
        self.get_sheet_data()
        self.add_user()

    def get_sheet_data(self):
        response = requests.get(url=PRICES_SHEET_GET_ENDPOINT, headers=SHEET_HEADERS)
        response.raise_for_status()

        response_data = response.json()

        self.sheet_data = response_data['prices']

    def update_iata_codes(self):
        for city_data in self.sheet_data:
            prices_sheet_params = {
                'price': {
                    'iataCode': city_data['iataCode']
                }
            }

            response = requests.put(url=f"{PRICES_SHEET_PUT_ENDPOINT}/{city_data['id']}",
                                    json=prices_sheet_params, headers=SHEET_HEADERS)
            response.raise_for_status()

    @staticmethod
    def add_user():
        print("Welcome to Alex's Flight Club!")
        print('We find the best flights and email them to you!')

        first_name = input('What is your first name? ')
        last_name = input('What is your last name? ')
        email_address = input('What is your email? ')

        users_sheet_params = {
            'user': {
                'firstName': first_name,
                'lastName': last_name,
                'email': email_address
            }
        }

        response = requests.post(url=USERS_SHEET_POST_ENDPOINT, json=users_sheet_params, headers=SHEET_HEADERS)
        response.raise_for_status()

        print('You are in the club!')

    @staticmethod
    def send_emails(flight):
        response = requests.get(url=USERS_SHEET_GET_ENDPOINT, headers=SHEET_HEADERS)
        response.raise_for_status()

        response_data = response.json()

        users_list = response_data['users']

        for user in users_list:
            NotificationManager().send_email(user, flight)
