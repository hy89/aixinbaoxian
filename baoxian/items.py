# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaoxianItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    position = scrapy.Field()
    phone = scrapy.Field()
    company = scrapy.Field()
    code = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    info_url = scrapy.Field()
    crawl_time = scrapy.Field()
    code_url = scrapy.Field()
