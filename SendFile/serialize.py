__author__ = 'Ivan Shafran'

def serialize(string, encoding='1251', max_int_size=4):
    length = len(string)
    byte_length = length.to_bytes(max_int_size, byteorder='little')
    byte_string = bytes(string, encoding)
    return byte_length + byte_string


def deserialize(get, encoding='1251', max_int_size=4):
    length = int.from_bytes(get(max_int_size), byteorder='little')
    string = get(length).decode(encoding)
    return string

if __name__ == '__main__':
    print(serialize("Ivan Shafran"))