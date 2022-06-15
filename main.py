import hashlib
import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import bcrypt
import mysql.connector


class Credentials(BaseModel):
    username: str
    hashed_password: str


class Message(BaseModel):
    api_key: str
    from_display_name: str
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
mydb = mysql.connector.connect(
    host ="34.79.189.28",
    user ="admin",
    passwd ="3(6L<C\\1-0GK=KG%",
    database= "app"
)

users = []
stored_creds = {}
api_key_to_user = {}
username_to_user = {}

cursor = mydb.cursor()

query = "SELECT * FROM users"

cursor.execute(query)

myresult = cursor.fetchall()

@app.get("/")
def home():
    return myresult


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
    username_to_user[user.username] = user
    users.append(user)
    return {"API_KEY": user.api_key}


@app.post("/send-message")
def send_message(message: Message):
    sent = False
    if not check_api_key(message.api_key):
        return {"Error": "Api key isn't valid"}
    if message.to_username in username_to_user.keys():
        username_to_user[message.to_username].messages.append(message)
        sent = True
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


def check_api_key(api_key):
    if api_key in api_key_to_user.keys():
        return True
    return False
