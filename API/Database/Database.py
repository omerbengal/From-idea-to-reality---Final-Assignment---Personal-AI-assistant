import json
from datetime import datetime
from time import sleep
from typing import Literal
import firebase_admin
from firebase_admin import db, credentials


class Database:

    # https://console.firebase.google.com/u/0/project/jarvis-15883/database/jarvis-15883-default-rtdb/data

    def __init__(self):
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

    # def set(self, key: str, value):
    #     path = "/" + key
    #     db.reference(path).set(value)

    def update(self, path_after_root: str, key: str, value):
        path = "/" + path_after_root
        self.db.reference(path).update({key: value})

    # def delete(self, key: str):
    #     self.root_ref.delete(key)

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
            })

    def get_user_memory(self, uid: str):
        return self.get("Users/" + uid + "/Memory")

    def update_user_memory(self, uid: str, category: str, memory_instance: str):
        # Now in format of "YYYYMMDDHHMMSS"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.update("Users/" + uid + "/Memory/" + category, timestamp, memory_instance)

    def get_user_history(self, uid: str):
        return self.get("Users/" + uid + "/History")

    def update_user_history(self, uid: str, who_sent: Literal["Assistant", "User"], history_instance: str):
        # Now in format of "YYYYMMDDHHMMSS"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.update("Users/" + uid + "/History", timestamp, {"Who sent": who_sent, "Content": history_instance})


if __name__ == "__main__":
    db = Database()
    db.update("Users/Demo", "google_token", "")
