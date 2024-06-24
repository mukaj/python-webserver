import socket

from .request import Request
from .response import Response


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept()  # wait for client

    byte_request = conn.recv(4096)
    request: Request = Request.from_string(byte_request.decode())

    if request.target == "/":
        response = Response(status=200)
        conn.sendall(response.send_response())
    elif request.target_paths and request.target_paths[1] == "echo":
        message = request.target_paths[2]
        response = Response(status=200, body=message)
        response.headers["Content-Type"] = "text/plain"
        response.headers["Content-Length"] = str(len(message))
        conn.sendall(response.send_response())
    else:
        response = Response(status=404)
        conn.sendall(response.send_response())
        # conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
