import scrapy
from ..items import ScrapingItem

class CountriesSpider(scrapy.Spider):
    name = "countries"
    start_urls = [
        'https://www.scrapethissite.com/pages/simple/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.logger.info("User-Agent: " + response.request.headers['User-Agent'].decode('utf-8'))
        self.logger.info("Proxy: " + response.request.meta['proxy'])
        self.logger.info("Response status: " + str(response.status))
        self.logger.info("Coletando dados...")

        for country in response.css('.country'):
            content = ScrapingItem(
                nameCountry=country.css('h3.country-name').xpath('normalize-space(.)').get(),
                capitalCountry=country.css('.country-info .country-capital::text').get(),
                populationCountry=country.css('.country-info .country-population::text').get(),
                areaCountry=country.css('.country-info .country-area::text').get(),
            )
            yield content
