'''
to promote this project, we can use tensorFlow to predict the negative
or positive comment
'''
import jieba, os, time
from collections import defaultdict
import pandas as pd
from pyecharts import Pie

def cutOneWord(sentence):
    '''
    对每一句分词，然后去除停用词
    :param sentence:
    :return:
    '''
    segList = jieba.cut(sentence)
    segResult = []
    for w in segList:
        segResult.append(w)
    stopPath = os.path.join('source', 'hgdstop.txt')
    with open(stopPath, 'r', encoding='utf-8') as f:
        stopwords = f.readlines()
    newSent = []
    for word in segResult:
        if word in stopwords:
            continue
        else:
            newSent.append(word)

    return newSent


def classifyWords(wordList):
    # (1) 情感词
    scorePath = os.path.join('source','BosonNLP_sentiment_score.txt')
    with open(scorePath, 'r', encoding='utf8') as f:
        senList = f.readlines()
    senDict = defaultdict()
    for s in senList:
        try:
            senDict[s.split(' ')[0]] = s.split(' ')[1].strip('\n')
        except Exception:
            pass
    # (2) 否定词
    notPath = os.path.join('source','notDict.txt')
    with open(notPath, 'r', encoding='gbk') as f:
        notList = f.read().splitlines()
    # (3) 程度副词
    degreePath = os.path.join('source', 'degreeDict.txt')
    with open(degreePath, 'r') as f:
        degreeList = f.read().splitlines()
    degreeDict = defaultdict()
    for index , d in enumerate(degreeList):
        if index >=3 and index <=71:
            degreeDict[d] = 2
        elif index >=74 and index<=115:
            degreeDict[d] = 1.25
        elif index >=118 and index<=154:
            degreeDict[d] = 1.2
        elif index >= 157 and index<=185:
            degreeDict[d] =0.8
        elif index >= 188 and index<=199:
            degreeDict[d] = 0.5
        elif index >= 202 and index<= 231:
            degreeDict[d] = 1.5
        else:
            pass

    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()

    for index, word in enumerate(wordList):
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[index] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[index] = -1
        elif word in degreeDict.keys():
            degreeWord[index] = degreeDict[word]
    return senWord, notWord, degreeWord


def scoreSent(senWord, notWord, degreeWord, segResult):
    W = 1
    score = 0
    # 存所有情感词的位置的列表
    senLoc = list(senWord.keys())
    notLoc = list(notWord.keys())
    degreeLoc = list(degreeWord.keys())
    senloc = -1
    # notloc = -1
    # degreeloc = -1

    # 遍历句中所有单词segResult，i为单词绝对位置
    for i in range(0, len(segResult)):
        # 如果该词为情感词
        if i in senLoc:
            # loc为情感词位置列表的序号
            senloc += 1
            # 直接添加该情感词分数
            score += W * float(senWord[i])
            # print "score = %f" % score
            if senloc < len(senLoc) - 1:
                # 判断该情感词与下一情感词之间是否有否定词或程度副词
                # j为绝对位置
                for j in range(senLoc[senloc], senLoc[senloc + 1]):
                    # 如果有否定词
                    if j in notLoc:
                        W *= -1
                    # 如果有程度副词
                    elif j in degreeLoc:
                        W *= float(degreeWord[j])
        # i定位至下一个情感词
        if senloc < len(senLoc) - 1:
            i = senLoc[senloc + 1]
    return score

def test():
    word = '特爱这首歌'
    word = cutOneWord(word)
    senWord, notWord, degreeWord = classifyWords(word)
    print('分词后结果',word)
    print('情感词：',senWord)
    print('否定词：',notWord)
    print('程度词：',degreeWord)
    score = scoreSent(senWord, notWord, degreeWord, word)
    print(score)


def analysic(s):
    # word = '特别喜欢这首歌'
    word = cutOneWord(s)
    senWord, notWord, degreeWord = classifyWords(word)
    score = scoreSent(senWord, notWord, degreeWord, word)
    return score

def dealAll():
    comment_path = os.path.join('raw_data', 'cleanComment-utf-8.csv')
    classify_path = os.path.join('result', 'commentClassify1000.csv')
    comment_df = pd.read_csv(comment_path, encoding='utf-8', engine='python')
    comment = comment_df['评论内容']
    coms = []
    start_time = time.time()
    for i in range(0, 1000):
        if comment[i]:
            score = analysic(comment[i])
            if score >= 0:
                com = '好评'
            else:
                com = '差评'
            coms.append(com)
    classify = pd.Series(coms)
    comment_df['classify'] = classify
    comment_df.to_csv(classify_path, encoding='utf-8', index=0)
    stop_time = time.time()
    cost = stop_time - start_time
    print('共耗时：', cost)

def visualize():
    classify_path = os.path.join('result', 'commentClassify1000.csv')
    comment_df = pd.read_csv(classify_path, encoding='utf-8', engine='python')
    comment_df = comment_df.groupby('classify')
    attr = ['好评', '差评']
    comment_df = comment_df.size().values
    pie = Pie('1000条评论好评差评分布')
    pie.add('gender', attr, comment_df, is_label_show=True)
    pie.render()

test()