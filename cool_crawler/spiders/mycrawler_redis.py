from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisMixin

from cool_crawler.items import SpiderItem



class MyCrawler(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'buy_offer'
    redis_key = 'buy_offer:start_urls'

    rules = [Rule(LinkExtractor(allow=('/buyoffer/\d+.htm',)), callback='targetparse'),
             Rule(LinkExtractor(allow=('page=\d+',)), follow=True),
             Rule(LinkExtractor(allow=('/page/page/\d+',)), follow =True),
             Rule(LinkExtractor(allow=('/page/purchase.htm',)), follow=True, callback='countparse')]


    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.alowed_domains = filter(None, domain.split(','))
        super(MyCrawler, self).__init__(*args, **kwargs)

    def _set_crawler(self, crawler):
        CrawlSpider._set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def targetparse(self, response):
        offer_id = response.xpath('//div[@id="go-content"]/input[@id="aliclick-offerid"]/@value').extract()[0]
        offer_cat_ls = response.xpath('//div[@class="go-crumbs"]/a[last()]/@href').re(r'--(\d+)\.')
        if len(offer_cat_ls) == 0:
            offer_cat = None
        else:
            offer_cat = offer_cat_ls[0]
        company = response.xpath('//h4[@title]/text()').extract()[0]
        memberid = response.xpath('//div[@class="cell-block"]/a[@class="more-offer"]/@href').re(r'memberId=(.*)&.*')[0]
        product_ls = response.xpath('//table[@class="list-table"]/tbody/tr/td[1]/text()').extract()
        amount_ls = response.xpath('//table[@class="list-table"]/tbody/tr/td[2]/text()').re('(\d+)\D*')
        unit_ls = response.xpath('//table[@class="list-table"]/tbody/tr/td[2]/text()').re('\d*(\w+)')

        num_item = len(product_ls)
        for indx in range(0,num_item):
            buyoffer = SpiderItem()
            buyoffer['offer_id'] = offer_id
            buyoffer['type'] = 'BUY'
            buyoffer['memberid'] = memberid
            buyoffer['company'] = company
            buyoffer['offer_cat'] = offer_cat
            buyoffer['product'] = product_ls[indx]
            buyoffer['amount'] = amount_ls[indx]
            buyoffer['unit'] = unit_ls[indx]
            yield buyoffer

    def countparse(self,response):
        f = open('count_redirect.txt', 'a')
        f.write(response.url + '\n')
        f.close()