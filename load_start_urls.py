__author__ = 'huyichao'


import redis

with open('task.txt', 'r') as task:
    memberid_ls = task.readlines()
start_urls = (
       'http://go.1688.com/page/portal.htm?member_id=' + ele.strip() for ele in memberid_ls
)

r = redis.Redis()
count = 1
for ele in start_urls:
    r.lpush('buy_offer:start_urls', ele)
    count += 1
    print count
    print ele
