import socket
import struct
import sys
import time
import datetime
import argparse

parser = argparse.ArgumentParser(description="Gather options from the user")
parser.add_argument("--forever", default=False,dest="forever", action="store_true",help="Specify if you want it to send packets forever")
parser.add_argument("--group",default="224.0.0.1",help="Specify multicast group")
parser.add_argument("--port",default=5000,dest="port",type=int,help="Specify send port")
parser.add_argument("--message",default="Insert message here",dest="message",help="Message to send")
parser.add_argument("--source",default="0.0.0.0",help="Source IP to listen on")
args = parser.parse_args()

message_counter = 0

while args.forever:
    time.sleep(1)
    multicast_group = (args.group, args.port)

    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.source,0))

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(0.2)

    ttl = struct.pack('b', 5)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        # Send data to the multicast group
        final_meassage = "{0} {1} {2}".format(args.message,str(message_counter),datetime.datetime.now().isoformat())
        print 'Sending "%s"' % final_meassage
        sent = sock.sendto(final_meassage, multicast_group)

    finally:
        print 'Closing socket'
        sock.close()

    message_counter = message_counter + 1
