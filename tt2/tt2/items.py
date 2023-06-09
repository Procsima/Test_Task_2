# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    authors = scrapy.Field()
    summary = scrapy.Field()
    text = scrapy.Field()
    images = scrapy.Field()
    pass
