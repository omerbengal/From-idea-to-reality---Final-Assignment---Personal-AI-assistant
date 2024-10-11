import firebase_admin
from firebase_admin import db, credentials


class Database:

    # https://console.firebase.google.com/u/0/project/jarvis-15883/database/jarvis-15883-default-rtdb/data

    def __init__(self):
        cred = credentials.Certificate("credentials.json")
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


if __name__ == "__main__":
    db = Database()
    db.update("Users", "Demo", {"demo_key": "demo_value"})