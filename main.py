from datetime import datetime
from os import system
from amazon_inventory import *

def check_input(type_to_check):
    def wrapper(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            is_okay = True
            if type_to_check == "int":
                try:
                    int(result)
                except:
                    input(f"The input should be \"{type_to_check}\".")
                    is_okay = False
            elif type_to_check == "float":
                try:
                    float(result)
                except:
                    input(f"The input should be \"{type_to_check}\".")
                    is_okay = False
            elif type_to_check == "date":
                try:
                    datetime.strptime(result, "%Y-%m-%d")
                except ValueError:
                    input(f"The input should be \"{type_to_check}\".")
                    is_okay = False
            return result, is_okay
        return inner
    return wrapper

@check_input("int")
def int_input(string):
    return input(string)

@check_input("float")
def float_input(string):
    return input(string)

@check_input("date")
def date_input(string):
    return input(string)

def sorted_by(data, key):
    if key == "expiration_date":
        system("clear")
        print(f"Sorted by {key}")
        print_report(sort_by_expiration_date(data))
        input("\nPress <Enter> to continue")
    elif key == "quantity":
        system("clear")
        print(f"Sorted by {key}")
        print_report(sort_by_quantity(data))
        input("\nPress <Enter> to continue")
    elif key == "price":
        system("clear")
        print(f"Sorted by {key}")
        print_report(sort_by_price(data))
        input("\nPress <Enter> to continue")




def main():
    warehouse_data = load_data()

    while True:
        system("clear")
        print("\nWarehouse Inventory Menu:")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Update Item")
        print("4. Get Full Report")
        print("5. Get Expired Items")
        print("6. Search Item")
        print("7. Sort by Expiration Date")
        print("8. Sort by Price")
        print("9. Sort by Quantity")
        print("10. Restore a backup")
        print("0. Quit") 
        
        choice = int_input("Enter your choice (1–10) or Quit: ")
        if choice[1]:
            choice = choice[0]

        match choice:
            case "1":
                item_name = input("Enter item name: ")
                while not item_name:
                    item_name = input("Enter item name: ")
                item_quantity = int_input("Enter item quantity: ")
                while not item_quantity[1]:
                    item_quantity = int_input("Enter item quantity: ")
                item_quantity = item_quantity[0]
                expiration_date = date_input("Enter expiration date (YYYY-MM-DD): ")
                while not expiration_date[1]:
                    expiration_date = date_input("Enter expiration date (YYYY-MM-DD): ")
                expiration_date = expiration_date[0]
                item_price = float_input("Enter item price: ")
                while not item_price[1]:
                    item_price = float_input("Enter item price: ")
                item_price = item_price[0]
                comment = f"{item_name} added to the inventory"
                add_item(warehouse_data, vscomment=comment, item=item_name, quantity=item_quantity, expiration_date=expiration_date, price=item_price)
                warehouse_data = load_data()
            case "2":
                item_name = input("Enter item name to remove: ")
                comment = f"{item_name} removed from the inventory"
                remove_item(warehouse_data, vscomment=comment, item=item_name)
                warehouse_data = load_data()
            case "3":
                item_name = input("Enter item name to update: ")
                item_quantity = int_input("Enter new item quantity (or leave blank to skip) or \"0\": ")
                if item_quantity[0] == "":
                    item_quantity = (item_quantity[0], True)
                while not item_quantity[1]:
                    item_quantity = int_input("Enter item quantity: ")
                item_quantity = item_quantity[0]
                expiration_date = date_input("Enter new expiration date (YYYY-MM-DD) (or leave blank to skip): ")
                if expiration_date[0] == "":
                    expiration_date = (expiration_date[0], True)
                while not expiration_date[1]:
                    expiration_date = date_input("Enter expiration date (YYYY-MM-DD): ")
                expiration_date = expiration_date[0]
                item_price = float_input("Enter new item price (or leave blank to skip) or \"0.0\": ")
                if item_price[0] == "":
                    item_price = (item_price[0], True)
                while not item_price[1]:
                    item_price = float_input("Enter item price: ")
                item_price = item_price[0]
                comment = f"{item_name} updated in the inventory"
                update_item(warehouse_data, vscomment=comment, item=item_name, quantity=item_quantity, expiration_date=expiration_date, price=item_price)
                warehouse_data = load_data()
            case "4":
                get_full_report(warehouse_data)
                input("\nPress <Enter> to continue")
            case "5":
                print("Expired Items:")
                expired_items = get_expired_items(warehouse_data)
                print_report(expired_items)
                input("\nPress <Enter> to continue")
            case "6":
                system("clear")
                print("Here you can search for one item:")
                item_name = input("Enter an itemname: ")
                print_report(search_item(warehouse_data, item=item_name))
                input("\nPress <Enter> to continue")
            case "7":
                sorted_by(warehouse_data, "expiration_date")
            case "8":
                sorted_by(warehouse_data, "price")
            case "9":
                sorted_by(warehouse_data, "quantity")
            case "10":
                restore_version(FILENAME)
                warehouse_data = load_data()
            case "0":
                print("Exiting the program.")
                break

if __name__ == "__main__":
    
    main()