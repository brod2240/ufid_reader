from src.client import *
from src.validation import *

def parsing_main_loop(shared_queue):
    client_socket = init_socket()
    while(1):
        UFID, name = run_client() # might be rewritten, but run client currently uses sockets to communicate with a seperate hardcoded IP, and a hardcoded csv vile for student info
        # UFID, name are what is returned by the communication between other user or, in future, the website database


        shared_queue.put(name) # might add extra info as well
        shared_queue.put(status)
        # shared queue can be accessed by both gui and parsing main loop. Parsing adds data for the gui to pull and use to display the corresponding frames

        if(shutdown == 1): # change to be shared between both threads to shut down both at once, probably through the queue
            break

