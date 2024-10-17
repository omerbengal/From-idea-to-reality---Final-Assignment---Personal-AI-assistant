from Database.Database import Database
import sys
import os
from urllib.parse import unquote

from GoogleServices.google_services_factory import GoogleServicesFactory
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from request_manager import RequestManager
from pydantic import BaseModel  # To handle request body

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


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

# Request model for logging event


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
        google_services.finish_auth_flow(code)
        return True
    except Exception as e:
        GoogleServicesFactory.release_instance(uid)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/Jarvis/setup_credentials")
def setup_credentials(uid: str) -> bool:
    google_services = GoogleServicesFactory().get_instance(uid)
    try:
        result = google_services.setup_credentials()
        return result
    except Exception as e:
        GoogleServicesFactory.release_instance(uid)
        raise HTTPException(status_code=500, detail=str(e))

# Add log_event route


@app.post("/Jarvis/log_event")
def log_event(event: dict):
    print(event)
    try:
        # Call the log_event method in Database.py
        Database().log_event(event["user_id"],
                             event["event_name"], event["event_details"])
        return {"message": "Event logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
