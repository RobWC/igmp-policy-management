from manager import Manager
import redis
import datetime
import time
import signal
import json
import sys


r = redis.StrictRedis(host='localhost', port=6379, db=0)

time_list = []

igmp_policy_template = '''
policy-options {
    policy-statement igmp-allowed {
        term allow-{{ customer_name }}{
            from {
                route-filter {{ group_addr }} exact;
                source-address-filter {{ source_addr }} exact;
            }
            then accept;
        }
    }
}
'''

def pub_handler(message):
    print "+====================================================+"

    json_msg = json.loads(message["data"])

    #message recieved start
    msg_rec_start = datetime.datetime.now()
    print "Recieved message at {0}".format(msg_rec_start)

    #connection start timing
    connection_start = datetime.datetime.now()
    mgr = Manager("10.0.1.234","root","Juniper")
    mgr.open()

    #open config start timing
    open_config_start = datetime.datetime.now()
    mgr.open_config(type="ephemeral")

    #load config timing
    load_config_start = datetime.datetime.now()
    mgr.load_config_template(igmp_policy_template,dict(customer_name=json_msg["client"],group_addr=json_msg["group"],source_addr="10.0.1.20/32",routes=["224.2.2.2/32"],source_address_filter="2.2.2.2/32"))
    load_config_stop = datetime.datetime.now()

    #commit config timing
    commit_config_start = datetime.datetime.now()
    mgr.commit_config()
    commit_config_stop = datetime.datetime.now()

    #open config stop timing
    open_config_stop = datetime.datetime.now() - open_config_start
    print "Total time for config: {0}".format(open_config_stop.total_seconds())

    #connection stop timing
    mgr.close()
    connection_stop = datetime.datetime.now() - connection_start
    print "Total time for QFX: {0}".format(connection_stop.total_seconds())

    #msg recieved stop
    msg_rec_stop = datetime.datetime.now()
    total_time = msg_rec_stop - msg_rec_start
    print "Total time for operation: {0}".format(total_time.total_seconds())
    print "-====================================================-"



pubsub_listener = r.pubsub(ignore_subscribe_messages=True)

pubsub_listener.subscribe(**{'igmp_groups':pub_handler})
listen_thread = pubsub_listener.run_in_thread(sleep_time=0.001)

def sigint_handler(signal, frame):
        print('Closing connections and exiting...')
        listen_thread.stop()
        pubsub_listener.close()
        print('Connections closed')
        sys.exit(0)

while True:
    signal.signal(signal.SIGINT, sigint_handler)
    time.sleep(1)
