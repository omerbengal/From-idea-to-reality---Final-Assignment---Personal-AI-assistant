import datetime
import setup
from utilities import *


SETUP = setup.GoogleServices()


def get_Xth_saturday_from_date(X: int, date: datetime = datetime.datetime.now(datetime.timezone.utc)) -> datetime:
    days_from_today_to_nearest_saturday = 5 - date.weekday() if date.weekday() <= 5 else 6  # nopep8
    days_from_today_to_X_saturday = days_from_today_to_nearest_saturday + (X * 7)  # nopep8
    return add_days_to_date(date, days_from_today_to_X_saturday)


def _get_all_calendars_data() -> list[dict[str, str]]:
    results = SETUP.calendar_service.calendarList().list().execute()
    calendars_dicts = results.get("items", [])
    return calendars_dicts


def add_days_to_date(date: datetime, days: int) -> datetime:
    return date + datetime.timedelta(days=days)


def get_now() -> datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _get_all_events_from_specific_calendar_up_to_certain_date(calendarID: str, time_max: datetime) -> list[dict[str, str]]:
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


def get_all_events_from_today_up_to_certain_date(time_max: datetime, calendars: list[dict[str, str]] = None) -> dict[str, list[dict[str, str]]]:  # nopep8
    events = {}
    if calendars is None or len(calendars) == 0:
        calendars = _get_all_calendars_data()
    for calendar in calendars:
        calendar_id = calendar["id"]
        calendar_title = calendar["summary"]
        events[calendar_title] = _get_all_events_from_specific_calendar_up_to_certain_date(calendar_id, time_max)  # nopep8
    return events


def example_get_and_print_events_from_primary_calendar_from_toady_up_to_nearest_saturday():
    events = _get_all_events_from_specific_calendar_up_to_certain_date("primary", get_Xth_saturday_from_date(0))  # nopep8

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
