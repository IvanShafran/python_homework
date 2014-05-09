__author__ = 'Ivan Shafran'

import subprocess
import logging
import socketserver
import hashlib
import serialize


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def send(self, text):
        self.request.sendall(serialize.serialize(text))

    def get(self):
        return serialize.deserialize(self.request.recv)

    def run_query(self, query):
        result_file = open("query_result.log", 'w', encoding=serialize.default_encoding)
        try:
            subprocess.call(query, stdout=result_file)
        except:
            self.send("Some error during query")
        else:
            for line in open("query_result.log", 'r', encoding=serialize.default_encoding):
                self.send(line)

        result_file.close()
        self.send(serialize.end_of_stream)

    def handle(self):
        logging.info("Got connection from %s.", self.client_address[0])

        while True:
            msg = self.get()
            if msg:
                self.run_query(msg)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    HOST, PORT = '127.0.0.1', 12345

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    main()
