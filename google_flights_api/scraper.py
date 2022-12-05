import datetime
import logging
import json
import requests
import re
from pattern.web import Element

logging.basicConfig(level=logging.DEBUG)

class Scraper():
    """
    Scraper for cheap flights on Expedia website
    """

    REQUEST_ID_REGEX = r"data-leg-natural-key=\"(\w+)\">"

    def __init__(self, departure_date, return_date, departure_airport, return_airport):
        self.departure_date = departure_date
        self.return_date = return_date
        self.departure_airport = departure_airport
        self.return_airport = return_airport

        self.formatted_url = self.format_base_url()

        get_request = requests.get(self.formatted_url)

        self.e = Element(get_request.content)

        self.departure_request_id = self.get_departure_flight_request_ID()

        self.arribal_request_id = self.get_return_flight_request_ID()

        self.json_url = self.get_flight_data_JSON_URL()

    def format_base_url(self):
        """
        
        """

        base_url = "https://www.expedia.com/Flights-Search?trip=roundtrip"\
                "&leg1=from:{DEPT_AIRPORT},to:{RETURN_AIRPORT},departure:{DEPT_DATE}TANYT"\
                "&leg2=from:{RETURN_AIRPORT},to:{DEPT_AIRPORT},departure:{RETURN_DATE}TANYT"\
                "&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass"\
                "%3Aeconomy&mode=search&origref=www.expedia.com"

        formatted_url = base_url.format(DEPT_AIRPORT=self.departure_airport,
                                        RETURN_AIRPORT=self.return_airport,
                                        DEPT_DATE=self.departure_date,
                                        RETURN_DATE=self.return_date)

        return formatted_url


    def get_departure_flight_request_ID(self):
        """
        
        """
        departure_request_id = self.e("div#originalContinuationId")[0].content

        return departure_request_id


    def get_return_flight_request_ID(self):
        """
        
        """

        arrival_request_content = self.e("div.flex-card")[0].content

        arrival_request_id = re.search(self.REQUEST_ID_REGEX, arrival_request_content)

        try:
            arrival_request_id = arrival_request_id.group(1)
        except AttributeError:
            logging.debug("Cannot find arrival request ID!")

            arribal_request_id = ""

        return arrival_request_id

    def get_flight_data_JSON_URL(self):

        json_url = "https://www.expedia.com/Flight-Search-Paging?c={DEPT_ID}&is=1" \
            "&fl0={ARRV_ID}&sp=asc&cz=200&cn=0&ul=1"

        json_url = json_url.format(
            DEPT_ID=self.departure_request_id,
            ARRV_ID=self.arribal_request_id
        )

        return json_url

    def get_flight_data_JSON(self):
        get_request = requests.get(self.json_url)
        e = Element(get_request.content)

        data_dict = json.loads(e.content)
        data_dict = data_dict["content"]["legs"]

        if not data_dict:
            return []

        flight_info_list = []

        for key in data_dict.keys():
            if data_dict[key]["price"]["totalPriceAsDecimal"]:
                single_flight_dict = {
                    "price($)": data_dict[key]["price"]["totalPriceAsDecimal"],
                    "flight_duration(hours)": data_dict[key]["duration"]["hours"] + data_dict[key]["duration"]["minutes"]/float(60),
                    "source": "Expedia",
                    "departure_date": self.departure_date,
                    "return_date": self.return_date
                }

                flight_info_list.append(single_flight_dict)

        return flight_info_list


        