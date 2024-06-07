import datetime
from setup import CALENDAR_SERVICE

CALENDARS = {
    "primary": "primary",
    "birthdays": "526f029f573f9d364bc5c58714241dc4fe864f2c67db8b1af64ca0b2a1f761db@group.calendar.google.com",
    "reichman": "qk0ltn045s6fuo1pal302sebb7rn7dch@import.calendar.google.com",
}


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
