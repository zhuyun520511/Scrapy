爬取美女网  
====
这是之前很就写的[美女网](https://www.plmm.com.cn/)小型爬虫, 现在没什么兴趣爬它了  
当然, 下面的代码也是惨不忍睹, 仅供小白学习使用, 大佬如有兴趣, 看了可以指点指点, 洗耳恭听      
```
port requests, re, random, os
from bs4 import BeautifulSoup
from multiprocessing import Pool
import urllib.request

#  获取120个门户网站
def spider_url_list():
    url = "https://www.plmm.com.cn/"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    resopnse = requests.get(url, headers=headers)
    soup = BeautifulSoup(resopnse.content.decode(), "lxml")
    # wb_title = soup.select("ul > li > div > ul > li > a > span.text")   # 找到所有副题标签
    wb_url_son = soup.find_all("a")
    url_all_list = []
    n = 0
    # 获取主页面所有url
    for item in wb_url_son:
        url = item.get('href')
        if len(str(url)) > 30 and len(str(url)) < 40:
            if "tags" in  str(url):
                pass
            else:
                url_all_list.append(url)
                n += 1
    print(n/2)
    print("获取url_son_list结束")
    data_list = url_all_list
    c = [i_url for i_url in range(0, len(data_list)) if i_url%2 != 0]
    c_url = []
    for i_c in c:
        c_url.append(data_list[i_c])
    global data_list_new
    data_list_new = c_url
    print("开始打印data_list",data_list_new)
    print("结束spider_url_list程序")


# 获取浏览网站的图片地址
# spider_img_list
def main(url):  # 传入多图窗口url就可以爬取图片了  
    print("开始执行spider_img_list函数")
    try:
        print("执行到这里------------------headers")
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        req = urllib.request.Request(url, headers=headers)
        print("执行到这里------------------x = random.randint(0,2) + random.random()")
        response = urllib.request.urlopen(req)
        Html_read = response.read().decode('utf-8')
        pat = r'data-med="(.*?)@!w960'
        re_image = re.compile(pat, re.S)
        
        url_image = re_image.findall(Html_read)
        print(len(url_image))
        print("print(len(url_image))")
        x = random.randint(0,2) + random.random()
        print("执行到这里------------------x = random.randint(0,2) + random.random()")
        
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        titles = soup.select("div > div.main > h1")
        print("开始打印:soup.select")
        for title in titles:
            title = title.get_text()
            print(title)
        
        dirName = u"{}".format(title)
        print("打印dirName",dirName)
        
        path = r"C:\big data folder\美女网爬取\%s" % dirName
        print(path)
        os.mkdir(path)
        print("os.mkdir(dirName)---------------2")
                
        n = 1
        for y in url_image:
            y_change = "https:" + y
            print("打印循环参数:", y_change)
            
            filename = '%s/%s.jpg' % (path, n)
            print(filename)
            try:
                # urllib.request.urlretrieve(y_change , r"C:\big data folder\美女网爬取\%s.jpg" % (time.time()))
                urllib.request.urlretrieve(y_change , filename)
                print("正在下载...%d" % n)
            except:
                print("下载失败")
                pass
            n += 1
    except:
        print("执行spieder_img_list函数出错，跳出")
        pass


def run():
    n = 0
    spider_url_list()    #  获取120个门户网站，data_list
    print("开始打打印图片网页url地址")
    for url in data_list_new:
        n += 1
        url = "https://" + url[2:]
        print(n,url)


if __name__ == '__main__':
    run()
    pool = Pool()
    pool.map(main, ["https://" + url[2:]for url in data_list_new])

```

