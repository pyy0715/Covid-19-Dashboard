## import Streamlit Library
import os
import re
import json

import pandas as pd
import numpy as np
import datetime

from PIL import Image
from mapboxgl.utils import create_color_stops, create_numeric_stops
from mapboxgl.viz import *
import streamlit as st
import plotly.express as px

from preprocessing import process_app

token = 'pk.eyJ1IjoibW9vbmhqIiwiYSI6ImNrNWh3dTd5OTA2ZzgzbHNiYjgxNWswb3UifQ.3Kr6ca8BPegIKxbyW4ppJA'


# day, city centroid dictionary
day_dict = {'하루':'1D', '3일':'3D', '7일':'7D', '15일': '15D'}
city_dict = {'서울':'seoul', '인천':'incheon', '경기':'gyeonggi'}
centroid_dict = {
    '서울': {'lat' : 37.5642135, 'lon' :127.0016985},
    '경기': {'lat' : 37.457167 , 'lon' :127.190292},
    '인천': {'lat' : 37.593355, 'lon' :126.592526},
    }
zoom_dict = {
    '서울': 9,
    '경기': 7.7,
    '인천': 9,
    }

## Title
st.title('COVID-19 Dashboard')


## Header/Subheader
st.header('In Korea, COVID-19 Dashboard With Plotly')
st.subheader('Version 20-04-24')
## Text
st.text("현재는 서울, 경기, 인천 수도권 지역의 그래프만 나타내고 있습니다. \n더 많은 시각화 차트와 기능들을 제공하기 위해 조금만 기다려주세요!")

# @st.cache(allow_output_mutation=True)
def load_data(city):
    patent_dir = './data/'
    patent_dir2 = './file/'
    df = pd.read_csv(os.path.join(patent_dir, city + '.csv'))
    with open(os.path.join(patent_dir, city + '.geojson'), encoding='utf-8') as jsonfile:
        geo_json=json.load(jsonfile)
    img = Image.open(os.path.join(patent_dir2, city + '.jpg'))
    resize_image = img.resize((1200, 400))
    return df, geo_json, resize_image




def write_main_page():
    st.title('안내사항')
    st.write("""
이 웹 어플리케이션은 **Streamlit**을 활용하여 간단한 시각화 툴을 만들고 웹 어플리케이션을 배포하는 과정을 안내하기 위한 샘플로 만들어졌습니다.

현재 전 세계적으로 COVID-19 바이러스가 유행함에 따라, 많은 안타까운 일들이 발생하고 있습니다. 

이에 따라 IT업계에 종사하시는 분들 역시 바이러스 확산을 막기 위해, 자신의 위치에서 공익적인 목적의 서비스를 제공하는 것에서 크게 감명을 받게 되었습니다.

이와 더불어 정부에서도 [질병관리본부](http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=)에서 국내 및 시도별 발생동향 등을 제공하고 있습니다.

하지만 자신의 지역에서의 추세 현황을 확인하기 위해서는 시도별 페이지에 들어가야 하며, 시도별로 통합된 형태의 정보를 제공하고 있지 않아 큰 아쉬움을 느끼게 되어 프로젝트 결심을 하게 되었습니다.

따라서 저희는 수도권 지역에서의 확진자 현황을 크롤링하고, 통합된 형태의 데이터를 제공하는 것과 시각화 차트를 제공하는 것에 목적을 둡니다.

현재는 수도권 지역으로 한정되어 프로젝트를 진행하지만, 향후 전국적으로 확대할 계획입니다.

마지막으로 COVID-19 바이러스의 신속한 해결을 기원합니다.🙏️🙏️🙏️\n

- **목적**
    - 수도권 지역에서의 확진자 현황을 통합된 형태의 데이터로 제공합니다.

    - 수도권 지역에서의 자치구별 발생 현황을 일별에 따른 그래프 형태로 제공합니다.

- **Graph**
    - 1월 23일부터 현재까지 서울, 경기, 인천 현황을 그래프로 확인할 수 있습니다.

## Source
- [Code](https://github.com/pyy0715/Corona19_Dashboard)

## Contributor
- [박용연](https://github.com/pyy0715)
- [문현종](https://github.com/hj0302)
"""
             )

@st.cache
def plot_confirmed(df, page):
    fig = px.bar(
        df,
        x="city", y="cum_count",
        animation_frame="confirmed_date",
        animation_group="city",
        range_y=[0, df['cum_count'].max()+5]
        )
    
    fig.update_layout(title_text=f'In {page}, Inferenced Peoples With Animation Bar Plot', showlegend=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_xaxes(tickangle=45, title_text="Time Axis")
    fig.update_yaxes(tickangle=15, ticksuffix="명", title_text="Inferenced Peoples")

    return fig

@st.cache
def plot_map_confirmed(df, json, centroid_dict, page):
    fig = px.choropleth_mapbox(
        data_frame=df, 
        geojson=json,
        locations="city",
        color="cum_count",
        featureidkey="properties.city",
        mapbox_style="open-street-map",
        animation_frame='confirmed_date',
        animation_group='city',
        center = centroid_dict[page], 
        zoom= zoom_dict[page],
        opacity=0.5,
        range_color=(0, df['cum_count'].max()+5),
        labels={'cum_count':'Inferenced Peoples'}
        )
    fig.update_layout(title_text=f'In {page}, Inferenced Peoples With Animation Heat Map', showlegend=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def create_layout():
    st.sidebar.title("도시")
    page = st.sidebar.selectbox("도시를 선택해주세요.",
                                ["Main",
                                 "서울",
                                 "경기",
                                 "인천"])
    st.sidebar.title("날짜")
    day = st.sidebar.selectbox("날짜별 간격을 선택해주세요.",
                                ["선택",
                                 "하루",
                                 "3일",
                                 "7일",
                                 "15일"])
    st.sidebar.title("관리")
    st.sidebar.info(
        """
        이 앱은 오픈소스 프로젝트로 운영되며, 여러분의 많은 관심 부탁드립니다.
        **Park Young Yeon**에 의해 유지 보수되고 있습니다.
        만약 저에 대해 더 알고 싶다면 [LinkedIn](linkedin.com/in/young-yeon-park-67086a14b/)을 방문해주세요.
        """
    )
    st.sidebar.title("문의사항 및 이슈")
    st.sidebar.info(
        "문제가 있거나 오류가 발생할 경우 [Github](https://github.com/pyy0715/Corona19_Dashboard/issues)이나"
        "[Gmail](https://mail.google.com/mail/u/0/#inbox)을 통해 알려주세요!"
    )

    if page == 'Main':
        write_main_page()
    if (page!='Main') & (day in ["하루", "3일", "7일","15일"]):
        df, json, img = load_data(city_dict[page])
        day_df = process_app(page, df, day_dict[day])

        fig=plot_confirmed(day_df, page)
        fig2=plot_map_confirmed(day_df, json, centroid_dict, page)

        st.image(img, width=400)
        st.plotly_chart(fig)
        st.plotly_chart(fig2)


def main():
    create_layout()


if __name__ == "__main__":
    main()