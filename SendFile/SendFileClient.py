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
        ans = serialize.deserialize(self.sock.recv)
        return ans if ans else None


def main():
    HOST, PORT = '127.0.0.1', 12345

    client = Client(HOST, PORT)

    cmd_text = input()
    while cmd_text != 'exit':
        if not os.path.isfile(cmd_text):
            logging.error("File %s doesn't exist", cmd_text)
        else:
            filename = 'changed_' + cmd_text
            file = open(filename, 'w')
            for x in open(cmd_text):
                file.write(client.send(x))
            file.close()
            print("File is received successfully. It's named - " + str(filename))

        cmd_text = input()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    main()