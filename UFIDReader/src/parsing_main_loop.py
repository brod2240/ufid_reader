from validation import *
from comms import *
from queue import Queue
import sys
import select
import usb.core
import hid


def parsing_main_loop(shared_queue):
    #client_socket = init_socket()
    #current_gui_state = "default"
    while(1):
        #current_gui_state = shared_queue.get()

        #if(current_gui_state == "shutdown"):
            #break
            # add any other required shutdown processes, make sure things are properly stopped

        UFID = read_ufid()
        if UFID != "-1" :



           # status = retrieve_data_socket(UFID,client_socket)

        # display UFID, and the status is what will be sent to gui thread to decide what to display

        #shared_queue.put(name) # might add extra info as well
            shared_queue.put(1)
       # print(shared_queue.get())
        # shared queue can be accessed by both gui and parsing main loop. Parsing adds data for the gui to pull and use to display the corresponding frames



def read_ufid():
    device = usb.core.find(idVendor=0x04d8,idProduct=0xf3cb)
    #device = hid.device()
    #device.open(0x04d8,0xf3cb)

    if device is None:
        print("ERROR: NOT FOUND")
        return -1
    #device.set_configuration()

    cfg = device.get_active_configuration()
    intf = cfg[(0,0)]

    ep = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
   # i = device[0].interfaces()[5].bInterfaceNumber
    try:
       device.detach_kernel_driver(0)
    except usb.core.USBError as err:
       print(err)
    #deviceHID = hid.device()
    #deviceHID.open(0x04d8,0xf3cb)
    while(1) :
        try:
            data = device.read(ep.bEndpointAddress,8)
            return 1
            #data_integer = int.from_bytes(data.tobytes(),byteorder='little')
            #decoded = ''.join([chr(x) for x in data])
            #data = lambda ba: ''.join([f'{b:02x}' for b in ba])
            #print(data)
        except usb.core.USBError as err:
            print(err)

    #scanner_output = " " 
    #if select.select([sys.stdin],[],[],0.1)[0]:
       # scanner_output = sys.stdin.readline().strip()
       # print(scanner_output)
    #scanner_output = input("Enter UFID or ISO (8 or 16 digits), or type 'close' to end: ")
    #print(scanner_output)
    #if not re.match(r"^(\d{8}|\d{16})$", scanner_output):
        #return "-1"
    
   # return scanner_output
        

        

if __name__ == '__main__':
    queue = Queue()
    parsing_main_loop(queue)
