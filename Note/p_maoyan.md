抓取猫眼电影  
====

我们先看一段简单的爬虫代码:   
```Python
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'yyy',  'Cookie': 'xxx'}

for i in range(10):
	url_saves = r"https://maoyan.com/board/4?offset=" + str(i * 10)
	
	wb_data_new = requests.get(url_saves, headers=headers)
	soup = BeautifulSoup(wb_data_new.text, 'lxml')
	tops = soup.select("i.board-index")
	titles = soup.select('dl.board-wrapper > dd > a ')
	times = soup.select('p.releasetime')
	In_stars = soup.select("p.star")
	
	for top, title, time, star in zip(tops, titles, times, In_stars):
		print(  top.get_text(),
		      title.get("title"),
		       time.get_text()[5:],
		       star.get_text()[20:28])
```

很简单的规则, 通过url的变换参数, 提取不同网页的数据即可  
url变换:  
```
https://maoyan.com/board/4?offset=10
https://maoyan.com/board/4?offset=20
https://maoyan.com/board/4?offset=30
...
```

在Python3中BeautifulSoup整合到了Bs4中, 所以是:          
`from bs4 import BeautifulSoup`   

但值得注意的是, bs4以及BeatifulSoup, 美味的汤,  在我们爬虫中不常用, 常用的解析工具是xpath   

现在说下BeatufulSoup以及怎么使用, 这里节选部分关键使用部分:     

## [BeatufulSoup](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)   
Beautiful Soup是一个可以从HTML或XML文件中提取数据的Python库   
它能够通过你喜欢的转换器实现惯用的文档导航,查找,修改文档的方式   
Beautiful Soup会帮你节省数小时甚至数天的工作时间, 当然, 其他工具也可以, 只要抓取到想要的数据即可   


下面的一段HTML代码将作为例子被多次用到.这是 爱丽丝梦游仙境的 的一段内容(以后内容中简称为 爱丽丝 的文档):   

```Html
html_doc = """
<html>
<head>
	<title>The Dormouse's story</title>
</head>
<body>
	<p class="title"><b>The Dormouse's story</b></p>

	<p class="story">Once upon a time there were three little sisters; and their names were
	<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
	<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>

	<p class="story">...</p>
</body>
"""
```
使用bs4解析这段html:  
```Python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())

# <html>
#  <head>
#   <title>
#    The Dormouse's story
#   </title>
#  </head>
#  <body>
#   <p class="title">
#    <b>
#     The Dormouse's story
#    </b>
#   </p>
#   <p class="story">
#    Once upon a time there were three little sisters; and their names were
#    <a class="sister" href="http://example.com/elsie" id="link1">
#     Elsie
#    </a>
#    ,
#    <a class="sister" href="http://example.com/lacie" id="link2">
#     Lacie
#    </a>
#    and
#    <a class="sister" href="http://example.com/tillie" id="link2">
#     Tillie
#    </a>
#    ; and they lived at the bottom of a well.
#   </p>
#   <p class="story">
#    ...
#   </p>
#  </body>
```

几个简单的浏览结构化数据的方法:   
```Python
soup.title
# <title>The Dormouse's story</title>

soup.title.name
# u'title'

soup.title.string
# u'The Dormouse's story'

soup.title.parent.name
# u'head'

soup.p
# <p class="title"><b>The Dormouse's story</b></p>

soup.p['class']
# u'title'

soup.a
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

soup.find_all('a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find(id="link3")
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
```


从文档中找到所有<a>标签的链接:   
```Python
for link in soup.find_all('a'):
    print(link.get('href'))

# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie
```


从文档中获取所有文字内容:   
```Python
print(soup.get_text())

# The Dormouse's story
#
# The Dormouse's story
#
# Once upon a time there were three little sisters; and their names were
# Elsie,
# Lacie and
# Tillie;
# and they lived at the bottom of a well.
#
# ...
```
