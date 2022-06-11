import hashlib
import os

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import bcrypt
import urllib.parse


class Credentials(BaseModel):
    username: str
    hashed_password: str


class Message(BaseModel):
    from_username: str
    to_username: str
    message: str


class User(BaseModel):
    username: str
    password: str
    display_name: str
    api_key: Optional[str] = None
    messages: Optional[list] = []


salt = bcrypt.gensalt()

app = FastAPI()

users = []
stored_creds = {}
api_key_to_user = {}


@app.get("/")
def home():
    return {"data": "Working"}


@app.get("/user/{apikey}")
def getUser(apikey: int):
    for user in users:
        if user.api_key == apikey:
            return {"Data": "You have an account"}
    return {"Data": "You don't have an account"}


@app.post("/create-user")
def create_user(user: User):
    for u in users:
        if u.username == user.username:
            return {"Error": "Username Taken"}

    user.api_key = generate_api_key()
    stored_creds[user.username] = user.password
    api_key_to_user[user.api_key] = user
    users.append(user)
    return {"API_KEY": user.api_key}


@app.post("/send-message")
def send_message(message: Message):
    sent = False
    for user in users:
        if user.username == message.to_username:
            user.messages.append(message)
            sent = True
            break
    if sent:
        return {"Success": "Message Sent!"}
    else:
        return {"Error": "User Does Not Exist!"}


@app.post("/login")
def login(creds: Credentials):
    if stored_creds[creds.username] == creds.hashed_password:
        for user in users:
            if user.username == creds.username:
                api_key = generate_api_key()
                user.api_key = api_key
        return {"API_KEY": api_key}

    else:
        return {"Error": "Username or Password is Incorrect"}


@app.get("/inbox/{api_key}")
def get_inbox(api_key):
    if api_key in api_key_to_user:
        return api_key_to_user[api_key].messages
    else:
        return {"Error": "User Doesn't Exist!"}


def generate_api_key():
    return hashlib.sha256(os.urandom(32)).hexdigest()
