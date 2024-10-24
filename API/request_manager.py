import threading
from open_ai_singleton import OpenAISingleton
from GoogleServices.tasks_handler import *
from GoogleServices.calendar_handler import get_now, get_xth_saturday_from_date, get_all_events_from_today_up_to_certain_date, \
    get_all_events_from_min_time_to_max_time
from structure_break_manager import StructureBreakManager
from personal_information_manager import PersonalInformationManager
import json
import datetime


class RequestManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RequestManager, cls).__new__(cls)
        return cls._instance

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
        To do that, you will understand the user's tasks and calendar events, future plans, interests, thoughts, ideas, and past experiences.
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

        ### Task ###
        You will get a task that the user wishes you to do or to answer.
        A task will come in the form of >>>>>task<<<<<
        
        ### Other ###
        You will get other types of inputs that you should handle.
        Other types of inputs will come in the form of $$$$$other$$$$$
        Answer these inputs as best as you can. Do not lie to the user, and do not provide false information.
        
        ### Recent Conversation History ###
        You will get the last 10 messages in the conversation between the user and the bot.
        These messages will be in a dictionary, where the key is the timestamp of the message, and the value is another dictionary containing the content of the message and who sent it.
        The items in the dictionary are sorted by timestamp in descending order. This means that the most recent message will be the first item in the dictionary.
        These messages will come in the form of &&&&&recent_history&&&&&
        Use this information to provide more personalized responses to the user.
        
        Do not answer anything which the user did not ask for. 
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
                            "time_min": {
                                "type": "string",
                                "format": "date-time",
                                "description": "The minimum date and time to get events from.",
                            },
                            "time_max": {
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


    # maybe add argument: "calendars: list[dict[str, str]]"
    def get_all_events_from_today_up_to_certain_date_function(self, time_max: datetime):
        """Get all events from some calendars up to a certain date"""
        events = get_all_events_from_today_up_to_certain_date(
            time_max, self.uid)  # maybe add argument: "calendars"
        return json.dumps(events, indent=4, ensure_ascii=False)


    def get_all_events_from_min_time_to_max_time_function(self, time_min: datetime, time_max: datetime,):
        """Get all events from a minimum datetime to a maximum datetime"""
        events = get_all_events_from_min_time_to_max_time(
            time_min, time_max, self.uid)
        return json.dumps(events, indent=4, ensure_ascii=False)


    def get_all_tasks_function(self):
        """Get all tasks, organized by lists"""
        tasks = get_all_tasks(self.uid)
        return json.dumps(tasks, indent=4, ensure_ascii=False)


    def get_all_uncompleted_tasks_function(self):
        """Get all uncompleted tasks, organized by lists"""
        tasks = get_all_uncompleted_tasks(self.uid)
        return json.dumps(tasks, indent=4, ensure_ascii=False)


    def get_recent_conversation_history(self, limit=10):
        """
        Retrieves the recent conversation history between the user and the bot and returns it as a formatted string.
        :param limit: The number of recent messages and responses to retrieve (default is 10 user messages + 10 bot replies).
        :return: A formatted string representing the recent conversation history.
        """
        # Fetch the recent conversation history (last 10 user-bot exchanges).
        conversation_history = self.db.get_recent_conversation(self.uid, limit)

        return conversation_history


    def get_response(self, prompt: str) -> str:
        st_br = StructureBreakManager().break_structure(prompt)

        information = st_br["information"]
        if information:
            PersonalInformationManager(self.uid).organize_personal_information(information)

        task = st_br["task"]

        other = st_br["other"]

        # Fetch the recent conversation history (20 messages in total: 10 user + 10 bot)
        recent_history = self.get_recent_conversation_history(limit=10)

        updated_memory = self.db.get_user_memory(self.uid)
        messages = [
            {"role": "system", "content": self.AI_PERSONAL_ASSISTANT_SYSTEM_ROLE},
            {"role": "system", "content": f"!!!!!{updated_memory}!!!!!"},
            {"role": "system", "content": f"&&&&&{recent_history}&&&&&"},
        ]

        if task:
            messages.append({"role": "user", "content": f">>>>>{task}<<<<<"})

        if other:
            messages.append({"role": "user", "content": f"$$$$${other}$$$$$"})

        available_functions = {
            "get_Xth_saturday_from_date": self.get_xth_saturday_from_date_function,
            "get_all_events_from_min_time_to_max_time": self.get_all_events_from_min_time_to_max_time_function,
            "get_all_tasks": self.get_all_tasks_function,
            "get_all_uncompleted_tasks": self.get_all_uncompleted_tasks_function,
        }
        
        response = OpenAISingleton().get_response_with_function_calling(
            messages=messages,
            functions=self.FUNCTIONS,
            available_functions=available_functions,
            temperature=0.25
        )

        return response