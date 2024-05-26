import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CALENDARS = {
    "primary": "primary",
    "birthdays": "526f029f573f9d364bc5c58714241dc4fe864f2c67db8b1af64ca0b2a1f761db@group.calendar.google.com",
    "reichman": "qk0ltn045s6fuo1pal302sebb7rn7dch@import.calendar.google.com",
}


def setup_credentials():
    """Setup the credentials for the Google Calendar API.
    Returns:
        Credentials: The credentials for the Google Calendar API.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def build_service():
    global SERVICE
    SERVICE = build("calendar", "v3", credentials=setup_credentials())


def add_days_to_date(date: datetime, days: int) -> datetime:
    return date + datetime.timedelta(days=days)


def get_nearest_saturday() -> datetime:
    today = datetime.datetime.now(datetime.timezone.utc)
    # Calculate the number of days to add to reach Saturday (5 - today.weekday())
    # If today is Sunday (weekday() returns 6), we add 6 days to reach the next Saturday
    days_to_saturday = 5 - today.weekday() if today.weekday() <= 5 else 6
    return add_days_to_date(today, days_to_saturday)


def get_now() -> datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def get_events(calendarID: str, time_max: datetime) -> list:
    now = get_now().isoformat()
    events_result = (
        SERVICE.events()
        .list(
            calendarId=calendarID,
            maxResults=100,
            timeMin=now,
            timeMax=time_max.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    return events


def main():
    try:
        build_service()

        # Call the Calendar API
        events = get_events(CALENDARS["primary"], get_nearest_saturday())

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
