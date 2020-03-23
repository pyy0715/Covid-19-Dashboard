# Corona Dashboard 

본 프로젝트는 코로나 바이러스의 심각성을 인지하고,

시간에 따른 바이러스의 확산, 시/도 별 사망자 추이 등의 시각화를 다룰 예정입니다.

시각화 결과는 대시보드를 통해 구축되어집니다.


## Crawling

### 수집 사이트
| 지역 | 주소                                            |
|------|-------------------------------------------------|
| 서울 | https://www.seoul.go.kr/coronaV/coronaStatus.do |
| 인천 | https://www.incheon.go.kr/health/HE020409       |
| 경기 |        |


### 실행
```
scrapy crawl seoul -o seoul.csv -t csv
scrapy crawl incheon -o incheon.csv -t csv
```

## EDA
`plotly`
`Bokeh`

## Dashboard
`Streamlit`
