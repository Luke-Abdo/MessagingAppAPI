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
        api_key = f.read().strip()
        print(api_key)

    response = r.get(f"{our_server}/login/{api_key}")

    print(response.json())


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


if __name__ == '__main__':
    main()
