from setup import TASKS_SERVICE


def get_tasks_lists() -> list:
    results = TASKS_SERVICE.tasklists().list().execute()
    return results.get("items", [])


def get_tasks_from_list(tasklistID: str) -> list:
    results = TASKS_SERVICE.tasks().list(tasklist=tasklistID).execute()
    return results.get("items", [])


def example_get_and_print_tasks_from_first_list():
    tasks_lists = get_tasks_lists()  # get all tasks lists # nopep8

    # print all tasks lists
    # for list in tasks_lists:
    #     print(f"{list['title']} ({list['id']})")

    # print() # spacing # nopep8

    tasks = get_tasks_from_list(tasks_lists[0]["id"])

    for task in tasks:
        title = task["title"]
        notes = task.get("notes", "")
        due = task.get("due", "")
        status = task.get("status", "")
        print(f"title: {title}\nnotes: {notes}\ndue: {due}\nstatus: {status}\n")  # nopep8
