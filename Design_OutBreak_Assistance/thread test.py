import threading
import time

boss=1


def print_hello():
    global boss
    for i in range(20):
        time.sleep(0.5)
        print("Hello")

        boss=boss+1


def print_hi():

    for i in range(20):
        time.sleep(2)
        print("Hi")
        print("Boss=", boss)


t1 = threading.Thread(target=print_hello)
t2 = threading.Thread(target=print_hi)
t1.start()
t2.start()