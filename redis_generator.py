import redis
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0)
number = 0

while True:
    r.rpush("groups","client{0}".format(number))
    number = number + 1
    time.sleep(5)
