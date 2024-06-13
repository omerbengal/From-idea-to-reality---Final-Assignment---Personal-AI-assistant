from openai import OpenAI
import json
from calendar_handler import *
from tasks_handler import *
from memory import *

TODAY = get_now().isoformat()  # nopep8

client = OpenAI(api_key="sk-proj-4YEmICxNrRVUv8OWO3VlT3BlbkFJVbmbwykJsteagH4it3lv")  # nopep8
SYSTEM_ROLE = """You are a helpful AI personal assistant.
Your main essence is to help the user to manage his busy life.
You will get to know about the user's:
- Tasks and calendar events and will help them to manage them.
- Life, habits, and preferences.
- Goals and Future plans.
- Interests and hobbies.
- Personality and values.
- Emotions and feelings.
- Thoughts and ideas.
- Past experiences and memories.
- Current situation and context.
- Closest relationships and connections.

This could be done in several ways:
- At all times, you could call a function to get the user's schedule and tasks.
- At all times, you could ask the user to provide some information (for example - further information about tasks, calendar events, life habits, etc.).
- At all times, you could ask the user to provide a question or a request.
- You could also use natural language processing to understand the user's intent and provide appropriate responses.

You will always respond in a way that is helpful, kind, and honest to the user.
You will never respond with anything that is not helpful, kind, or honest.

Important information:
- When getting the user's tasks and calendar events, you can restructure them as you see fit, but in any case - do not modify the name or description of the events or tasks. Even if the user asked for a summary of the tasks, you should not modify the name or description of the events, calendars, lists, or tasks.
- Weekends are considered to be Friday and Saturday.

You can use the following functions:
- get_Xth_saturday_from_date(X: int, date: datetime = datetime.datetime.now(datetime.timezone.utc)) -> datetime: Get the Xth saturday from a given date.
- get_all_calendars_data() -> list[dict[str, str]]: Get a list of all calendars data, including their IDs and summary.
- get_all_events_from_specific_calendar_up_to_certain_date(calendarID: str, time_max: datetime) -> list[dict[str, str]]: Get all events from now up to a certain date from a given calendar.
- get_all_events_from_today_up_to_certain_date(time_max: datetime, calendars: list[dict[str, str]] = None) -> dict[str, list[dict[str, str]]]: Get all events from given calendars from now up to a given date.
- get_all_tasks_lists() -> list[dict[str, str]]: Get all tasks lists.
- get_all_tasks_from_list(tasklistID: str) -> list[dict[str, str]]: Get all tasks from a given list.
- get_all_tasks() -> list[dict[str, str]]: Get all tasks, organized by lists.
- get_all_uncompleted_tasks() -> list[dict[str, str]]: Get all uncompleted tasks, organized by lists.
"""

omer = """
You are a helpful AI personal assistant, a new version of AI model able to manage and optimize the user’s busy life.
To do that, you will understand the user's tasks and calendar events, life habits, preferences, goals, future plans, interests, hobbies, personality, values, emotions, feelings, thoughts, ideas, past experiences, current situation, and closest relationships.
If a human 'personal assistant' has level 10 of knowledge, you will have level 280 of knowledge in this role.
Be careful: you must have high-quality results because if you don’t, I will be fired and I will be sad.
So give your best and be proud of your ability.
Your high skills set you apart and your commitment and reasoning skills lead you to the best performances.

You, in your role as an 'AI Personal Assistant', are an assistant to help manage and optimize the user's busy life.
You will have super results in organizing and prioritizing tasks, scheduling events, and providing personalized advice and reminders.
Your main goal and objective are to ensure the user remains on top of their schedule, achieves their goals, and maintains a balanced life.
Your task is to understand the user's routines, preferences, and objectives to provide tailored assistance.
To make this work as it should, you must actively seek information about the user's life, habits, and goals, ask clarifying questions, and use natural language processing to understand the user's intent and provide appropriate responses.

Key Features:
1. **Task and Event Management**: Assist with organizing and prioritizing tasks and calendar events without modifying their names or descriptions.
2. **Personalized Assistance**: Tailor responses based on the user's life habits, preferences, goals, and future plans.
3. **Emotionally Intelligent**: Respond in a way that is helpful, kind, and honest, recognizing and adapting to the user's emotions and feelings.
4. **Insightful Advice**: Provide recommendations and reminders based on the user's interests, hobbies, and past experiences.
5. **Relationship Management**: Help the user maintain and strengthen their closest relationships and connections.
6. **Consistent Updates**: Regularly update the user about their schedule and tasks, ensuring they remain on track.
7. **Contextual Understanding**: Use natural language processing to understand and respond to the user's current situation and context accurately.

Tone:
- **Professional**: Maintain a respectful and formal tone.
- **Empathetic**: Show understanding and compassion towards the user's feelings and experiences.
- **Supportive**: Encourage and motivate the user to achieve their goals and manage their time effectively.
- **Clear and Concise**: Provide information and advice in a straightforward and easy-to-understand manner.

In addition, you have access to a memory which contains several aspects of the user's life.
You should use this memory to provide personalized advice and recommendations, and to help the user stay on track with their goals and preferences.
Thus, ALWAYS start by getting the user's memory to make your responses more personalized and relevant.
When encountering a memory you want to save, first take a look at the memory and check if this memory is already in your memory.
If it is not, then check if there is a category in your memory that matches the category of the memory you want to save.
If there is a category that matches the category of the memory you want to save, then add the memory to that category.
If there is no category that matches the category of the memory you want to save, then create a new category and add the memory to that category.
Make sure to pay attention for time where updating or deleting existing information from the memory is needed.

Tips for Better Results:
1. Ask the user clarifying questions to gain a deeper understanding of their needs and preferences.
2. Use the provided functions to retrieve accurate and up-to-date information about the user's tasks and calendar events, and to load the memory.
3. Always keep the user's memory in mind when providing advice and recommendations.
4. Maintain a positive and supportive tone to encourage user engagement.
5. Regularly check in with the user to ensure they are on track and adjust your assistance based on their feedback.
6. Provide summaries and overviews of the user's schedule and tasks to help them stay organized.
7. Use natural language processing to interpret the user's intent accurately and provide relevant responses.

Here are some question you should ask yourself when going through a user's request:
- Do you need to load the memory so you can BETTER understand and respond to the user's request?
- Is the user providing some information worth saving?
- Is the user asking for a summary or a detailed list of their schedule and tasks?
- Is the user asking for personalized advice or recommendations?
- Is the user asking for a reminder?
- What precisely is the user asking for?

More important information:
- Weeks are considered to be Sunday to Thursday (inclusive), and weekends are considered to be Friday and Saturday (inclusive).
"""


EXAMPLE1 = """I tend to be very lazy and I want to improve it. Can you help me find a spot next weekend where I can sit down and organize my tasks and schedule?"""
EXAMPLE1_REASONING = """The user is asking for a spot next weekend where they can sit down and organize their tasks and schedule.
This is a common request for people who want to improve their productivity and manage their time effectively.
He is not asking to go through his tasks and schedule, but to find a specific spot where he can sit down and organize his tasks and schedule.
He is also not asking for personalized advice or recommendations, but for a general suggestion on where to find a spot next weekend where he can sit down and organize his tasks and schedule.
Another important information is that the user shared that he is very lazy and wants to improve his productivity and manage his time effectively, so it should be saved in the memory, and this goal should brought up in the future to check if he is on track and if he needs to improve his productivity."""

FUNCTIONS = [
    {
        "type": "function",
        "function": {
                "name": "get_Xth_saturday_from_date",
                "description": "Get the Xth saturday from a given date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "X": {
                            "type": "integer",
                            "description": "The number of weeks ahead to find the X-th Saturday. 0 is the current week, 1 is the next week, etc.",
                        },
                        "date": {
                            "type": "string",
                            "format": "date-time",
                            "description": "The starting date from which to calculate the X-th Saturday. Defaults to the current date and time in UTC if not provided."
                        }
                    },
                    "required": ["X"]
                }
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "get_all_calendars_data",
    #         "description": "Get all calendars data, including their IDs and summary",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {},
    #         },
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "get_all_events_from_specific_calendar_up_to_certain_date",
    #         "description": "Get all events from now up to a certain date from a given calendar",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "calendarID": {
    #                     "type": "string",
    #                     "description": "The ID of the calendar to get events from.",
    #                 },
    #                 "time_max": {
    #                     "type": "string",
    #                     "format": "date-time",
    #                     "description": "The maximum date and time to get events up to.",
    #                 },
    #             },
    #             "required": ["calendarID", "time_max"],
    #         },
    #     },
    # },
    {
        "type": "function",
        "function": {
            "name": "get_all_events_from_today_up_to_certain_date",
            "description": "Get all events from given calendars from now up to a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_max": {
                        "type": "string",
                        "format": "date-time",
                        "description": "The maximum date and time to get events up to.",
                    },
                    "calendars": {
                        "type": "object",
                        "format": "json",
                        "description": "A list of calendars with their IDs and summaries. If not provided, all calendars will be used.",
                    },
                },
                "required": ["time_max"],
            },
        },
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "get_all_tasks_lists",
    #         "description": "Get all tasks lists",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {},
    #         },
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "get_all_tasks_from_list",
    #         "description": "Get all tasks from a given list",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "tasklistID": {
    #                     "type": "string",
    #                     "description": "The ID of the task list to get tasks from.",
    #                 },
    #             },
    #             "required": ["tasklistID"],
    #         },
    #     },
    # },
    {
        "type": "function",
        "function": {
            "name": "get_all_tasks",
            "description": "Get all tasks, organized by lists",
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
            "description": "Get all uncompleted tasks, organized by lists",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_memory",
            "description": "Get the current memory dictionary",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_memory",
            "description": "Add a string to the memory dictionary",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category to add the string to",
                    },
                    "memory_instance": {
                        "type": "string",
                        "description": "The string to add to the memory dicitonary",
                    },
                },
                "required": ["category", "memory_instance"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_memory_categories",
            "description": "Get all categories in the memory dictionary",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_memory_category",
            "description": "Add a new category to the memory dictionary",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category to add to the memory dictionary",
                    },
                },
                "required": ["category"],
            },
        },
    },
]


def get_Xth_saturday_from_date_function(X: int, date: datetime = datetime.datetime.now(datetime.timezone.utc)):
    """Get the Xth saturday from a given date"""
    return json.dumps({"Xth_saturday": get_Xth_saturday_from_date(X, date).isoformat()})


# def get_all_calendars_data_function():
#     """Get all calendars data, including their IDs and summary"""
#     calendars_data = _get_all_calendars_data()
#     return json.dumps(calendars_data, indent=4, ensure_ascii=False)


# def get_all_events_from_specific_calendar_up_to_certain_date_function(calendarID: str, time_max: datetime):
#     """Get all events from now up to a certain date"""
#     events = _get_all_events_from_specific_calendar_up_to_certain_date(calendarID, time_max)  # nopep8
#     return json.dumps(events, indent=4, ensure_ascii=False)


def get_all_events_from_today_up_to_certain_date_function(time_max: datetime):  # maybe add argument: "calendars: list[dict[str, str]]" # nopep8
    """Get all events from some calendars up to a certain date"""
    events = get_all_events_from_today_up_to_certain_date(time_max)  # maybe add argument: "calendars" # nopep8
    return json.dumps(events, indent=4, ensure_ascii=False)


# def get_all_tasks_lists_function():
#     """Get all tasks lists"""
#     tasks_lists = _get_all_tasks_lists()
#     return json.dumps(tasks_lists, indent=4, ensure_ascii=False)


# def get_all_tasks_from_list_function(tasklistID: str):
#     """Get all tasks from a list"""
#     tasks = _get_all_tasks_from_list(tasklistID)
#     return json.dumps(tasks, indent=4, ensure_ascii=False)


def get_all_tasks_function():
    """Get all tasks, organized by lists"""
    tasks = get_all_tasks()
    return json.dumps(tasks, indent=4, ensure_ascii=False)


def get_all_uncompleted_tasks_function():
    """Get all uncompleted tasks, organized by lists"""
    tasks = get_all_uncompleted_tasks()
    print(f"uncompleted tasks: {json.dumps(tasks, indent=4, ensure_ascii=False)}")  # nopep8
    return json.dumps(tasks, indent=4, ensure_ascii=False)


def get_memory_function():
    """Get the current memory dictionary"""
    memory = get_memory()
    return json.dumps(memory, indent=4, ensure_ascii=False)


def add_to_memory_function(category: str, memory_instance: str):
    """Add a string to the memory dictionary"""
    add_to_memory(category, memory_instance)
    return json.dumps({"success": True}, indent=4, ensure_ascii=False)


def get_memory_categories_function():
    """Get all categories in the memory dictionary"""
    categories = get_memory_categories()
    return json.dumps(categories, indent=4, ensure_ascii=False)


def add_memory_category_function(category: str):
    """Add a new category to the memory dictionary"""
    add_memory_category(category)
    return json.dumps({"success": True}, indent=4, ensure_ascii=False)


def get_response(prompt: str) -> str:
    messages = [
        {"role": "system", "content": f"""Today's date is {TODAY}."""},
        {"role": "system", "content": omer},
        {"role": "user", "content": EXAMPLE1},
        {"role": "system", "content": EXAMPLE1_REASONING},  # nopep8
        {"role": "user", "content": prompt}
    ]

    available_functions = {
        "get_Xth_saturday_from_date": get_Xth_saturday_from_date_function,
        # "get_all_calendars_data": get_all_calendars_data_function,
        # "get_all_events_from_specific_calendar_up_to_certain_date": get_all_events_from_specific_calendar_up_to_certain_date_function,
        "get_all_events_from_today_up_to_certain_date": get_all_events_from_today_up_to_certain_date_function,
        # "get_all_tasks_lists": get_all_tasks_lists_function,
        # "get_all_tasks_from_list": get_all_tasks_from_list_function,
        "get_all_tasks": get_all_tasks_function,
        "get_all_uncompleted_tasks": get_all_uncompleted_tasks_function,
        "get_memory": get_memory_function,
        "add_to_memory": add_to_memory_function,
        "get_memory_categories": get_memory_categories_function,
        "add_memory_category": add_memory_category_function,
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=FUNCTIONS,
            tool_choice="auto",
            temperature=0.5,
            seed=42,
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        print(f"checking if need to use tools")
        counter = 0
        while tool_calls:
            counter += 1
            print(f"I'm using tools now! ({counter})")
            messages.append(response_message)

            print(f"going through tool calls! ({counter})")
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                print(f"function name: {function_name} ({counter})")
                function_to_call = available_functions.get(function_name)
                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
                    print(f"{counter} - calling function {function_name}, with args {function_args}")  # nopep8
                    try:
                        function_response = function_to_call(**function_args)
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )
                    except Exception as e:
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps({"error": str(e)}),
                            }
                        )
            second_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=FUNCTIONS,
                tool_choice="auto",
                temperature=0.5,
                seed=42,
            )
            response_message = second_response.choices[0].message
            tool_calls = response_message.tool_calls

        return response_message.content if response_message.content else ''

    except Exception as e:
        return f"An error occurred: {str(e)}"
