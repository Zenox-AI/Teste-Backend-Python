import scrapy

class CountriesSpider(scrapy.Spider):
    name = "countries"
    start_urls = [
        'https://www.scrapethissite.com/pages/simple/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for country in response.css('.country'):
            # Exibe user-agent
            self.logger.info("User-Agent: " + response.request.headers['User-Agent'].decode('utf-8'))
            yield {
                'name': country.css('h3.country-name').xpath('normalize-space(.)').get(),
                'capital': country.css('.country-info .country-capital::text').get(),
                'population': country.css('.country-info .country-population::text').get(),
                'area': country.css('.country-info .country-area::text').get(),
            }
