import datetime
import setup
from utilities import *


CALENDARS = {
    "primary": "primary",
    "birthdays": "526f029f573f9d364bc5c58714241dc4fe864f2c67db8b1af64ca0b2a1f761db@group.calendar.google.com",
    "reichman": "qk0ltn045s6fuo1pal302sebb7rn7dch@import.calendar.google.com",
}
SETUP = setup.GoogleServices()


def get_all_calendars_data() -> list[str]:
    results = SETUP.calendar_service.calendarList().list().execute()
    calendars_dicts = results.get("items", [])
    return calendars_dicts


def add_days_to_date(date: datetime, days: int) -> datetime:
    return date + datetime.timedelta(days=days)


def get_nearest_saturday(date: datetime = datetime.datetime.now(datetime.timezone.utc)) -> datetime:
    # Calculate the number of days to add to reach Saturday (5 - today.weekday())
    # If today is Sunday (weekday() returns 6), we add 6 days to reach the next Saturday
    days_from_today_to_nearest_saturday = 5 - date.weekday() if date.weekday() <= 5 else 6  # nopep8
    return add_days_to_date(date, days_from_today_to_nearest_saturday)


def get_now() -> datetime:
    return datetime.datetime.now(datetime.timezone.utc)

    # def get_events_up_to_certain_date(calendarID: str, time_max: datetime) -> list:
    #     now = get_now().isoformat()
    #     events_result = (
    #         SETUP.calendar_service.events()
    #         .list(
    #             calendarId=calendarID,
    #             maxResults=100,
    #             timeMin=now,
    #             timeMax=time_max.isoformat(),
    #             singleEvents=True,
    #             orderBy="startTime",
    #         )
    #         .execute()
    #     )
    #     events = events_result.get("items", [])

    #     return events


def get_all_events_from_specific_calendar_up_to_certain_date(calendarID: str, time_max: datetime) -> list[dict]:
    now = get_now().isoformat()

    # Convert time_max to datetime if it's a string
    if isinstance(time_max, str):
        time_max = datetime.datetime.fromisoformat(time_max)

    events_result = (
        SETUP.calendar_service.events()
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

    for event in events:
        event["title"] = clean_bidirectional_text(event["summary"])
        if "description" in event:
            event["description"] = clean_bidirectional_text(event["description"])  # nopep8
        if "location" in event:
            event["location"] = clean_bidirectional_text(event["location"])  # nopep8

    return events


def get_all_events_from_all_calendars_up_to_certain_date(time_max: datetime) -> dict[str, list[dict]]:
    events = {}
    calendars = get_all_calendars_data()
    for calendar in calendars:
        calendar_id = calendar["id"]
        calendar_title = calendar["summary"]
        events[calendar_title] = get_all_events_from_specific_calendar_up_to_certain_date(calendar_id, time_max)  # nopep8
    return events


def example_get_and_print_events_from_primary_calendar_from_toady_up_to_nearest_saturday():
    events = get_all_events_from_specific_calendar_up_to_certain_date(
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
