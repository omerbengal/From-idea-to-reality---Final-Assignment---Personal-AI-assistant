from datetime import datetime, timezone
import pytz


def clean_bidirectional_text(input_string):
    # List of common bidirectional text formatting characters to remove
    bidirectional_chars = ['\u202A', '\u202B', '\u202C', '\u200F', '\u202D', '\u202E']

    # Remove each character from the string
    for char in bidirectional_chars:
        input_string = input_string.replace(char, '')

    return input_string


def datetime_to_reformatted_str(i_datetime: datetime | str) -> str:
    if isinstance(i_datetime, str):
        i_datetime = datetime.fromisoformat(i_datetime)

    print("before formatting")
    israel_tz = pytz.timezone('Asia/Jerusalem')

    # Check if the datetime is naive (no timezone info)
    if i_datetime.tzinfo is None:
        # If naive, assume it's in Israel time and localize it
        i_datetime = israel_tz.localize(i_datetime)
    elif i_datetime.tzinfo != israel_tz:
        # If it has a different timezone, convert it to Israel time
        i_datetime = i_datetime.astimezone(israel_tz)

    # Convert to UTC
    i_datetime_utc = i_datetime.astimezone(timezone.utc)

    reformatted = i_datetime_utc.isoformat().replace('+00:00', 'Z')
    print("after formatting")
    return reformatted