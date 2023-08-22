""" 결과물 """
from tracemalloc import start
import pandas as pd
import os
import numpy as np
from collections import Counter
import joblib
from datetime import datetime
import matplotlib.pyplot as plt
import time
from wordcloud import WordCloud

#import warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)

base = os.path.dirname(os.path.abspath(__file__)) # 경로설정
#df = pd.read_csv(os.path.join(base,'data','news_crawl_all_tok.csv'))
df = joblib.load(os.path.join(base,'data','df'))
#print(df)

# 날짜 리스트 생성
days_list = []
for y in range(2012,2023):
    for m in range(1,13):
        if m < 10:
            m1 = '0'+str(m)
        else:
            m1 = str(m)
        days_list.append(str(y)+"."+str(m1)+".01")
days_list = days_list[:-8]

# 시각화 용 날짜 리스트
datetime_list = list(map(lambda x : x[2:7],days_list))

#print(days_list)
def freqency_list(target):
    count_list = []
    for m in days_list:
        condition = df['date'] == m
        words = np.hstack(df[condition]['tokenized'].values)
        word_count = Counter(words)
        count_list.append(word_count[target])

    plt.figure(figsize=(30,8))
    plt.bar(days_list,count_list,color='dodgerblue')
    plt.xticks(days_list,datetime_list, rotation = 45)
    plt.locator_params(axis='x', nbins=len(days_list)/6)
    #print(plt.show())
    return plt.show()#count_list

# test code
#freqency_list('베트남')


def trend_check(start_date,end_date,numbers=50): # input:('2022.01', '2022.03', 15)
    print(start_date,"~",end_date,"트렌드 추출")
    start_date = datetime.strptime(start_date,'%Y.%m')
    end_date = datetime.strptime(end_date,'%Y.%m')

    df['datetime'] = list(map(lambda x : datetime.strptime(x,'%Y.%m.%d'),df['date']))
    condition = (start_date <= df['datetime']) & (df['datetime'] <= end_date)
    words = np.hstack(df[condition]['tokenized'].values)
    word_count = Counter(words)
    mcwc = word_count.most_common(numbers)

    # 5개씩 출력
    #for i in range((numbers+4)//5):
    #    print(mcwc[i*5:(i+1)*5])

    return mcwc

# test code
#trend_check('2020.03','2020.09')

def vis_wordcloud(trend):
    font_path = "/Users/yutaejun/Library/Fonts/NanumGothic.otf"
    wordcloud = WordCloud(background_color='white',font_path = font_path,colormap='autumn',
                        width = 1000, height = 1000, random_state = 10).\
    generate_from_frequencies(dict(trend))
    plt.figure(figsize = (6,6))
    plt.imshow(wordcloud)

    plt.axis('off')

    return plt.show()

# test code
# vis_wordcloud(trend_check('2020.03','2020.09'))

""" Interface """
print("____식품산업_트렌드_키워드_추출&분석_툴_v1.0____")
while True:
    print("[서비스 목록]-----------------------------------")
    print("(1) 특정 기간의 트렌드 키워드 확인")
    print("(2) 특정 키워드의 월별 뉴스제목 등장빈도 확인")
    print("(3) 종료")

    s = input("-----------------------------------------[입력:")
    if s == str(1):
        print("[트렌드 키워드 확인]")
        s1 = input("범위 시작날짜 (YYYY.MM) 입력 :")
        s2 = input("범위 종료날짜 (YYYY.MM) 입력 :")
        #s3 = input("확인할 키워드 개수 입력 :")
        try:
            s1 = str(s1)
            s2 = str(s2)
            #s3 = int(s3)
            vis_wordcloud(trend_check(s1,s2))#,s3))
            print(" ")
            time.sleep(1)
        except:
            print("입력값이 잘못된것 같습니다.")
            print("처음으로 돌아갑니다.")
            print(" ")
        continue
    elif s == str(2):
        print("[뉴스빈도 확인]")
        s1 = input("키워드를 입력하세요 :")
        try:
            freqency_list(s1)
            print("시각화 완료.")
            print(" ")
            time.sleep(1)
        except:
            print("뭔가 잘못된것 같습니다.")
            print("다른 키워드로 검색해 보세요.")
            print("처음으로 돌아갑니다.")
            print(" ")
        continue
    elif s == str(3):
        print("_____________프로그램을 종료합니다._____________")
        time.sleep(1)
        break
    else:
        print("잘못된 값 입력 :",s)
        print(" ")
        continue
