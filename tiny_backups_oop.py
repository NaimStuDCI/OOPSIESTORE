import os

class TinyBackups:

    def __init__(self, file_to_backup, max_backups = 5):
        self.orig_filename = file_to_backup
        self.total_backups = max_backups

    def do_backups(self):    

        # delete the oldest backup
        backup_filename = self.orig_filename[0:-3] + "bk" + str(self.total_backups)
        if os.path.exists(backup_filename):
            os.remove(backup_filename)

        # rename the remaining backups
        counter = self.total_backups
        while counter > 1:
            new_backup_filename = self.orig_filename[0:-3] + "bk" + str(counter)
            old_backup_filename = self.orig_filename[0:-3] + "bk" + str(counter - 1)
            if os.path.exists(old_backup_filename):
                os.rename(old_backup_filename, new_backup_filename)
            counter -= 1

        # rename the original filename to the first backup
        backup_filename = self.orig_filename[0:-3] + "bk" + str(counter)
        if os.path.exists(self.orig_filename):
            os.rename(self.orig_filename, backup_filename)

# Decorator for use in amazon_inventory_oop
def create_backups(file_to_backup, max_backups):
    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            
            tiny_backups = TinyBackups(file_to_backup, max_backups)
            tiny_backups.do_backups()

            return func(*args, **kwargs)
        return wrapper
    return inner_decorator