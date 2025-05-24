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