# -*- coding: utf-8 -*-
import scrapy
import re
from corona_crawl.items import CoronaCrawlItem

class SeoulSpider(scrapy.Spider):
    name = 'seoul'

    def start_requests(self):
        #  province2http = {
        #      'seoul': 'https://www.seoul.go.kr/coronaV/coronaStatus.do',
        #      'incheon': 'https://www.incheon.go.kr/health/HE020409'
        #      }

    
        #  callback2parse ={
        #     'seoul': self.parse_seoul,
        #     'incheon': self.parse_incheon
        #     }
            
            
        #  for province, http in province2http.items():
        #     yield scrapy.Request(url=http, callback=callback2parse[province])
        yield scrapy.Request(url='https://www.seoul.go.kr/coronaV/coronaStatus.do', callback=self.parse_seoul)
    

    def parse_seoul(self, response):
         print('Seoul Crawling...')
         pages = response.xpath("//div[starts-with(@id, 'cont-page')]")

         for page in pages:
             for idx, item in enumerate(page.css('tr')[1:]):
                 doc = CoronaCrawlItem()

                 confirmed_date = item.css('td:nth_child(3)::text').get()
                 city = item.css('td:nth_child(5)::text').get()
                 sex_age = item.css('td:nth_child(4)::text').get()
                 state = item.css('td:nth_child(8) b::text').get()

                 age = int(re.sub('[^0-9]', '', sex_age))
                 sex = re.sub('[^ㄱ-힗]', '', sex_age)

                 if state is None:
                    state = 1 # 치료중
                 else:
                    state = 0   # 퇴원 

                 doc['confirmed_date'] = confirmed_date
                 doc['province'] = '서울'
                 doc['city'] = city
                 doc['sex'] = sex
                 doc['age'] = age
                 doc['state'] = state

                 yield doc