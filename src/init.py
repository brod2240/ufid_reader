import threading
from queue import Queue
from parsing_main_loop import *
from gui_main_loop import *

# main python code, start threads and begin function

def init_threads():
    shared_queue = Queue()

    parsing_thread = threading.Thread(target=parsing_main_loop, args=(shared_queue,))
    gui_thread = threading.Thread(target=gui_main_loop, args=(shared_queue,))

    parsing_thread.start()
    gui_thread.start()

    parsing_thread.join()
    gui_thread.join()

if __name__ == '__main__':
    init_threads()
    exit(0)
