# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.

from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

DEPARTURE_CITY_CODE = 'LON'

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.sheet_data

if sheet_data[0]['iataCode'] == '':
    for city_data in sheet_data:
        city_name = city_data['city']
        city_data['iataCode'] = flight_search.get_iata_code(city_name)

    data_manager.sheet_data = sheet_data
    data_manager.update_iata_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_later = datetime.now() + timedelta(days=(6 * 30))

for city_data in sheet_data:
    flight = flight_search.check_flights(
        fly_from=DEPARTURE_CITY_CODE,
        fly_to=city_data['iataCode'],
        date_from=tomorrow,
        date_to=six_months_later
    )

    if flight is None:
        continue

    if int(flight.price) <= int(city_data['lowestPrice']):
        # notification_manager.send_message(flight)
        data_manager.send_emails(flight)
