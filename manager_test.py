from manager import Manager

mgr = Manager("10.0.1.234","root","Juniper")
mgr.open()
mgr.get_facts()
