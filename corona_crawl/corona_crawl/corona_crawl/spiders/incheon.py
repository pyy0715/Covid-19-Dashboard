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
         pages = response.css('section:nth-child(3) table tbody tr')
         citys = response.css('div.section4-body > div > div.patient-profile-wrap > a > strong:nth-child(2)::text').getall()

         for idx, item in enumerate(pages):
             doc = CoronaCrawlItem()
             sex_age = item.css('td:nth-child(3)::text').get()
             confirmed_date = item.css('td:nth-child(4)::text').get()
             city = citys[idx]


             sex = sex_age.split(' / ')[0]
             age = sex_age.split(' / ')[1]

             doc['confirmed_date'] = confirmed_date
             doc['province'] = '인천'
             doc['city'] = city
             doc['sex'] = sex
             doc['age'] = age

             yield doc
