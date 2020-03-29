import os
import re
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

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


class gyeonggi:
    def __init__(self):
        self.url = 'https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page=1'
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.confirmed_date = []
        self.city = []
        self.sex = []
        self.age = []
        self.province = '경기'

    def update(self, add_df):
        if os.path.isfile('./data/gyeonggi.csv'):
            original_df = pd.read_csv('./data/gyeonggi.csv')
            add_df.to_csv('./data/gyeonggi.csv', encoding='utf-8-sig', index=False)
            print(f'Updated gyeonggi_df: {original_df.shape} -> {add_df.shape}')
        else:
            add_df.to_csv('./data/gyeonggi.csv', encoding='utf-8-sig', index=False)

    def preprocessing_age(self, lst):
        update_lst = [ int(i) for i in lst]
        update_age = [ birth_to_age(i) for i in update_lst]
        return update_age
    
    def run(self):
        self.driver.get(self.url)
        assert "확진자 세부현황" in self.driver.title

        pages = self.driver.find_elements_by_css_selector('#ajax-paging-navigation > li > a')
        last_page = int(pages[-1].get_attribute('href')[-2:])
        print(f'총 페이지 수는 {last_page}개 입니다.')
        
        split_pages = [i+1 for i in range(last_page) if i%10==0][1:]
        
        # Page Crawling
        for i in range(1, last_page+1):

            # Next Page+10
            if i in split_pages:
                print('Page가 넘어갑니다....\n')
                all_button = self.driver.find_elements_by_css_selector('#ajax-paging-navigation > li')
        
                if len(all_button)==13:
                    more_button = self.driver.find_element_by_css_selector('#ajax-paging-navigation > li:nth-child(12) > a > span')
                else:
                    more_button = self.driver.find_element_by_css_selector('#ajax-paging-navigation > li:nth-child(13) > a > span')
            
                more_button.click()
                time.sleep(5)
                
            self.driver.find_element_by_link_text(str(i)).click()
            time.sleep(5)

            # Read Table
            rows = self.driver.find_elements_by_xpath("//*[@id='boardList']/tbody/tr")
            for row in rows:
                self.confirmed_date.append(row.find_element_by_css_selector("td:nth-child(7)").text)
                self.driver.implicitly_wait(15)

                self.city.append(row.find_element_by_css_selector("td:nth-child(3)").text)
                self.driver.implicitly_wait(15)
                
                self.sex.append(row.find_element_by_css_selector("td:nth-child(4)").text)
                self.driver.implicitly_wait(15)

                self.age.append(row.find_element_by_css_selector("td:nth-child(5)").text[1:3])
                self.driver.implicitly_wait(15)

            print(f'Page{i} is Crawling Completed')
        
        # Crawling complete
        self.driver.quit()

        # Preprocessing
        self.age = self.preprocessing_age(self.age)

        df = pd.DataFrame({'confirmed_date': self.confirmed_date,
        'province': self.province,
        'city': self.city,
        'sex': self.sex,
        'age': self.age})

        # dataframe to csv
        self.update(df)


if __name__ == '__main__':
    crawl = gyeonggi()
    crawl.run()



