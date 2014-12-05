
import gevent
import redis
from gevent import Greenlet

class Listener(Greenlet):
    def __init__(self,channel):
        Greenlet.__init__(self)
        self.channel = channel
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def _run(self):
        name = self.r.brpoplpush(self.channel,"cooking")
        print name


g = Listener("food1")
g2 = Listener("food2")

gevent.joinall([g,g2])
