# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from mro.items import UniversalItem
import re


class Mcr(scrapy.Spider):
    name = 'forbes'
    start_urls = [
        'https://www.forbes.com/companies/icbc/',
    ]

    def parse(self, response):
    	item = UniversalItem()
        item['name'] = response.xpath('//*[@id="left_rail"]/div[1]/div[1]/h1/text()').re(r'\d+ (.+)')[0]
        item['by date'] = response.xpath('//*[@id="left_rail"]/div[1]/div[1]/ul/li[1]/span/text()').extract_first()
        item['market cap'] = response.xpath('//*[@id="left_rail"]/div[1]/div[1]/ul/li[2]/text()').extract_first() + response.xpath('//*[@id="left_rail"]/div[1]/div[1]/ul/li[2]//span/text()').extract_first()
        for dl in response.xpath('//*[@id="left_rail"]/div[1]/div[1]/dl'):
        	item[dl.xpath('./dt/text()').extract_first()] = dl.xpath('./dd/text()').extract_first() or dl.xpath('./dd/a/@href').extract_first()
        item['description'] = response.xpath('//div[@class="profile"]/text()').extract_first() + response.xpath('//*[@id="fulldesc"]/text()').extract_first()
        item['url'] = response.url
        yield item
        url = response.xpath('//div[@class="next-button"]/a/@href').extract_first()
        if url:
        	yield scrapy.Request(url=response.urljoin(url), callback=self.parse)













