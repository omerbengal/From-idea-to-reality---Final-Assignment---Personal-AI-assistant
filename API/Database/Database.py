import json
from datetime import datetime
from typing import Literal
import firebase_admin
from firebase_admin import db, credentials


class Database:
    # https://console.firebase.google.com/u/0/project/jarvis-15883/database/jarvis-15883-default-rtdb/data

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if not firebase_admin._apps:
            with open('../config.json') as config_file:
                config = json.load(config_file)

            cred = credentials.Certificate(config["FIREBASE_CREDENTIALS_JSON"])
            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://jarvis-15883-default-rtdb.europe-west1.firebasedatabase.app"
            })

        self.db = db
        self.root_ref = self.db.reference("/")

    def get(self, path_after_root: str):
        return self.root_ref.child(path_after_root).get()

    def update(self, path_after_root: str, key: str, value):
        path = "/" + path_after_root
        self.db.reference(path).update({key: value})

    def check_user_exists(self, uid: str):
        return self.get("Users/" + uid) is not None

    def create_user(self, uid: str):
        if not self.check_user_exists(uid):
            # The user does not exist, create it
            self.update("Users", uid, {
                "Memory": {
                    "Personal details": "",
                    "Interests And Hobbies": "",
                    "Relationships": "",
                },
                "History": "",
                "google_token": ""
            })
            # Log the user creation event
            self.log_event(uid, "user_created", f"User {uid} created")

    def get_user_memory(self, uid: str):
        return self.get("Users/" + uid + "/Memory")

    def update_user_memory(self, uid: str, category: str, memory_instance: str):
        # Now in format of "YYYYMMDDHHMMSS"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.update("Users/" + uid + "/Memory/" +
                    category, timestamp, memory_instance)
        self.log_event(uid, "memory_updated", f"Memory updated in {category}")

    def get_user_history(self, uid: str):
        return self.get("Users/" + uid + "/History")

    def update_user_history(self, uid: str, who_sent: Literal["Assistant", "User"], history_instance: str):
        # Now in format of "YYYYMMDDHHMMSS"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.update("Users/" + uid + "/History", timestamp,
                    {"Who sent": who_sent, "Content": history_instance})

    def log_event(self, user_id: str, event_name: str, event_details: str):
        """
        Logs an event to the 'analytics' node in Firebase Realtime Database.
        The structure will be: 
        analytics -> event_name -> user_id -> timestamp -> event_details
        :param user_id: ID of the user who triggered the event
        :param event_name: Name of the event (e.g., 'task_created', 'calendar_checked')
        :param event_details: Details or description of the event
        """
        # Now in format of "YYYYMMDDHHMMSS"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        event_data = {
            'event_details': event_details
        }

        # Log event under the structure: analytics/event_name/user_id/timestamp
        # analytics_ref = self.root_ref.child(
        #     f"analytics/{event_name}/{user_id}/{timestamp}")
        # analytics_ref.set(event_data)
        self.update("analytics/" + event_name + "/" +
                    user_id, timestamp, event_data)

    def get_recent_conversation(self, uid: str, limit: int = 10):
        """
        Fetches the last `limit` user messages and corresponding bot responses for the given user.
        :param uid: The user ID for whom the conversation is fetched.
        :param limit: The number of message pairs (user + assistant responses) to retrieve.
        :return: A list of dictionaries containing 'Who sent' and 'Content' of each message.
        """
        # Get the user's history from Firebase
        history = self.get(f"Users/{uid}/History") or {}

        limit_for_dict = -1 * limit

        history_dict = {}

        # get last 10 history items
        last_ten_history = history.items()
        for item in last_ten_history:
            history_dict[item[0]] = item[1]

        # reverse the dict
        history_dict = dict(reversed(list(history_dict.items())))

        return history_dict


if __name__ == "__main__":
    omer = [('20241024202946', {'Content': "I don't have your name in my memory. Could you please tell me your name?",
                                'Who sent': 'Assistant'}),

            ('20241024202958', {
        'Content': "It seems like you're asking about the messages you've sent, but I don't have a record of your name. Could you please tell me your name? This will help me assist you better!",
        'Who sent': 'Assistant'}),

            ('20241024203258', {
        'Content': "I don't have your name stored in my memory. Could you please tell me your name? This will help me assist you better!",
        'Who sent': 'Assistant'}),

            ('20241024203313', {
        'Content': 'Hello Omer! How can I assist you today? If you have any tasks, events, or questions in mind, feel free to share!',
        'Who sent': 'Assistant'}),

            ('20241024203411', {'Content': 'Your name is Omer. How can I assist you today?', 'Who sent': 'Assistant'}),

            ('20241024203445',
             {'Content': 'The message you sent 6 messages ago was: "What is the message I sent you 3 messages ago?"',
              'Who sent': 'Assistant'}),

            ('20241024203719', {
            'Content': 'The message you sent 7 messages ago was: "What is the message I sent you 3 messages ago?"',
            'Who sent': 'Assistant'}),

            ('20241024204009', {
            'Content': "I'm unable to retrieve messages from that far back in our conversation history. However, I can assist you with any current tasks or questions you have. How can I help you today?",
            'Who sent': 'Assistant'}),

            ('20241024204141', {
            'Content': "Hello Omer! I'm here and ready to assist you. How are you doing today? If there's anything specific you'd like help with, just let me know!",
            'Who sent': 'Assistant'}),

            ('20241024204424', {
            'Content': "Hello Omer! How's it going? If there's anything you need help with today, just let me know!",
            'Who sent': 'Assistant'})]
