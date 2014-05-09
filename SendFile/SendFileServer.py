__author__ = 'Ivan Shafran'

import logging
import socketserver
import serialize

def conversion(string):
    return "Changed by Ivan Shafran: " + string

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Got connection from %s.", self.client_address[0])
        while True:
            msg = serialize.deserialize(self.request.recv)
            if msg:
                self.request.sendall(serialize.serialize(conversion(msg)))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    HOST, PORT = '127.0.0.1', 12345

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    main()