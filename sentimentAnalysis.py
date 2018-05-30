'''
to promote this project, we can use tensorFlow to predict the negative
or positive comment
'''
import jieba, os
from collections import defaultdict

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


def classifyWords(wordDict):
    # (1) 情感词
    scorePath = os.path.join('source','BosonNLP_sentiment_score.txt')
    with open(scorePath, 'r') as f:
        senList = f.readlines()
    senDict = defaultdict()
    for s in senList:
        senDict[s.split(' ')[0]] = s.split(' ')[1]
    # (2) 否定词
    notPath = os.path.join('source','notDict.txt')
    with open(notPath, 'r') as f:
        notList = f.readlines()
    # (3) 程度副词
    degreePath = os.path.join('source', 'degreeDict.txt')
    with open(notPath, 'r', ) as f:
        degreeList = f.readlines()
    degreeDict = defaultdict()
    for d in degreeList:
        degreeDict[d.split(',')[0]] = d.split(',')[1]

    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()

    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    return senWord, notWord, degreeWord


def scoreSent(senWord, notWord, degreeWord, segResult):
    W = 1
    score = 0
    # 存所有情感词的位置的列表
    senLoc = senWord.keys()
    notLoc = notWord.keys()
    degreeLoc = degreeWord.keys()
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

def analysic():
    word = '这首歌很好听'
    word = cutOneWord(word)
    print(word)

analysic()