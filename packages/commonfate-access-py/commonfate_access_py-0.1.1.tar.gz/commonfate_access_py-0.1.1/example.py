import time
import commonfate_access


# @action
# def do_stuff():
#     print("hello world")


# run a loop here. In a production environment this could be
# a web application like Flask or Django serving HTTP requests,
# rather than just a sleep.
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("interrupted!")
