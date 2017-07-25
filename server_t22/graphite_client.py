# from https://github.com/gnemoug/distribute_crawler
from socket import socket
import traceback
from time import time
import sys
    
class Graphite_Client(object):
    """
        The client thats send data to graphite.
        
        Can have some ideas from /opt/graphite/examples/example-client.py
    """
    
    def __init__(self, host="192.168.31.181", port=2003):
        self._sock = socket()
        self._sock.connect((host,port))

    def send(self, data = None):
        data = ("\n%s %g %s\n" % ('TEST.AAA', 10, int(time()))).encode() + \
               ("\n%s %g %s\n" % ('TEST.BBB', 20, int(time()))).encode()
        self._sock.send(data)

            
if __name__ == '__main__':


    gc = Graphite_Client('192.168.31.181', 2003)
    gc.send()