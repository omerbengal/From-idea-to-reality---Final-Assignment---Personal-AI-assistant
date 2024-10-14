from open_ai_singleton import OpenAISingleton
from calendar_handler import *
from memory_handler import *
from Database.Database import Database


class PersonalInformationManager:
    def __init__(self, uid: str):
        self.uid = uid
        self.db = Database()
        self.TODAY = get_now().isoformat()
        self.memory_categories_explanations = """Personal details - Information about the user's life, such as their name, age, gender, and occupation. The information in this category should only be about the user himself, not about his friends or any other person.
                                                                                            Life Goals - Objectives that the user wants to achieve in their life.
                                                                                            Interests And Hobbies - Activities and life interests that the user enjoys.
                                                                                            Life Habits - Habits and routines that the user follows.
                                                                                            Relationships - Information about the user's relationships. Each relationship should contain data on a single person (such as their name, age, gender, and occupation) and the person's relationship to the user (such as "friend", "family member", "romantic partner", or "acquaintance").
                                                                                            Values - Beliefs and principles that the user holds dear.
                                                                                            Emotions - Emotions that the user experiences (such as happiness, sadness, anger, or fear) with context to their life events.
                                                                                            Ideas And Thoughts - Ideas and thoughts that the user has about a particular topic or situation."""
        self.PERSONAL_INFORMATION_MANAGER_SYSTEM_ROLE = f"""
                ### Important information ###
                - Date format is "DD/MM/YYYY".
                - Today's date is {self.TODAY}.
                - Weeks start on Sunday and end on Thursday.
                - Weekends start on Friday and end on Saturday.

                ### System Role ###
                You are an expert details analyzer.
                You will act as a middleman between a user and an AI personal assistant.
                You will get a list of personal information about the user's life - this list will come in the form of >>>>>list<<<<<.
                Your task is to analyze the list and insert each information item in the best suitable category in the memory if it is not already there.

                ### Personal information classification ###
                You will get a description for each available category.
                This description will come in the form of !!!!!category_description!!!!!.
                You should use this explanation to classify the information you get from the user.

                ### General instructions ###
                - Make sure to only use double quotes.
                - You must never alter the content provided to you, but you can rephrase it a bit to make it more readable.
                - The insformation list should contain only personal information of the user, and not temporary information related to the specific task the user requested.
                - If a piece of information (or a part of it) already exists in the memory, do not add it again, but instead update the existing information.
                """

        self.FUNCTIONS = [
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
        ]

    def get_memory_function(self):
        """Get the current memory dictionary"""
        memory = self.db.get_user_memory(self.uid)
        return json.dumps(memory, indent=4, ensure_ascii=False)

    def add_to_memory_function(self, category: str, memory_instance: str):
        """Add a string to the memory dictionary"""
        self.db.update_user_memory(self.uid, category, memory_instance)
        return json.dumps({"success": True}, indent=4, ensure_ascii=False)

    def get_memory_categories_function(self):
        """Get all categories in the memory dictionary"""
        categories = self.db.get_user_memory(self.uid).keys()
        return json.dumps(categories, indent=4, ensure_ascii=False)

    def organize_personal_information(self, personal_information: list[str]):
        messages = [
            {"role": "system", "content": self.PERSONAL_INFORMATION_MANAGER_SYSTEM_ROLE},
            {"role": "system", "content": f"!!!!!{
                self.memory_categories_explanations}!!!!!"},
            {"role": "user", "content": f">>>>>{personal_information}<<<<<"}
        ]

        available_functions = {
            "get_memory": self.get_memory_function,
            "add_to_memory": self.add_to_memory_function,
            "get_memory_categories": self.get_memory_categories_function,
        }

        response = OpenAISingleton().get_response_with_function_calling(
            messages=messages,
            functions=self.FUNCTIONS,
            available_functions=available_functions,
            temperature=0.25
        )

        return response
