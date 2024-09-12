from sys import exit
import socket, re

#import RPi.GPIO as GPIO # for use with Raspberry Pi 4 SBC for interrupt control from GPIO, will need to be changed for other SBCs / Microcontrollers.
#shutdown_button_GPIO = 16 # comment out all Rpi GPIO code for use with non Pi4

# def retrieve_user_data(): //for using the get api for website, not sockets
#     try:
#             scanner_output = input("Enter UFID or ISO (8 or 16 digits), or type 'close' to end: ") # can probably leave text, this is not being displayed
#             if scanner_output.lower() == "close":
#                 client_socket.send("close".encode("utf-8"))
#                 return "shutdown"

#             if not re.match(r"^(\d{8}|\d{16})$", scanner_output):
#                 return "error_with_scan"

#             client_socket.send(scanner_output.encode("utf-8"))
#             try:
#                 name_length_bytes = client_socket.recv(1)
#                 if not name_length_bytes:
#                     print("Connection closed by server.")
#                     break

#                 name_length = int.from_bytes(name_length_bytes, byteorder='big')
#                 name = client_socket.recv(name_length).decode("utf-8")
#                 print("Received Name:", name)
#                 return name, accept
            


            
#             except socket.error as err:
#                 print("Error when receiving info from server:", err)
#                 break
#     except KeyboardInterrupt:
#         print("Keyboard Interrupt entered. Exiting...")
#     finally:
#         client_socket.close()

        


def retrieve_data_socket(UFID, client_socket):
    try:
            client_socket.send(UFID.encode("utf-8"))
            valid = client_socket.recv(1) # 1 if found in corresponding database entry, 0 if not (bool)

            name_length_bytes = client_socket.recv(1)
            name_length = int.from_bytes(name_length_bytes, byteorder='big')
            if(name_length == -1):
                print("Connection closed by server.")
                return "closed"
            
            name = client_socket.recv(name_length).decode("utf-8")
            
            return valid, name 
    except socket.error as err:
        print("Error when receiving info from server:", err)
    except KeyboardInterrupt:
        print("Keyboard Interrupt entered. Exiting...")
    finally:
        client_socket.close()

# def daily_interrupt():
#     #temp

def init_socket():
    server_ip = "10.136.122.126" # needs to be hardcoded based on laptop ip used in server file
    server_port = 8912 # not a reserved port used in tcp or udp

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        return client_socket
    except socket.error as err:
        print("Socket error:", err)
        exit(1)
    