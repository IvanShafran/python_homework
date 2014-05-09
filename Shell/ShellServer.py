__author__ = 'Ivan Shafran'

import subprocess
import logging
import socketserver
import serialize


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    password_dict = dict()

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
            self.send("Please log in or register")
            self.send("Choose 'Log in' or 'Register'")
            self.send(serialize.end_of_stream)

            msg = self.get()
            if msg == 'Log in':
                self.send("Enter login and password(in new line)")
                self.send(serialize.end_of_stream)

                login = self.get()
                self.send(serialize.end_of_stream)
                password = self.get()

                if login in self.password_dict:
                    if self.password_dict[login] == hash(password):
                        self.send("You log in successfully")
                        self.send(serialize.end_of_stream)
                        break
                    else:
                        self.send("Wrong login or password")
                else:
                    self.send("User with this login doesn't exist")

            elif msg == 'Register':
                self.send("Enter login and password(in new line)")
                self.send(serialize.end_of_stream)

                login = self.get()
                self.send(serialize.end_of_stream)
                password = self.get()

                if login not in self.password_dict:
                    self.password_dict[login] = hash(password)
                    self.send("You register and log in successfully")
                    self.send(serialize.end_of_stream)
                    break
                else:
                    self.send("User with this login already exists")

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
