# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import logging
from scrapy import signals
from itemadapter import is_item, ItemAdapter


class RandomUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agents=crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.user_agents))


class RandomProxyMiddleware:
    def __init__(self, proxies):
        self.proxies = proxies
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(proxies=crawler.settings.getlist('PROXIES'))

    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy

    def process_exception(self, request, exception, spider):
        if isinstance(exception, (ConnectionRefusedError, TimeoutError, )):
            self.logger.warning(f"Failed to connect using proxy {request.meta['proxy']}, retrying a different proxy...")
            new_request = request.copy()
            new_request.dont_filter = True
            new_request.priority = request.priority + 1
            return new_request
        return None