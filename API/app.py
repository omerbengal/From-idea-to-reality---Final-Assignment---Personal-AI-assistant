from urllib.parse import unquote
from GoogleServices.google_services_factory import GoogleServicesFactory
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from request_manager import RequestManager


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

        # get the request
        response = RequestManager(uid).get_response(request)
        print(response)
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