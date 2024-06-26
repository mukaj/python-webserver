import socket
import threading
import sys
import gzip

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
    elif request.target_paths and request.target_paths[1] == "files":
        if request.method == "GET":
            response = Response(status=200)
            file_name = request.target_paths[2]

            try:
                with open(file=sys.argv[2] + file_name) as target_file:
                    content = target_file.read()
                    response.headers["Content-Type"] = "application/octet-stream"
                    response.headers["Content-Length"] = str(len(content))
                    response.body = content
            except FileNotFoundError:
                response.status = 404
        elif request.method == "POST":
            response = Response(status=201)
            file_name = request.target_paths[2]

            try:
                with open(file=sys.argv[2] + file_name, mode="x") as target_file:
                    target_file.write(request.body)
            except FileNotFoundError:
                response.status = 404

    else:
        response = Response(status=404)

    if "gzip" in request.accept_encodings:
        response.body = gzip.compress(response.body.encode())
        response.headers["Content-Length"] = str(len(response.body))
        response.headers["Content-Encoding"] = "gzip"

    conn.sendall(response.send_response())
    conn.close()


def main():
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
