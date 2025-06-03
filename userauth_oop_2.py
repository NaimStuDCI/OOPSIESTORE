import json, hashlib

class User:

    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password  
        self.role = role

    def check_password(self, password):
        return self.password == password
    
    def is_admin(self):
        return self.role == "admin"
    
class UserManager:

    USERS_FILE = "users_2.json"
    
    def __init__(self):
        self.users = self.load_users()

    def hash_password(self, password):
        """ Generates a SHA-256 hash of a password. """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self):
        """Reads the user's database from the JSON file."""
        with open(self.USERS_FILE, "r") as json_file:
            users = set()
            users_dictionary = json.load(json_file)
            for user in users_dictionary.keys():
                users.add(User(user, users_dictionary[user]["password"], users_dictionary[user]["role"]))
        return users

    def find_user(self, username):
        """Finds a user by username."""
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def add_user(self, username, password, role="user"):
        """Adds a new user to the database."""
        if self.find_user(username):
            print(f"User {username} already exists.")
            return False
        new_user = User(username, password, role)
        new_user.password = self.hash_password(new_user.password)
        self.users.add(new_user)
        self.save_users()
        return True
    
    def del_user(self, username):
        """Deletes an existing user from the database."""
        try:
            self.users.remove(self.find_user(username))
        except:
            print(f"\nUser \"{username}\" does not exist.\n")
            return False
        print(f"\nUser \"{username}\" successfully deleted.\n")
        self.save_users()
        return True
    
    def save_users(self):
        """Writes the user's database to the JSON file."""
        with open(self.USERS_FILE, "w") as json_file:
            users = {}
            for user in self.users:
                users[user.username] = {
                    "password": user.password,
                    "role": user.role
                }
            json.dump(users, json_file, indent = 4)

    def authenticate(self):
        user_id = input("\nPlease enter your User ID: ")
        password = input("Enter password: ")
        for user in self.users:
            if user.username == user_id and user.password == self.hash_password(password):
                return user.is_admin()
        return False

def authenticate_user(func):
    def wrapper(*args, **kwargs):
        users = UserManager()
        if users.authenticate():
            return func(*args, **kwargs)
        else:
            print("\nAuthentication failed!")
    return wrapper

if __name__ == "__main__":
    users = UserManager()
    print(f"\nThe Users of this App\n{"=" * 21}\n")
    for user in users.users:
        print(f"\"{user.username}\" is {user.role} with password = {user.password}")
