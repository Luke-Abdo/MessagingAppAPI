import json
from os.path import exists

import requests as r
import urllib.parse
import os.path

# Check if they have api key
# if they do, contact the api and just say welcome back {name}
# if they don't make them call the api and store their api key.


our_server = "http://127.0.0.1:50000"


def main():
    if not exists("api_key"):
        sign_up()

    with open("api_key", "r") as f:
        api_key = f.read()

    response = r.get(f"{our_server}/login/{api_key}")

    print(response.json())

    send_message(api_key, api_key, "Hello World")
    print_messages(get_inbox(api_key))


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

    api_key = response.json()["API_KEY"]
    with open("api_key", "w") as f:
        f.write(api_key)

    print(api_key)


def get_inbox(api_key):
    return r.get(f"{our_server}/inbox/{api_key}").json()


def send_message(from_api_key, to_api_key, message):
    data = {
        'from_api_key': from_api_key,
        'to_api_key': to_api_key,
        'message': message
    }

    r.post(f"{our_server}/send-message", json=data)


def print_messages(message_list):
    for message in message_list:
        print(f"From {message['from_api_key']} ")
        print(message['message'])


if __name__ == '__main__':
    main()
