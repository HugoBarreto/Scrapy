# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Livro(scrapy.Item):
    id = scrapy.Field()
    brand = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    discount = scrapy.Field()
    author = scrapy.Field()
    available = scrapy.Field()
    rating = scrapy.Field()
    evals = scrapy.Field()
    url = scrapy.Field()
