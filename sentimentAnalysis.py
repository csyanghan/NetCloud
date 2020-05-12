'''
to promote this project, we can use tensorFlow to predict the negative
or positive comment
'''
import jieba, os, time
from collections import defaultdict
import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts

class SentimentAnalysis:
  def __init__(self):
    # 哈工大停用词
    stopword_path = os.path.join('source', 'hgdstop.txt')
    with open(stopword_path, 'r', encoding='utf-8') as fp:
      self.stopwords = fp.readlines()
    
    # 波森情感词典
    score_path = os.path.join('source','BosonNLP_sentiment_score.txt')
    with open(score_path, 'r', encoding='utf8') as f:
      sen_list = f.readlines()
    self.sen_dict = dict()
    for s in sen_list:
      try:
        self.sen_dict[s.split(' ')[0]] = float(s.split(' ')[1].strip('\n'))
      except Exception:
        pass
    
    # 否定词  
    not_path = os.path.join('source','not_dict.txt')
    with open(not_path, 'r', encoding='utf8') as fp:
      not_list = fp.readlines()
    def filter_fun(word):
      split_word = word.split('\t')
      if (float(split_word[1]) == 0): return split_word[0]
    self.not_list = filter(filter_fun, not_list)

    # 程度副词
    degree_path = os.path.join('source', 'degreeDict.txt')
    with open(degree_path, 'r') as fp:
        degreeList = fp.read().splitlines()
    self.degree_dict = dict()
    for index , d in enumerate(degreeList):
        if index >=3 and index <=71:
            self.degree_dict[d] = 2
        elif index >=74 and index<=115:
            self.degree_dict[d] = 1.25
        elif index >=118 and index<=154:
            self.degree_dict[d] = 1.2
        elif index >= 157 and index<=185:
            self.degree_dict[d] =0.8
        elif index >= 188 and index<=199:
            self.degree_dict[d] = 0.5
        elif index >= 202 and index<= 231:
            self.degree_dict[d] = 1.5
        else:
            pass
    
  def cutword(self, word):
    # 分词后去除停用词
    segList = jieba.cut(word)
    return filter(lambda word: word not in self.stopwords, segList)
  
  def _classify_word(self, raw_word):
    word_list = self.cutword(raw_word)
    labeled_list = list()
    for index, word in enumerate(word_list):
        if word in self.sen_dict and word not in self.not_list and word not in self.degree_dict:
            labeled_list.append((index, 'sen', word, self.sen_dict[word]))
        elif word in self.not_list and word not in self.degree_dict:
            labeled_list.append((index, 'not', word, -1))
        elif word in self.degree_dict:
            labeled_list.append((index, 'deg', word, self.degree_dict[word]))
    return labeled_list
  
  def score(self, word):
    labeled_list = self._classify_word(word)
    score = 0
    weight = 1
    for w in labeled_list:
      if w[1] == 'sen':
        score += weight * w[3]
        weight = 1
      else:
        weight *= w[3]
    return score

def analysic():
  start_time = time.time()
  sa = SentimentAnalysis()
  result_path = os.path.join('result', 'commentWithClassify.csv')
  comment_path = os.path.join('raw_data', 'cleanComment-utf-8.csv')
  comment_df = pd.read_csv(comment_path, encoding='utf-8', engine='python')
  comment_df['score'] = None
  for index, comment in comment_df.iterrows():
    comment_word = comment['评论内容']
    if not comment_word:
      continue
    if sa.score(comment_word) >= 0:
      comment_df.loc[index, 'score'] = 'positive'
    else:
      comment_df.loc[index, 'score'] = 'negtive'
  comment_df.to_csv(result_path, encoding='utf-8', index=0)
  stop_time = time.time()
  print('共耗时：', stop_time - start_time)

def visualize():
  result_path = os.path.join('result', 'commentWithClassify.csv')
  comment_df = pd.read_csv(result_path, encoding='utf-8', engine='python')
  comment_df = comment_df.groupby('score')
  attr = ['负向','正向']
  comment_df = comment_df.size().values
  attr_value = [list(z) for z in zip(attr, list(comment_df))]
  print(attr_value, 'attr_value')
  render_path = os.path.join('result', 'pie_negtive_positive.html')
  (
    Pie()
    .add('', [['负向', 4361], ['正向', 9643]])
    .set_colors(["blue", "red"])
    .set_global_opts(title_opts=opts.TitleOpts(title="评论正向负向分布"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render(render_path)
  )

if __name__ == '__main__':
  visualize()
