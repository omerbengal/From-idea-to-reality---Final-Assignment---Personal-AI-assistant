import sys
import os
from datetime import datetime
from urllib.parse import unquote
from GoogleServices.calendar_handler import get_all_events_from_min_time_to_max_time
from GoogleServices.google_services_factory import GoogleServicesFactory
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from request_manager import RequestManager

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
def finish_auth_flow(uid: str, code: str) -> bool:
    google_services = GoogleServicesFactory().get_instance(uid)
    try:
        return google_services.finish_auth_flow(code)
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


# NOT WORKING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.get("/Jarvis/get_all_calendars_events_for_today")
def get_all_calendars_events_for_today(uid: str):
    try:
        time_min = datetime.now().isoformat()
        time_max = datetime.now().replace(hour=23).isoformat()
        events = get_all_events_from_min_time_to_max_time(time_min, time_max, uid)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# NOT WORKING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!