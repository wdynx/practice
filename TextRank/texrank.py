# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 16:09:07 2020

@author: wyx
"""


#-*- encoding:utf-8 -*-
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import jieba

filepath='news.txt'
with open(filepath) as f:
    text=f.read() 

# 输出关键词，设置文本小写，窗口为2
tr4w=TextRank4Keyword()
tr4w.analyze(text=text,lower=True,window=2)
print('关键词：')
for item in tr4w.get_keywords(20,word_min_len=2):
    print(item.word,item.weight)


# 输出重要的句子
tr4s=TextRank4Sentence()
tr4s.analyze(text=text,lower=True,source='all_filters')
print('摘要：')
# 重要性最高的句子
for item in tr4s.get_key_sentences(num=1):
	# index是语句在文本中位置，weight表示权重
    print(item.index, item.weight, item.sentence)
