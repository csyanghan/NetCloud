# !/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time  : 2018/5/19
# @Author: Ctum
# @Email : shuerhy@163.com
# @File  : analyse
import os, requests, time, csv, re
import pandas as pd
from bs4 import BeautifulSoup
from threading import Thread
'''
analyse the raw data
'''
headers = {
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
def load_comments_csv():
    '''
    load comments csv file
    :return: pandas dataFrame
    '''
    location = os.path.join('raw_data', 'comment.csv')
    comments_df = pd.read_csv(location, encoding='utf-8',header=0)
    return comments_df

def load_user_urls():
    users_url = []
    comment_df = load_comments_csv()
    # dropna() 当一行全部为nan时丢弃
    user_id = comment_df['用户ID']

    ids = len(user_id)
    use_id = [user_id.iloc[i] for i in range(ids)]
    for item in use_id:
        users_url.append('http://music.163.com/user/home?id={user_id}'.format(user_id=item))
    return list(set(users_url))

def standard_time(timestamp):
    current_year = time.localtime().tm_year
    age = (current_year - 1970) - int(timestamp) // (1000 * 365 * 24 * 3600)
    return age

def save_useInfo_to_file():
    '''
    Get more information about commenter,including age,gender,region,song count,follwers
    :return:
    '''
    location1 = os.path.join('raw_data', 'userInfo.csv')
    with open(location1, 'a+', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['rank' ,'gender', 'age','follows' ,'region','listen_count'])
    users_url = load_user_urls()
    numa = len(users_url)
    for index, user_url in enumerate(users_url):
        try:
            html = BeautifulSoup(requests.get(user_url, headers=headers).text, 'lxml')
            follows = +int(html.find(id='follow_count').string) *2 + int(html.find(id='fan_count').string)
            # rank = html.find('div', class_='f-cb').find_all('span')[1].contents[0]
            rank = html.select('.lev.u-lev.u-icn2.u-icn2-lev')[0].contents[0].string
            gender = ''
            if html.find('div', class_='f-cb').find('i', class_='icn').get('class')[2].count('1')==1:
                gender = 'Male'
            else:
                gender = 'Female'
            age = None
            if len(html.find_all('span', class_='sep', id='age')) == 0:
                age = None
            else:
                age = html.find('span', class_='sep', id='age').get('data-age')
                age = standard_time(age)
            region = ''
            if len(html.find_all('div', class_='inf s-fc3')) != 0:
                if html.find_all('div', class_='inf s-fc3')[0].find('span'):
                    lo = html.find_all('div', class_='inf s-fc3')[0].find('span').string
                    location_pattern = re.compile('所在地区：(.+)')
                    location = re.search(location_pattern, lo)
                    if location:
                        region = location.group(1)
                    else:
                        region = ''
            num = html.find('h4').string
            pa = re.compile('(\d+)')
            nu = re.search(pa, num)
            if nu:
                listen_count = nu.group(1)
            else:
                listen_count = None
            temp=[rank, gender,age, follows, region,listen_count]
            with open(location1, 'a+', newline='',encoding='utf-8-sig') as f1:
                writer1 = csv.writer(f1)
                writer1.writerow(temp)
            print('Write{index}/{num} user Info to file!'.format(index=index, num=numa))
        except Exception as e:
            print('Fail to store NO.{index} user Info:{error}'.format(index=index, error=e))

def threading_save_to_csv(threads = 8):
    start_time = time.time()
    location1 = os.path.join('raw_data', 'userInfo.csv')
    with open(location1, 'a+', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['rank', 'gender', 'age', 'follows', 'region', 'listen_count'])
    users_url = load_user_urls()
    numa = len(users_url)
    print('There are {num} userInfo'.format(num=numa))
    threads_list = []
    per = numa // threads
    for i in range(threads):
        begin = i * per
        if i < threads-1:
            end = (i+1) * per
        else:
            end_page = numa
        t = Thread(target=thread_fun_csv, args=(begin, end))
        threads_list.append(t)
    for i in range(threads):
        threads_list[i].start()
    for i in range(threads):
        threads_list[i].join()
    end_time = time.time()
    cost  = end_time - start_time
    print('using {threads} Threads to save all userInfo, cost {cost} s'.format(threads=threads, cost=cost))

def thread_fun_csv(begin, end):
    time.sleep(1)
    users_url = load_user_urls()[begin:end]
    numa = len(load_user_urls())
    for index, user_url in enumerate(users_url):
        try:
            html = BeautifulSoup(requests.get(user_url, headers=headers).text, 'lxml')
            follows = +int(html.find(id='follow_count').string) * 2 + int(html.find(id='fan_count').string)
            # rank = html.find('div', class_='f-cb').find_all('span')[1].contents[0]
            rank = html.select('.lev.u-lev.u-icn2.u-icn2-lev')[0].contents[0].string
            gender = ''
            if html.find('div', class_='f-cb').find('i', class_='icn').get('class')[2].count('1') == 1:
                gender = 'Male'
            else:
                gender = 'Female'
            age = None
            if len(html.find_all('span', class_='sep', id='age')) == 0:
                age = None
            else:
                age = html.find('span', class_='sep', id='age').get('data-age')
                age = standard_time(age)
            region = ''
            if len(html.find_all('div', class_='inf s-fc3')) != 0:
                if html.find_all('div', class_='inf s-fc3')[0].find('span'):
                    lo = html.find_all('div', class_='inf s-fc3')[0].find('span').string
                    location_pattern = re.compile('所在地区：(.+)')
                    location = re.search(location_pattern, lo)
                    if location:
                        region = location.group(1)
                    else:
                        region = ''
            num = html.find('h4').string
            pa = re.compile('(\d+)')
            nu = re.search(pa, num)
            if nu:
                listen_count = nu.group(1)
            else:
                listen_count = None
            temp = [rank, gender, age, follows, region, listen_count]
            location1 = os.path.join('raw_data', 'userInfo.csv')
            with open(location1, 'a+', newline='', encoding='utf-8-sig') as f1:
                writer1 = csv.writer(f1)
                writer1.writerow(temp)
            print('Write{index}/{num} user Info to file!'.format(index=(index+begin), num=numa))
        except Exception as e:
            print('Fail to store NO.{index} user Info:{error}'.format(index=(begin+index), error=e))

threading_save_to_csv()