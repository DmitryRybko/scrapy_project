# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    min = scrapy.Field()
    max = scrapy.Field()
    cur = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()


class VacancyItem(scrapy.Item):
    pass
