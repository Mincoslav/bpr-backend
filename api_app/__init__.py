import fastapi
from fastapi.middleware.cors import CORSMiddleware


app = fastapi.FastAPI()

# FastAPI config will go here if needed

# For local development
origins = [
    "http://localhost:3000/",
    "http://localhost:8080",
]

# For prod 
# TODO: add stuff from: https://fastapi.tiangolo.com/tutorial/security/ 
#       and: https://fastapi.tiangolo.com/tutorial/cors/
origins_allow_all = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_allow_all,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)