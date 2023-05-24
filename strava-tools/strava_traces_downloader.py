"""
Script that can reconstruct a gpx track of a Strava activity from public information

usage: strava_traces_downloader.py [-h] -a ID_number [-o output.gpx]

Download GPS traces from Strava

optional arguments:
-h, --help                              show help message and exit
-a ID_number, --activity ID_number      ID of activity to download (default: None)
-o output.gpx, --output output.gpx      name of GPX file output (default: output.gpx)
"""

import sys
import datetime
import json
import urllib3
import urllib
import os
import shutil
import socket
import time
from datetime import timedelta
import argparse
import requests
import traceback
from bs4 import BeautifulSoup
import dateutil.parser
from common.login import Login

STRAVA_PATH_STREAM = "https://www.strava.com/activities/"
STRAVA_ACTIVITIES_SESSION = "https://www.strava.com/activities/"
DEFAULT_OUTPUT_FILE = output.gpx

#  GPX Format
HEAD_FILE = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n \
<gpx xmlns=\"http://www.topografix.com/GPX/1/1\" creator=\"\" version=\"1.1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\">\n"
FOOT_FILE = "</gpx>"


def save_as_fpx(activity_id, points, elevation_points, time_points, started_unix_time, output_file):
    final_file = open(output_file, 'w')
    final_file.write(HEAD_FILE)
    final_file.write('<trk>\n')
    final_file.write('<name> Activity ' + str(activity_id) + '</name>\n')
    final_file.write('<trkseg>\n')
    points_counter = 0

    for point in points:
        # points 0,0 are from protected area, do not save them
        if not (str(point[0]) == '0.0') and not (str(point[1]) == '0.0'):
            final_file.write('\t<trkpt lat="' + str(point[0]) + '"' + ' lon="' + str(point[1]) + '">\n')
            final_file.write('\t\t<ele>' + str(elevation_points[points_counter]) + '</ele>\n')
            if not args.notime:
                try:
                    final_file.write('\t\t<time>' + datetime.datetime.utcfromtimestamp(
                        int(started_unix_time) + int(time_points[points_counter])).strftime(
                        '%Y-%m-%dT%H:%M:%SZ') + '</time>\n')
                except ValueError:
                    print("Can't get time for this point. Try -nt option")
                    sys.exit(1)
            final_file.write('\t</trkpt>\n')
        points_counter += 1

    final_file.write('</trkseg>\n')
    final_file.write('</trk>\n')
    final_file.write(FOOT_FILE)
    final_file.close()
    print(f"INFO: Activity {str(activity_id)} = {len(points)}, output_file")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Download GPS Traces from Strava",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--activity", metavar="ID_number", type=int, help="ID of activity to download")
    parser.add_argument("-ai", "--acitivityinterval", nargs=2, metavar=())
