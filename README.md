# 뉴스 토픽 변화 분석과 정책 추천

2022년 1학기 연세대학교 '데이터마이닝이론및응용' (이원상 교수님) 

**참여** : 김서연, 김연재, 윤수진, 이가람

## Directory Structure
<pre>
<code>
├── Crawling
│   └── PolicyCrawling.ipynb
├── Data
│   ├── NewsData
│   ├── NewsPreprocessedData
│   ├── PolicyData
│   ├── PolicyLDA
│   └── PolicyPreprocessedData
├── LDA
│   ├── Mecab-ko-for-Google-Colab
│   ├── NewsLDA.ipynb
│   ├── NewsLDA_NonSequential
│   └──  PolicyKeywords_LDA.ipynb
├── Preprocessing
│   ├── NewsTFIDF.ipynb
│   ├── NewsTextPreprocessing.ipynb
│   └── PolicyTextPreprocessing.ipynb
├── README.md
└── RecommenderSystem
    ├── PolicyRecommenderSystem.ipynb
    └── PolicyRecommenderSystem.py
</code>
</pre>

## Abstract

>정부의 정책에 대한 정보 및 홍보 부족, 정책의 이해도 부족 등에 따라 정책 참여도에 대한 문제가 대두되고 있다. 이에 대해 여론의 관심사를 파악할 수 있고 여론의 변화를 반영할 수 있으며 개인에게 필요한 정책을 추천하여 국민들로 하여금 정책에 대한 인지적 장벽을 허물고자 하였다. 따라서 여론의 관심사를 파악할 수 있는 뉴스기사 데이터를 이용해 LDA를 진행하여 반기별 주요 토픽의 변화를 분석하였다. 또한 LDA 결과로 추출된 키워드에 대해 정책을 평가하여 어떤 정책이 어떤 분야에 대해 국민의 니즈를 반영하고 있는지 파악하였다.

>더불어 국민들이 정책에 대해 쉽게 접근할 수 있도록 관심 분야의 뉴스를 선택하면 해당 뉴스와 관련된 정책을 추천하는 시스템을 제안하여 국민들의 정책에 대한 이해도를 높였다. 이에 대해 뉴스 및 정책 데이터에 대해 TF-IDF를 진행하고 각 키워드의 유사도를 계산하여 선택한 뉴스에 대해 가장 높은 연관성을 갖는 정책이 추천될 수 있도록 하였다. 

## Research Question

1. 뉴스기사로 연도별 관심사의 변화를 파악할 수 있는가?
	- 2018 ~ 2021 뉴스 분석으로 연도별 주요토픽과 변화 파악
2. 현존하는 정책이 국민의 관심사를 잘 반영하는가?
	- 뉴스기사 토픽 분석으로 국민의 관심사 및 요구사항 파악
3. 정책에 대한 국민의 인지도를 제고할 방안이 있는가?
	- 정책 참여도 증가 방안으로써 국민의 요구사항에 맞는 정책추천 제안

## Data

1. BIGKINDS (빅카인즈) - 뉴스 데이터
수집기간: 2018.01.01 ~ 2021.12.31 (4년)

2. '이렇게 달라집니다' - 정책 데이터
수집 기간: 2018년 상반기 ~ 2021년 하반기 (4년)

## Methodology

**RQ1. 뉴스기사로 연도별 관심사의 변화를 파악할 수 있는가?**<br>
**RQ2. 현존하는 정책이 국민의 관심사를 잘 반영하는가?**

A. TF-IDF

**Application**
- 정책 데이터에 대해 TF-IDF 점수를 활용해 주요 키워드 20개씩 추출

**수행 과정**
1. TF-IDF를 활용해 추출한 반기별 정책의 주요 키워드 20개의 등장 빈도를 기반으로 개별 정책 scoring
2. 정책의 score 분포를 확인하여 	q3인 9 이상의 score를 가지는 정책만 추출하여 뉴스 LDA에서 등장한 토픽과 연관하여 분석

B. LDA(Latent Dirichlet Allocation), pyLDAvis

**Application**
- 수집한 뉴스 기사 데이터를 2018 ~ 2021년 까지 4년의 상반기, 하반기로 나누고 8기간에 대해 각 반기별 주요 토픽 추출
- 추출한 토픽에 대해 시간에 따른 주요 토픽의 변화 분석 및 반기별 뉴스 주요 토픽에 대해 대응하는 정책이 제정되었는지 분석

**수행 과정**
1. 한음절 단위의 단어는 주요 토픽에서 큰 의미를 갖지 않는 경우가 많아 삭제
2. LDA에 들어갈 corpus, dictionary 생성
3. 적절한 토픽 수를 선정하여 LDA 모델링 진행
4. LDA 결과를 pyLDAvis 라이브러리를 활용하여 시각화
5. 기준인 saliency와 discriminative power 간의 가중치 조정을 통해 키워드 추출

**RQ3. 정책에 대한 국민의 인지도를 제고할 방안이 있는가?**

A. Word2Vec

**Application**
- 정책, 뉴스기사 키워드쌍에 대한 Word2Vec 단어 유사도 도출을 통해 관계 점수 생성

B. Recommender System

**Application**
- 텍스트 데이터에서 가장 널리 사용되는 텍스트 임베딩 모델 Word2Vec로 각 단어의 임베딩 벡터 학습

**수행 과정**
1. TF-IDF를 통해 정책별, 뉴스기사별 상위 10개 주요 키워드 생성
2. 339M 크기의 wikipedia corpus로 pretrained된 Word2Vec을 직접 크롤링한 데이터셋에 fine tuning하여 최종 임베딩 벡터 생성
3. 뉴스기사 키워드 10개와 정책 키워드 10개간의 Word2Vec 유사도 평균을 뉴스기사-정책 쌍에 대해 계산하여 관계 점수 테이블 생성
4. 뉴스기사 키워드 입력시 관계점수가 높은 상위 10개의 정책을 보여주는 추천 시스템 구축

## Result

### Recommender System
![RecommenderSystem](https://user-images.githubusercontent.com/59776953/170975028-94f9e285-90f1-47da-a1ee-a59f840c4eb0.png)

### News LDA
![LDA1](https://user-images.githubusercontent.com/59776953/170975056-a792596e-ddb0-43aa-9092-70486db5082d.jpg)
![LDA2](https://user-images.githubusercontent.com/59776953/170975072-c6aa5e9b-66cf-4e48-a2a3-d9c0deb6f4d3.jpg)
![LDA3](https://user-images.githubusercontent.com/59776953/170975086-eca6b4a3-11ff-40e7-bd8b-c3f1bf77b9b2.jpg)
![LDA4](https://user-images.githubusercontent.com/59776953/170975100-553c7878-e235-4396-88c7-6f56f60cfc26.jpg)

### Policy LDA
![PolicyLDA](https://user-images.githubusercontent.com/59776953/170975163-f1aae639-7c30-4368-b88d-8aa08a831af3.jpg)
