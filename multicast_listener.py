import socket
import struct
import argparse

parser = argparse.ArgumentParser(description="Gather options from the user")
parser.add_argument("--forever", default=False,dest="forever", action="store_true",help="Specify if you want it to send packets forever")
parser.add_argument("--group",default="224.0.0.1",help="Specify multicast group")
parser.add_argument("--port",default=5000,dest="port",type=int,help="Specify send port")
parser.add_argument("--source",default="0.0.0.0",help="Source IP to listen on")
args = parser.parse_args()

class McastSocket(socket.socket):
    def __init__(self, local_port, reuse=False):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        if(reuse):
            self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.bind(('', local_port))
    def mcast_add(self, mcast_addr, mcast_iface):
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(mcast_addr) + socket.inet_aton(mcast_iface))

sock = McastSocket(local_port=args.port, reuse=True)
sock.mcast_add(mcast_addr=args.group, mcast_iface=args.source)

while True:
    data, addr = sock.recvfrom(1024)
    print data
