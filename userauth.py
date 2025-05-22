import json

USERS_FILE = "users.json"

def read_users():
    """Reads the user's database from the JSON file."""
    with open(USERS_FILE, "r") as json_file:
        users = json.load(json_file)
    return users

def write_users(users):
    """Writes the user's database to the JSON file."""
    with open(USERS_FILE, "w") as json_file:
        json.dump(users, json_file, indent = 4)

def authenticate(users, is_admin = False):
    user_id = input("Please enter your User ID: ")
    password = input("Enter password: ")
    for user in users.keys():
        if user == user_id and users[user]["password"] == password and users[user]["role"] == "admin":
            is_admin = True
    return is_admin

def authenticate_user(func):
    def wrapper(*args, **kwargs):
        users = read_users()
        if authenticate(users):
            return func(*args, **kwargs)
        else:
            input("Authentication failed!")
    return wrapper