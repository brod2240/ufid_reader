from src.validation import *
from src.comms import *

def parsing_main_loop(shared_queue):
    client_socket = init_socket()
    #current_gui_state = "default"
    while(1):
        #current_gui_state = shared_queue.get()

        #if(current_gui_state == "shutdown"):
            #break
            # add any other required shutdown processes, make sure things are properly stopped

        UFID = read_ufid()
        if(UFID == "-1"):
            continue

        valid = retrieve_data_socket(UFID, client_socket)

        if(valid):
            status = 1

        # display UFID, and the status is what will be sent to gui thread to decide what to display

        #shared_queue.put(name) # might add extra info as well
        shared_queue.put(status)
        # shared queue can be accessed by both gui and parsing main loop. Parsing adds data for the gui to pull and use to display the corresponding frames



def read_ufid():
    scanner_output = input("Enter UFID or ISO (8 or 16 digits), or type 'close' to end: ")

    if not re.match(r"^(\d{8}|\d{16})$", scanner_output):
        return "-1"
    
    return scanner_output
        

        

