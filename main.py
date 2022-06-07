import hashlib
import os

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import bcrypt
import urllib.parse


class User(BaseModel):
    username: str
    password: str
    display_name: str


salt = bcrypt.gensalt()

app = FastAPI()

users = []

creds = {}

api_keys = {}


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
    print(api_keys[api_key])

    return {"API_KEY": api_key}


@app.get("/login/{api_key}")
def login(api_key):
    if api_key in api_keys.keys():
        return {"Welcome back": api_keys.get(api_key).username}

    return "Please sign up"


def generate_api_key():
    return hashlib.sha256(os.urandom(32)).hexdigest()
