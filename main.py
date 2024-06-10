from googleapiclient.errors import HttpError
import setup
from calendar_handler import *
from tasks_handler import *
from openAI import *


def main():
    try:
        message = "show me ALL my uncompleted tasks"
        response = get_response(message)
        print(response)

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
