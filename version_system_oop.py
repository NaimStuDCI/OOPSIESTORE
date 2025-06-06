import json, os, shutil
from datetime import datetime
from userauth_oop import authenticate_user

class Version:
    """Represents a version of the warehouse inventory backup."""

    def __init__(self, filename, comment):
        self.filename = filename
        self.comment = comment

class VersionManager:
    """Manages the versioning system for warehouse inventory backups."""
    
    CONFIG_FILE = "warehouse_inventory.json"
    DIRECTORY = "./backups/"

    def __init__(self):
        """Initializes the VersionManager and reads existing backups."""
        if not os.path.exists(self.DIRECTORY):
            os.makedirs(self.DIRECTORY)
        self.history = self.read_backups()

    def read_backups(self):
        """Reads the backup history from the JSON file."""
        with open(self.CONFIG_FILE, "r") as json_file:
            versions = []
            version_dictionary = json.load(json_file)
            for version in version_dictionary.keys():
                versions.append(Version(version, version_dictionary[version]))
        return versions
    
    def write_backups(self):
        """Writes the current backup history to the JSON file."""
        with open(self.CONFIG_FILE, "w") as json_file:
            versions = {}
            for version in self.history:
                versions[version.filename] = version.comment
            json.dump(versions, json_file, indent = 4)

    def print_backups(self):
        """Prints the history of backups in a readable format."""
        print("\nThe list of available backup files:\n")
        index = 0
        for version in self.history:
            index += 1
            timestamp = version.filename[0:-4][-14:]  # Extract timestamp
            dummy_date = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
            timestamp = dummy_date.strftime("%d. %B %Y, %H:%M:%S")
            print(f"{index}: \"{version.comment}\" created at {timestamp}")
    
    def create_copie(self, filename):
        """Creates a copy of the file with a timestamp."""
        new_filename = filename[0:-4] + datetime.now().strftime("%Y%m%d%H%M%S" + ".csv")
        if os.path.exists(filename):
            shutil.copy(filename, f"{self.DIRECTORY}{new_filename}")
        return new_filename
    
    def update_backups(self, filename, vscomment):
        """Updates the backup history with a new entry."""
        key_name = self.create_copie(filename)
        self.history.append(Version(key_name, vscomment))
        self.write_backups()

    @authenticate_user # Decorator to authenticate user before restoring a version imported from userauth_oop
    def restore_version(self, filename):
        """Restores a version of the file from the backup history."""
        self.history = self.read_backups()
        self.print_backups()
        while (index := input(f"\nEnter the index number of the backup you wish to restore, or press <ENTER> to skip backup: ")) != "":
            if index.isdigit():
                index = int(index)
                if index > 0 and index <= len(self.history):  # Do backup
                    version_filename = self.history[index - 1].filename
                    self.update_backups(filename, f"restored from {version_filename}")
                    shutil.copy(f"{self.DIRECTORY}{version_filename}", filename)
                    return            
                else:
                    print("\nInvalid index. Please try again.")
        print("\nNo backup restored.")

# Version system decorator for use in amazon_inventory_oop
def use_version_system_oop(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        vers_man = VersionManager()
        vers_man.update_backups(kwargs["filename"], kwargs["vscomment"])
        return
    return wrapper

if __name__ == "__main__":
    pass