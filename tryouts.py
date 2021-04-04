import time
from threading import Thread
def wait_seconds():
    time.sleep(30)
    print("I waited 30 seconds "+str(time.time()))

def wait_minute():
    time.sleep(60)
    print("I waited 60 seconds " + str(time.time()))

data_thread = Thread(target=wait_seconds)
task2 = Thread(target=wait_minute)
while True:
    print("I start at "+str(time.time()))
    data_thread.start()
    task2.start()
