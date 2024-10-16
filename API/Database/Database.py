# import json
# from datetime import datetime
# from typing import Literal
# import firebase_admin
# from firebase_admin import db, credentials


# class Database:

#     # https://console.firebase.google.com/u/0/project/jarvis-15883/database/jarvis-15883-default-rtdb/data

#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(Database, cls).__new__(cls)
#             cls._instance._initialize()
#         return cls._instance

#     def _initialize(self):
#         if not firebase_admin._apps:
#             with open('../config.json') as config_file:
#                 config = json.load(config_file)

#             cred = credentials.Certificate(config["FIREBASE_CREDENTIALS_JSON"])
#             firebase_admin.initialize_app(cred, {
#                 "databaseURL": "https://jarvis-15883-default-rtdb.europe-west1.firebasedatabase.app"
#             })

#         self.db = db
#         self.root_ref = self.db.reference("/")

#     def get(self, path_after_root: str):
#         return self.root_ref.child(path_after_root).get()

#     # def set(self, key: str, value):
#     #     path = "/" + key
#     #     db.reference(path).set(value)

#     def update(self, path_after_root: str, key: str, value):
#         path = "/" + path_after_root
#         self.db.reference(path).update({key: value})

#     # def delete(self, key: str):
#     #     self.root_ref.delete(key)

#     def check_user_exists(self, uid: str):
#         return self.get("Users/" + uid) is not None

#     def create_user(self, uid: str):
#         if not self.check_user_exists(uid):
#             # The user does not exist, create it
#             self.update("Users", uid, {
#                 "Memory": {
#                     "Personal details": "",
#                     "Life Goals": "",
#                     "Interests And Hobbies": "",
#                     "Life Habits": "",
#                     "Relationships": "",
#                     "Values": "",
#                     "Emotions": "",
#                     "Ideas And Thoughts": ""
#                 },
#                 "History": "",
#                 "google_token": ""
#             })

#     def get_user_memory(self, uid: str):
#         return self.get("Users/" + uid + "/Memory")

#     def update_user_memory(self, uid: str, category: str, memory_instance: str):
#         # Now in format of "YYYYMMDDHHMMSS"
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         self.update("Users/" + uid + "/Memory/" +
#                     category, timestamp, memory_instance)

#         self.update("Users/" + uid + "/Memory/" +
#                     category, timestamp, memory_instance)

#     def get_user_history(self, uid: str):
#         return self.get("Users/" + uid + "/History")

#     def update_user_history(self, uid: str, who_sent: Literal["Assistant", "User"], history_instance: str):
#         # Now in format of "YYYYMMDDHHMMSS"
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         self.update("Users/" + uid + "/History", timestamp,
#                     {"Who sent": who_sent, "Content": history_instance})


# if __name__ == "__main__":
#     db = Database()
#     db.create_user("Demo")

import json
from datetime import datetime
from typing import Literal
import firebase_admin
from firebase_admin import db, credentials


class Database:

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
                    "Life Goals": "",
                    "Interests And Hobbies": "",
                    "Life Habits": "",
                    "Relationships": "",
                    "Values": "",
                    "Emotions": "",
                    "Ideas And Thoughts": ""
                },
                "History": "",
                "google_token": ""
            })
            # Log the user creation event
            self.log_event(uid, "user_created", f"User {uid} created")

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
        analytics_ref = self.root_ref.child(
            f"analytics/{event_name}/{user_id}/{timestamp}")
        analytics_ref.set(event_data)

        print(f"Event logged: {event_name} for user {user_id} at {timestamp}")

    def update_user_memory(self, uid: str, category: str, memory_instance: str):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.update("Users/" + uid + "/Memory/" +
                    category, timestamp, memory_instance)
        self.log_event(uid, "memory_updated", f"Memory updated in {category}")

    def update_user_history(self, uid: str, who_sent: Literal["Assistant", "User"], history_instance: str):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.update("Users/" + uid + "/History", timestamp,
                    {"Who sent": who_sent, "Content": history_instance})


if __name__ == "__main__":
    db = Database()
    db.create_user("Demo2")
    # db.log_event("Demo", "calendar_checked", "User checked Google Calendar")
