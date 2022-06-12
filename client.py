import json
from os.path import exists

import requests as r
import urllib.parse
import os.path

# Check if they have api key
# if they do, contact the api and just say welcome back {name}
# if they don't make them call the api and store their api key.


our_server = "https://psychic-force-349901.nw.r.appspot.com/"


class User:
    username: str
    password: str
    display_name: str
    api_key: str
    messages: str


class Message:
    api_key: str
    to_username: str
    from_display_name: str
    message: str

    def __init__(self, api_key, to_username, from_display_name, message):
        self.api_key = api_key
        self.to_username = to_username
        self.from_display_name = from_display_name
        self.message = message


def main():
    if not exists("api_key"):
        sign_up()

    with open("api_key", "r") as f:
        api_key = f.read()


    message = Message(api_key, "Luke","Dick", "Message")
    print(message.to_username)
    print(send_message(message))

    print(get_inbox(api_key).json())


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


def send_message(message: Message):
    data = {
        'api_key': message.api_key,
        'from_display_name': message.from_display_name,
        'to_username': message.to_username,
        'message': message.message
    }

    return r.post(f"{our_server}/send-message", json=data).text


def print_messages(message_list):
    for message in message_list:
        print(f"From {message['from_username']} ")
        print(message['message'])


if __name__ == '__main__':
    main()
