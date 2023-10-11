# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapingItem(scrapy.Item):
    nameCountry = scrapy.Field()
    capitalCountry = scrapy.Field()
    populationCountry = scrapy.Field()
    areaCountry = scrapy.Field()
