__author__ = 'Ivan Shafran'

import os
import socket
import logging
import serialize

class Client():
    def __init__(self, host, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            logging.error("Can't create client socket because of %s", e)
        else:
            logging.info("Client socket is created.")

        self.connect(host, port)

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
        except socket.error as e:
            logging.error("Can't connect to %s with on port %d. Error %f", host, port, e)
        else:
            logging.info("Connected to %s with on port %d", host, port)

    def send(self, msg):
        self.sock.sendall(serialize.serialize(msg))


def main():
    HOST, PORT = '127.0.0.1', 12345

    client = Client(HOST, PORT)

    answer = ''
    while answer != serialize.end_of_stream:
        print(answer)
        answer = serialize.deserialize(client.sock.recv)


    cmd_text = input()
    while cmd_text != 'exit':
        client.send(cmd_text)

        answer = serialize.deserialize(client.sock.recv)
        while answer != serialize.end_of_stream:
            print(answer)
            answer = serialize.deserialize(client.sock.recv)

        cmd_text = input()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    main()
