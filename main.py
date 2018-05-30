# !/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time  : 2018/5/19
# @Author: Ctum
# @Email : shuerhy@163.com
# @File  : main
'''
the File is the main file
'''
try:
    from Crawl import Crawler
except ImportError:
    from .Crawl import Crawler

if __name__ == '__main__':
    # Notice: the params must be String
    spiderMan = Crawler('447926067')
    spiderMan.threading_save_to_csv()
