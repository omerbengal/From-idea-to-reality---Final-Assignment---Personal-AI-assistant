from datetime import timezone
import pytz


def clean_bidirectional_text(input_string):
    # List of common bidirectional text formatting characters to remove
    bidirectional_chars = ['\u202A', '\u202B', '\u202C', '\u200F', '\u202D', '\u202E']

    # Remove each character from the string
    for char in bidirectional_chars:
        input_string = input_string.replace(char, '')

    return input_string


def datetime_to_reformatted_str(i_datetime) -> str:
    israel_tz = pytz.timezone('Asia/Jerusalem')
    i_datetime_utc = israel_tz.localize(i_datetime).astimezone(timezone.utc)
    return i_datetime_utc.isoformat().replace('+00:00', 'Z')