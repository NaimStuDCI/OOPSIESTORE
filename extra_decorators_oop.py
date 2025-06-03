import os, shutil, sys, time

class ProgressBar:

    def __init__(self, speed = 0.025):
        self.speed = speed

    def show_bar(self):
        for i in range(21):
            time.sleep(self.speed)
            sys.stdout.write("\r")
            sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
            sys.stdout.flush()
        print('\nDone')

class TinyBackups:

    def __init__(self, file_to_backup, max_backups = 5):
        self.orig_filename = file_to_backup
        self.total_backups = max_backups

    def do_backups(self):    

        # delete the oldest backup
        backup_filename = self.orig_filename.rsplit(".", 1)[0] + ".bk" + str(self.total_backups)
        if os.path.exists(backup_filename):
            os.remove(backup_filename)

        # rename the remaining backups
        counter = self.total_backups
        while counter > 1:
            new_backup_filename = self.orig_filename.rsplit(".", 1)[0] + ".bk" + str(counter)
            old_backup_filename = self.orig_filename.rsplit(".", 1)[0] + ".bk" + str(counter - 1)
            if os.path.exists(old_backup_filename):
                os.rename(old_backup_filename, new_backup_filename)
            counter -= 1

        # rename the original filename to the first backup
        backup_filename = self.orig_filename.rsplit(".", 1)[0] + ".bk" + str(counter)
        if os.path.exists(self.orig_filename):
            shutil.copy(self.orig_filename, backup_filename)

def progress_bar(func):
    """Decorator to show a progress bar while executing the function."""
    def wrapper(*args,**kwargs):
        print()
        progress_bar = ProgressBar(0.05)
        progress_bar.show_bar()
        result = func(*args,**kwargs)
        return result
    return wrapper

# Decorator for use in amazon_inventory_oop
def create_backups(file_to_backup, max_backups):
    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            
            tiny_backups = TinyBackups(file_to_backup, max_backups)
            tiny_backups.do_backups()

            return func(*args, **kwargs)
        return wrapper
    return inner_decorator

if __name__ == "__main__":
    progress = ProgressBar()
    progress.show_bar()
    
    file_to_backup = os.path.basename(__file__)  # The name of THIS file in the file system
    num_of_backups = 5
    tiny_backup = TinyBackups(file_to_backup, num_of_backups)
    tiny_backup.do_backups()