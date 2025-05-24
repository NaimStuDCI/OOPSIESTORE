from os import system  # only for "clear screen"
from amazon_inventory_oop import *

# import os
# if os.name == "nt": clear_crt = "cls"
# else: clear_crt = "clear"

clear_crt = "cls"
filename = "warehouse_inventory.csv"

class MenuManager:

    running = True
    choice = None

    def print_menu(self):
        system(clear_crt)
        print(f"\nWarehouse Inventory Menu:\n{"=" * 25}\n")
        print(" 1. Add Item")
        print(" 2. Remove Item")
        print(" 3. Update Item")
        print(" 4. Get Full Report")
        print(" 5. Get Expired Items")
        print(" 6. Search Item")
        print(" 7. Sort by Expiration Date")
        print(" 8. Sort by Price")
        print(" 9. Sort by Quantity")
        print("10. Restore a backup")
        print(f"\n 0. Quit\n")

    def get_choice(self):
        try:
            self.choice = int(input("Enter your choice: "))
        except:
            self.choice = None

# Main part
warehouse = MenuManager()
inventory = InventoryManager()

# Main loop
while warehouse.running:

    warehouse.print_menu()
    warehouse.get_choice()

    match warehouse.choice:

        case 4:
            system(clear_crt)
            print("\nThe full report - unsorted\n")
            inventory.print_full_report()
            input("\nPress <RETURN> to continue.\n")

        case 5:
            system(clear_crt)
            print("\nThe list of expired items\n")
            inventory.print_expired_items()
            input("\nPress <RETURN> to continue.\n")

        case 6:
            system(clear_crt)
            print("\nSearch an item\n")
            inventory.search_item(input("Enter the itemname you want to search: "))
            input("\nPress <RETURN> to continue.\n")

        case 7:
            system(clear_crt)
            print("\nThe full report - sorted by expiration date\n")
            inventory.print_sorted_by_expiration_date()
            input("\nPress <RETURN> to continue.\n")
        
        case 8:
            system(clear_crt)
            print("\nThe full report - sorted by price\n")
            inventory.print_sorted_by_price()
            input("\nPress <RETURN> to continue.\n")

        case 9:
            system(clear_crt)
            print("\nThe full report - sorted by quantity\n")
            inventory.print_sorted_by_quantity()
            input("\nPress <RETURN> to continue.\n")

        case 10:
            system(clear_crt)
            print("\nRestore data from an existing backup\n")
            vers_man = VersionManager()
            vers_man.restore_version(filename)           
            input("\nPress <RETURN> to continue.\n")

        case 0:
            system(clear_crt)
            print("\nThank you for using this program!\n")
            warehouse.running = False

        case _:
            system(clear_crt)
            input("\nInvalid input!\n\nPress <RETURN> and try again.\n")