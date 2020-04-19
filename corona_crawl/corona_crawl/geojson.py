import json
import pandas as pd
import geopandas as gpd
import numpy as np

import warnings
warnings.filterwarnings("ignore")

token = 'pk.eyJ1IjoibW9vbmhqIiwiYSI6ImNrNWh3dTd5OTA2ZzgzbHNiYjgxNWswb3UifQ.3Kr6ca8BPegIKxbyW4ppJA'

class ploygon_to_json:
    def __init__(self, geo_data, df, gu_list):
        self.geo_data = geo_data
        self.df = df
        self.gu_list = gu_list
        self.name = [x for x in globals() if globals()[x] is df][0]  


    def only_city(self):
        city_df = self.df
        city_df['city'] = np.where(city_df['city'].isin(self.gu_list), city_df['city'], '기타')
        city_df = city_df.loc[city_df['city']!='기타']
        city_df = city_df[['province', 'city']].drop_duplicates()
        city_df = city_df.reset_index(drop=True)
        
        return city_df

    
    def df_to_geo(self):
        geo_df = gpd.read_file(self.geo_data)
        geo_df = pd.DataFrame(geo_df)
        geo_df.rename(columns={'SIG_KOR_NM': 'city'}, inplace=True)

        if self.name=='seoul':
            geo_metry = geo_df.iloc[139:164, :]
        if self.name=='incheon':
            geo_metry = geo_df.iloc[170:180, :]
        if self.name=='gyeonggi':
            geo_metry = geo_df.iloc[18:60, :]

        return geo_metry

    def to_json(self, df, geometry):
        geo_df = pd.merge(df, geometry[['city', 'geometry']], on ='city')
        gpd.GeoDataFrame(geo_df).to_file(f"./data/{self.name}.geojson", driver='GeoJSON')

    def forward(self):
        df = self.only_city()
        geo_metry = self.df_to_geo()
        self.to_json(df, geo_metry)



geo_data = './geo_data/TL_SCCO_SIG.json'

incheon = pd.read_csv('./data/incheon.csv', encoding='utf-8')
seoul = pd.read_csv('./data/seoul.csv', encoding='utf-8')
gyeonggi = pd.read_csv('./data/gyeonggi.csv', encoding='utf-8')


seoul_gu = [
    '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구',
    '노원구',
    '도봉구', '동대문구','동작구',
    '마포구',
    '서대문구', '서초구', '성동구', '성북구','송파구',
    '양천구', '영등포구', '용산구', '은평구',
    '종로구', '중랑구', '중구']

incheon_gu =['연수구', '부평구', '서구', '남동구', '미추홀구', '계양구', '중구', '동구', '부평구','강화군','웅진군']

gyeonggi_gu=['가평군', '고양시', '과천시', '광명시', '광주시', '구리시',
'군포시', '김포시', '남양주시', '동두천시', '부천시', '성남시',
'수원시', '시흥시', '안산시', '안성시', '안양시', '양주군',
'양평군', '여주군', '연천군', '오산시', '용인시', '의왕시',
'의정부시', '이천시', '파주시', '평택시', '포천군', '하남시', '화성시']



if __name__ == '__main__':
    ploygon_to_json(geo_data, seoul, seoul_gu).forward()
    ploygon_to_json(geo_data, gyeonggi, gyeonggi_gu).forward()
    ploygon_to_json(geo_data, incheon, incheon_gu).forward()