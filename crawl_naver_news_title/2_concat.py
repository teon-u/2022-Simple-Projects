""" 두 CSV 파일 합치기 """
# 한번에 크롤링하지 뭣하러 ?? -> 두개 PC에서 따로 크롤링해서 이어붙이는게 소요시간 50% 감축
# + 한번에 두 단어를 검색했을 때 정보의 편향 발생
import pandas as pd
import os
base = os.path.dirname(os.path.abspath(__file__)) # 경로설정
df1 = pd.read_csv(os.path.join(base,'data','news_crawl_food.csv'))
df2 = pd.read_csv(os.path.join(base,'data','news_crawl_sikp.csv'))
df = pd.concat([df1,df2])
df = df.sort_values('date')
df = df.reset_index(drop=True)
df = df[['date','title']]
#print(df)
df.to_csv(os.path.join(base,'data','news_crawl_all.csv'))