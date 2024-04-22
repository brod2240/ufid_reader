from sys import exit
import socket,re

def init_server_socket():
    server_ip = "123.123.123"  # Listen on all available interfaces
    server_port = 8000  # Port to listen on

    try:
        global server_socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create server socket
        server_socket.bind((server_ip, server_port))  # Bind the socket to the address and port
        server_socket.listen(0)  # Listen for incoming connections with a backlog of 0
        print("Server listening on", server_ip, "port", server_port)
    except socket.error as err:
        print("Error when initializing server socket:", err)
        exit(1)

    return server_socket

def run_server():
    try:
        while True:
            client_socket, client_address = server_socket.accept() # Accept incoming connection
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            # Handle client connection (in a separate thread/process if needed)
            handle_client(client_socket, client_address)
    except KeyboardInterrupt:  # Handle keyboard interrupt for graceful shutdown
        print("Keyboard Interrupt entered. Exiting...")
        server_socket.close()
        exit(0)

def handle_client(client_socket):
    try:
        while True:
            # Receive data from the client
            request = client_socket.recv(16).decode("utf-8")  # Assuming the client sends 16-byte data
            if not request:
                break  # No more data from client, close connection
            # Process the received data (you may implement your logic here)
            # For now, just print it

            # if we receive "close" from the client, then we break
            # out of the loop and close the conneciton
            if request.lower() == "close":
                # send response to the client which acknowledges that the
                # connection should be closed and break out of the loop
                client_socket.send("closed".encode("utf-8"))
                break

            print("Received data:", data)
            # Send response back to client (if needed)
            # client_socket.sendall(response.encode("utf-8"))

            # VALIDATION CODE CALL
            # VALIDATION CODE CALL

            response = bytes([name_length]) + name.encode("utf-8") + picture
            
            # Send response back to client
            client_socket.sendall(response)

    except socket.error as err:
        print("Error when receiving/sending data to client:", err)
        client_socket.close()
        print("Connection to client closed")
        # close server socket
        server_socket.close()
        exit(0)    

if __name__ == "__main__":
    run_server(init_server_socket())
    exit(0)
    
    

