import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/tasks.readonly"
]

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
    elif creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def calendar_service_build():
    global CALENDAR_SERVICE
    CALENDAR_SERVICE = build("calendar", "v3", credentials=setup_credentials())


def tasks_service_build():
    global TASKS_SERVICE
    TASKS_SERVICE = build("tasks", "v1", credentials=setup_credentials())


def add_days_to_date(date: datetime, days: int) -> datetime:
    return date + datetime.timedelta(days=days)


def get_nearest_saturday() -> datetime:
    today = datetime.datetime.now(datetime.timezone.utc)
    # Calculate the number of days to add to reach Saturday (5 - today.weekday())
    # If today is Sunday (weekday() returns 6), we add 6 days to reach the next Saturday
    days_from_today_to_nearest_saturday = 5 - \
        today.weekday() if today.weekday() <= 5 else 6
    return add_days_to_date(today, days_from_today_to_nearest_saturday)


def get_now() -> datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def get_events_up_to_certain_date(calendarID: str, time_max: datetime) -> list:
    now = get_now().isoformat()
    events_result = (
        CALENDAR_SERVICE.events()
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


def get_tasks_lists() -> list:
    results = TASKS_SERVICE.tasklists().list().execute()
    return results.get("items", [])


def get_tasks_from_list(tasklistID: str) -> list:
    results = TASKS_SERVICE.tasks().list(tasklist=tasklistID).execute()
    return results.get("items", [])


def example_get_and_print_events_from_primary_calendar_from_toady_up_to_nearest_saturday():
    events = get_events_up_to_certain_date(
        CALENDARS["primary"], get_nearest_saturday())

    if not events:
        print("No upcoming events found.")

    for event in events:
        title = event.get("summary", "")
        begda = event.get("start", {}).get("dateTime", "")
        endda = event.get("end", {}).get("dateTime", "")
        status = event.get("status", "")  # confirmed, tentative, cancelled # nopep8
        description = event.get("description", "")
        location = event.get("location", "")

        print(f"title: {title}\nbegda: {begda}\nendda: {endda}\nstatus: {status}\ndescription: {description}\nlocation: {location}\n")  # nopep8


def example_get_and_print_tasks_from_first_list():
    tasks_lists = get_tasks_lists()  # get all tasks lists # nopep8

    # print all tasks lists
    # for list in tasks_lists:
    #     print(f"{list['title']} ({list['id']})")

    # print() # spacing # nopep8

    tasks = get_tasks_from_list(tasks_lists[0]["id"])

    for task in tasks:
        title = task["title"]
        notes = task.get("notes", "")
        due = task.get("due", "")
        status = task.get("status", "")
        print(f"title: {title}\nnotes: {notes}\ndue: {due}\nstatus: {status}\n")  # nopep8


def main():
    try:
        calendar_service_build()
        tasks_service_build()

        print()
        print("Example events from primary calendar from today up to nearest Saturday:\n")
        example_get_and_print_events_from_primary_calendar_from_toady_up_to_nearest_saturday()
        print("---------------------------------------")
        print("Example tasks from first list:\n")
        example_get_and_print_tasks_from_first_list()

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
