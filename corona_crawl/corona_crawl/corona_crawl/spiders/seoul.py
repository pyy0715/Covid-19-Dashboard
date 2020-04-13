# -*- coding: utf-8 -*-
import scrapy
import re
from corona_crawl.items import CoronaCrawlItem

from datetime import date

def calculate_age(dtob):
    today = date.today()
    return today.year - dtob+1

def birth_to_age(birth):
    if birth<10:
        birth = int('200'+str(birth))  
    elif 10<=birth<=22:
        birth = int('20'+str(birth))   
    else:
        birth = int('19'+str(birth))
        
    return calculate_age(birth)

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
        yield scrapy.Request(url='http://www.seoul.go.kr/coronaV/coronaStatus.do?menu_code=01', callback=self.parse_seoul)
    

    def parse_seoul(self, response):
         print('Seoul Crawling...')
         pages = response.xpath("//div[starts-with(@id, 'cont-page')]")

         for page in pages:
             for idx, item in enumerate(page.css('tr')[1:]):
                 doc = CoronaCrawlItem()

                 confirmed_date = item.css('td:nth_child(3)::text').get()
                 city = item.css('td:nth_child(4)::text').get()
                #  sex_birth = item.css('td:nth_child(4)::text').get()

                #  birth = int(re.sub('[^0-9]', '', sex_birth))
                #  age = birth_to_age(birth)

                #  sex = re.sub('[^ㄱ-힗]', '', sex_birth)

                 doc['confirmed_date'] = confirmed_date
                 doc['province'] = '서울'
                 doc['city'] = city
                 doc['sex'] = None
                 doc['age'] = None

                 yield doc