# -*- coding: utf-8 -*-
import json
import re
import shutil
import urllib
import urllib2

import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from mro.items import UniversalItem


class BearCadsSpider(CrawlSpider):
    name = "bear_cads1"
    allowed_domains = ["http://bearingfinder.ntnamericas.com"]
    pr = False
    data = pandas.read_csv("spiders/csv_data/Bearingfinder/NTN.csv", sep=',')
    catalog = list(data.catalog_number)
    ids = list(data.id)
    catalog_ids = dict(zip(catalog, ids))

    proxy = 'http://163.172.48.109:15002/'

    urls = []
    for sku in catalog:
        urls.append(
            'http://bearingfinder.ntnamericas.com/keyword/?keyword={}&refer=http://bearingfinder.ntnamericas.com'.format(
                str(sku)))
    start_urls = urls

    def parse(self, response):
        # self.logger.info('Parse function called on %s', response.url)
        if response.xpath('//nav[@id="plp-product-title"]').extract():
            if response.xpath('//a[@id="plp-cadcart"]/@data-itemnumber'):
                sku = response.xpath('//a[@id="plp-cadcart"]/@data-itemnumber').extract()[0]
            else:
                title = response.xpath('//title/text()').extract()[0]
                sku = re.findall(r'# (.+?),', title)[0]
            shortname = ''

            url = self.get_url(response)
            url = 'http://bearingfinder.ntnamericas.com' + url + '&currentcadview=2'

            response.request.cookies.update({
                'p.cad': '%7B%22systemUnit%22%3A%22inch%22%2C%22DL_2D%22%3A%22pdf%22%7D',
                'p.caduser_1': '%5B%7B%22V%22%3A%22Vlad%22%2C%22AID%22%3A106%2C%22MID%22%3A0%2C%22Value%22%3A%22Vlad%22%7D%2C%7B%22V%22%3A%22Ilnitskiy%22%2C%22AID%22%3A107%2C%22MID%22%3A0%2C%22Value%22%3A%22Ilnitskiy%22%7D%2C%7B%22V%22%3A%22vl.ilnitskiy%40gmail.com%22%2C%22AID%22%3A130%2C%22MID%22%3A0%2C%22Value%22%3A%22vl.ilnitskiy%40gmail.com%22%7D%2C%7B%22V%22%3A%22vl.ilnitskiy%40gmail.com%22%2C%22AID%22%3A1745%2C%22MID%22%3A0%2C%22Value%22%3A%22vl.ilnitskiy%40gmail.com%22%7D%2C%7B%22V%22%3A%22MRO%20%2F%20end%20user%22%2C%22AID%22%3A1792%2C%22MID%22%3A0%2C%22Value%22%3A%22MRO%20%2F%20end%20user%22%7D%2C%7B%22V%22%3A%22Free%22%2C%22AID%22%3A112%2C%22MID%22%3A0%2C%22Value%22%3A%22Free%22%7D%2C%7B%22V%22%3A%2201001%22%2C%22AID%22%3A122%2C%22MID%22%3A0%2C%22Value%22%3A%2201001%22%7D%2C%7B%22V%22%3A%22UKRAINE%22%2C%22AID%22%3A124%2C%22MID%22%3A0%2C%22Value%22%3A%22UKRAINE%22%7D%5D',
                # 'p.ins': 'True'
            })
            return scrapy.Request(
                url=url,
                callback=self.parse_cad_page,
                dont_filter=True,
                cookies=response.request.cookies,
                meta={
                    'catalog_number': sku,
                    'shortname': shortname,
                    # 'dont_merge_cookies': True,
                    # 'cookiejar': 1
                    'proxy': self.proxy
                }
            )

    def get_url(self, response):
        if response.xpath('//a[text()="2D Sectional View"]/@data-url'):
            url = response.xpath('//a[text()="2D Sectional View"]/@data-url').extract()[0]
            return url.replace('amp;', '')
        else:
            print 'ON PRODUCT PAGE, BUT THERE IS NOT 2D SECTIONAL VIEW'
            return

    def parse_cad_page(self, response):
        cadstoreid = None
        if response.xpath('//select[@data-caddownloaddir="c:\_download"]/@data-cadstoreid'):
            cadstoreid = response.xpath('//select[@data-caddownloaddir="c:\_download"]/@data-cadstoreid').extract()[0]
            downloaddir = 'c:\_download'
        elif response.xpath('//select[@data-caddownloaddir="c:\_insert"]/@data-cadstoreid'):
            cadstoreid = response.xpath('//select[@data-caddownloaddir="c:\_insert"]/@data-cadstoreid').extract()[0]
            downloaddir = 'c:\_insert'

        if not cadstoreid:
            print "CAN'T GET CAD STORE ID"
            return

        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json; charset=UTF-8',
            'Content-Length': '110',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Referer': str(response.request.url)
        }
        payload = '{"cadStoreID":' + cadstoreid + ',"downloadFormat":"pdf","insertSystem":"ALIBRE_DESIGN_2d","downloadDir":"c:\\\_download"}'
        url = response.request.url

        response.request.cookies.update({
            # 'ASP.NET_SessionId': 'ndp25eu5havlaov15zfuvfv0',
            # 'p.cc': '',
            # 'p.dl': '0',
            'p.cad': '%7B%22systemUnit%22%3A%22inch%22%2C%22DL_2D%22%3A%22pdf%22%7D',
            'p.caduser_1': '%5B%7B%22V%22%3A%22Vlad%22%2C%22AID%22%3A106%2C%22MID%22%3A0%2C%22Value%22%3A%22Vlad%22%7D%2C%7B%22V%22%3A%22Ilnitskiy%22%2C%22AID%22%3A107%2C%22MID%22%3A0%2C%22Value%22%3A%22Ilnitskiy%22%7D%2C%7B%22V%22%3A%22vl.ilnitskiy%40gmail.com%22%2C%22AID%22%3A130%2C%22MID%22%3A0%2C%22Value%22%3A%22vl.ilnitskiy%40gmail.com%22%7D%2C%7B%22V%22%3A%22vl.ilnitskiy%40gmail.com%22%2C%22AID%22%3A1745%2C%22MID%22%3A0%2C%22Value%22%3A%22vl.ilnitskiy%40gmail.com%22%7D%2C%7B%22V%22%3A%22MRO%20%2F%20end%20user%22%2C%22AID%22%3A1792%2C%22MID%22%3A0%2C%22Value%22%3A%22MRO%20%2F%20end%20user%22%7D%2C%7B%22V%22%3A%22Free%22%2C%22AID%22%3A112%2C%22MID%22%3A0%2C%22Value%22%3A%22Free%22%7D%2C%7B%22V%22%3A%2201001%22%2C%22AID%22%3A122%2C%22MID%22%3A0%2C%22Value%22%3A%2201001%22%7D%2C%7B%22V%22%3A%22UKRAINE%22%2C%22AID%22%3A124%2C%22MID%22%3A0%2C%22Value%22%3A%22UKRAINE%22%7D%5D',
            # '__utma': '231644992.372785498.1506708522.1507983766.1507986733.16',
            # '__utmc': '231644992',
            # '__utmz': '231644992.1506708522.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            # 'visitor_id65442': '372741251',
            # 'visitor_id65442-hash': '346693a56061607d267c4767de4b84b24e34b8137037c04bbd952144e8ad7dbf34421ddcdc5c9a844c7a64920a6fc56eec0b9b30',
            # 'p.dm': 'desktop',
            # 'p.us': 'ndp25eu5havlaov15zfuvfv0',
            # 'p.s': '51835259',
            # 'p.ins': 'True',
            # 'p.c': '7115',
            # 'p.d': 'Pub',
            # 'p.cg': '0',
            # 'p.v': '1006',
            # 'p.umd.7115.0.._1': '%7B%22LD%22%3A%222017-08-23T09%3A57%3A16.11%22%2C%22SN%22%3A51835259%2C%22VR%22%3A1006%2C%22CG%22%3A0%2C%22LE%22%3A0%2C%22MA%22%3A%5B%5D%7D',
            # 'p.ud.7115.0.._1': '%5B%5D'
        })

        return scrapy.Request(
            method='POST',
            url=url,
            callback=self.get_cad_direct_url,
            dont_filter=True,
            headers=headers,
            cookies=response.request.cookies,
            body=payload,
            meta=response.meta
        )

    def get_cad_direct_url(self, response):
        hxs = HtmlXPathSelector(response)
        if 'CadDownloadUrl' in response.body:
            data = json.loads(response.body)

            print '\n'
            print 'CAD DOWNLOAD URL'
            print data['CadDownloadUrl']
            print '\n'

            item = UniversalItem()
            catalog_number = response.request.meta['catalog_number']
            item['catalog_number'] = catalog_number
            item['ids'] = self.catalog_ids[catalog_number]
            try:
                url = data['CadDownloadUrl']
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                file_name = '%s.pdf' % urllib.quote_plus(str(catalog_number))
                with open('bear_download/' + file_name, 'wb') as file:
                    shutil.copyfileobj(resp.fp, file)
            except Exception:
                print 'EXCEPTION'
                return
            else:
                item['cad'] = file_name
            return item
        else:
            print '\n'
            print response.request.meta
            print response.body
            print '\n'
            print 'THERE IS NOT CAD DOWNLOAD URL'
            print '\n'
            return
