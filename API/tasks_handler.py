import json
import setup
from utilities import *


SETUP = setup.GoogleServices()


def _get_all_tasks_lists() -> list[dict[str, str]]:
    results = SETUP.tasks_service.tasklists().list().execute()
    return results.get("items", [])


def _get_all_tasks_from_list(tasklistID: str) -> list[dict[str, str]]:
    results = SETUP.tasks_service.tasks().list(tasklist=tasklistID).execute()
    tasks = results.get("items", [])

    # Clean bidirectional text
    for task in tasks:
        task["title"] = clean_bidirectional_text(task["title"])
        if "notes" in task:
            task["notes"] = clean_bidirectional_text(task["notes"])
    return tasks


def get_all_tasks() -> list[dict[str, str]]:
    lists = _get_all_tasks_lists()
    tasks = {}
    for list in lists:
        tasks[list["title"]] = _get_all_tasks_from_list(list["id"])
    return tasks


def get_all_uncompleted_tasks() -> list[dict[str, str]]:
    tasks = get_all_tasks()
    uncompleted_tasks = {}
    for list in tasks:
        uncompleted_tasks[list] = [task for task in tasks[list] if task["status"] != "completed"]  # nopep8
    return uncompleted_tasks


def example_get_and_print_tasks_from_first_list():
    tasks_lists = _get_all_tasks_lists()  # get all tasks lists # nopep8

    # print all tasks lists
    # for list in tasks_lists:
    #     print(f"{list['title']} ({list['id']})")

    # print() # spacing # nopep8

    tasks = _get_all_tasks_from_list(tasks_lists[0]["id"])

    for task in tasks:
        title = task["title"]
        notes = task.get("notes", "")
        due = task.get("due", "")
        status = task.get("status", "")
        print(f"title: {title}\nnotes: {notes}\ndue: {due}\nstatus: {status}\n")  # nopep8
