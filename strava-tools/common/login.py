import os
from http.cookiejar import LWPCookieJar

import requests
from bs4 import BeautifulSoup

STRAVA_URL_LOGIN = "https://www.strava.com/login"
STRAVA_URL_SESSION = "https://www.strava.com/session"
STRAVA_ACTIVITIES_SESSION = "https://www.strava.com/activities/"
STRAVA_LOGGED_OUT_FINGERPRINT = "logged-out"
COOKIE_FILE_DIR = ".authdata"


class Login:
    verbose = False
    login_session = ""
    authenticity_token = ""

    def __init__(self, verbose=False):
        self.verbose = verbose

    def cookies_save_to_disk(self, login_username, session, authenticity_token):
        session.cookies.save(ignore_discard=True)
        file = open(COOKIE_FILE_DIR + "_" + str(login_username) + "_authenticity_token", "w")
        file.write(authenticity_token)
        file.close()

    def cookies_remove_from_disk(self, login_username):
        if os.path.exists(COOKIE_FILE_DIR + "_" + str(login_username)):
            os.remove(COOKIE_FILE_DIR + "_" + str(login_username))

        if os.path.exists(COOKIE_FILE_DIR + "_" + str(login_username) + "_authenticity_token"):
            os.remove(COOKIE_FILE_DIR + "_" + str(login_username) + "_authenticity_token")

    def cookies_get_from_disk(self, login_username, session):
        if self.verbose:
            print("Loading saved cookies...")
        session.cookies.load(ignore_discard=True)
        file = open(COOKIE_FILE_DIR + "_" + str(login_username) + "_authenticity_token", "r")
        authenticity_token = file.read()
        file.close()

        return authenticity_token

    def force_login(self, login_username):
        if self.verbose:
            print("Force a new login...")
        self.cookies_remove_from_disk(login_username)

    def login(self, login_username, login_password):

        session = requests.session()
        session_from_disk = False

        session.cookies = LWPCookieJar(COOKIE_FILE_DIR + "_" + str(login_username))
        if os.path.exists(COOKIE_FILE_DIR + "_" + str(login_username)):
            # Load saved cookies from the file and use them in a request
            authenticity_token = self.cookies_get_from_disk(login_username, session)
            session_from_disk = True
        else:
            auth_r = session.get(STRAVA_URL_LOGIN)
            soup = BeautifulSoup(auth_r.content, "html.parser")

            get_details = soup.find("input", attrs={
                "name": "authenticity_token"
            })
            authenticity_token = get_details.attrs.get("value")

            if self.verbose:
                print("LOGIN TOKEN: " + authenticity_token)

            # Form data that the page sends when logging in
            login_data = {
                "email": login_username,
                "password": login_password,
                "utf8": "%E2%9C%93",
                "authenticity_token": authenticity_token
            }

            # Authenticate
            auth_r = session.post(STRAVA_URL_SESSION, data=login_data)
            self.cookies_save_to_disk(login_username, session, authenticity_token)

        auth_r = session.get("https://www.strava.com/dashboard")

        self.login_session = session
        self.authenticity_token = authenticity_token

        if int(auth_r.text.find(STRAVA_LOGGED_OUT_FINGERPRINT)) >= 0:
            if session_from_disk:
                if self.verbose:
                    print("Saved cookies failed, getting new session data...")
                self.cookies_remove_from_disk(login_username)
                return self.login(login_username, login_password)
            return False
        return True
