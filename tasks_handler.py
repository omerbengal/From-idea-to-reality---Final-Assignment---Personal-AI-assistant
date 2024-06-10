import setup


SETUP = setup.GoogleServices()


def get_tasks_lists() -> list:
    results = SETUP.tasks_service.tasklists().list().execute()
    return results.get("items", [])


def get_tasks_from_list(tasklistID: str) -> list:
    results = SETUP.tasks_service.tasks().list(tasklist=tasklistID).execute()
    return results.get("items", [])


def get_all_tasks() -> list:
    tasks = []
    lists = get_tasks_lists()
    for list in lists:
        tasks.extend(get_tasks_from_list(list["id"]))
    return tasks


def get_all_uncompleted_tasks() -> list:
    tasks = get_all_tasks()
    return [task for task in tasks if not task["status"] == "completed"]


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
