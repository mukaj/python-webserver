import socket

from .request import Request


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept()  # wait for client

    byte_request = conn.recv(4096)
    request: Request = Request.from_string(byte_request.decode())

    if request.target == "/":
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
