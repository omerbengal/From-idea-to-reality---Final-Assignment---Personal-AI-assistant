from urllib.parse import unquote

from setup import GoogleServices
from request_manager import RequestManager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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
@app.get("/Jarvis")
def get_response_from_jarvis(request: str, uid: str) -> str:
    # try:
    #     # url decode the request
    #     request = request.replace("%20", " ")
    #     request = unquote(request)
    #
    #     # get the request
    #     response = RequestManager(uid).get_response(request)
    #     print(response)
    #     return response
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    return GoogleServices(uid).start_auth_flow()

@app.get("/Jarvis/auth")
def auth(uid: str, code: str):
    GoogleServices(uid).finish_auth_flow(code)