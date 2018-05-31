# 项目说明
这个项目是课程： 大数据从理论到实践 课程的实验代码
主要内容是对[《鼓楼》](http://music.163.com/#/song?id=447926067)评论进行分析

# 目录结构
* `raw_data` 文件夹是爬虫爬取得数据
* `result` 文件夹是实验结果
* `source` 文件夹里一些需要的资源，例如：情感词典、停用词表、程度词表、否定词表
* `Crawl.py` `paramsEncrypto.py` 加密爬取网易云评论时的参数 抓取评论数据 `crawUserInfo.py` 根据评论者ID抓取用户个人信息
* `dataClean.py` 数据清洗，主要去掉一些重复数据
* `dataAnalyse.py` `hot.py` 主要是一些可视化分析及热力图
* `sentimentAnalysis.py` 情感分析，基于情感字典

# 实验结果
* 评论者等级分布
![](https://github.com/Ctum/NetCloud/blob/master/result/Rank%E6%8E%92%E8%A1%8C%E6%A6%9C.png)
* 评论者年龄分布
![](https://github.com/Ctum/NetCloud/blob/master/result/age%E5%88%86%E5%B8%83.png)
* 评论者男女比例
![](https://github.com/Ctum/NetCloud/blob/master/result/%E7%94%B7%E5%A5%B3%E6%AF%94%E4%BE%8B.png)
* 热力图
![](https://github.com/Ctum/NetCloud/blob/master/result/%E7%83%AD%E5%8A%9B%E5%9B%BE.JPG)
* 词云
![](https://github.com/Ctum/NetCloud/blob/master/result/world_cloud.jpg)
* 1000条评论结果
由于这个花时间比较长，我做了这1000条大概跑了150s，总共大概有14000条数据
![](https://github.com/Ctum/NetCloud/blob/master/result/1000%E6%9D%A1%E8%AF%84%E8%AE%BA%E5%A5%BD%E8%AF%84%E5%B7%AE%E8%AF%84%E5%88%86%E5%B8%83.png)
