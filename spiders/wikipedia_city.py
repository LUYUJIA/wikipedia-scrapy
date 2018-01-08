# -*- coding: utf-8 -*-
import scrapy
import codecs

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia_city'
    allowed_domains = ['wikipedia.org']

    def start_requests(self):
        urls = [
            'https://ja.wikipedia.org/wiki/日本の地方公共団体一覧',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        link_list=response.xpath(u'//div[@id="mw-content-text"]//a[contains(text(), "区") or contains(text(), "市") or contains(text(), "町") or contains(text(), "村")]')
        for link in link_list:
            yield scrapy.Request(url='https://ja.wikipedia.org'+link.xpath('./@href').extract_first(),
                meta={'link_text': link.xpath('./text()').extract_first()},
                callback=self.parse_city)

    def parse_city(self, response):
        description="".join(response.xpath('//div[@id="mw-content-text"]/div/p//text()').extract())
        yield {
            'name': response.meta['link_text'],
            'description': description
        }
