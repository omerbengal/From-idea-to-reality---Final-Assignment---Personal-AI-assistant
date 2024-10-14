# import json
# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from Database.Database import Database
#
#
# class GoogleServices:
#     SCOPES = [
#         "https://www.googleapis.com/auth/calendar.readonly",
#         "https://www.googleapis.com/auth/tasks.readonly"
#     ]
#
#     def __init__(self, uid: str):
#         self.db = Database()
#         self.creds = self.setup_credentials(uid)
#
#     def setup_credentials(self, uid: str):
#         """Setup the credentials for the Google APIs."""
#         creds = None
#         user_token = self.db.get("Users/" + uid + "/google_token")
#         # check if the token is not an empty string
#         if user_token != "":
#             try:
#                 with open(f"token-{uid}.json", "w") as token:
#                     json.dump(user_token, token, indent=4)
#                 creds = Credentials.from_authorized_user_file(f"token-{uid}.json", self.SCOPES)
#             except Exception as e:
#                 print(f"Error loading token.json: {e}")
#                 os.remove(f"token-{uid}.json")  # Delete invalid token file
#
#         if creds and creds.expired and creds.refresh_token:
#             print("herererererererere")
#             try:
#                 creds.refresh(Request())
#             except Exception as e:
#                 print(f"Error refreshing credentials: {e}")
#                 creds = None
#                 os.remove(f"token-{uid}.json")  # Delete invalid token file
#
#         if not creds or not creds.valid:
#             google_credentials = self.db.get("google_credentials")
#             if google_credentials:
#                 with open("google_credentials.json", "w") as file:
#                     json.dump(google_credentials, file, indent=4)
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     "google_credentials.json", self.SCOPES
#                 )
#                 # print("auth url is: " + flow.authorization_url()[0])
#                 creds = flow.run_local_server(port=0)
#
#                 if creds:
#                     self.db.update("Users/" + uid, "google_token", creds.to_json())
#                 else:
#                     raise Exception("Failed to obtain credentials")
#             else:
#                 raise Exception("Google credentials not found")
#
#         return creds
#
#     def get_calendar_service(self):
#         return build("calendar", "v3", credentials=self.creds)
#
#     def get_tasks_service(self):
#         return build("tasks", "v1", credentials=self.creds)

#-------------------------------------------------------------------------------

# import json
# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from Database.Database import Database
#
#
# class GoogleServices:
#     SCOPES = [
#         "https://www.googleapis.com/auth/calendar.readonly",
#         "https://www.googleapis.com/auth/tasks.readonly"
#     ]
#
#     def __init__(self, uid: str):
#         self.db = Database()
#         self.creds = self.setup_credentials(uid)
#
#     def setup_credentials(self, uid: str):
#         """Setup the credentials for the Google APIs."""
#         creds = None
#         user_token = self.db.get("Users/" + uid + "/google_token")
#
#         # Check if the token is not empty
#         if user_token:
#             try:
#                 creds = Credentials.from_authorized_user_info(user_token, self.SCOPES)
#             except Exception as e:
#                 print(f"Error loading credentials: {e}")
#
#         # Refresh credentials if expired
#         if creds and creds.expired and creds.refresh_token:
#             try:
#                 creds.refresh(Request())
#             except Exception as e:
#                 print(f"Error refreshing credentials: {e}")
#                 creds = None
#
#         # If there are no valid credentials, start the OAuth flow
#         if not creds or not creds.valid:
#             google_credentials = self.db.get("google_credentials")
#             if google_credentials:
#                 with open("google_credentials.json", "w") as file:
#                     json.dump(google_credentials, file, indent=4)
#
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     "google_credentials.json", self.SCOPES
#                 )
#
#                 # Generate the authorization URL
#                 auth_url, _ = flow.authorization_url(prompt='consent')
#
#                 # Send this URL to the user
#                 print(f"Please visit this URL to authorize access to your Google Calendar and Tasks: {auth_url}")
#
#                 # Wait for the user to enter the authorization code
#                 # You should replace `input()` with how you collect user input via the bot
#                 auth_code = input("Enter the authorization code you received: ")  # Replace with Telegram bot code
#
#                 # Use the provided code to fetch the token
#                 flow.fetch_token(code=auth_code)
#                 creds = flow.credentials
#
#                 # Save credentials to the database
#                 if creds:
#                     self.db.update("Users/" + uid, "google_token", creds.to_json())
#                 else:
#                     raise Exception("Failed to obtain credentials")
#             else:
#                 raise Exception("Google credentials not found")
#
#         return creds
#
#     def get_calendar_service(self):
#         return build("calendar", "v3", credentials=self.creds)
#
#     def get_tasks_service(self):
#         return build("tasks", "v1", credentials=self.creds)

# ----------------------------------------------------

# import json
# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from Database.Database import Database
#
#
# class GoogleServices:
#     SCOPES = [
#         "https://www.googleapis.com/auth/calendar.readonly",
#         "https://www.googleapis.com/auth/tasks.readonly"
#     ]
#
#     def __init__(self, uid: str):
#         self.db = Database()
#         self.creds = self.setup_credentials(uid)
#
#     def setup_credentials(self, uid: str):
#         """Setup the credentials for the Google APIs."""
#         creds = None
#         user_token = self.db.get("Users/" + uid + "/google_token")
#
#         # Check if the token is not empty
#         if user_token:
#             try:
#                 creds = Credentials.from_authorized_user_info(user_token, self.SCOPES)
#             except Exception as e:
#                 print(f"Error loading credentials: {e}")
#
#         # Refresh credentials if expired
#         if creds and creds.expired and creds.refresh_token:
#             try:
#                 creds.refresh(Request())
#             except Exception as e:
#                 print(f"Error refreshing credentials: {e}")
#                 creds = None
#
#         # If there are no valid credentials, start the OAuth flow
#         if not creds or not creds.valid:
#             google_credentials = self.db.get("google_credentials")
#             if google_credentials:
#                 with open("google_credentials.json", "w") as file:
#                     json.dump(google_credentials, file, indent=4)
#
#                 flow = Flow.from_client_secrets_file(
#                     "google_credentials.json", scopes=self.SCOPES, redirect_uri="http://localhost:8000/callback"
#                 )
#
#                 # Generate the authorization URL
#                 auth_url, _ = flow.authorization_url(prompt='consent')
#
#                 # Send this URL to the user
#                 print(f"Please visit this URL to authorize access to your Google Calendar and Tasks: {auth_url}")
#
#                 # Wait for the user to enter the authorization code
#                 # You should replace `input()` with how you collect user input via the bot
#                 auth_code = input("Enter the authorization code you received: ")  # Replace with Telegram bot mechanism
#
#                 # Use the provided code to fetch the token
#                 flow.fetch_token(code=auth_code)
#                 creds = flow.credentials
#
#                 # Save credentials to the database
#                 if creds:
#                     self.db.update("Users/" + uid, "google_token", creds.to_json())
#                 else:
#                     raise Exception("Failed to obtain credentials")
#             else:
#                 raise Exception("Google credentials not found")
#
#         return creds
#
#     def get_calendar_service(self):
#         return build("calendar", "v3", credentials=self.creds)
#
#     def get_tasks_service(self):
#         return build("tasks", "v1", credentials=self.creds)


#----------------------------------------------------------------

# import json
# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from Database.Database import Database
# import re
#
#
# class GoogleServices:
#     SCOPES = [
#         "https://www.googleapis.com/auth/calendar.readonly",
#         "https://www.googleapis.com/auth/tasks.readonly"
#     ]
#
#     def __init__(self, uid: str):
#         self.db = Database()
#         self.creds = self.setup_credentials(uid)
#
#
#     def start_auth_flow(self, uid: str):
#         """Setup the credentials for the Google APIs."""
#         creds = None
#         print("1")
#         user_token = self.db.get("Users/" + uid + "/google_token")
#         print("2")
#         # Check if the token is not empty
#         if user_token and user_token != "":
#             print("3")
#             try:
#                 creds = Credentials.from_authorized_user_info(user_token, self.SCOPES)
#             except Exception as e:
#                 print(f"Error loading credentials: {e}")
#         print("4")
#         # Refresh credentials if expired
#         if creds and creds.expired and creds.refresh_token:
#             print("5")
#             try:
#                 creds.refresh(Request())
#             except Exception as e:
#                 print(f"Error refreshing credentials: {e}")
#                 creds = None
#         print("6")
#         # If there are no valid credentials, start the OAuth flow
#         if not creds or not creds.valid:
#             print("7")
#             google_credentials = self.db.get("google_credentials")
#             if google_credentials:
#                 print("8")
#                 with open("google_credentials.json", "w") as file:
#                     json.dump(google_credentials, file, indent=4)
#                 print("9")
#                 flow = Flow.from_client_secrets_file(
#                     "google_credentials.json", scopes=self.SCOPES, redirect_uri="http://localhost:8000/callback"
#                 )
#                 print("10")
#                 # Generate the authorization URL
#                 auth_url, _ = flow.authorization_url(prompt='consent')
#
#                 # Send this URL to the user
#                 print(f"Please visit this URL to authorize access to your Google Calendar and Tasks: {auth_url}")
#
#
#     def setup_credentials(self, uid: str):
#         """Setup the credentials for the Google APIs."""
#         creds = None
#         print("1")
#         user_token = self.db.get("Users/" + uid + "/google_token")
#         print("2")
#         # Check if the token is not empty
#         if user_token and user_token != "":
#             print("3")
#             try:
#                 creds = Credentials.from_authorized_user_info(user_token, self.SCOPES)
#             except Exception as e:
#                 print(f"Error loading credentials: {e}")
#         print("4")
#         # Refresh credentials if expired
#         if creds and creds.expired and creds.refresh_token:
#             print("5")
#             try:
#                 creds.refresh(Request())
#             except Exception as e:
#                 print(f"Error refreshing credentials: {e}")
#                 creds = None
#         print("6")
#         # If there are no valid credentials, start the OAuth flow
#         if not creds or not creds.valid:
#             print("7")
#             google_credentials = self.db.get("google_credentials")
#             if google_credentials:
#                 print("8")
#                 with open("google_credentials.json", "w") as file:
#                     json.dump(google_credentials, file, indent=4)
#                 print("9")
#                 flow = Flow.from_client_secrets_file(
#                     "google_credentials.json", scopes=self.SCOPES, redirect_uri="http://localhost:8000/callback"
#                 )
#                 print("10")
#                 # Generate the authorization URL
#                 auth_url, _ = flow.authorization_url(prompt='consent')
#
#                 # Send this URL to the user
#                 print(f"Please visit this URL to authorize access to your Google Calendar and Tasks: {auth_url}")
#
#                 # The user might paste the entire logged line, so we will parse it.
#                 auth_code = input("Enter the authorization code or redirect URL you received: ")
#
#                 # Use the provided code to fetch the token
#                 flow.fetch_token(code=auth_code)
#                 creds = flow.credentials
#
#                 # Save credentials to the database
#                 if creds:
#                     self.db.update("Users/" + uid, "google_token", creds.to_json())
#                 else:
#                     raise Exception("Failed to obtain credentials")
#             else:
#                 raise Exception("Google credentials not found")
#
#         return creds
#
#     def get_calendar_service(self):
#         return build("calendar", "v3", credentials=self.creds)
#
#     def get_tasks_service(self):
#         return build("tasks", "v1", credentials=self.creds)

# -------------------------------------------------------

# import json
# import os
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from Database.Database import Database
# import secrets
#
#
# class GoogleServices:
#     SCOPES = [
#         "https://www.googleapis.com/auth/calendar.readonly",
#         "https://www.googleapis.com/auth/tasks.readonly"
#     ]
#
#     def __init__(self, uid: str):
#         self.db = Database()
#         self.uid = uid
#         self.creds = None
#         self.flow = None
#
#     def start_auth_flow(self):
#         """Start the authentication flow and return the authorization URL."""
#         google_credentials = self.db.get("google_credentials")
#         if not google_credentials:
#             raise Exception("Google credentials not found")
#
#         with open("google_credentials.json", "w") as file:
#             json.dump(google_credentials, file, indent=4)
#
#         self.flow = Flow.from_client_secrets_file(
#             "google_credentials.json",
#             scopes=self.SCOPES,
#             redirect_uri="http://localhost:8000/callback"
#         )
#
#         auth_url, _ = self.flow.authorization_url(prompt='consent')
#
#         # Store the flow object for this user
#         self.db.update(f"Users/{self.uid}", "auth_flow", self.flow.to_json())
#
#         return auth_url
#
#     def finish_auth_flow(self, auth_code):
#         """Finish the authentication flow using the provided authorization code."""
#         # Retrieve the stored flow object
#         flow_json = self.db.get(f"Users/{self.uid}/auth_flow")
#         if not flow_json:
#             raise Exception("Authentication flow not started or expired")
#
#         self.flow = Flow.from_json(flow_json)
#
#         try:
#             self.flow.fetch_token(code=auth_code)
#             self.creds = self.flow.credentials
#
#             if self.creds:
#                 self.db.update(f"Users/{self.uid}", "google_token", self.creds.to_json())
#                 # Clear the stored flow object
#                 self.db.update(f"Users/{self.uid}", "auth_flow", "")
#             else:
#                 raise Exception("Failed to obtain credentials")
#         except Exception as e:
#             # Clear the stored flow object on error
#             self.db.update(f"Users/{self.uid}", "auth_flow", "")
#             raise e
#
#     def setup_credentials(self):
#         """Setup the credentials for the Google APIs."""
#         user_token = self.db.get(f"Users/{self.uid}/google_token")
#         if user_token:
#             try:
#                 self.creds = Credentials.from_authorized_user_info(json.loads(user_token), self.SCOPES)
#             except Exception as e:
#                 print(f"Error loading token: {e}")
#                 self.db.update(f"Users/{self.uid}", "google_token", "")
#
#         if self.creds and self.creds.expired and self.creds.refresh_token:
#             try:
#                 self.creds.refresh(Request())
#                 self.db.update(f"Users/{self.uid}", "google_token", self.creds.to_json())
#             except Exception as e:
#                 print(f"Error refreshing credentials: {e}")
#                 self.creds = None
#                 self.db.update(f"Users/{self.uid}", "google_token", "")
#
#         return self.creds is not None and self.creds.valid
#
#     def get_calendar_service(self):
#         if not self.creds:
#             raise Exception("Credentials not set up")
#         return build("calendar", "v3", credentials=self.creds)
#
#     def get_tasks_service(self):
#         if not self.creds:
#             raise Exception("Credentials not set up")
#         return build("tasks", "v1", credentials=self.creds)

import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from Database.Database import Database


class GoogleServices:
    SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/tasks.readonly"
    ]

    def __init__(self, uid: str):
        self.db = Database()
        self.uid = uid
        self.creds = None

    def start_auth_flow(self):
        """Start the authentication flow and return the authorization URL."""
        google_credentials = self.db.get("google_credentials")
        if not google_credentials:
            raise Exception("Google credentials not found")

        with open("google_credentials.json", "w") as file:
            json.dump(google_credentials, file, indent=4)

        flow = Flow.from_client_secrets_file(
            "google_credentials.json",
            scopes=self.SCOPES,
            redirect_uri="http://localhost:8000/callback"
        )

        auth_url, _ = flow.authorization_url(prompt='consent')

        # Delete the google_credentials.json file
        os.remove("google_credentials.json")

        return auth_url

    def finish_auth_flow(self, auth_code):
        """Finish the authentication flow using the provided authorization code."""
        google_credentials = self.db.get("google_credentials")
        if not google_credentials:
            raise Exception("Google credentials not found")

        with open("google_credentials.json", "w") as file:
            json.dump(google_credentials, file, indent=4)

        flow = Flow.from_client_secrets_file(
            "google_credentials.json",
            scopes=self.SCOPES,
            redirect_uri="http://localhost:8000/callback"
        )

        # Delete the google_credentials.json file
        os.remove("google_credentials.json")

        try:
            flow.fetch_token(code=auth_code)
            self.creds = flow.credentials

            if self.creds:
                self.db.update(f"Users/{self.uid}", "google_token", self.creds.to_json())
            else:
                raise Exception("Failed to obtain credentials")
        except Exception as e:
            raise e

    def setup_credentials(self):
        """Setup the credentials for the Google APIs."""
        user_token = self.db.get(f"Users/{self.uid}/google_token")
        if user_token:
            try:
                self.creds = Credentials.from_authorized_user_info(json.loads(user_token), self.SCOPES)
            except Exception as e:
                print(f"Error loading token: {e}")
                self.db.update(f"Users/{self.uid}", "google_token", "")

        if self.creds and self.creds.expired and self.creds.refresh_token:
            try:
                self.creds.refresh(Request())
                self.db.update(f"Users/{self.uid}", "google_token", self.creds.to_json())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                self.creds = None
                self.db.update(f"Users/{self.uid}", "google_token", "")

        return self.creds is not None and self.creds.valid

    def get_calendar_service(self):
        if not self.creds:
            raise Exception("Credentials not set up")
        return build("calendar", "v3", credentials=self.creds)

    def get_tasks_service(self):
        if not self.creds:
            raise Exception("Credentials not set up")
        return build("tasks", "v1", credentials=self.creds)