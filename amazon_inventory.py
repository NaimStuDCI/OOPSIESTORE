import csv, os, sys, time 
from datetime import datetime
from version_system import *
from userauth import authenticate_user

FILENAME = "warehouse_inventory.csv"

def load_data():
    """Loads the data from the CSV file."""
    with open(FILENAME,mode="r",newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)
    
def create_backups(func):
    """Decorator to create backups of the CSV file."""
    def wrapper(*args, **kwargs):
        """Creates a backup of the CSV file before executing the function."""
        num_of_backups = 5
        # delete the oldest backup
        backupname = FILENAME[0:-3] + "bk" + str(num_of_backups)
        if os.path.exists(backupname):
            os.remove(backupname)
        # rename the remaining backups
        while num_of_backups > 1:
            new_filename = FILENAME[0:-3] + "bk" + str(num_of_backups)
            old_filename = FILENAME[0:-3] + "bk" + str(num_of_backups - 1)
            if os.path.exists(old_filename):
                os.rename(old_filename, new_filename)
            num_of_backups -= 1
        # rename the original filename to the first backup
        new_filename = FILENAME[0:-3] + "bk" + str(num_of_backups)
        if os.path.exists(FILENAME):
            os.rename(FILENAME, new_filename)
        return func(*args, **kwargs)
    return wrapper

def use_version_system(func):
    """Decorator to use the version system for backups.
    Creates a backup of the CSV file before executing the function."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        history = read_backups()
        comment = kwargs.get("vscomment")        
        input()
        update_backups(FILENAME, history, comment)
        return result
    return wrapper

# @create_backups
@use_version_system
def save_data(data,vscomment):
    """Saves the data to the CSV file."""
    with open(FILENAME,mode="w",newline="") as file:
        fieldnames = ["item","quantity","expiration_date","price"]
        writer = csv.DictWriter(file,fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Here two decorators
def progress_bar(func):
    """Decorator to show a progress bar while executing the function."""
    def wrapper(*args,**kwargs):
        for i in range(21):
            time.sleep(0.1)
            sys.stdout.write("\r")
            sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
            sys.stdout.flush()
        print('\nDone')
        result = func(*args,**kwargs)
        return result
    return wrapper

def check_item_present(func):
    """Decorator to check if the item is present in the data."""
    def wrapper(data,*args,**kwargs):
        item = kwargs.get("item")
        if any(d["item"]== item for d in data):
            return func(data,*args,**kwargs)
        else :
            print(f"Item {item} not found")
            input()
            return 
    return wrapper

def check_valid_itemdata(func):
    """Decorator to check if the item data is valid
    and convert it to the correct type."""
    def wrapper(*args, **kwargs):
        item_name = kwargs.get("item")
        item_quantity = kwargs.get("quantity")
        item_price = kwargs.get("price")
        expiration_date = kwargs.get("expiration_date")
        comment = kwargs.get("vscomment")
        try:
            int(item_quantity)
        except:
            item_quantity = "0"
        try:
            float(item_price)
        except:
            item_price = "0.0"
        try:
            datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            expiration_date = "1970-01-01"
        return func(*args, vscomment=comment, item=item_name, quantity=item_quantity, expiration_date=expiration_date, price=item_price)
    return wrapper

@check_valid_itemdata
@authenticate_user
@progress_bar
def add_item(data,vscomment,item,quantity,expiration_date,price):
    """Adds an item to the data."""
    data.append({
        "item":item,
        "quantity":quantity,
        "expiration_date":expiration_date,
        "price":price
    })
    save_data(data,vscomment=vscomment)
    return

@check_item_present
@authenticate_user
@progress_bar
def update_item(data,vscomment, item,quantity=None,expiration_date=None,price=None):
    """Updates an item in the data."""
    for d in data :
        if d["item"] == item:
            if quantity:
                d["quantity"]=quantity
            if expiration_date:
                d["expiration_date"] = expiration_date
            if price:
                d["price"]= price
    save_data(data, vscomment=vscomment)
    return

@check_item_present
@authenticate_user
@progress_bar
def remove_item(data,vscomment, item):
    """Removes an item from the data."""
    data = [d for d in data if d["item"].lower() != item.lower()]#dummy delete
    save_data(data, vscomment=vscomment)
    return

def sort_by_expiration_date(data):
    """Sorts the data by expiration date."""
    return sorted(data,key=lambda x:datetime.strptime(x["expiration_date"],"%Y-%m-%d"))

def sort_by_quantity(data):
    """Sorts the data by quantity."""
    return sorted(data,key=lambda x:int(x["quantity"]))

def sort_by_price(data):
    """Sorts the data by price."""
    return sorted(data,key=lambda x:float(x["price"]))

def get_full_report(data):
    """Generates a full report of the data."""
    if not data:
        print("No items in the inventory.")
        return None
    data = sort_by_expiration_date(data)
    print("\nFull Inventory Report\n")
    print_report(data) 

def get_expired_items(data):
    """Gets the expired items from the data."""
    expired_items = [d for d in data if datetime.strptime(d["expiration_date"],"%Y-%m-%d") < datetime.now()]
    return expired_items

def print_report(data):
    """Prints the report of the data or part of data."""   
    if data:
        print("-" * 60)
        print(f"|{'Item':<20} | {'Quantity':<10} | {'Expiration Date':<20} | {'Price':<10}|")
        print("-" * 60)
        for item in data:
            print(f"|{item['item']:<20} | {item['quantity']:<10} | {item['expiration_date']:<20} | {item['price']:<10}|")
            
@check_item_present
def search_item(data, item):
    """Searches for an item in the data."""
    result = []
    for i in data:
        if i["item"] == item:
            result.append(i)
    return result

if __name__ == "__main__":
    print("done") 