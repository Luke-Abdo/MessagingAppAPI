import json
from os.path import exists

import requests as r
import urllib.parse
import os.path

# Check if they have api key
# if they do, contact the api and just say welcome back {name}
# if they don't make them call the api and store their api key.


our_server = "http://127.0.0.1:50000"


class User():
    username: str
    password: str
    display_name: str
    api_key: str
    messages: str


def main():
    if not exists("api_key"):
        sign_up()

    with open("api_key", "r") as f:
        api_key = f.read()


def sign_up():
    name = input("Enter your username: ")
    password = input("Enter your password: ")
    display_name = input("Enter your display name: ")

    data = {
        'username': name,
        'password': password,
        'display_name': display_name
    }

    end_point = our_server + "/create-user"
    response = r.post(end_point, json=data)

    # Change
    if response.text == '"Error": "Username Taken"':
        print("Username is taken, Try again")
        sign_up()

    print(response.json())
    api_key = response.json()["API_KEY"]
    with open("api_key", "w") as f:
        f.write(api_key)


def get_inbox(api_key):
    return r.get(f"{our_server}/inbox/{api_key}")


def send_message(from_api_key, to_api_key, message):
    data = {
        'from_username': from_api_key,
        'to_username': to_api_key,
        'message': message
    }

    r.post(f"{our_server}/send-message", json=data)


def print_messages(message_list):
    for message in message_list:
        print(f"From {message['from_username']} ")
        print(message['message'])


if __name__ == '__main__':
    main()
