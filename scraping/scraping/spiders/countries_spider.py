import scrapy

class CountriesSpider(scrapy.Spider):
    name = "countries"
    start_urls = [
        'https://www.scrapethissite.com/pages/simple/'
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'pt-BR'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        for country in response.css('.country'):
            yield {
                'name': country.css('h3.country-name').xpath('normalize-space(.)').get(),
                'capital': country.css('.country-info .country-capital::text').get(),
                'population': country.css('.country-info .country-population::text').get(),
                'area': country.css('.country-info .country-area::text').get(),
            }
