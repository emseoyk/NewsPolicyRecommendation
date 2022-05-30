import ast
import pandas as pd
from gensim.models import Word2Vec
from gensim.models.word2vec import Word2Vec

class PolicyRecommenderSystem:

  def __init__(self, model_path, policy_path, news_path):
    self.model = Word2Vec.load(model_path)
    self.policy_df = pd.read_csv(policy_path, encoding = 'utf-8')
    self.news_df = pd.read_csv(news_path, encoding = 'utf-8')

  def calculateScore(self, news_keywords, policy_keywords):
    sum_score = 0
    news_len = len(news_keywords)
    policy_len = len(policy_keywords)
    total_len = news_len * policy_len
    for news_keyword in news_keywords:
      for policy_keyword in policy_keywords:
        try:
          sum_score += self.model.wv.similarity(news_keyword, policy_keyword)
        except:
          total_len -= 1
    if total_len != 0:
      mean_score = sum_score / total_len
    else:
      mean_score = 0

    return mean_score

  
  def recommendPolicy(self, newsTitle, top_k = 10):
    news_keywords = self.news_df.loc[self.news_df['title'] == newsTitle, 'top_keywords'].item()
    news_keywords = ast.literal_eval(news_keywords)
    news_year = self.news_df.loc[self.news_df['title'] == newsTitle, 'year'].item()
    news_month = self.news_df.loc[self.news_df['title'] == newsTitle, 'month'].item()
    if news_month < 7:
      news_period = '상반기'
    else:
      news_period = '하반기'
    score_list = []
    temp_policy_df = self.policy_df.copy()
    if news_period == '하반기':
      temp_policy_df = temp_policy_df[temp_policy_df['year'] <= news_year]
    else:
      curr_policy_df = temp_policy_df[(temp_policy_df['year'] == news_year) & (temp_policy_df['period'] == '상반기')]
      prev_policy_df = temp_policy_df[temp_policy_df['year'] < news_year]
      temp_poliy_df = pd.concat([prev_policy_df, curr_policy_df])
    for i in range(len(temp_policy_df)):
      policy_keywords = temp_policy_df.loc[i, 'tf-idf']
      policy_keywords = ast.literal_eval(policy_keywords)
      score = self.calculateScore(news_keywords, policy_keywords)
      score_list.append(score)
    idx_score_list = [(i, j) for i, j in enumerate(score_list)]
    sorted_idx_score_list = sorted(idx_score_list, key = lambda x: -x[1])
    sorted_idx = [x for (x, y) in sorted_idx_score_list[:top_k]]
    top_k_policy = temp_policy_df.iloc[sorted_idx]['정책명']
    
    return top_k_policy