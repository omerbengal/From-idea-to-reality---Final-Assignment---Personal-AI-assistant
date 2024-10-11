import datetime
import json

import setup
from utilities import *


SETUP = setup.GoogleServices()


def get_xth_saturday_from_date(x: int, date: datetime = datetime.datetime.now(datetime.timezone.utc)) -> datetime:
    days_from_today_to_nearest_saturday = 5 - date.weekday() if date.weekday() <= 5 else 6
    days_from_today_to_x_saturday = days_from_today_to_nearest_saturday + (x * 7)
    return add_days_to_date(date, days_from_today_to_x_saturday)


def _get_all_calendars_data() -> list[dict[str, str]]:
    results = SETUP.calendar_service.calendarList().list().execute()
    calendars_dicts = results.get("items", [])
    return calendars_dicts


def add_days_to_date(date: datetime, days: int) -> datetime:
    return date + datetime.timedelta(days=days)


def get_now() -> datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _get_all_events_from_specific_calendar_from_min_time_to_max_time(calendar_id: str, time_min: datetime, time_max: datetime) -> list[dict[str, str]]:
    events_result = (
        SETUP.calendar_service.events()
        .list(
            calendarId=calendar_id,
            maxResults=100,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    for event in events:
        event["title"] = clean_bidirectional_text(event["summary"])
        if "description" in event:
            event["description"] = clean_bidirectional_text(event["description"])
        if "location" in event:
            event["location"] = clean_bidirectional_text(event["location"])

    return events


def _get_all_events_from_specific_calendar_up_to_certain_date(calendar_id: str, time_max: datetime) -> list[dict[str, str]]:
    now = get_now()

    # Convert time_max to datetime if it's a string
    if isinstance(time_max, str):
        time_max = datetime.datetime.fromisoformat(time_max)

    return _get_all_events_from_specific_calendar_from_min_time_to_max_time(calendar_id, now, time_max)


def get_all_events_from_min_time_to_max_time(time_min: datetime, time_max: datetime) -> dict[str, list[dict[str, str]]]:
    events = {}
    calendars = _get_all_calendars_data()
    for calendar in calendars:
        calendar_id = calendar["id"]
        calendar_title = calendar["summary"]
        events[calendar_title] = _get_all_events_from_specific_calendar_from_min_time_to_max_time(calendar_id, time_min, time_max)
    return events


def get_all_events_from_today_up_to_certain_date(time_max: datetime) -> dict[str, list[dict[str, str]]]:
    events = {}
    calendars = _get_all_calendars_data()
    for calendar in calendars:
        calendar_id = calendar["id"]
        calendar_title = calendar["summary"]
        events[calendar_title] = _get_all_events_from_specific_calendar_up_to_certain_date(calendar_id, time_max)
    return events


def example_get_and_print_events_from_primary_calendar_from_toady_up_to_nearest_saturday():
    events = _get_all_events_from_specific_calendar_up_to_certain_date("primary", get_xth_saturday_from_date(0))

    if not events:
        print("No upcoming events found.")

    for event in events:
        title = event.get("summary", "")
        begda = event.get("start", {}).get("dateTime", "")
        endda = event.get("end", {}).get("dateTime", "")
        status = event.get("status", "")  # confirmed, tentative, cancelled # nopep8
        description = event.get("description", "")
        location = event.get("location", "")

        print(f"title: {title}\nbegda: {begda}\nendda: {endda}\nstatus: {status}\ndescription: {description}\nlocation: {location}\n")