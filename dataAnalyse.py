# -*- coding: utf-8 -*-
import os, jieba,re, sys
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from PIL import Image
from pyecharts import Bar, Pie, Line, Geo

def cla(n, lim):
    return '[%.f,%.f)'%(lim*(n//lim),lim*(n//lim)+lim)

def mapclassify(s):
    pattern = '-\s(.*)市'
    pattern1 = '(.*)市'
    pattern2 = '-\s(.*)州'
    city = re.search(pattern, s)
    if city:
        return city.group(1)
    else:
        city = re.search(pattern1, s)
        if city:
            return city.group(1)
        else:
            city = re.search(pattern1, s)
            if city:
                return city.group(1)
            else:
                return ''
class Analyse(object):
    def __init__(self):
        pass

    def draw_cloud(self):
        abs_path = os.path.split(os.path.realpath(__file__))[0]
        mask_path = os.path.join('source', 'mask.jpg')
        save_path = os.path.join('result', 'world_cloud.jpg')
        comment_path = os.path.join('raw_data', 'cleanComment.csv')
        comment_df = pd.read_csv(comment_path,engine='python',
                                 encoding='utf-8-sig')['评论内容']
        comment_text = ''
        for i in range(len(comment_df)):
            comment_text += str(comment_df.iloc[i])
        cut_text = ' '.join(jieba.cut(comment_text))
        color_mask = np.array(Image.open(mask_path))
        cloud = WordCloud(font_path='C:\Windows\Fonts\msyhbd.ttc',
        background_color='white',
        mask=color_mask,max_words=200,max_font_size=500)
        word_cloud = cloud.generate(cut_text)
        word_cloud.to_file(save_path)

    def load_comment_csv(self):
        comment_path = os.path.join('raw_data', 'cleanComment.csv')
        comment_df = pd.read_csv(comment_path, encoding='utf-8-sig')
        return comment_dfm

    def load_userInfo_csv(self):
        userInfo_path = os.path.join('raw_data', 'userInfo.csv')
        userInfo_df = pd.read_csv(userInfo_path, encoding='utf-8-sig')
        return userInfo_df

    def generate_all_chart(self):
        '''
        this function will generate all the chart including 'age distribution'
        'region distribution', 'like count distribution', 'the relation between like count
        and time', 'comment length', 'commentator listening song count distribution'
        'commentator sex proporation','rank distribution'
        :return: None
        '''
        userInfo = self.load_userInfo_csv()
        # age distribution
        userInfo_age = userInfo['age']
        userInfo_age = userInfo_age.dropna(axis=0, how='any')
        print(userInfo_age)

    def rank(self):
        attr = [i for i in range(1,12)]
        user_rank = self.load_userInfo_csv().groupby('rank')
        user_rank = user_rank.size().values
        print(len(user_rank))
        bar = Bar('Rank排行榜')
        bar.add('Rank',attr, user_rank,is_stack=True)
        bar.render()

    def gender(self):
        user_gender = self.load_userInfo_csv().groupby('gender')
        attr = ['女', '男']
        user_gender = user_gender.size().values
        pie = Pie('男女比例')
        pie.add('gender', attr, user_gender, is_label_show=True)
        pie.render()

    def age(self):
        user_age = self.load_userInfo_csv().dropna(subset=['age'])
        user_age = user_age[user_age['age'] <60]
        user_age = user_age[user_age['age'] > 12]
        user_age = user_age.sort_values(by='age')
        classify = pd.Series([cla(g, 3) for g in user_age.age])
        user_age['classify'] = classify
        user_age = user_age.groupby(classify).size()
        bar = Bar('age分布')
        attr = ['{fir}-{sec}'.format(fir = f, sec =f+3) for f in range(12,60,3)]
        attr.remove('54-57')
        bar.add('age', attr, user_age.values, is_stack=True)
        bar.render()

    def listen_count(self):
        user_listen = self.load_userInfo_csv().dropna()
        user_listen[['listen_count']] = user_listen[['listen_count']].astype(int)
        user_listen = user_listen.sort_values('listen_count')
        user_listen = user_listen[user_listen > 5]
        classify = pd.Series([cla(l, 500) for l in user_listen.listen_count])
        user_listen['classify'] = classify
        user_listen = user_listen.groupby('classify').size()
        attr = user_listen.index.values
        bar = Bar('听歌分钟数')
        bar.add('lsiten_count',attr, user_listen.values)
        bar.render()

    # def map(self):
    #     user_region = self.load_userInfo_csv().dropna(subset=['region'])
    #     classify = pd.Series([mapclassify(s) for s in user_region.region])
    #     user_region['classify'] = classify
    #     user_region = user_region.groupby('classify').size()
    #     array = user_region.index.values
    #     array2 = user_region.values
    #     data = []
    #     for i in range(1,295):
    #         item = (array[i], array2[i])
    #         data.append(item)
    #     geo = Geo("评论者分布", "commentor", title_color="#fff",
    #               title_pos="center", width=1200,
    #               height=600, background_color='#404a59')
    #     attr, value = geo.cast(data)
    #     geo.add("", attr, value, type="heatmap", is_visualmap=True, visual_range=[0, 300],
    #             visual_text_color='#fff')
    #     geo.render()
a =Analyse()
a.listen_count()