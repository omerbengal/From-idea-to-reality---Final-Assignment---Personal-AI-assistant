from open_ai_singleton import OpenAISingleton


class StructureBreakManager:
    def __init__(self):
        self.memory_categories_explanations = """Personal details - Information about the user's life, such as their name, age, gender, and occupation. The information in this category should only be about the user himself, not about his friends or any other person.
                                                                            Life Goals - Objectives that the user wants to achieve in their life.
                                                                            Interests And Hobbies - Activities and life interests that the user enjoys.
                                                                            Life Habits - Habits and routines that the user follows.
                                                                            Relationships - Information about the user's relationships. Each relationship should contain data on a single person (such as their name, age, gender, and occupation) and the person's relationship to the user (such as "friend", "family member", "romantic partner", or "acquaintance").
                                                                            Values - Beliefs and principles that the user holds dear.
                                                                            Emotions - Emotions that the user experiences (such as happiness, sadness, anger, or fear) with context to their life events.
                                                                            Ideas And Thoughts - Ideas and thoughts that the user has about a particular topic or situation."""
        self.STRUCTURE_BREAKER_SYSTEM_ROLE = """
        ### Important information ###
        - Date format is "DD/MM/YYYY".
        - Today's date is {TODAY}.
        - Weeks start on Sunday and end on Thursday.
        - Weekends start on Friday and end on Saturday.
        
        ### System Role ###
        You are an expert words analyzer.
        You will act as a middleman between a user and an AI personal assistant.
        You will get a prompt from the user and analyze it, it will come in the form of >>>>>prompt<<<<<.
        The prompt can potentially contain one or more of the following ideas:
        - Some personal information about the user's life.
        - A task for the AI personal assistant to do.
        - A question or a request for information.
        
        ### Output ###
        You will analyze the prompt and provide a dictionary with the following structure:
        {
            "information": <List of information items - each one is a string>,
            "task": <The task to do - a string>
            "question": <The question or request for information - a string>
        }
        
        ### Personal information instructions ###
        - Only extract personal information that fits one of the memory categories provided in the form of !!!!!memory_categories_explanations!!!!!
        - If there is no personal information - return an empty list.
        
        ### General instructions ###
        - Make sure to only use double quotes.
        - You must never alter the task, question or the information in the prompt.
        - If there is no task - return an empty string.
        - If there is no question - return an empty string.
        """


    def break_structure(self, prompt: str) -> dict:
        messages = [
            # {"role": "system", "content": f"""Today's date is {TODAY}."""},
            {"role": "system", "content": self.STRUCTURE_BREAKER_SYSTEM_ROLE},
            {"role": "system", "content": f"!!!!!{self.memory_categories_explanations}!!!!!"},
            # {"role": "user", "content": EXAMPLE3},
            # {"role": "system", "content": EXAMPLE3_REASONING},
            # # {"role": "assistant", "content": EXAMPLE1_OUTPUT},
            # {"role": "user", "content": EXAMPLE4},
            # {"role": "system", "content": EXAMPLE4_REASONING},
            # # {"role": "assistant", "content": EXAMPLE2_OUTPUT},
            {"role": "user", "content": f">>>>>{prompt}<<<<<"}
        ]

        response = OpenAISingleton().get_response_dict(
            messages=messages,
            temperature=0.33
        )

        return response