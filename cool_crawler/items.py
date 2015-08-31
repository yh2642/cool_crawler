#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    offer_id = scrapy.Field()
    type = scrapy.Field()
    company = scrapy.Field()
    memberid = scrapy.Field()
    product = scrapy.Field()
    amount = scrapy.Field()
    unit = scrapy.Field()
    offer_cat = scrapy.Field()
    crawled = scrapy.Field()
    spider = scrapy.Field()


