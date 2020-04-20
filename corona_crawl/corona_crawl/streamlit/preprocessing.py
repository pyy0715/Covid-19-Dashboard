import re
import pandas as pd 
import numpy as np
import datetime


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

def process_app(page, df, period): 

    if page=='인천':
        regex = re.compile('\d+.\d+.\d+')

        df['confirmed_date'] = df['confirmed_date'].apply(lambda x: regex.search(x.strip()).group())
        df['confirmed_date']= pd.to_datetime(df['confirmed_date'], format='%Y.%m.%d')
        df['city'] = np.where(df['city'].isin(incheon_gu), df['city'], '기타')
        df = df.loc[df['city']!='기타']
        
    if page=='서울':
        regex = re.compile('\d.\d+')

        df['confirmed_date'] = df['confirmed_date'].apply(lambda x: regex.search(x.strip()).group())
        df['confirmed_date'] = df['confirmed_date'].apply(lambda x: '2020.'+x)
        df['confirmed_date']= pd.to_datetime(df['confirmed_date'], format='%Y.%m.%d')
        df['city'] = np.where(df['city'].isin(seoul_gu), df['city'], '기타')
        df = df.loc[df['city']!='기타']

    if page=='경기':
        regex = re.compile('\d.\d+')

        df['confirmed_date'] = df['confirmed_date'].apply(lambda x: regex.search(x.strip()).group())
        df['confirmed_date'] = df['confirmed_date'].apply(lambda x: '2020.'+x)
        df['confirmed_date']= pd.to_datetime(df['confirmed_date'], format='%Y.%m.%d')
        df['city'] = np.where(df['city'].isin(gyeonggi_gu), df['city'], '기타')
        df = df.loc[df['city']!='기타']


    # CITY_CUMSUM INFRENCED PEOPLES
    day_df = df.groupby(['confirmed_date', 'city'])['city'].count().reset_index(name="count")
    day_df['cum_count'] = day_df['count'].iloc[::1].groupby(day_df['city']).cumsum()

    day_df = day_df.pivot(index='confirmed_date', columns='city', values='cum_count')
    day_df = day_df.fillna(method='pad').fillna(0)

    idx = pd.date_range(day_df.index.min(), day_df.index.max())
    day_df = day_df.reindex(idx, method='pad')

    day_df = day_df.stack().reset_index()
    day_df.columns = ['confirmed_date', 'city', 'cum_count']

    # Generate Days Resampling
    day_idx = pd.date_range(start=day_df['confirmed_date'].min(),
                            periods=len(day_df.set_index('confirmed_date').resample('3D').first()), 
                            freq=period)

    # Reset Index
    day_df= day_df.set_index('confirmed_date').loc[day_idx].reset_index()

    # Type Change
    day_df['confirmed_date'] = day_df['confirmed_date'].astype(str)
    
    return day_df

