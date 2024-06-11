from googleapiclient.errors import HttpError
import setup
from calendar_handler import *
from tasks_handler import *
from openAI import *


def main():
    try:
        #         tasks = get_all_uncompleted_tasks()
        #         tasks_json = json.dumps(tasks, ensure_ascii=False, indent=4)
        #         message = f"""Here are all my tasks: {tasks_json}
        # Can you summarize them for me?"""

        #         response = get_response(message)
        #         print(response)

        message = f"""can you summarize and sectionize all my uncompleted tasks for me?
        also provide a paragraph of your insights about the tasks and the expected outcome of the tasks?"""

        response = get_response(message)
        print(response)

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
