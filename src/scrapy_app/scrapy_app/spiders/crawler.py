# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlerSpider(CrawlSpider):
    name = 'crawler'

    # allowed_domains = ['https://google.com']
    # start_urls = ['http://https://google.com/']

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        CrawlerSpider.rules = [
            Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(CrawlerSpider, self).__init__(*args, **kwargs)

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def parse_item(self, response):
        i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()

        i['url'] = response.url
        return i
