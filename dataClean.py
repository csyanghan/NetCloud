'''
简单去重,不知道为什么返回的数据很多重复的
'''
import csv,os
import pandas as pd

def clean_comment():
    path = os.path.join('raw_data', 'comment-utf-8.csv')
    comment = pd.read_csv(path, encoding='utf-8')
    comment = comment.drop_duplicates(['用户ID'])
    store_path = os.path.join('raw_data', 'cleanComment-utf-8.csv')
    comment.to_csv(store_path, encoding='utf-8', index=0)

clean_comment()