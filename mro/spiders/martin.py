import json
import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from mro.items import MartinItem

class martin_spider(CrawlSpider):
    name = "martin_test"
    data = pandas.read_csv("spiders/csv_data/martin/martin.csv", sep=',')
    catalogs = list(data.catalog_number)
    ids = list(data.id)
    catalog_ids = dict(zip(catalogs, ids))
    items = []

    def start_requests(self):
        url = 'http://www.martinsprocket.com/api/Services/getSearchResults'
        for catalog in self.catalogs:
            yield scrapy.Request(
                                url=url,
                                method='POST',
                                headers={'Content-Type':'application/json'},
                                body=json.dumps(catalog),
                                callback=self.parse_url
                                )

    def parse_url(self, response):
        data = json.loads(response.body_as_unicode())
        for item in data:
            if item['LinkText'] in self.catalogs:
                url = item['Url']
                yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        sku = response.url.rsplit('Part_Number=')[-1].replace('%20', ' ')
        if not sku in self.items:
            img =  response.xpath('//img[@alt="'+sku+'"]/@src').extract_first()
            domain = response.url.rsplit('/')[2]
            img_url = 'http://' + domain + img
            item = MartinItem()
            item['id'] = self.catalog_ids[sku]
            item['catalog_number'] = sku
            item['img_url'] = img_url
            self.items.append(sku)
        return item


