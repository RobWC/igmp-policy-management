from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.cfg.resource import Resource
from jnpr.junos.utils.config import Config
from jinja2 import Template

igmp_policy_template1 = '''
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

igmp_policy_template = '''
policy-options {
    policy-statement igmp-allowed {
        term allow-{{ customer_name }}-1 {
            from {
                route-filter {{ group_addr }} exact;
                source-address-filter {{ source_addr }} exact;
            }
            then accept;
        }
        term allow-{{ customer_name }}-2 {
            from {
                {% for route in routes %}
                route-filter {{ route }} exact;
                {% endfor %}
                {% if source_address_filter is defined %}
                source-address-filter {{ source_address_filter }} exact;
                {% endif %}
            }
            then accept;
        }
        term deny-everything-else {
            then reject;
        }
    }
}
'''

dev = Device(host="10.0.1.234",user="root",password="Juniper")
dev.open()

pprint(dev.facts)

try:
    #attempt to open a configuration
    output = dev.rpc("<open-configuration><private/></open-configuration>")
except Exception as err:
    #output an error if the configuration is not availble
    print err

try:
    output = dev.cu.load(igmp_policy_template1,format="text",merge=True)
except Exception as err:
    print err

output = dev.rpc.commit_configuration()

output = dev.rpc.close_configuration()

print output

dev.close()

class Manager():
    def __init__(self,host,user,password)
        self.dev = Device(host="10.0.1.234",user="root",password="Juniper")
        self.dev.bind(cu=Config)

    def open(self):
        self.dev.open()

    def load_config_template(self,template,template_vars)
        new_template = Template(template)
        final_template = new_template.render(template_vars)

        try:
            output = dev.cu.load(final_template,format="text",merge=True)
        except Exception as err:
            print err

    def commit_config(self):
        self.dev.rpc.commit_configuration()
        self.dev.rpc.close_configuration()


#apply igmp group to interface
#create igmp group
#open an ephemeral config
#standard commit
