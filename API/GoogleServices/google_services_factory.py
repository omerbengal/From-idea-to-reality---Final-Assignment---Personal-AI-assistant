import os
import sys

# add the GoogleServices directory to the sys path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from setup import GoogleServices


class GoogleServicesFactory:
    _instances = {}

    @classmethod
    def get_instance(cls, uid: str):
        if uid not in cls._instances:
            cls._instances[uid] = GoogleServices(uid)
        return cls._instances[uid]

    @classmethod
    def release_instance(cls, uid: str):
        if uid in cls._instances:
            del cls._instances[uid]