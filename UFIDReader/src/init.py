import threading, os, time
#import customtkinter
from queue import Queue
from parsing_main_loop import *
from gui_main_loop import *

# main python code, start threads and begin function

def start_gui():
    os.system("FRAMEBUFFER=/dev/fb1 startx -- -dpi 60")
    time.sleep(5)
   # os.system("DISPLAY=:0 python gui_main_loop.py")
    os.system("DISPLAY=:0 python ../GUI/gui.py")
    

def init_threads():
    shared_queue = Queue()

    parsing_thread = threading.Thread(target=parsing_main_loop, args=(shared_queue,))
    gui_thread = threading.Thread(target=gui_main_loop, args=(shared_queue,))

    parsing_thread.start()
   # start_gui()
    gui_thread.start()

   # parsing_thread.join()
   # gui_thread.join()

#def init_tests()

    

if __name__ == '__main__':
    #start_gui()
    init_threads()
    exit(0)
