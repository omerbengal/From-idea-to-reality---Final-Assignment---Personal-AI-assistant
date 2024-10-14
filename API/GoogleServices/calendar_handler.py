import datetime

from google_services_factory import GoogleServicesFactory
from API.utilities import *


def get_xth_saturday_from_date(x: int, date: datetime = datetime.datetime.now(datetime.timezone.utc)) -> datetime:
    days_from_today_to_nearest_saturday = 5 - date.weekday() if date.weekday() <= 5 else 6
    days_from_today_to_x_saturday = days_from_today_to_nearest_saturday + (x * 7)
    return add_days_to_date(date, days_from_today_to_x_saturday)


def _get_all_calendars_data(uid: str) -> list[dict[str, str]]:
    google_services = GoogleServicesFactory().get_instance(uid)
    results = google_services.get_calendar_service().calendarList().list().execute()
    GoogleServicesFactory.release_instance(uid)

    calendars_dicts = results.get("items", [])
    return calendars_dicts


def add_days_to_date(date: datetime, days: int) -> datetime:
    return date + datetime.timedelta(days=days)


def get_now() -> datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _get_all_events_from_specific_calendar_from_min_time_to_max_time(calendar_id: str, time_min: datetime, time_max: datetime, uid: str) -> list[dict[str, str]]:
    google_services = GoogleServicesFactory().get_instance(uid)
    events_result = (
        google_services.get_calendar_service().events()
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
    GoogleServicesFactory.release_instance(uid)

    events = events_result.get("items", [])

    for event in events:
        event["title"] = clean_bidirectional_text(event["summary"])
        if "description" in event:
            event["description"] = clean_bidirectional_text(event["description"])
        if "location" in event:
            event["location"] = clean_bidirectional_text(event["location"])

    return events


def _get_all_events_from_specific_calendar_up_to_certain_date(calendar_id: str, time_max: datetime, uid: str) -> list[dict[str, str]]:
    now = get_now()

    # Convert time_max to datetime if it's a string
    if isinstance(time_max, str):
        time_max = datetime.datetime.fromisoformat(time_max)

    return _get_all_events_from_specific_calendar_from_min_time_to_max_time(calendar_id, now, time_max, uid)


def get_all_events_from_min_time_to_max_time(time_min: datetime, time_max: datetime, uid: str) -> dict[str, list[dict[str, str]]]:
    events = {}
    calendars = _get_all_calendars_data(uid)
    for calendar in calendars:
        calendar_id = calendar["id"]
        calendar_title = calendar["summary"]
        events[calendar_title] = _get_all_events_from_specific_calendar_from_min_time_to_max_time(calendar_id, time_min, time_max, uid)
    return events


def get_all_events_from_today_up_to_certain_date(time_max: datetime, uid: str) -> dict[str, list[dict[str, str]]]:
    events = {}
    calendars = _get_all_calendars_data(uid)
    for calendar in calendars:
        calendar_id = calendar["id"]
        calendar_title = calendar["summary"]
        events[calendar_title] = _get_all_events_from_specific_calendar_up_to_certain_date(calendar_id, time_max, uid)
    return events