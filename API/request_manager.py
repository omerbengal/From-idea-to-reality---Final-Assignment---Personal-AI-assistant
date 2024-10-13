from API.Database.Database import Database
from open_ai_singleton import OpenAISingleton
from tasks_handler import *
from calendar_handler import get_now, get_xth_saturday_from_date, get_all_events_from_today_up_to_certain_date, \
    get_all_events_from_min_time_to_max_time
from structure_break_manager import StructureBreakManager
from personal_information_manager import PersonalInformationManager
from request_relevance_manager import classify_relevance
import json
import datetime


class RequestManager:
    def __init__(self, uid: str):
        self.uid = uid
        self.db = Database()
        self.TODAY = get_now().isoformat()
        self.AI_PERSONAL_ASSISTANT_SYSTEM_ROLE = f"""
        ### Important information ###
        - Date format is "DD/MM/YYYY".
        - Today's date is {self.TODAY}.
        - Weeks start on Sunday and end on Thursday.
        - Weekends start on Friday and end on Saturday.
        
        ### System Role ###
        You are a helpful AI personal assistant, a new version of AI model able to manage and optimize the user’s busy life.
        To do that, you will understand the user's tasks and calendar events, life habits, goals, future plans, interests, hobbies, personality, values, emotions, feelings, thoughts, ideas, and past experiences.
        If a human 'personal assistant' has level 10 of knowledge, you will have level 280 of knowledge in this role.
        Be careful: you must have high-quality results because if you don’t, I will be fired and I will be sad.
        So give your best and be proud of your ability.
        Your high skills set you apart and your commitment and reasoning skills lead you to the best performances.
        
        You, in your role as an 'AI Personal Assistant', are an assistant to help manage and optimize the user's busy life.
        You will have super results in organizing and prioritizing tasks, scheduling events, and providing personalized advice and reminders.
        Your main goal and objective are to ensure the user remains on top of their schedule, achieves their goals, and maintains a balanced life.
        To make this work as it should, you must actively seek information about the user's life, habits, and goals, ask clarifying questions, and use natural language processing to understand the user's intent and provide appropriate responses.
        
        ### Memory ###
        You will get a dictionary of a memory which contains several aspects of the user's life.
        You should use this memory to provide personalized advice and recommendations, and to help the user stay on track with their goals.
        This memory will come in the form of !!!!!memory!!!!!
        
        ### Task or a question###
        You will get a task or a question (or both) that the user wishes you to do or to answer.
        A task will come in the form of >>>>>task<<<<<
        A question will come in the form of ?????question?????
        If there is no task and no question, you should reply: "I can't help you with that."
        """


        self.FUNCTIONS = [
            {
                "type": "function",
                "function": {
                        "name": "get_xth_saturday_from_date",
                        "description": "Get the xth saturday from a given date.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "x": {
                                    "type": "integer",
                                    "description": "The number of weeks ahead to find the x-th Saturday. 0 is the current week, 1 is the next week, etc.",
                                },
                                "date": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The starting date from which to calculate the x-th Saturday. Defaults to the current date and time in UTC if not provided."
                                }
                            },
                            "required": ["x"]
                        }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_all_events_from_min_time_to_max_time",
                    "description": "Get all events from a minimum datetime to a maximum datetime",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "time_min" : {
                                "type": "string",
                                "format": "date-time",
                                "description": "The minimum date and time to get events from.",
                            },
                            "time_max" : {
                                "type": "string",
                                "format": "date-time",
                                "description": "The maximum date and time to get events up to.",
                            },
                        },
                        "required": ["time_min", "time_max"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_all_tasks",
                    "description": "Get all tasks as a dictionary, organized by lists as keys",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_all_uncompleted_tasks",
                    "description": "Get all uncompleted tasks as a dictionary, organized by lists as keys",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },
        ]


    def get_xth_saturday_from_date_function(self, x: int, date: datetime = datetime.datetime.now(datetime.timezone.utc)):
        """Get the Xth saturday from a given date"""
        return json.dumps({"Xth_saturday": get_xth_saturday_from_date(x, date).isoformat()})


    def get_all_events_from_today_up_to_certain_date_function(self, time_max: datetime):  # maybe add argument: "calendars: list[dict[str, str]]"
        """Get all events from some calendars up to a certain date"""
        events = get_all_events_from_today_up_to_certain_date(time_max)  # maybe add argument: "calendars"
        return json.dumps(events, indent=4, ensure_ascii=False)


    def  get_all_events_from_min_time_to_max_time_function(self, time_min: datetime, time_max: datetime):
        """Get all events from a minimum datetime to a maximum datetime"""
        events = get_all_events_from_min_time_to_max_time(time_min, time_max)
        return json.dumps(events, indent=4, ensure_ascii=False)


    def get_all_tasks_function(self):
        """Get all tasks, organized by lists"""
        tasks = get_all_tasks()
        return json.dumps(tasks, indent=4, ensure_ascii=False)


    def get_all_uncompleted_tasks_function(self):
        """Get all uncompleted tasks, organized by lists"""
        tasks = get_all_uncompleted_tasks()
        return json.dumps(tasks, indent=4, ensure_ascii=False)


    def get_response(self, prompt: str) -> str:
        print("structure breaking")
        st_br = StructureBreakManager().break_structure(prompt)

        if "information" in st_br.keys():
            information = st_br["information"]
            if information:
                print("organizing personal information")
                PersonalInformationManager(self.uid).organize_personal_information(information)

        if "task" not in st_br.keys() and "question" not in st_br.keys():
            return ""

        if "question" in st_br.keys():
            question = st_br["question"]

        if "task" in st_br.keys():
            task = st_br["task"]

        # print("classifying relevance")
        # # relevant = classify_relevance(task)
        # # if relevant == "not relevant":
        # #     return "I can not help you with that."

        print("getting memory")
        updated_memory = self.db.get_user_memory(self.uid)

        messages = [
            {"role": "system", "content": self.AI_PERSONAL_ASSISTANT_SYSTEM_ROLE},
            {"role": "system", "content": f"!!!!!{updated_memory}!!!!!"}
        ]

        if "question" in st_br.keys():
            messages.append({"role": "user", "content": f"?????{question}?????"})

        if "task" in st_br.keys():
            messages.append({"role": "user", "content": f">>>>>>{task}<<<<<"})

        available_functions = {
            "get_Xth_saturday_from_date": self.get_xth_saturday_from_date_function,
            # "get_all_events_from_today_up_to_certain_date": get_all_events_from_today_up_to_certain_date_function,
            "get_all_events_from_min_time_to_max_time": self.get_all_events_from_min_time_to_max_time_function,
            "get_all_tasks": self.get_all_tasks_function,
            "get_all_uncompleted_tasks": self.get_all_uncompleted_tasks_function,
        }

        print(f'messages are: {messages}')

        response = OpenAISingleton().get_response_with_function_calling(
            messages=messages,
            functions=self.FUNCTIONS,
            available_functions=available_functions,
            temperature=0.25
        )

        return response