#导入requests库，该库是第三方库，需要自行下载
import requests
#导入jieba库，该库是第三方库，需要自行下载
import jieba
#导入pandas库，该库是第三方库，需要自行下载
import pandas as pd
#导入re库
import re
#导入imageio库的imread模块
from imageio import imread
#从wordcloud库导入WordCloud和ImageGenerator，该库是第三方库，需要自行下载
from wordcloud import WordCloud, ImageColorGenerator

#定义url，limit表示每次取的数量，offset表示从第几个开始取，“26620756”是歌曲id，可根据需求替换
url = 'https://music.163.com/api/v1/resource/comments/R_SO_4_26620756?limit=100&offset={}'

#定义headers防反爬措施
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }

#定义词云的字体，制作中文词云图时必须选择中文的字体
font = r'C:\Windows\Fonts\simsun.ttc'

#定义列表来存放评论数据
comments = []

#通过循环获取数据，1000是获取的总数量，调整该数字可改变获取的数量
for i in range(0, 1000, 100): 
    res = requests.get(url.format(i), headers=headers).json()
    for comment in res.get('comments'):
        comments.append(comment.get('content'))

#清除表情文字
comments = [re.sub('(\[.*?\])', '', comment) for comment in comments]

#使用jieba库切分评论获取长度大于1的词语
cut = [w for comment in comments for w in jieba.cut(comment) if len(w) > 1]

#将切分好的词语转化为Series对象
ser = pd.Series(cut)

#使用value_counts()获取统计数据再用to_dict()转化为字典
res_dic = ser.value_counts().to_dict()

#打开图片文件作为模板，可自行修改需要的文件
mask = imread(r'C:\Users\MyPC\Desktop\heart.jfif', pilmode='RGB')

###定义生成词云的函数
def word_cloud():
    #用图片生成ImageColorGenerator对象
    image_colors = ImageColorGenerator(mask)

    #创建一个词云对象并调用generate_from_frequencies()后赋值给wc
    wc = WordCloud(font_path=font, height=912, width=912, mask=mask, max_words=300, max_font_size=200, color_func=image_colors).generate_from_frequencies(res_dic)

    #将词云转化为图片然后保存
    wc.to_image().save('heart.png')

#调用生成词云的函数
word_cloud()
