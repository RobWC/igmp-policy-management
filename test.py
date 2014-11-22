from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.cfg.resource import Resource
from jnpr.junos.utils.config import Config


dev = Device(host="10.0.1.234",user="root",password="Juniper")
dev.open()

pprint(dev.facts)

dev.cli("request system reboot")

dev.close()

#apply igmp group to interface
#create igmp group
#open an ephemeral config
#standard commits

igmp_policy_template = '''
policy-statement igmp-allowed {
    term allow-customer-1 {
        from {
            route-filter 224.1.1.1/32 exact;            # Group address
            source-address-filter 1.1.1.1/32 exact;     # Source address
        }
        then accept;
    }
    term allow-customer-2 {
        from {
            route-filter 224.2.2.2/32 exact;
            route-filter 224.2.2.3/32 exact;
            source-address-filter 2.2.2.2/32 exact;
        }
        then accept;
    }
    term deny-everything-else {
        then reject;
    }
}
'''
