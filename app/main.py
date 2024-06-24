import socket
import threading

from .request import Request
from .response import Response


def handle_connection(conn, addr):
    byte_request = conn.recv(4096)
    request: Request = Request.from_string(byte_request.decode())

    if request.target == "/":
        response = Response(status=200)
    elif request.target_paths and request.target_paths[1] == "echo":
        message = request.target_paths[2]
        response = Response(status=200, body=message)
        response.headers["Content-Type"] = "text/plain"
        response.headers["Content-Length"] = str(len(message))
    elif request.target_paths and request.target_paths[1] == "user-agent":
        response_body = request.headers["User-Agent"]
        response = Response(status=200, body=response_body)
        response.headers["Content-Type"] = "text/plain"
        response.headers["Content-Length"] = str(len(response_body))
    else:
        response = Response(status=404)

    conn.sendall(response.send_response())
    conn.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()

    try:
        while True:
            conn, addr = server_socket.accept()  # wait for client
            threading.Thread(target=handle_connection, args=(conn, addr)).start()
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
