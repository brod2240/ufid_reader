from sys import exit
import socket,re

import RPi.GPIO as GPIO # for use with Raspberry Pi 4 SBC for interrupt control from GPIO, will need to be changed for other SBCs / Microcontrollers.
shutdown_button_GPIO = 16

def run_client(client_socket):
    try:
        while True:
            scanner_output = input() # blocking
            if not re.match(r"^(\d{8}|\d{16})$", scanner_output): # make sure scanner output is 
               continue
            else:
                # send UFID or ISO as 16 bytes to server
                try:
                    client_socket.send(scanner_output.encode("utf-8")[:16])      
                except socket.err as err:
                    print("Error when sending UFID or ISO to server.")
                    exit(1)

                # server then sends back name_length, name, and picture based on sent UFID or ISO 
                try:
                    name_length = client_socket.recv(1).decode()
                    name_length = name_length.int() # for first sent byte, send length of name so its known how many bytes to read next
                    # names shouldnt be bigger than 255 chars so a byte is enough, hopefully

                    name = client_socket.recv(name_length)

                    picture = client_socket.recv(1024) # dont know how picture will be sent/how big it is, probably need another function to reconstruct it from the bytes for use with GUI
                except socket.err as err:
                    print("Error when receiving info from server.")
                    exit(1)

            # add update function for GUI
            # contantly run GUI on another thread? need to consistently send GUI through HDMI to output
            # ie GUI_update(name, picture)

    except KeyboardInterrupt: # for testing
        print("Keyboard Interrupt entered. Exiting...")
        exit(0)

def button_shutdown(): # for use with GPIO interrupt.
    print("Shutdown button pressed. Exiting...")
    exit(0)

def init_socket():
    server_ip = "123.123.123" # needs to be hardcoded based on laptop ip used in server file
    server_port = 8000 # same ^

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

def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(shutdown_button_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP) # might need to have pullup based on switch/push button used
    GPIO.add_event_detect(shutdown_button_GPIO, GPIO.BOTH, callback=button_shutdown, bouncetime=100) # interrupt for GPIO shutdown button connection

if __name__ == '__main__':
    init_GPIO()
    run_client(init_socket())
    exit(0)
