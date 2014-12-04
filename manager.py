from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.cfg.resource import Resource
from jnpr.junos.utils.config import Config
from jinja2 import Template

class Manager():
    def __init__(self,host,user,password):
        self.dev = Device(host=host,user=user,password=password)
        self.dev.bind(cu=Config)

    def open(self):
        try:
            self.dev.open()
            print "Connection Open"
        except Exception as err:
            print err

    def close(self):
        try:
            self.dev.close()
            print "Connection Closed"
        except Exception as err:
            print err

    def get_facts(self):
        pprint(self.dev.facts)

    def open_config(self,type):
        try:
            #attempt to open a configuration
            output = self.dev.rpc("<open-configuration><{0}/></open-configuration>".format(type))
            print "Open {0} configuration".format(type)
        except Exception as err:
            #output an error if the configuration is not availble
            print err

    def load_config_template(self,template,template_vars):
        new_template = Template(template)
        final_template = new_template.render(template_vars)

        try:
            output = self.dev.cu.load(final_template,format="text",merge=True)
            print "Load Complete"
        except Exception as err:
            print err

    def commit_config(self):
        try:
            self.dev.rpc.commit_configuration()
            self.dev.rpc.close_configuration()
            print "Commit Complete"
        except Exception as err:
            print err
