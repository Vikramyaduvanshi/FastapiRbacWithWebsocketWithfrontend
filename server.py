# server.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Auth_router import Auth
from Chatroutes import UserChat
from Cron_jobs.scheduler import start_scheduler
from AllsignalFetch import General

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Server Running"}

@app.on_event("startup")
async def startup_event():
    start_scheduler()

app.include_router(Auth.router)
app.include_router(UserChat.chatrouter)
app.include_router(General.allsignalrouter)