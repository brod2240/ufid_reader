from sys import exit
import socket, re

#import RPi.GPIO as GPIO # for use with Raspberry Pi 4 SBC for interrupt control from GPIO, will need to be changed for other SBCs / Microcontrollers.
#shutdown_button_GPIO = 16 # comment out all Rpi GPIO code for use with non Pi4

def run_client(client_socket):
    try:
        while True:
            scanner_output = input("Enter UFID or ISO (8 or 16 digits), or type 'close' to end: ")
            if scanner_output.lower() == "close":
                client_socket.send("close".encode("utf-8"))
                break

            if not re.match(r"^(\d{8}|\d{16})$", scanner_output):
                continue

            client_socket.send(scanner_output.encode("utf-8"))
            try:
                name_length_bytes = client_socket.recv(1)
                if not name_length_bytes:
                    print("Connection closed by server.")
                    break

                name_length = int.from_bytes(name_length_bytes, byteorder='big')
                name = client_socket.recv(name_length).decode("utf-8")
                print("Received Name:", name)
            except socket.error as err:
                print("Error when receiving info from server:", err)
                break
    except KeyboardInterrupt:
        print("Keyboard Interrupt entered. Exiting...")
    finally:
        client_socket.close()

def button_shutdown(): # for use with GPIO interrupt.
    print("Shutdown button pressed. Exiting...")
    client_socket.close()
    exit(0)

def init_socket():
    server_ip = "10.136.134.74" # needs to be hardcoded based on laptop ip used in server file
    server_port = 8912 # not a reserved port used in tcp or udp

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        return client_socket
    except socket.error as err:
        print("Socket error:", err)
        exit(1)

#def init_GPIO():
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(shutdown_button_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP) # might need to have pullup based on switch/push button used
    #GPIO.add_event_detect(shutdown_button_GPIO, GPIO.BOTH, callback=button_shutdown, bouncetime=100) # interrupt for GPIO shutdown button connection

if __name__ == '__main__':
    client_socket = init_socket()
    run_client(client_socket)
