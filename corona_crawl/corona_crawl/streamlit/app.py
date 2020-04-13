## import Streamlit Library
import pandas as pd
import re
import datetime
import numpy as np
import streamlit as st
import plotly.express as px


## Title
st.title('COVID-19 Dashboard')


## Header/Subheader
st.header('In Korea, COVID-19 Time Series Plot With Plotly')
st.subheader('현재 서울지역의 그래프만 확인 가능한 상태입니다.')
## Text
st.text("Hello Streamlit! 이 페이지는 아직 개발중입니다. 더 많은 시각화 차트와 기능들을 제공하기 위해 조금만 기다려주세요!")


@st.cache
def load_data():
    seoul = pd.read_csv('./data/seoul.csv')

    regex = re.compile('\d.\d+')

    seoul['confirmed_date'] = seoul['confirmed_date'].apply(lambda x: regex.search(x.strip()).group())
    seoul['confirmed_date'] = seoul['confirmed_date'].apply(lambda x: '2020.'+x)
    seoul['confirmed_date']= pd.to_datetime(seoul['confirmed_date'], format='%Y.%m.%d')
    seoul_gu = [
    '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구',
    '노원구',
    '도봉구', '동대문구','동작구',
    '마포구',
    '서대문구', '서초구', '성동구', '성북구','송파구',
    '양천구', '영등포구', '용산구', '은평구',
    '종로구', '중랑구', '중구']
    seoul['city'] = np.where(seoul['city'].isin(seoul_gu), seoul['city'], '기타')

    # CITY_CUMSUM INFRENCED PEOPLES
    day_seoul = seoul.groupby(['confirmed_date', 'city'])['city'].count().reset_index(name="count")
    day_seoul['cum_count'] = day_seoul['count'].iloc[::1].groupby(day_seoul['city']).cumsum()

    day_seoul = day_seoul.pivot(index='confirmed_date', columns='city', values='cum_count')
    day_seoul = day_seoul.fillna(method='pad').fillna(0)

    idx = pd.date_range(day_seoul.index.min(), day_seoul.index.max())
    day_seoul = day_seoul.reindex(idx, method='pad')

    day_seoul = day_seoul.stack().reset_index()
    day_seoul.columns = ['confirmed_date', 'city', 'cum_count']

    day3_idx = pd.date_range(start=day_seoul['confirmed_date'].min(),
                            periods=len(day_seoul.set_index('confirmed_date').resample('3D').first()), 
                            freq='3D')
    day7_idx = pd.date_range(day_seoul['confirmed_date'].min(), 
                            periods=len(day_seoul.set_index('confirmed_date').resample('7D').first()), 
                            freq='7D')
    day15_idx = pd.date_range(day_seoul['confirmed_date'].min(), 
                            periods=len(day_seoul.set_index('confirmed_date').resample('15D').first()), 
                            freq='15D')

    day3_seoul= day_seoul.set_index('confirmed_date').loc[day3_idx].reset_index()
    day7_seoul= day_seoul.set_index('confirmed_date').loc[day7_idx].reset_index()
    day15_seoul= day_seoul.set_index('confirmed_date').loc[day15_idx].reset_index()


    day_seoul['confirmed_date'] = day_seoul['confirmed_date'].astype(str)
    day3_seoul['confirmed_date'] = day3_seoul['confirmed_date'].astype(str)
    day7_seoul['confirmed_date'] = day7_seoul['confirmed_date'].astype(str)
    day15_seoul['confirmed_date'] = day15_seoul['confirmed_date'].astype(str)
    
    return day_seoul, day3_seoul, day7_seoul, day15_seoul



def write_main_page():
    st.title('안내사항')
    st.write("""
이 웹 어플리케이션은 **Streamlit**을 활용하여 간단한 시각화 툴을 만들고 웹 어플리케이션을 배포하는 과정을 안내하기 위한 샘플로 만들어졌습니다.
현재 전 세계적으로 COVID-19 바이러스가 유행함에 따라, 많은 안타까운 일들이 발생하고 있습니다. 
이에 따라 IT업계에 종사하시는 분들 역시 바이러스 확산을 막기 위해, 자신의 위치에서 공익적인 목적의 서비스를 제공하는 것에서 크게 감명을 받게 되었습니다.
정부에서도 [질병관리본부](http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=)를 통해 국내 및 시도별 발생동향 등을 제공하고 있습니다.
하지만 자신의 지역에서의 추세 현황을 확인하기 위해서는 시도별 페이지에 들어가야 하며, 시도별로 통합된 형태의 정보를 제공하고 있지 않아 큰 아쉬움을 느끼게 되어 프로젝트 결심을 하게 되었습니다.
따라서 저희는 수도권 지역에서의 확진자 현황을 크롤링하고, 통합된 형태의 데이터를 제공하는 것과 시각화 차트를 제공하는 것에 목적을 둡니다.
현재는 수도권 지역으로 한정되어 프로젝트를 진행하지만, 향후 전국적으로 확대할 계획입니다.
COVID-19 바이러스의 신속한 해결을 기원합니다.🙏️🙏️🙏️

- 목적
    - 수도권 지역에서의 확진자 현황을 통합된 형태의 데이터로 제공합니다.
    - 수도권 지역에서의 발생 현황을 시간대에 따라 그래프 형태로 제공합니다.

현재는 서울, 경기, 인천 지역 수도권의 그래프만 나타내고 있으며 
웹 어플리케이션에서는 다음과 같은 기능이 있습니다.
- Raw Data
    - 테이블 형태의 데이터셋을 확인할 수 있습니다.
- Graph: Confirmed
    - 1월 23일부터 현재까지 서울, 경기, 인천 현황을 그래프로 확인할 수 있습니다.
## Source
- [Code](https://github.com/pyy0715/Corona19_Dashboard)
## Contributor
- [박용연](https://github.com/pyy0715)
- [문현종](https://github.com/hj0302)
"""
             )

@st.cache
def plot_confirmed(df):
     fig = px.bar(df,
             x="city", y="cum_count",
             animation_frame="confirmed_date",
             animation_group="city",
             range_y=[0, df['cum_count'].max()+5])
    
     fig.update_layout(title_text='Inferenced Peoples In Seoul City With Animation Bar Plot', showlegend=False)
     fig.update_xaxes(tickangle=45, title_text="City")
     fig.update_yaxes(tickangle=15, ticksuffix="명", title_text="Inferenced Peoples")

     return fig


def create_layout(day_seoul, day3_seoul, day7_seoul, day15_seoul):
    st.sidebar.title("도시")
    page = st.sidebar.selectbox("도시를 선택해주세요.",
                                ["Main",
                                 "서울",
                                 "경기",
                                 "인천"])

    day = st.sidebar.selectbox("날짜별 간격을 선택해주세요.",
                                ["하루",
                                 "3일",
                                 "7일",
                                 "15일"])
    if page == 'Main':
        write_main_page()
    elif (page == '서울') & (day=='하루'):
        st.title('Seoul COVID19 Time Series Plot')
        st.dataframe(day_seoul)
        fig = plot_confirmed(day_seoul)
        st.plotly_chart(fig)
    elif (page == '서울') & (day=='3일'):
        st.title('Seoul COVID19 Time Series Plot')
        st.dataframe(day3_seoul)
        fig = plot_confirmed(day3_seoul)
        st.plotly_chart(fig)
    elif (page == '서울') & (day=='7일'):
        st.title('Seoul COVID19 Time Series Plot')
        st.dataframe(day7_seoul)
        fig = plot_confirmed(day7_seoul)
        st.plotly_chart(fig)
    elif (page == '서울') & (day=='15일'):
        st.title('Seoul COVID19 Time Series Plot')
        st.dataframe(day15_seoul)
        fig = plot_confirmed(day15_seoul)
        st.plotly_chart(fig)

def main():
    df, day3_df, day7_df, day15_df = load_data()
    create_layout(df, day3_df, day7_df, day15_df)


if __name__ == "__main__":
    main()