from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.cfg.resource import Resource
from jnpr.junos.utils.config import Config

igmp_policy_template = '''
policy-options {
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
}
'''

dev = Device(host="172.16.237.128",user="root",password="Juniper")
dev.open()

dev.bind(cu=Config)

pprint(dev.facts)

try:
    output = dev.rpc("<open-configuration><private/></open-configuration>")
except Exception as err:
    print err

try:
    output = dev.cu.load(igmp_policy_template,format="text",merge=True)
except Exception as err:
    print err

#output = dev.rpc("<commit-configuration></commit-configuration>")

#print output

output = dev.rpc.commit_configuration()

output = dev.rpc.close_configuration()

print output

dev.close()

#apply igmp group to interface
#create igmp group
#open an ephemeral config
#standard commits
