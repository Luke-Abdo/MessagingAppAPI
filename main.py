import hashlib
import os

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import bcrypt
import urllib.parse


class Message(BaseModel):
    from_api_key: str
    to_api_key: str
    message: str


class User(BaseModel):
    # messages = []
    username: str
    password: str
    display_name: str


salt = bcrypt.gensalt()

app = FastAPI()

# List of user objects
users = []

# Username -> Hashed Password
creds = {}

# API key -> User
api_keys = {}

inboxes = {}


@app.get("/")
def home():
    return {"data": "Working"}


@app.get("/user/{apikey}")
def getUser(apikey: int):
    for key in api_keys:
        if key == apikey:
            return {"Data": "You have an account"}
    return {"Data": "You don't have an account"}


@app.post("/create-user")
def create_user(user: User):
    for u in users:
        if u.username == user.username:
            return {"Error": "Username Taken"}

    api_key = generate_api_key()

    users.append(user)
    creds[user.username] = (bcrypt.hashpw(user.password.encode(), salt), api_key)
    api_keys[api_key] = user
    inboxes[api_key] = []
    print(api_keys[api_key])

    return {"API_KEY": api_key}


@app.post("/send-message")
def send_message(message: Message):
    inboxes[message.to_api_key].append(message)
    return {"Success": "Message Sent"}


@app.get("/login/{api_key}")
def login(api_key):
    if api_key in api_keys.keys():
        return {"Welcome back": api_keys.get(api_key).username}

    return "Please sign up"


@app.get("/inbox/{api_key}")
def get_inbox(api_key):
    if api_key not in inboxes:
        return {"Error": "No account"}

    return inboxes[api_key]


def generate_api_key():
    return hashlib.sha256(os.urandom(32)).hexdigest()
