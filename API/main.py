from request_manager import RequestManager

def main():
    try:
        #         tasks = get_all_uncompleted_tasks()
        #         tasks_json = json.dumps(tasks, ensure_ascii=False, indent=4)
        #         message = f"""Here are all my tasks: {tasks_json}
        # Can you summarize them for me?"""

        #         response = get_response(message)
        #         print(response)

        # message = f"""can you summarize and sectionize all my uncompleted tasks for me?
        # also provide a paragraph of your insights about the tasks and the expected outcome of the tasks?"""

        # get all calendar events from today to next weekend
        # events = get_all_events_from_today_up_to_certain_date(get_Xth_saturday_from_date(1))
        # put it in a json FILE
        # with open("omeromeromer.json", "w") as f:
        #     json.dump(events, f, indent=4, ensure_ascii=False)

        # print(events)

        # message = f"""My best friend Shaked is getting married next Tuesday. The wedding starts at 18:00. What will I be missing?"""
        # message = f"""When I ask you what is my next event on my calendar - I want you to provide the title, date, time, and duration."""
        message = f"""What are my next 3 events on my calendar?"""
        response = RequestManager("Demo").get_response(message)
        print(response)

        # structure_breaker = break_structure(message)
        # print(structure_breaker)

    except Exception as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
