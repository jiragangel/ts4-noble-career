import inspect

def display_all_attributes(object, f):
    all_members = inspect.getmembers(object)

    for name, value in all_members:
        print(f"{name}: {value}", file=f)