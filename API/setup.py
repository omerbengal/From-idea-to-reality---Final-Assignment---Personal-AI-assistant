import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleServices:

    SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/tasks.readonly"
    ]

    def __init__(self, uid: str):
        self.creds = self.setup_credentials(uid)


    def setup_credentials(self, uid: str):
        """Setup the credentials for the Google APIs."""
        creds = None
        if os.path.exists("token.json"):
            try:
                creds = Credentials.from_authorized_user_file(
                    "token.json", self.SCOPES)
            except Exception as e:
                print(f"Error loading token.json: {e}")
                os.remove("token.json")  # Delete invalid token file
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    creds = None
                    os.remove("token.json")  # Delete invalid token file
            if not creds or not creds.valid:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "google_credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            if creds:
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
            else:
                raise Exception("Failed to obtain credentials")
        return creds


    def get_calendar_service(self):
        return build("calendar", "v3", credentials=self.creds)


    def get_tasks_service(self):
        return build("tasks", "v1", credentials=self.creds)
