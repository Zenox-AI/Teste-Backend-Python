import scrapy


class ScrapingItem(scrapy.Item):
    nameCountry = scrapy.Field()
    capitalCountry = scrapy.Field()
    populationCountry = scrapy.Field()
    areaCountry = scrapy.Field()
