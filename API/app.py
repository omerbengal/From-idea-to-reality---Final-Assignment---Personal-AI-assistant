from GoogleServices.google_services_factory import GoogleServicesFactory
from fastapi import FastAPI
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
    google_services = GoogleServicesFactory().get_instance(uid)
    auth_url = google_services.start_auth_flow()
    GoogleServicesFactory.release_instance(uid)
    return auth_url

@app.get("/Jarvis/auth")
def auth(uid: str, code: str):
    google_services = GoogleServicesFactory().get_instance(uid)
    google_services.finish_auth_flow(code)
    GoogleServicesFactory.release_instance(uid)