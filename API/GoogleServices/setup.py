import json
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# add the root directory to the sys path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Absolute import
from API.Database.Database import Database


class GoogleServices:
    SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/tasks.readonly"
    ]

    def __init__(self, uid: str):
        self.db = Database()
        self.uid = uid
        self.creds = None
        self.calendar_service = None
        self.tasks_service = None

    def start_auth_flow(self) -> str:
        """Start the authentication flow and return the authorization URL."""
        google_credentials = self.db.get("google_credentials")
        if not google_credentials:
            raise Exception("Google credentials not found")

        # Parse the JSON string into a dictionary if it's stored as a string
        if isinstance(google_credentials, str):
            google_credentials = json.loads(google_credentials)

        flow = Flow.from_client_config(
            client_config=google_credentials,
            scopes=self.SCOPES,
            redirect_uri="http://localhost:8000/callback"
        )

        auth_url, _ = flow.authorization_url(prompt='consent')

        return auth_url

    def finish_auth_flow(self, auth_code) -> bool:
        """Finish the authentication flow using the provided authorization code."""
        google_credentials = self.db.get("google_credentials")
        if not google_credentials:
            raise Exception("Google credentials not found")

        # Parse the JSON string into a dictionary if it's stored as a string
        if isinstance(google_credentials, str):
            google_credentials = json.loads(google_credentials)

        flow = Flow.from_client_config(
            client_config=google_credentials,
            scopes=self.SCOPES,
            redirect_uri="http://localhost:8000/callback"
        )

        try:
            flow.fetch_token(code=auth_code)
            self.creds = flow.credentials

            if self.creds:
                self.db.create_user(self.uid) # Create the user if it doesn't exist
                self.db.update(f"Users/{self.uid}", "google_token", self.creds.to_json())
                return True
            else:
                raise Exception("Failed to obtain credentials")
        except Exception as e:
            self.creds = None
            raise e

    def setup_credentials(self) -> bool:
        """Setup the credentials for the Google APIs."""

        user_token = self.db.get(f"Users/{self.uid}/google_token")
        if user_token:
            try:
                self.creds = Credentials.from_authorized_user_info(json.loads(user_token), self.SCOPES)
            except Exception as e:
                self.db.update(f"Users/{self.uid}", "google_token", "")
                raise Exception(f"Error loading token: {e}")

        if self.creds and self.creds.expired and self.creds.refresh_token:
            try:
                self.creds.refresh(Request())
                self.db.update(f"Users/{self.uid}", "google_token", self.creds.to_json())
            except Exception as e:
                self.creds = None
                self.db.update(f"Users/{self.uid}", "google_token", "")
                raise Exception(f"Error refreshing credentials: {e}")

        return self.creds is not None and self.creds.valid

    def get_calendar_service(self):
        if not self.calendar_service:
            if not self.setup_credentials():
                raise Exception("Credentials not set up")
            self.calendar_service = build("calendar", "v3", credentials=self.creds)
        return self.calendar_service

    def get_tasks_service(self):
        if not self.tasks_service:
            if not self.setup_credentials():
                raise Exception("Credentials not set up")
            self.tasks_service = build("tasks", "v1", credentials=self.creds)
        return self.tasks_service