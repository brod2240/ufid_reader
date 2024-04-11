from sys import exit
import socket,re

def run_client(client_socket):
    try:
        while True:
            if(not button_shutdown()):
                break

            scanner_output = input() # blocking
            if not re.match(r"^(\d{8}|\d{16})$", scanner_output):
               continue
            else:
                client_socket.send(scanner_output.encode("utf-8")[:16])            
    except KeyboardInterrupt:
        print("Keyboard Interrupt entered. Exiting...")
        exit(0)

def button_shutdown():
    # add functionality for button gpio?
    # interrupt for this button? Might not need this function if so...
    return True

def init_socket():
    server_ip = "123.123.123" # idk
    server_port = 8000 

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create client socket using TCP
    except socket.err as err:
        print("Error when initializing socket.")
        exit(1)

    try:
        client_socket.connect((server_ip,server_port))
    except socket.err as err:
        print("Error when establishing connection with server.")
        exit(1)

    return client_socket


if __name__ == '__main__':
    client_socket = init_socket()
    run_client(client_socket)
    exit(0)




