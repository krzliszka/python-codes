import argparse
import datetime
import logging
import json
import requests
import re
from pattern.web import Element

from scraper import Scraper
from google_flights_API import GoogleFlightsAPI

logging.basicConfig(level=logging.DEBUG)


def parse_arguments():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("departure_date", help="Provide departure date in MM/DD/YYYY")
    parser.add_argument("return_date", help="Provide return date in MM/DD/YYYY")
    parser.add_argument("departure_airport", help="Provide desrination airport code, e.g. KRK")
    parser.add_argument("return_airport", help="Provide return airport code, e.g. LAX")

    arg = parser.parse_args()

    departure_date = arg.departure_date
    return_date = arg.return_date
    departure_airport = arg.departure_airport
    return_airport = arg.return_airport

    return departure_date, return_date, departure_airport, return_airport

def print_results(flight_info_list, departure_airport, return_airport):
    flight_info_list = sorted(flight_info_list, key=lambda k: k["price ($): "])

    print('**********************************************************')
    print(f'10 cheapest flights from {departure_airport} to {return_airport}')
    print('**********************************************************')

    for i in flight_info_list[:10]:
        print('------------------------')
        print(json.dumps(i, indent=4))

    flight_info_list = sorted(flight_info_list, key=lambda k: k['flight_duration (hours): '])

    print('**********************************************************')
    print(f'10 shortest flights from {departure_airport} to {return_airport}: ')
    print('**********************************************************')

    for i in flight_info_list[:10]:
        print('------------------------')
        print(json.dumps(i, indent=4))

    print('----------------------------')
    print('Total of %s flights were found: ' % len(flight_info_list))
    print('----------------------------')

departure_date, return_date, departure_airport, return_airport = parse_arguments()

flight_info_list = []

departure_date = datetime.datetime.strptime(departure_date, "%m/%d/%Y")
return_date = datetime.datetime.strptime(return_date, "%m/%d/%Y")

departure_date -= datetime.timedelta(days=1)
return_date -= datetime.timedelta(days=1)

for x in range(3):
    for y in range(3):
        start_date = str(departure_date.month) + "/" + str(departure_date.day) + "/" + str(departure_date.year)
        end_date = str(return_date.month) + "/" + str(return_date.day) + "/" + str(return_date.year)

        scraper = Scraper(start_date, end_date, departure_airport, return_airport)

        google_flights = GoogleFlightsAPI(start_date, end_date, departure_airport, return_airport)

        flight_info_list.extend(scraper.get_flight_data_JSON())

        flight_info_list.extend(google_flights.get_flight_data_JSON())

    return_date -= datetime.timedelta(days=3)
    departure_date += datetime.timedelta(days=1)

print_results(flight_info_list, departure_airport, return_airport)