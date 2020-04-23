# Korea Covid-19 Dashboard
[![License](https://img.shields.io/github/license/pyy0715/Corona19_Dashboard.svg)](https://github.com/pyy0715/Corona19_Dashboard)  [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpyy0715%2FCorona19_Dashboard)](https://hits.seeyoufarm.com)  [![Build Status](https://img.shields.io/github/forks/pyy0715/Corona19_Dashboard.svg)](https://github.com/pyy0715/Corona19_Dashboard)  [![Build Status](https://img.shields.io/github/stars/pyy0715/Corona19_Dashboard.svg)](https://github.com/pyy0715/Corona19_Dashboard)


본 프로젝트는 Covid-19 바이러스의 심각성을 인지하고,

시간에 따른 바이러스의 확산, 시/도 별 사망자 추이 등의 시각화를 다룰 예정입니다.

시각화 결과는 대시보드를 통해 구축되어집니다.

대시보드는 [Covid19-Dasboard](https://yyeon-covid19-korea.herokuapp.com/)에서 확인 가능합니다.

</br>

### Data Source
그룹  | 지역 | 주소                                                               | Package    | Code
--- | -- | ---------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------
수도권 | 서울 | <https://www.seoul.go.kr/coronaV/coronaStatus.do>                | `scrapy`   | [Link](https://github.com/pyy0715/Corona19_Dashboard/blob/master/corona_crawl/corona_crawl/corona_crawl/spiders/seoul.py)
수도권 | 인천 | <https://www.incheon.go.kr/health/HE020409>                      | `scrapy`   | [Link](https://github.com/pyy0715/Corona19_Dashboard/blob/master/corona_crawl/corona_crawl/corona_crawl/spiders/incheon.py)
수도권 | 경기 | <https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page=1> | `Selenium` | [Link](https://github.com/pyy0715/Corona19_Dashboard/blob/master/corona_crawl/corona_crawl/gyeonggi.py)
행정구역 | 전국 | <http://www.gisdeveloper.co.kr/?p=2332> | - | -

</br>

### Instruction
```{bash}
git clone https://github.com/pyy0715/Corona19_Dashboard.git
cd Corona19_Dashboard/corona_crawl/corona_crawl
mkdir data
conda env create -f environment.yml
conda activate Corona19

# 서울(Seoul)
python -m scrapy crawl seoul -o data/seoul.csv -t csv

# 인천(Incheon)
python -m scrapy crawl incheon -o data/incheon.csv -t csv

# 경기(Gyeonggi)
python gyeonggi.py
```
</br>

### Exploratory Data Analysis

* **Animation Bar Plot**
 ![newplot](https://user-images.githubusercontent.com/47301926/77945194-392f9980-72fb-11ea-8a02-3a782a0b9a22.png)

* **Animiation Heat Map**
![newplot (1)](https://user-images.githubusercontent.com/47301926/80133256-ef735f80-85d7-11ea-88ad-039034536419.png)

</br>

### Note

* 사이트의 크롤링 주소가 계속 바뀌는 현상이 있어서 크롤링이 실행되지 않을 경우 `Issue`에 남겨주세요.
</br>
* 위와 마찬가지로 제공되는 데이터가 달라질 수 있습니다. 
예를들어, 4월 15일 이후부터 서울시에서는 확진자의 연령을 공개하지 않습니다.

### Reference
[Streamlit]('https://www.streamlit.io/')