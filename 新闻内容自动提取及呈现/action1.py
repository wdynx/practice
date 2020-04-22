# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 18:21:53 2020

@author: wyx
"""


import requests
from bs4 import BeautifulSoup
import jieba
import jieba.posseg as pseg
import re

# 1） 抓取正文内容，对非中文内容进行清洗

url='https://3w.huanqiu.com/a/c36dc8/3xqGPRBcUE6?agt=8'
html=requests.get(url,timeout=10)
# print(html.content)

soup=BeautifulSoup(html.content,'html.parser',from_encoding='utf-8')
text=soup.get_text()
# print(text)

words=pseg.lcut(text)
# print(words)

news_person={word for word,flag in words if flag=='nr'}
news_place={word for word,flag in words if flag=='ns'}
news_verb={word for word,flag in words if flag=='v'}
# print('人物：',news_person)
# print('动词：',news_verb)
# print('地点：',news_place)

pattern=re.compile('[^\u4e00-\u9fa5 ，。：；‘’“”！、]')
newText=re.sub(pattern,'',text).split()
newText={sentence for sentence in newText if len(sentence)>10}
newText='。'.join(newText)
# print(newText)

# 2）文章关键词
from textrank4zh import TextRank4Keyword, TextRank4Sentence
# 输出关键词，设置文本小写，窗口为2
tr4w = TextRank4Keyword()
tr4w.analyze(text=newText, window=3)
print('关键词：')
for item in tr4w.get_keywords(20,word_min_len=2):
    print(item.word, item.weight)

# 3）文章摘要，即关键句
# 输出重要的句子
tr4s = TextRank4Sentence()
tr4s.analyze(text=newText,source = 'all_filters')
print('摘要：')
# 重要性较高的三个句子
for item in tr4s.get_key_sentences(num=3):
	# index是语句在文本中位置，weight表示权重
    print(item.index, item.weight, item.sentence)
    
# 4）词云可视化
from wordcloud import WordCloud,STOPWORDS
def create_word_cloud(f):
	cut_text = jieba.cut(f)
	cut_text = " ".join(cut_text)
	wc = WordCloud(
		max_words=100,
		width=2000,
		height=1200,
        stopwords=STOPWORDS,
        font_path="C:/WINDOWS/Fonts/MSYH.TTC",
    )
	wordcloud = wc.generate(cut_text)
	wordcloud.to_file("wordcloud.jpg")
create_word_cloud(newText)
