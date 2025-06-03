import csv
from datetime import datetime
from version_system_oop import *
from userauth_oop import authenticate_user
from extra_decorators_oop import progress_bar, create_backups

class Item:
    """Represents an item in the warehouse inventory."""
    def __init__(self, item, quantity = 0, expiration_date = "1970-01-01", price = 0.0):
        """Initializes an item with its name, quantity, expiration date, and price."""
        self.item = item
        self.quantity = quantity
        self.expiration_date = expiration_date
        self.price = price

    def update_values(self):
        """Updates the values of the item."""
        print(f"\nUpdate the values for \"{self.item}\": Press <ENTER> to skip update")

        # Quantity update
        while (new_value := input(f"\nQuantity is: \"{self.quantity}\" and should be: ")) != "":
            if new_value.isdigit():
                self.quantity = new_value
                break
            else:
                print("\nOnly natural numbers, including 0!\n")

        # Expiration date update
        while (new_value := input(f"\nExpiration date is: \"{self.expiration_date}\" and should be: ")) != "":
            try:
                datetime.strptime(new_value, "%Y-%m-%d")
                self.expiration_date = new_value
                break
            except:
                print("\nThe format must be \"YYYY-MM-DD\"!\n")

        # Price update
        while (new_value := input(f"\nPrice is: \"{self.price}\" and should be: ")) != "":
            try:
                if float(new_value) >= 0:
                    self.price = new_value
                    break
            except:
                print("\nOnly positiv numbers, including 0!\n")
    
class InventoryManager:
    """Manages the warehouse inventory using a CSV file."""
    FILENAME = "warehouse_inventory.csv"
    DIRECTORY = "./backups/"
    def __init__(self):
        """Initializes the InventoryManager and loads the inventory data."""
        if not os.path.exists(self.DIRECTORY):
            os.makedirs(self.DIRECTORY)
        self.data = self.load_data()

    def load_data(self):
        """Reads the inventory data from the CSV file."""
        with open(self.FILENAME, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            data = []
            for row in reader:
                data.append(Item(row["item"], row["quantity"], row["expiration_date"], row["price"]))
        return data

    def reload_data(self):
        """Reloads the inventory data from the CSV file."""
        self.data = self.load_data()

    @progress_bar
    # @create_backups(FILENAME, 5)
    @use_version_system_oop
    def write_data(self,*args, **kwargs):
        """Writes the inventory data to the CSV file."""
        with open(self.FILENAME, "w", newline="") as csv_file:
            fieldnames = ["item", "quantity", "expiration_date", "price"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.data:
                writer.writerow({"item": item.item, "quantity": item.quantity, "expiration_date": item.expiration_date, "price": item.price})

    
    @authenticate_user
    def add_item(self, new_item_name):
        """Adds an item to the inventory."""
        for item in self.data:
            if item.item == new_item_name:
                print(f"\nItem \"{new_item_name}\" already exists in inventory.")
                return
        new_item = Item(new_item_name)
        new_item.update_values()
        self.data.append(new_item)
        self.write_data(filename = self.FILENAME,vscomment=f"New Item '{new_item_name}' added to inventory.")
        print(f"\nItem \"{new_item_name}\" successfully added to inventory.")

    @authenticate_user
    def remove_item(self, item_name):
        """Removes an item from the inventory."""
        for item in self.data:
            if item.item == item_name:
                self.data.remove(item)
                self.write_data(filename = self.FILENAME, vscomment=f"Item '{item_name}' removed from inventory.")
                print(f"\nItem \"{item_name}\" successfully removed from inventory.")
                return
        print(f"\nItem \"{item_name}\" not found in inventory.")



    @authenticate_user
    def update_item(self, item_name):
        """Updates an item in the inventory."""
        for item in self.data:
            if item.item == item_name:
                item.update_values()

                # Decorate / undecorate method "write_data()" with "use_version_system_oop(filename, vscomment)"
                # dummy = self.write_data
                # self.write_data = use_version_system_oop(self.FILENAME, f"Item '{item_name}' updated.")(self.write_data)
                # self.write_data()
                # self.write_data = dummy

                self.write_data(filename = self.FILENAME, vscomment=f"Item '{item_name}' updated.")
                #v_manager = VersionManager()
                #v_manager.update_backups(self.FILENAME, f"Item '{item_name}' updated.")

                print(f"\nItem \"{item_name}\" successfully updated.")
                return
        print(f"\nItem \"{item_name}\" not found in inventory.")

    def print_report(self,list_items = []):
        """Prints the inventory data in a readable format."""
        print(f"\n{'Item':<20} {'Quantity':<10} {'Expiration Date':<20} {'Price':<10}\n")
        for item in list_items:
            print(f"{item.item:<20} {item.quantity:<10} {item.expiration_date:<20} {item.price:<10}")

    def search_item(self, item_name):
        """Searches for an item in the inventory."""
        for item in self.data:
            if item.item == item_name:
                self.print_report([item])
                return
        print(f"\nItem \"{item_name}\" not found in inventory.")

    def print_full_report(self):
        """Prints the full inventory report."""
        self.print_report(self.data)

    def print_sorted_by_quantity(self):
        """Sorts the data by quantity."""
        self.print_report(sorted(self.data,key=lambda x:int(x.quantity)))

    def print_sorted_by_expiration_date(self):
        """Sorts the inventory by expiration date."""
        self.print_report(sorted(self.data,key=lambda x:datetime.strptime(x.expiration_date,"%Y-%m-%d")))

    def print_sorted_by_price(self):
        """Sorts the inventory by price."""
        self.print_report(sorted(self.data,key=lambda x:float(x.price)))

    def print_expired_items(self):
        """Prints the expired items in the inventory."""
        expired_items = [item for item in self.data if datetime.strptime(item.expiration_date,"%Y-%m-%d") < datetime.now()]
        if expired_items:
            self.print_report(expired_items)
        else:
            print("No expired items in the inventory.")

if __name__ == "__main__":
    pass