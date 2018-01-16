# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
import re

urls = [
'https://www.linkedin.com/in/dmitry-eydinov-668a261a/',
'https://www.linkedin.com/in/anna-kozyura-27595037/',
'https://www.linkedin.com/in/mina-khachatryan-b49b1111/',
'https://www.linkedin.com/in/aleksey-lilinchuk-16028347/',
'https://www.linkedin.com/in/olga-kukharenko-376aa864/',
'https://www.linkedin.com/in/olga-lantsova-63195568/',
'https://www.linkedin.com/in/andrei-khrometsky-64785530/'
]

cookies = {"visit":"v=1&G", 
'bcookie':"v=2&c30e1053-36b2-46ad-8983-21eba85091df",
'bscookie':"v=1&201712310010181f760551-f8b1-494d-8d30-f2ec336b17f4AQGsq3gJGZpwLXR5ttk3Iq2LGi1x_9vN",
'_gat':'1', 
'sl':"v=1&lPfDy", 
'lang':"v=2&lang=ru-ru", 
'JSESSIONID':"ajax:5168539906656706082",
'li_at':'AQEDASVjumECGWBCAAABYKnoLrkAAAFgzfSyuU4AdpNr848Hnxwo2FS0QDmRxyq7S61DhkxWfi-nuoZ_eWb41I_0rNnmQWYiEDk98GQZlVdvxU1XYEmYKPv5qoY3qfIjy81V8xPcn8HnZzEBUDhxPCG_', 
'liap':'true',
'lidc':"b=TGST03:g=669:u=1:i=1514679054:t=1514764652:s=AQHjbxxZzA3tERcFCF4kRKLYXpE2HrzO",
'RT':'s=1514678981287&r=https%3A%2F%2Fwww.linkedin.com%2Fhome',
'_ga':'GA1.2.1161794755.1514678950',
'_lipt':'CwEAAAFgqehOlC2S0EQtm6j2pS8CE4oTut57RvEXloqAehqr84dXdwRbvOj378_YM_M-QUogxO1ZFjhiz6keg9FDMPJ8c5BxqBRFFDVo2LqAoloNpmfPKvpdEuY'
}

class Mcr(scrapy.Spider):
    name = 'linkedin'
    handle_httpstatus_list = [999]

    def start_requests(self):
        for url in range(2):
            yield scrapy.Request(url=urls[0], cookies=cookies, dont_filter=True, callback=self.parse_data)


    def parse_data(self, response):
        print re.findall(r'firstName:([a-zA-z]+),',response.body.replace('&quot;', ''))[0]






