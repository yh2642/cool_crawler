__author__ = 'huyichao'


import redis
r = redis.Redis()

start_urls = (
       'http://go.1688.com/page/portal.htm?member_id=' + ele.strip() for ele in r.lrange('memberid_queue', 0, r.llen('sell_offer:start_urls'))
)

count = 1
for ele in start_urls:
    r.lpush('buy_offer:start_urls', ele)
    count += 1
    print count
    print ele
