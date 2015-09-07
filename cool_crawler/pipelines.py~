# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from twisted.enterprise import adbapi              #导入twisted的包
import MySQLdb
import MySQLdb.cursors
from datetime import datetime


class CoolCrawlerPipeline(object):
    def __init__(self):                            #初始化连接mysql的数据库相关信息
        self.dbpool = adbapi.ConnectionPool(
                dbapiName='MySQLdb',
                host='localhost',
                db = 'test1',
                user = 'root',
                passwd = 'root',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )

    # pipeline dafault function                    #这个函数是pipeline默认调用的函数
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        #item["crawled"] = datetime.utcnow()
        #item["spider"] = spider.name
        return item

    # insert the data to databases                 #把数据插入到数据库中
    def _conditional_insert(self, tx, item):
        p=open('yeah.txt','a')
        #p.write(item["product"].encode('gbk'))
        sql = "insert into buy_offer values (%s, %s,%s, %s, %s,%s, %s, %s)"
        try:
            tx.execute(sql,(item["offer_id"][0:], item["type"][0:],item["company"][0:], item["memberid"][0:],
                        item["product"][0:],item["amount"][0:], item["unit"][0:], item["offer_cat"]))
            print 'SUCCESS[ITEM]: %s, %s' % (item['memberid'], item['offer_id'])
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            if e.args[0] == 1062:
                tx.execute("UPDATE buy_offer SET amount = amount * 2  WHERE buyofferId = %s and product = %s and amount = %s",
                           (item["offer_id"], item["product"],item["amount"]))
                print '*******************************************************************************'
            p.write("Error %d: %s %s %s \n" % (e.args[0],item['offer_id'].encode('gbk'), item['product'].encode('gbk'), item['amount'].encode('gbk')))
        p.close()