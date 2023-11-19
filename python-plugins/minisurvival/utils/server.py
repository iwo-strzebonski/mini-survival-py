from socket import socket, AF_INET, SOCK_STREAM, SHUT_WR


def create_server():
    serversocket = socket(AF_INET, SOCK_STREAM)
    # serversocket.bind(("localhost", 9000))
    serversocket.bind(("0.0.0.0", 80))
    serversocket.listen(5)

    while 1:
        (clientsocket, _address) = serversocket.accept()
        clientsocket.send(
            b"HTTP/1.1 200 OK\n"
            + b"Content-Type: text/html\n"
            + b"\n"  # Important!
            + b"<html><body>Hello World</body></html>\n"
        )
        clientsocket.shutdown(SHUT_WR)
        clientsocket.close()

    serversocket.close()
