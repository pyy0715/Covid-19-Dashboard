# -*- coding: utf-8 -*-
import scrapy
import re
from corona_crawl.items import CoronaCrawlItem

class IncheonSpider(scrapy.Spider):
    name = 'incheon'

    def start_requests(self):
        yield scrapy.Request(url='https://www.incheon.go.kr/health/HE020409', callback=self.parse_incheon)
        
    

    def parse_incheon(self, response):
         print('Incheon Crawling...')
         pages = response.css('section > div.section4-body > div.patient-profile-route-group')

         for idx, item in enumerate(pages):
             doc = CoronaCrawlItem()
             
             text = item.xpath("div[1]/a/text()[3]").get()
             city = item.xpath("div[1]/a/strong[2]/text()").get()

             text = re.sub('[\t\r\n()]','',text)
             text = text.split('/')

             sex_age = text[0]
             confirmed_date = text[1]

             sex = sex_age[0]
             age = sex_age[1:3]

             city = re.sub(' ', '', city)
             confirmed_date = re.sub(' ', '', confirmed_date)

             doc['confirmed_date'] = confirmed_date
             doc['province'] = '인천'
             doc['city'] = city
             doc['sex'] = sex
             doc['age'] = age

             yield doc
