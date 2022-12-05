import logging
import json
import re
import requests
from pattern.web import Element

logging.basicConfig(leve=logging.DEBUG)


class GoogleFlightsAPI():
    """
    
    """
    
    MM_DD_YYYY_REGEX = r"(\d{1,2})\/(\d{1,2})\/(\d{4})"

    google_flight_api = "https://www.googleapis.com/gpxExpress/v1/trips/search?key={API_KEY}"

    api_key = ""

    def __init__(self, departure_date, return_date, departure_airport, return_airport):
        self.url = self.google_flight_api.format(API_KEY=self.api_key)
        self.departure_date = self.modify_date(departure_date)
        self.return_date = self.modify_date(return_date)
        self.departure_airport = departure_airport
        self.return_airport = return_airport

        self.data_dict = self.create_data_dict()

    def modify_date(self, date):
        
        is_date = re.search(self.MM_DD_YYYY_REGEX, date)
        try:
            month = is_date.group(1)
            day = is_date.group(2)
            year = is_date.group(3)
        except AttributeError:
            logging.warning("The provided date is invalid. Date must be in MM/DD/YYYY format")

        return year + "-" + month + "-" + day

    def create_data_dict(self):
        """
        Add outbound and inboud flight details
        """

        data = {
            "request": {
                "slice": [
                    {
                        "origin": "",
                        "destination": "",
                        "date": ""
                    },
                    {
                        "origin": "",
                        "destination": "",
                        "date": ""
                    }
                ],
                "passengers": {
                    "adultCount": 1,
                    "infantInLapCount": 0,
                    "infantInSeatCount": 0,
                    "childCount": 0,
                    "seniorCount": 0
                },
                "solutions": 50,
                "refundable": False
            }
        }

        # setting the outbound flight fields
        data["request"]["slice"][0]["origin"] = self.departure_airport
        data["request"]["slice"][0]["destination"] = self.return_airport
        data["request"]["slice"][0]["date"] = self.departure_date

        # setting the inbound flight fields
        data["request"]["slice"][1]["origin"] = self.return_airport
        data["request"]["slice"][1]["destination"] = self.departure_airport
        data["request"]["slice"][1]["date"] = self.return_date

        return data

    def get_flight_data_JSON(self):
        re = requests.post(
            self.url,
            data=json.dumps(self.data_dict),
            headers={
                'Content-Type': 'application/json'
            }
        )

        data = json.loads(re.content)

        data = data["trips"]["tripOption"]

        if not data:
            return []

        flight_info_list = []

        for idx in range(len(data)):
            price = float(data[idx]["saleTotal"].replace("USD", ""))

            single_flight_dict = {
                "price: $": float(data[idx]["saleTotal"].replace("USD", "")),
                "flight_duration (hours)": data[idx]["slice"][0]["duration"] / float(60),
                "source": "Google Flights",
                "departure_date": self.departure_date,
                "return_date": self.return_date
            }
            flight_info_list.append(single_flight_dict)

        return flight_info_list