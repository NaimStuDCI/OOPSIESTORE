from datetime import datetime
import json, os, shutil
from main import int_input
from userauth import authenticate_user

CONFIG_FILE = "warehouse_inventory.json"
DIRECTORY = "./backups/"

def read_backups():
    """Reads the backup history from the JSON file."""
    with open(CONFIG_FILE, "r") as json_file:
        history = json.load(json_file)
    return history

def write_backups(history):
    """Writes the backup history to the JSON file."""
    with open(CONFIG_FILE, "w") as json_file:
        json.dump(history, json_file, indent = 4)

def print_backups(history):
    """Prints the history of backups in a readable format."""
    for index, (file_name, file_comment) in enumerate(history.items(), start=1):    
        timestamp = file_name[0:-4][-14:]  # Extract timestamp
        dummy_date = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        timestamp = dummy_date.strftime("%d. %B %Y, %H:%M:%S")
        print(f"{index}: \"{file_comment}\" created at {timestamp}")

def create_copie(filename):
    """Creates a copy of the file with a timestamp."""
    new_filename = filename[0:-4] + datetime.now().strftime("%Y%m%d%H%M%S" + ".csv")
    if os.path.exists(filename):
        shutil.copy(filename, f"{DIRECTORY}{new_filename}")
    return new_filename

def update_backups(filename, history, vscomment):
    """Updates the backup history with a new entry."""
    key_name = create_copie(filename)
    history[key_name] = vscomment
    write_backups(history)
    print_backups(history)

@authenticate_user
def restore_version(filename):
    """Restores a version of the file from the backup history."""
    print("\n")
    history = read_backups()
    print_backups(history)
    list_of_files = list(history.keys())
    index = int_input("Enter the index of the backup you want to restore: ")
    while not index[1]:
        index = int_input("Enter the index of the backup you want to restore: ")
    index = int(index[0])
    if index < 1 or index > len(list_of_files):
        print("Invalid index. Please try again.")
        input()
        return
    version_filename = list(history.keys())[index - 1]
    update_backups(filename, history, f"restored from {version_filename}")
    shutil.copy(f"{DIRECTORY}{version_filename}", filename)
