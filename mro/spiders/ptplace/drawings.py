# -*- coding: utf-8 -*-
import scrapy

from mro.BaseSpiders.base_spiders import BaseMroSpider


class Ptplace(BaseMroSpider):
    name = "ptplace_draw"
    search_url = 'http://medias.schaeffler.de/medias/de!hp.ds/?tab=direkt&pattern={}#produkt'
    path_to_data = 'mro/spiders/csv_data/ptplace/Product_2018-3-1 (FAG) (1).csv'
    separator = ','
    output_fields = ('id', 'catalog_number', 'drawings')

    def start_requests(self):
        for row in self.catalog:
            yield scrapy.Request(url=self.search_url.format(row.replace('.', '-')),
                                 callback=self.parse_item,
                                 cookies=self.base_cookies,
                                 meta={'row': row}
                                 )

    def parse_item(self, response):
        catalog = response.meta['row']
        catalog_ = catalog.replace('.', '-')
        for name in response.xpath(
                '//*[@id="std-layout1_popup"]/div[1]/div/div/div[2]/table[1]/tr/td[1]/div[1]/a/nobr'):
            search_catalog = name.xpath('./text()').extract_first() or ''
            if search_catalog == catalog_ or search_catalog.replace('-', '') == catalog_:
                url = name.xpath('./../@href').extract_first()
                if url:
                    return scrapy.Request(url=response.urljoin(url),
                                          callback=self.parse_next,
                                          meta=response.meta
                                          )

    def parse_next(self, response):
        catalog = response.meta['row']
        exclude_images = ['eigen_rot', 'transpix']
        images = [img for img in response.xpath('//table/tr/td/img/@src').extract() if
                  all([i not in img for i in exclude_images])]
        for img in filter(lambda x: all([i not in x for i in exclude_images]),
                          response.xpath('//table/tr/td/img/@src').extract()):
            yield self.create_item(self.catalog_id[catalog], catalog, response.urljoin(img))
