妹子网爬虫  
=====

这个也是很久之前晚上流传的妹子图片爬虫,  很厉害的人写的, 从代码质量就可看出  
以及对反爬虫的研究  

这段代码, 它设置了referer, 如果在下去图片的时候不带这个东西, 即使浏览器下载也没法成功    

使用了etree xpath解析html解析数据,  在爬虫中, xpath比re好用多得多, 比美味的汤也用的多得多   
顺带一提, 在谷歌浏览器中, 有专门针对xpath的小工具, 可以直接在小工具内写xpath语法验证, 很方便      
```Python
# coding:utf-8
import requests, os
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool

def header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers

# 获取主页列表
def getPage(pageNum):
    baseUrl = 'http://www.mzitu.com/page/{}'.format(pageNum)
    selector = html.fromstring(requests.get(baseUrl).content)
    urls = []
    for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):
        urls.append(i)
        print(i)
    return urls


# 图片链接列表， 标题
# url是详情页链接
def getPiclink(url):
    sel = html.fromstring(requests.get(url).content)
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    title = sel.xpath('//h2[@class="main-title"]/text()')[0]
    dirName = u"【{}P】{}".format(total, title)
    os.mkdir(dirName)

    n = 1
    for i in range(int(total)):
        # 每一页
        try:
            link = '{}/{}'.format(url, i+1)
            s = html.fromstring(requests.get(link).content)
            # 图片地址在src标签中
            jpgLink = s.xpath('//div[@class="main-image"]/p/a/1、计算机/@src')[0]
            # print(jpgLink)
            # 文件写入的名称：当前路径／文件夹／文件名
            filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), dirName, n)
            print(u'开始下载图片:%s 第%s张' % (dirName, n))
            with open(filename, "wb+") as jpg:
                jpg.write(requests.get(jpgLink, headers=header(jpgLink)).content)
            n += 1
        except:
            pass


if __name__ == '__main__':
    pageNum = input(u'请输入页码：')
    p = getPage(pageNum)
    with ThreadPool(4) as pool:
        pool.map(getPiclink, p)

```

