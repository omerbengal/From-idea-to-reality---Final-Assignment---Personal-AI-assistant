def clean_bidirectional_text(input_string):
    # List of common bidirectional text formatting characters to remove
    bidirectional_chars = ['\u202A', '\u202B', '\u202C', '\u200F', '\u202D', '\u202E']  # nopep8

    # Remove each character from the string
    for char in bidirectional_chars:
        input_string = input_string.replace(char, '')

    return input_string
