from manager import Manager
import redis
import datetime
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0)

igmp_policy_template = '''
policy-options {
    policy-statement {{ customer_name }}-igmp-allowed {
        term allow-{{ customer_name }}-1 {
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

mgr = Manager("10.0.1.234","root","Juniper")
mgr.open()
mgr.get_facts()
mgr.open_config(type="ephemeral")

while True:
    print "Wait " + str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    name = r.brpoplpush("food","cooking")
    print name
    open_start = datetime.datetime.now()
    print "Open config " + str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    mgr.open_config(type="ephemeral")
    mgr.load_config_template(igmp_policy_template,dict(customer_name=name[1],group_addr="224.1.1.1/32",source_addr="1.1.1.1/32",routes=["224.2.2.2/32"],source_address_filter="2.2.2.2/32"))
    mgr.commit_config()
    print "Commit Complete " + str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    commit_stop = datetime.datetime.now() - open_start
    print commit_stop.total_seconds()
    r.ltrim()


mgr.close()
