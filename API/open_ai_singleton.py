import json
import threading
from openai import OpenAI

class OpenAISingleton:
    _model = "gpt-4o-mini"
    _instance = None
    _lock = threading.Lock()
    _api_key = 'sk-proj-4YEmICxNrRVUv8OWO3VlT3BlbkFJVbmbwykJsteagH4it3lv'  # Built-in API key

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(OpenAISingleton, cls).__new__(cls)
                    cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, *args, **kwargs):
        self.client = OpenAI(api_key=self._api_key, *args, **kwargs)

    def get_response_with_function_calling(self, messages: list[dict[str, str]], functions, available_functions: dict[str, callable], temperature: float, seed: int = 42) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=functions,
                tool_choice="auto",
                temperature=temperature,
                seed=seed,
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            print(f"checking if need to use tools")
            counter = 0
            while tool_calls:
                counter += 1
                print(f"I'm using tools now! ({counter})")
                messages.append(response_message)

                print(f"going through tool calls! ({counter}):\n{tool_calls}")
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    print(f"function name: {function_name} ({counter})")
                    function_to_call = available_functions.get(function_name)
                    if function_to_call:
                        function_args = json.loads(tool_call.function.arguments)
                        print(f"({counter}) calling function {function_name}, with args {function_args}")
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
                second_response = self.client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    tools=functions,
                    tool_choice="auto",
                    temperature=temperature,
                    seed=seed,
                )
                response_message = second_response.choices[0].message
                tool_calls = response_message.tool_calls

            return response_message.content if response_message.content else ''
        except Exception as e:
            raise Exception(str(e))

    def get_response_dict(self, messages: list[dict[str, str]], temperature: float, seed: int = 42) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=temperature,
                seed=seed,
            )
            response_message = response.choices[0].message

            return json.loads(response_message.content) if response_message.content else {}
        except Exception as e:
            raise Exception(str(e))

    def get_response_str(self, messages: list[dict[str, str]], temperature: float, seed: int = 42) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=temperature,
                seed=seed,
            )
            response_message = response.choices[0].message

            return response_message.content if response_message.content else ""
        except Exception as e:
            raise Exception(str(e))