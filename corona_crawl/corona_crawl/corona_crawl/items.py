# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoronaCrawlItem(scrapy.Item):
    confirmed_date = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    sex = scrapy.Field()
    age = scrapy.Field()
