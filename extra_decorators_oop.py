import sys, time

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

def progress_bar(func):
    """Decorator to show a progress bar while executing the function."""
    def wrapper(*args,**kwargs):
        print()
        progress_bar = ProgressBar(0.05)
        progress_bar.show_bar()
        result = func(*args,**kwargs)
        return result
    return wrapper

if __name__ == "__main__":
    progress = ProgressBar()
    progress.show_bar()