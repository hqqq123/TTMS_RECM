# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviedataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    release_date = scrapy.Field()
    length = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    area = scrapy.Field()
    type = scrapy.Field()
    brief = scrapy.Field()
    score = scrapy.Field()
    img = scrapy.Field()
