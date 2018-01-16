# -*- coding: utf-8 -*-
import json
import re
import shutil
import urllib
import urllib2
from collections import defaultdict

import pandas as pd
import scrapy
from mro.items import UniversalItem

out = pd.read_csv("mro/spiders/csv_data/Rexnord/test_items_1.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.ids)
cadids = [str(item).replace('"', '') for item in list(out.cadid)]
catalog_ids = dict(zip(catalog, ids))
catalog_cadids = dict(zip(catalog, cadids))


# out1 = pd.read_csv("/data/mro-crawls/rexnord/toshiba/toshiba/rexnord_cads_raw.csv", sep=',')
# catalog1 = [str(item).strip() for item in list(out1.catalog_number)]

class RexnordCadCrawl(scrapy.Spider):
    name = "rexnord_cad"
    allowed_domains = ["rexnord.com", "product-config.net"]
    pr = 0

    def start_requests(self):
        for row in catalog:
            # if row in catalog1:
            # 	continue
            cadid = catalog_cadids[row]
            url = 'https://www.product-config.net/cfg/rexnord/js/{}.js'.format(cadid)
            proxy = 'http://108.59.14.203:13041/'
            yield scrapy.Request(url=url,
                                 callback=self.parse_item,
                                 dont_filter=True,
                                 meta={'catalog_number': row, 'cadid': cadid, 'proxy': proxy})

    def parse_item(self, response):
        catalog_number = response.meta['catalog_number']
        cadid = response.meta['cadid']

        req1 = urllib2.Request('https://www.rexnord.com/Product/' + catalog_number)
        resp1 = urllib2.urlopen(req1)
        productId = re.findall(r'"productId":"(.+)","productName', resp1.read())[0]

        req = urllib2.Request(
            'https://www.rexnord.com/api/v1/products/' + productId + '?expand=documents,specifications,styledproducts,htmlcontent,attributes,crosssells,relatedproductbrand,excludeconfiguredproduct')
        resp = urllib2.urlopen(req)
        data = json.loads(resp.read())
        attributes = data['product']['htmlContent']

        variation_names = re.findall('this.cadManager.addRule\("(.+?)"', response.body)
        variation_values = re.findall('this.cadManager.addRule\(".+?","(.+?)"', response.body)
        row_variations = zip(variation_names, variation_values)

        variations_dict = defaultdict(list)
        for k, v in row_variations:
            variations_dict[k].append(v)

        variations = {}
        for variation in variations_dict:
            key = variation
            values = variations_dict[variation]

            if key == 'SHAFT_DIAMETER' and '"' in attributes:
                size = re.findall('(.+?)"', attributes)[0]
                size = size.replace('/', '_').replace('\\', '')
                if size in values:
                    final_value = size
                else:
                    final_value = values[0]
                variations[key] = final_value
                variations['UNITS'] = 'IN'
                continue

            elif key == 'SHAFT_DIAMETER' and '"' not in attributes:
                size = re.findall('(\d+)', attributes)[0]
                if size in values:
                    final_value = size
                else:
                    final_value = values[0]
                variations[key] = final_value
                variations['UNITS'] = 'MM'
                continue

            elif key == 'SEAL_TYPE':
                if 'Seal' in attributes:
                    seal = re.findall('(\w+) Seal', attributes)[0]
                    for value in values:
                        if seal in value:
                            variations[key] = value
                            break
                continue

            elif key == 'UNIT_TYPE':
                if 'Fixed' in attributes or 'fixed' in attributes:
                    if 'FIXED' in values:
                        variations[key] = 'FIXED'
                    else:
                        variations[key] = values[0]
                else:
                    if 'EXPANSION' in values:
                        variations[key] = 'EXPANSION'
                continue

            elif key == 'BORE_TYPE':
                if 'Shaft' in attributes:
                    if 'SHAFT' in values:
                        variations[key] = 'SHAFT'
                else:
                    if 'Square' in attributes or 'square' in attributes:
                        if 'SQUARE' in values:
                            variations[key] = 'SQUARE'
                    elif 'Hex' in attributes or 'hex' in attributes:
                        if 'HEX' in values:
                            variations[key] = 'HEX'
                continue

            elif key == 'TEETH':
                teeth = re.findall('(\d+) Teeth', attributes)
                if teeth:
                    variations[key] = teeth[0]
                continue

            elif key == 'BORE_DIAMETER':
                d = re.findall('(\d+)M', attributes)
                if d:
                    variations[key] = d[0]
                continue

        for key, values in variations_dict.iteritems():
            if key not in variations:
                for val in values:
                    if val.lower() in attributes.lower():
                        variations[key] = val

        for key, value in variations_dict.iteritems():
            if key not in variations:
                variations[key] = value[0]

        url = 'https://www.product-config.net/catalog3/cad?d=rexnord.cfg&id={}&f=sat'.format(cadid)
        i = 0
        for variation in variations:
            url += '&p{}={}&v{}={}'.format(i, variation, i, variations[variation])
            i += 1

        proxy = 'http://108.59.14.203:13041/'

        return scrapy.Request(
            url=url + '&p{}=REV_DATE&v{}=10-1-2017'.format(i, i),
            callback=self.download_cad,
            dont_filter=True,
            meta={'catalog_number': catalog_number, 'cadid': cadid, 'proxy': proxy}
        )

    def download_cad(self, response):
        catalog_number = response.meta['catalog_number']
        print catalog_number
        cadid = response.meta['cadid']
        data = response.body_as_unicode()
        data = json.loads(data)
        proxy = 'http://108.59.14.203:13041/'
        if 'error' in data:
            print data['error']

            new_url = 'https://www.product-config.net/catalog3/cad?d=rexnord.cfg&id={}&f=dxf-default&p0=REV_DATE&v0=10-1-2017'.format(
                cadid)
            return scrapy.Request(
                url=new_url,
                callback=self.download_cad,
                meta={'catalog_number': catalog_number, 'cadid': cadid, 'proxy': proxy}
            )

        # req1 = urllib2.Request(new_url)
        # resp1 = urllib2.urlopen(req1)
        # data = json.loads(resp1.read())
        # print 'data:' + str(resp1.read())
        # if 'url' in data:
        # 	self.pr += 1
        #	print 'DEFAULT FILES NUMBER:' + str(self.pr)
        # elif 'error' in data:
        #	print 'Error again'
        #	print data['error']

        url = data['url']

        item = UniversalItem()
        item['ids'] = catalog_ids[catalog_number]
        item['catalog_number'] = catalog_number
        try:
            url1 = 'http:' + url
            req = urllib2.Request(url1)
            resp = urllib2.urlopen(req)
            file_name = '%s.zip' % urllib.quote_plus(str(catalog_number).strip())
            with open('rexnord_download/' + file_name, 'wb') as file:
                shutil.copyfileobj(resp.fp, file)
        except Exception:
            print 'DOWNLOAD EXCEPTION'
            return
        else:
            item['cad'] = file_name
        return item
