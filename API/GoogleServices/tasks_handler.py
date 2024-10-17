import sys
import os

# add the root directory to the sys path
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from API.Database.Database import Database  # Import the Database class
from API.utilities import *
from API.GoogleServices.google_services_factory import GoogleServicesFactory


def _get_all_tasks_lists(uid: str) -> list[dict[str, str]]:
    google_services = GoogleServicesFactory().get_instance(uid)
    results = google_services.get_tasks_service().tasklists().list().execute()

    return results.get("items", [])


def _get_all_tasks_from_list(tasklistID: str, uid: str) -> list[dict[str, str]]:
    google_services = GoogleServicesFactory().get_instance(uid)
    results = google_services.get_tasks_service(
    ).tasks().list(tasklist=tasklistID).execute()

    tasks = results.get("items", [])

    # Clean bidirectional text
    for task in tasks:
        task["title"] = clean_bidirectional_text(task["title"])
        if "notes" in task:
            task["notes"] = clean_bidirectional_text(task["notes"])

    return tasks


def get_all_tasks(uid: str) -> dict[str, list[dict[str, str]]]:
    lists = _get_all_tasks_lists(uid)
    tasks = {}
    for list in lists:
        tasks[list["title"]] = _get_all_tasks_from_list(list["id"], uid)

    # Log event
    Database().log_event(uid, "tasks_checked", "User checked all tasks in all task lists")

    return tasks


def get_all_uncompleted_tasks(uid: str) -> dict[str, list[dict[str, str]]]:
    tasks = get_all_tasks(uid)
    uncompleted_tasks = {}
    for list in tasks:
        uncompleted_tasks[list] = [
            task for task in tasks[list] if task["status"] != "completed"]

    return uncompleted_tasks
