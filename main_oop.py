from os import system
from amazon_inventory_oop import *

# import os
# if os.name == "nt": clear_crt = "cls"
# else: clear_crt = "clear"

clear_crt = "clear"
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
        print(" 7. Sort By Expiration Date")
        print(" 8. Sort By Price")
        print(" 9. Sort By Quantity")
        print("10. Restore A Backup")
        print(f"\n 0. Quit\n")

    def get_choice(self):
        try:
            self.choice = int(input("Enter your choice: "))
        except:
            self.choice = None

    def run_choice(self):
         match self.choice:

            case 1:
                system(clear_crt)
                print("\nAdd an item to the warehouse\n")
                inventory.add_item(input("Enter item name: "))
                input("\nPress <RETURN> to continue.\n")

            case 2:
                system(clear_crt)
                print("\nRemove an item from the warehouse\n")
                inventory.remove_item(input("\nEnter item name to remove: "))
                input("\nPress <RETURN> to continue.\n")

            case 3:
                system(clear_crt)
                print("\nUpdate an existing item of the warehouse\n")
                inventory.update_item(input("\nEnter the name of the item: "))
                input("\nPress <RETURN> to continue.\n")

            case 4:
                system(clear_crt)
                print("\nThe full report - unsorted")
                inventory.print_full_report()
                input("\nPress <RETURN> to continue.\n")

            case 5:
                system(clear_crt)
                print("\nThe list of expired items")
                inventory.print_expired_items()
                input("\nPress <RETURN> to continue.\n")

            case 6:
                system(clear_crt)
                print("\nSearch an item\n")
                inventory.search_item(input("Enter the item name you want to search: "))
                input("\nPress <RETURN> to continue.\n")

            case 7:
                system(clear_crt)
                print("\nThe full report - sorted by expiration date")
                inventory.print_sorted_by_expiration_date()
                input("\nPress <RETURN> to continue.\n")
            
            case 8:
                system(clear_crt)
                print("\nThe full report - sorted by price")
                inventory.print_sorted_by_price()
                input("\nPress <RETURN> to continue.\n")

            case 9:
                system(clear_crt)
                print("\nThe full report - sorted by quantity")
                inventory.print_sorted_by_quantity()
                input("\nPress <RETURN> to continue.\n")

            case 10:
                system(clear_crt)
                print("\nRestore data from an existing backup\n")
                v_manager.restore_version(filename)
                inventory.__init__()  # Reload the CSV-file into self.data, ask Markus how to improve (smelly code)
                input("\nPress <RETURN> to continue.\n")

            case 0:
                system(clear_crt)
                print("\nThank you for using this program!\n")
                warehouse.running = False

            case _:
                system(clear_crt)
                input("\nInvalid input!\n\nPress <RETURN> and try again.\n")

# Main part
warehouse = MenuManager()
inventory = InventoryManager()
v_manager = VersionManager()

# Main loop
while warehouse.running:

    warehouse.print_menu()
    warehouse.get_choice()
    warehouse.run_choice()