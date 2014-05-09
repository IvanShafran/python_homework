__author__ = 'Ivan Shafran'

import subprocess

end_of_stream = 'end_of_stream'
default_encoding = '866'
default_max_int_size = 4


def serialize(string, encoding=default_encoding, max_int_size=default_max_int_size):
    length = len(string)
    byte_length = length.to_bytes(max_int_size, byteorder='little')
    byte_string = bytes(string, encoding)
    return byte_length + byte_string


def deserialize(get, encoding=default_encoding, max_int_size=default_max_int_size):
    length = int.from_bytes(get(max_int_size), byteorder='little')
    string = get(length).decode(encoding)
    return string

if __name__ == '__main__':
    print(serialize("Ivan Shafran"))
