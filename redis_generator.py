import redis
import time
import argparse
import json

parser = argparse.ArgumentParser(description="Gather options from the user")
parser.add_argument("--group",default="224.0.0.1",help="Specify multicast group")
args = parser.parse_args()

r = redis.StrictRedis(host='localhost', port=6379, db=0)
client_id = 0

while True:
    publish_data = {}
    publish_data["client"] = "client" + str(client_id)
    publish_data["group"] = args.group
    r.publish("igmp_groups",json.dumps(publish_data))
    client_id = client_id + 1
    time.sleep(3)
