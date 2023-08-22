# 뉴스 크롤링 & 식품산업 트렌딩 키워드 추출


| 뉴스 기사나 공공 데이터를 활용, 식품 산업의 트렌드 키워드를 뽑는 알고리즘 및 결과


## IDEA
- '트렌드 키워드' 란?
    - 단순히 많이 언급된 단어가 '트렌드 키워드' 인가?
    - BoW(Bag Of Words) 활용해 빈도수 검증하면 추출할 수 있을지도?
- 어떤 BI 를 도출?
    - 단순 추출에서 끝나지 않고, 월별 변화 추이를 시각화
    - 시각화를 연장, ARIMA 모델로 단순하게라도 미래의 키워드 빈도수 예측



## DATA
- 네이버 뉴스 크롤링
    - data/news_crawl_food.csv : '푸드' 검색어로 10년치 뉴스제목 검색 (월별 1000건, 123,999 row / [date, title])
    - data/news_crawl_sikp.csv : '식품' 검색어로 10년치 뉴스제목 검색 (월별 1000건, 123,999 row / [date, title])
    - data/news_crawl_all.csv : 위 두 데이터 합친것 (247,999 row / [date, title])
    - data/news_crawl_all_tok.csv : 중복되는 제목을 제거한것 (187,735 row / [date, title, text, tokenized])



## HOW
- 데이터 수집 방법 : BS4를 활용한 정적 크롤링. selenium 동적 크롤링은 네이버뉴스 양식에 맞는 기사(링크)도 가져올 수 있지만 느려서 정적 크롤링으로 정함
- 한국어 형태소 분석 : mecab (연산속도 빠름 & 성능 준수)
- Stopwords 제외 : 트렌드를 나타내지 않는 단어 (사업, 정부, 지역, 업체명 등) 제외
- 결과물 도출 : 예시 키워드를 보여주고, 키워드를 검색 시 월별 해당 키워드의 뉴스등장 빈도를 시각화 하는 간단한 인터페이스 생성
- 추후 진행 1 : 빈도 데이터를 토대로 이동평균선 생성한 뒤 ARIMA 모델 적용, 미래 유망 키워드 추출
- 추후 진행 2 : 인터페이스 수정, 웹 서비스화



## CODE
- crawl.py : 네이버 뉴스 제목 크롤링
- concat.py : 크롤링한 두 csv 파일 합침
- analyze.py : 형태소분석, stopword 소거를 통한 키워드 추출
- output.py : 결과출력 (시각화, 텍스트))



## REQUIREMENTS
- Pandas
    - pip install pandas
- Bs4 (BeautifulSoup4)
    - pip install beautifulsoup4
- Mecab
    - pip install python-mecab-ko
- joblib
    - pip install joblib