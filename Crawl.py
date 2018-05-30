# !/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time  : 2018/5/19
# @Author: Ctum
# @Email : shuerhy@163.com
# @File  : Crawl
'''
@description:
The file is used to crawl the comemnts of netCloud and store they
in Maysql and CSV
@reference:@Lyrichu(https://github.com/Lyrichu/NetCloud)
'''
import requests
import json
from threading import Thread
import os, time, csv
try:
    from paramsEncrypto import crypto, format_time
except ImportError:
    from .paramsEncrypto import crypto, format_time


class Crawler(object):
    '''
    the main
    '''
    def __init__(self, song_id):
        self.song_id = song_id
        self.root_dir = 'raw_data'
        if not os.path.exists(self.root_dir):
            os.mkdir(self.root_dir)
        self.comment_file_path = os.path.join(self.root_dir, 'comment.txt')
        self.comment_csv_path = os.path.join(self.root_dir, 'comment-utf-8.csv')
        self.user_info = os.path.join(self.root_dir, 'userIfo.csv')
        self.headers = {
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }
    def get_dict(self, offset):
        url, data = crypto(self.song_id, offset)
        response = requests.post(url, headers=self.headers, data=data)
        res = response.content
        res = res.decode('utf-8')
        response_dict = json.loads(res)
        return response_dict

    def get_all_comments(self):
        all_comments_list = []
        all_comments_list.append('用户ID,评论时间,点赞总数,评论内容\n')
        response_dict = self.get_dict(0)
        total_comment = int(response_dict['total'])
        if total_comment % 20 ==0:
            pages = total_comment // 20
        else:
            pages = int(total_comment / 20) + 1
        print('There are %d pages of comments' % pages)
        for i in range(1):
            res = self.get_dict(i)
            if i == 0:
                print('There ara %d comments' % res['total'])
            try:
                for item in res['comments']:
                    comment = item['content']
                    comment = comment.replace(',', '')
                    comment = comment.replace('\n', '')
                    likedCount = item['likedCount']
                    ftime = item['time']
                    comment_time = format_time(ftime)
                    userID = item['user']['userId']
                    total_info = '{userID},{comment_time},{likedCount},{comment}+"\n"'.format(
                        userID = userID, comment_time=comment_time, likedCount=likedCount,
                        comment=comment
                    )
                    all_comments_list.append(total_info)
            except Exception as e:
                print('Fail to get Page{id}'.format(id = i))
                print(e)
            else:
                print('Successful to get page{page}'.format(page= i))
        return all_comments_list

    def threading_save_to_file(self, threads = 8):
        start_time = time.time()
        all_comments_list = []
        all_comments_list.append('用户ID,评论时间,点赞总数,评论内容\n')
        with open(self.comment_file_path, 'a+', encoding='utf-8') as f:
            f.writelines(all_comments_list)
        response_dict = self.get_dict(0)
        total_comment = int(response_dict['total'])
        if total_comment % 20 == 0:
            pages = total_comment // 20
        else:
            pages = int(total_comment / 20) + 1
        print('There are %d pages of comments' % pages)
        threads_list = []
        per = pages // threads
        for i in range(threads):
            begin_page = i * per
            if i < threads-1:
                end_page = (i+1) * per
            else:
                end_page = pages
            t = Thread(target=self.thread_fun, args=(begin_page, end_page))
            threads_list.append(t)
        for i in range(threads):
            threads_list[i].start()
        for i in range(threads):
            threads_list[i].join()
        end_time = time.time()
        cost  = end_time - start_time
        print('using {threads} Threads to save all comments, cost {cost} s'.format(threads=threads, cost=cost))

    def thread_fun(self,begin_page, end_page):
        all_comments_list = []
        for i in range(begin_page, end_page):
            time.sleep(1)
            res = self.get_dict(i)
            if i == 0:
                print('There ara %d comments' % res['total'])
            try:
                for item in res['comments']:
                    comment = item['content']
                    comment = comment.replace(',', '')
                    comment = comment.replace('\n', '')
                    likedCount = item['likedCount']
                    ftime = item['time']
                    comment_time = format_time(ftime)
                    userID = item['user']['userId']
                    total_info = '{userID},{comment_time},{likedCount},{comment}+"\n"'.format(
                        userID = userID, comment_time=comment_time, likedCount=likedCount,
                        comment=comment
                    )
                    all_comments_list.append(total_info)
            except Exception as e:
                print('Fail to get Page{id}'.format(id = i))
                print(e)
            else:
                print('Successful to get page{page}'.format(page= i))
            with open(self.comment_file_path, 'a+', encoding='utf-8') as f:
                f.writelines(all_comments_list)
            all_comments_list.clear()
        print('page from {begin} to {end} hava been store!'.format(begin=begin_page, end=end_page))

    def threading_save_to_csv(self, threads = 8):
        start_time = time.time()
        header = ['用户ID','评论时间','点赞总数','评论内容']
        with open(self.comment_csv_path, 'a+', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        response_dict = self.get_dict(0)
        total_comment = int(response_dict['total'])
        if total_comment % 20 == 0:
            pages = total_comment // 20
        else:
            pages = int(total_comment / 20) + 1
        print('There are %d pages of comments' % pages)
        threads_list = []
        per = pages // threads
        for i in range(threads):
            begin_page = i * per
            if i < threads-1:
                end_page = (i+1) * per
            else:
                end_page = pages
            t = Thread(target=self.thread_fun_csv, args=(begin_page, end_page))
            threads_list.append(t)
        for i in range(threads):
            threads_list[i].start()
        for i in range(threads):
            threads_list[i].join()
        end_time = time.time()
        cost  = end_time - start_time
        print('using {threads} Threads to save all comments, cost {cost} s'.format(threads=threads, cost=cost))

    def thread_fun_csv(self,begin_page, end_page):
        all_comments_list = []
        for i in range(begin_page, end_page):
            time.sleep(1)
            res = self.get_dict(i)
            if i == 0:
                print('There ara %d comments' % res['total'])
            try:
                for item in res['comments']:
                    comment = item['content']
                    comment = comment.replace(',', '')
                    comment = comment.replace('\n', '')
                    likedCount = item['likedCount']
                    ftime = item['time']
                    comment_time = format_time(ftime)
                    userID = item['user']['userId']
                    total_Info = [userID, comment_time, likedCount, comment]
                    all_comments_list.append(total_Info)
            except Exception as e:
                print('Fail to get Page{id}'.format(id = i))
                print(e)
            else:
                print('Successful to get page{page}'.format(page= i))
            with open(self.comment_csv_path, 'a+', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(all_comments_list)
            all_comments_list.clear()
        print('page from {begin} to {end} hava been store!'.format(begin=begin_page, end=end_page))


    def save_to_file(self, comments):
        '''
        save into txt file
        :return:
        '''
        with open(self.comment_file_path, 'w', encoding='utf-8') as f:
            f.writelines(comments)
        print('Write to file {filename} successfully!'.format(filename=self.comment_file_path))
