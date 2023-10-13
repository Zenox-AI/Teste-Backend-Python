from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraping.spiders.countries_spider import CountriesSpider

process = CrawlerProcess(get_project_settings())
process.crawl(CountriesSpider)
process.start()
