import socket
import datetime
import csv
from validation import validate_id, validate_course, get_student_name

scan_records = []  # List to hold scan records

def init_server_socket():
    server_ip = "10.136.134.74" # Hard code server IP, adjust as needed
    server_port = 8912
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_ip} port {server_port}")
    return server_socket

def run_server(server_socket):
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("Server shutdown requested (Ctrl+C).")
    finally:
        server_socket.close()
        print("Server socket clocsed.")

def handle_client(client_socket):
    class_number = "27483"  # Hard code example class number, adjust as needed
    if not validate_course(class_number):
        print("Invalid class number")
        return

    try:
        while True:
            request = client_socket.recv(16).decode("utf-8")
            if not request:
                break

            if request == "close":  # Handle close command
                break

            valid, first_name, last_name = validate_id(class_number, request)
            if valid:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                record = (timestamp, request, f"{first_name} {last_name}")
                scan_records.append(record)

                name = f"{first_name} {last_name}"
                name_bytes = name.encode('utf-8')
                name_length = len(name_bytes)
                response = name_length.to_bytes(1, byteorder='big') + name_bytes
            else:
                temp = "Failure: UFID or ISO not found."
                temp_length = len(temp)
                response = temp_length.to_bytes() + temp.encode('utf-8')
            
            client_socket.sendall(response)
    except socket.error as err:
        print(f"Socket error: {err}")
    finally:
        client_socket.close()
        print("Connection closed. Writing to CSV if records are present...")
        if scan_records:
            write_to_csv(scan_records)

        exit(1)

def write_to_csv(records):
    filename = "ufid_barcodes.csv"
    fieldnames = ['Time Stamp', 'Student ID', 'Student Name']
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fieldnames)
        csvwriter.writerows(records)
    print(f"Data written to {filename}")

if __name__ == "__main__":
    server_socket = init_server_socket()
    run_server(server_socket)
