""" 뉴스 크롤링 코드 """
# 라이브러리 호출
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import time

# 날짜 리스트 생성
days_list = []
for y in range(2012,2023):
    for m in range(1,13):
        if m < 10:
            m1 = '0'+str(m)
        else:
            m1 = str(m)
        days_list.append(str(y)+"."+str(m1)+".01")
days_list = days_list[:-7]

# 전역변수 선언
target = '북한' # 검색어


page_number = list(map(lambda x : str(x),range(1,100)))
page_number.insert(0,"") # 페이지는 첫 페이지부터 최대 100페이지까지 크롤링
base = os.path.dirname(os.path.abspath(__file__)) # 경로설정
start = time.time()
print("크롤링 시작\n . . . . .")  

# 테스트용 간소화 코드 (실제 실행시에는 삭제)
#     page_number = [1,2]

# 네이버 뉴스검색 URL ( 검색어, 오래된순, 해당기간, 지면기사) -> 연관성으로 검색하는게 더 정제된 데이터 획득 -> 연관성 검색은 

url_search = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=0&photo=0&field=0&pd=3&ds={}&de={}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{}to{},a:all&start={}1"

# 100페이지 제목,주소 크롤링
news_title = []
#news_link = []
news_date = []
for d in range(len(days_list)):
    try:
        print(days_list[d],"~",days_list[d+1],"크롤링 시작 . . .")
        for i in page_number:
            print(i,"/100 page reading . . .")
            date_range = [days_list[d], days_list[d+1]] # 검색범위, 추후 아랫단 함수화해서 월단위 데이터로 추출
            date_number = [date_range[0].replace(".",""),date_range[1].replace(".","")]
            try:
                url = url_search.format(target, date_range[0], date_range[1], date_number[0], date_number[1], i)

                html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0.48496.75"})
                soup = BeautifulSoup(html.text, "html.parser")

                news_titles = soup.select("div.group_news > ul.list_news > li div.news_area > a")
                for l in news_titles:
                    news_title.append(l.text)
                    #news_link.append(l.attrs['href']) # 뉴스링크 따로 필요하지 않아서 제거
                    news_date.append(days_list[d])
            except:
                break # 페이지가 더 없으면 or 강제종료시 반복문 종료
    except:
        break # dayslist[d+1]이 없으면 오류처리 및 반복문 종료

# 크롤링 데이터를 데이터프레임으로 저장
df = pd.DataFrame({'date':news_date,
                'title':news_title})

# 데이터프레임을 CSV 파일으로 저장
df.to_csv(os.path.join(base,'data','news_crawl.csv'))

# 소요시간
print("크롤링 종료 \nTimeSpent :", round(time.time() - start,2),"sec\n",len(df),"row stored in data/news_crawl.csv")
