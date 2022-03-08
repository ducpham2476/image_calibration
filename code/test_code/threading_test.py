import threading
import time
import os
import datetime

threads = []


def thread_1():
    print(threading.currentThread().getName(), 'Starting')
    time.sleep(2)
    print(threading.currentThread().getName(), 'Exiting')
    # print("This is the first thread number {}".format(value))
    # print("Datetime 1:", datetime.datetime.today())


def thread_2():
    print(threading.currentThread().getName(), 'Starting')
    time.sleep(4)
    print(threading.currentThread().getName(), 'Exiting')
    # print("This is the second thread")
    # print("Datetime 2:", datetime.datetime.today())


# for index in range(2):
#     thread = threading.Thread(target=thread_1, args=(index,))
#     threads.append(thread)
#     thread.start()

first_thread = threading.Thread(name='1st_thread', target=thread_1)
second_thread = threading.Thread(name='2nd_thread', target=thread_1)
third_thread = threading.Thread(name='3rd_thread', target=thread_2)

first_thread.start()
second_thread.start()
third_thread.start()