from googleapiclient.errors import HttpError
from setup import *
from calendar_handler import *
from tasks_handler import *
from opanAI import *


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
