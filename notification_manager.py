import os
from twilio.rest import Client
import smtplib

MY_PHONE_NUMBER = os.environ.get('MY_PHONE_NUMBER')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
MY_EMAIL = os.environ.get('MY_EMAIL')
MY_EMAIL_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    @staticmethod
    def flight_message(flight):
        return f'Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to ' \
               f'{flight.destination_city}-{flight.destination_airport}, from' \
               f'{flight.out_date} to {flight.return_date}.'

    def send_message(self, flight):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message_body = self.flight_message(flight)

        client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=MY_PHONE_NUMBER
        )

    def send_email(self, user, flight):
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_EMAIL_PASSWORD)

            email_body = self.flight_message(flight)

            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=user['email'],
                msg=f"Subject:A quick note from Alex's Flight Club!\n\n{email_body}".encode('utf-8')
            )
