from urllib.parse import unquote
from request_manager import get_response
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# FastAPI setup
app = FastAPI()
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    # Allows all methods, including GET, POST, PUT, DELETE, etc.
    allow_methods=["*"],
    allow_headers=["*"],  # Allows all headers
)


# FastAPI routes
@app.get("/Jarvis")
def get_response_from_jarvis(request: str) -> str:
    try:
        # url decode the request
        request = request.replace("%20", " ")
        request = unquote(request)

        # get the request
        response = get_response(request)
        print(response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        # events = get_all_events_from_today_up_to_certain_date(get_Xth_saturday_from_date(1))  # nopep8
        # put it in a json FILE
        # with open("omeromeromer.json", "w") as f:
        #     json.dump(events, f, indent=4, ensure_ascii=False)

        # print(events)

        # message = f"""My best friend Shaked is getting married next Tuesday. The wedding starts at 18:00. What will I be missing?"""
        message = f"""What is the next event that have not started yet in my calendar?
        """
        response = get_response(message)
        print(response)

        # structure_breaker = break_structure(message)
        # print(structure_breaker)

    except Exception as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
