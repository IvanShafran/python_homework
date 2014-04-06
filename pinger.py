import os
import logging
import queue
import argparse
from threading import Thread

def ping(ipaddress):
    return 0 == os.system("ping " + ipaddress)

def check_ipaddress(checked_ipaddres_filename, ipaddress_queue):
    logging.basicConfig(level=logging.DEBUG, format='%(message)s',
                        filename=checked_ipaddres_filename)
    while not ipaddress_queue.empty():
        ipaddress = ipaddress_queue.get_nowait()
        if ping(ipaddress):
            logging.debug(ipaddress)
        ipaddress_queue.task_done()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check some ip addresses.")
    parser.add_argument("output_filename", type=str,
                        help="Name of file with list of address")
    parser.add_argument("number_of_threads", type=int, help="")
    parser.add_argument("ipaddress", nargs="+")
    args = parser.parse_args()

    number_of_threads = args.number_of_threads
    ipaddress_queue = queue.Queue()
    for line in args.ipaddress:
        ipaddress_queue.put_nowait(line.rstrip('\n'))

    checked_ipaddres_filename = args.output_filename

    for x in range(number_of_threads):
        thread = Thread(target=check_ipaddress, args=(checked_ipaddres_filename, ipaddress_queue))
        thread.daemon = False
        thread.start()