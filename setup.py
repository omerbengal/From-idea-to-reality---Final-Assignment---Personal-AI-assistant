# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build


# # If modifying these scopes, delete the file token.json.
# SCOPES = [
#     "https://www.googleapis.com/auth/calendar.readonly",
#     "https://www.googleapis.com/auth/tasks.readonly"
# ]


# def setup_credentials():
#     """Setup the credentials for the Google Calendar API.
#     Returns:
#         Credentials: The credentials for the Google Calendar API.
#     """
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
#     elif creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
#     return creds


# def calendar_service_build():
#     global CALENDAR_SERVICE
#     CALENDAR_SERVICE = build("calendar", "v3", credentials=setup_credentials())


# def tasks_service_build():
#     global TASKS_SERVICE
#     TASKS_SERVICE = build("tasks", "v1", credentials=setup_credentials())


import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleServices:
    _instance = None

    SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/tasks.readonly"
    ]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GoogleServices, cls).__new__(
                cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.creds = self.setup_credentials()
        self.calendar_service = None  # Ensure it's initialized to None
        self.tasks_service = None  # Ensure it's initialized to None
        self.get_calendar_service()
        self.get_tasks_service()

    def setup_credentials(self):
        """Setup the credentials for the Google APIs."""
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(
                "token.json", self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        elif creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def get_calendar_service(self):
        if self.calendar_service is None:
            self.calendar_service = build(
                "calendar", "v3", credentials=self.creds)
        return self.calendar_service

    def get_tasks_service(self):
        if self.tasks_service is None:
            self.tasks_service = build("tasks", "v1", credentials=self.creds)
        return self.tasks_service
