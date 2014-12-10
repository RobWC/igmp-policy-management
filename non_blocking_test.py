from manager import Manager
import redis
import datetime
import time
import signal
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
        term allow-{{ customer_name }}-2 {
            from {
                {% for route in routes %}route-filter {{ route }} exact;{% endfor %}
                {% if source_address_filter is defined %}source-address-filter {{ source_address_filter }} exact;{% endif %}
            }
            then accept;
        }
        term deny-everything-else {
            then reject;
        }
    }
}
'''

def pub_handler(message):
    #Connect to device to push config

    #open config

    #load config
    #mgr.load_config_template(igmp_policy_template,dict(customer_name=name,group_addr="224.1.1.1/32",source_addr="1.1.1.1/32",routes=["224.2.2.2/32"],source_address_filter="2.2.2.2/32"))

    #commit config
    #mgr.commit_config()
    #print "Commit Complete " + str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    #commit_stop = datetime.datetime.now() - open_start
    #time_list.append(commit_stop.total_seconds())
    #print commit_stop.total_seconds()
    print(message)


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
