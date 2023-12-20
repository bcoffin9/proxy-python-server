""" Serves as a web proxy that can cache requests to serve them faster than normal.
    Can calculate times of hits and misses. """
import socket
from datetime import datetime
import os
from urllib.parse import urlparse


def extract_hostname(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname


NOTFOUND_FILESIZE = os.path.getsize("./resources/not-found.html")

# Create a server socket
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set the SO_REUSEADDR flag on the socket
tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 12000
ADDRESS = (HOST, PORT)
tcp_server_socket.bind(ADDRESS)
tcp_server_socket.listen(1)
requested_hostn = ""

print('Server ready to serve on:', ADDRESS)

while True:
    tcp_client_socket, addr = tcp_server_socket.accept()
    print('Received a connection from:', addr)

    message = tcp_client_socket.recv(1024).decode()

    request_method = message.split()[0]
    if request_method != 'GET':
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        tcp_client_socket.send(response.encode())
        tcp_client_socket.close()
        continue

    print(message)
    filename = message.split()[1].partition("/")[2]
    print(f'FileName: {filename[1:]}')
    requested_hostn = extract_hostname("http://" + filename[1:])
    print(f'RequestedHostName generated: {requested_hostn}')
    safe_filename = filename.replace("/", "_").replace(".", "_")
    filetouse = "./cache/" + safe_filename + ".txt"
    print(f'Filetouse: {filetouse}')

    try:
        with open(filetouse, "r") as f:
            outputdata = f.read()
            response = "HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n\r\n" + outputdata
            tcp_client_socket.send(response.encode())
            print('Read from cache')

    except FileNotFoundError:
        accumulated_response = b""
        print(requested_hostn)
        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect((requested_hostn, 80))

            # Assume 'message' contains the full HTTP request from the client
            # Extract the request line (e.g., "GET /path/resource HTTP/1.1")
            request_line = message.split('\r\n')[0]

            # Extract the URL part from the request line (e.g., "/path/resource")
            url_part = request_line.split(' ')[1]
            print(f"URL Part: {url_part}")

            request = "GET " + url_part + " HTTP/1.0\r\nHost: " + requested_hostn + "\r\n\r\n"
            c.send(request.encode('utf-8'))

            while True:
                response = c.recv(4096)
                if not response:  # Break the loop if no more data is received
                    break
                accumulated_response += response  # Accumulate the received response
                tcp_client_socket.send(response)  # Send to client

            c.close()
            with open(filetouse, "wb") as cache_file:
                cache_file.write(accumulated_response)

        except Exception as e:
            # Print log and return 500 error to client
            print(f"Error processing request: {e}")
            tcp_client_socket.send(
                "HTTP/1.0 500 Internal Server Error\r\n".encode())

    tcp_client_socket.close()
