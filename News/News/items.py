# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy


class WebscrappingItem(scrapy.Item):
    # define the fields for your item here like:
    hrefs = scrapy.Field()
    images = scrapy.Field()
    headings = scrapy.Field()
    time = scrapy.Field()
    # text = scrapy.Field()
