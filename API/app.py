import sys
import os
import urllib
from datetime import datetime, timedelta
from urllib.parse import unquote

from open_ai_singleton import OpenAISingleton
from GoogleServices.calendar_handler import get_all_events_from_min_time_to_max_time
from GoogleServices.google_services_factory import GoogleServicesFactory
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from request_manager import RequestManager
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from API.Database.Database import Database

# FastAPI setup
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI routes
@app.get("/Jarvis/get_response")
def get_response(request: str, uid: str) -> str:
    try:
        # url decode the request
        request = request.replace("%20", " ")
        request = unquote(request)

        # update the user history with the user's request
        Database().update_user_history(uid, "User", request)

        # get the assistant's response
        response = RequestManager(uid).get_response(request)

        # update the user history with the assistant's response
        Database().update_user_history(uid, "Assistant", response)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/Jarvis/start_auth_flow")
def start_auth_flow(uid: str) -> str:
    google_services = GoogleServicesFactory().get_instance(uid)
    try:
        auth_url = google_services.start_auth_flow()
    except Exception as e:
        GoogleServicesFactory.release_instance(uid)
        raise HTTPException(status_code=500, detail=str(e))

    return auth_url


@app.get("/Jarvis/finish_auth_flow")
def finish_auth_flow(uid: str, encoded_url: str = Query(..., max_length=None)) -> bool:
    print(f"encoded_url: {encoded_url}")
    google_services = GoogleServicesFactory().get_instance(uid)
    decoded_url = urllib.parse.unquote(encoded_url)
    print(f"decoded_url: {decoded_url}")
    try:
        pattern = r"code=([^&]+)"
        match = re.search(pattern, decoded_url)
        if match:
            code = match.group(1)
            return google_services.finish_auth_flow(code)
        else:
            return False
    except Exception as e:
        GoogleServicesFactory.release_instance(uid)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/Jarvis/setup_credentials")
def setup_credentials(uid: str) -> bool:
    google_services = GoogleServicesFactory().get_instance(uid)
    try:
        return google_services.setup_credentials()
    except Exception as e:
        GoogleServicesFactory.release_instance(uid)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/Jarvis/get_two_hour_range_events")
def get_two_hour_range_events(uid: str):
    try:

        time_min = datetime.now()
        time_max = time_min + timedelta(hours=2)
        events = get_all_events_from_min_time_to_max_time(time_min, time_max, uid)

        role = """You are currently viewing your upcoming events.
        These events will come in the form of !!!!!events!!!!!"""
        task = """Extract the title and time of each event, and provide a clean and simple list of those.
        The format of each event should be:
        "<title>: <start time> - <end time>"
        
        If there are no events, return an empty string.
        
        All-day events should be the firsts in the list.
        If an event is an all-day event, the format should be "<title>: All day."
        Start time and end time should be in the format of HH:MM (24 hour format).
        No need to provide the location or description of the events.
        No need to put numbers or bullet points before each event.
        There should be a break line between each event."""

        messages = [
            {"role": "system", "content": role},
            {"role": "system", "content": f"!!!!!{events}!!!!!"},
            {"role": "user", "content": f">>>>>>{task}<<<<<"}
        ]

        response = OpenAISingleton().get_response_str(messages, 0.25)

        if response == "":
            return None

        response = "Here are your upcoming events in the next 2 hours:\n\n" + response
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))