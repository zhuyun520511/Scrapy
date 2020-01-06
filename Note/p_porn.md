Porn_Hun爬虫  
====
这是很久之前自己写的Porn爬虫, 解决日常需要   
这是一段标准小型爬虫代码, 如能理解, 爬虫基础就ok了   
爬虫最关键的不是什么网页提取, 字符串处理, 也不是速度问题, 而是最要命的, 人家根本就不想让爬虫访问, 所以, 反爬虫是爬虫里面最核心的   
这都是小打小闹,  即使我把速度提高到每秒100次访问, 对这个网站来说, 它仍然是欢迎我们的  
为什么? 我们的爬虫为它们这种网站产生了流量, 流量就是money   

```Python
import requests, time, csv
from lxml import etree
from multiprocessing import Pool
from retrying import retry
start = time.time()
file_csv = open(r'G:\big data folder\9-12\pornhub-8进程.csv', 'a' ,newline="", encoding='gbk')
writer = csv.writer(file_csv)
writer.writerow(['标题','长度','观看数','好评率','链接'])
def heade(Referer):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Referer':'{}'.format(Referer)}
    return headers

@retry(stop_max_attempt_number=5, wait_fixed=60)
def get_response(input_url, Referer):
    data = (requests.get(input_url, headers=heade(Referer))).content.decode()
    response = etree.HTML(data)
    return response

global eree_list
eree_list = list()

def content_resolve(url):
    
    try:
        response = get_response(url,url)
        titles = response.xpath('//li/div/div[3]/span/a/text()')
        durations = response.xpath('//li/div/div[1]/div[2]/div/var/text()')
        viewss = response.xpath('//li/div/div/div/span/var/text()')
        percents = response.xpath('//li/div/div/div/div/div[2]/text()')
        url_links = response.xpath('//li/div/div[3]/span/a/@href')

        for title, duration, views, percent, url_link in zip(titles, durations, viewss, percents,url_links):
            new_link = 'https://www.pornhub.com' + url_link
            writer.writerow([title, duration, views, percent, new_link])
            print('--写入成功'*5)
    except:
        eree_list.append(url)
        print('提取信息错误，这个url地址是: ', url)
        
def main(num):
    origin_url = r'https://www.pornhub.com/video?page={}'.format(num)
    print('正在抓取的网页url: ',origin_url)
    content_resolve(origin_url)

if __name__ == '__main__':
    pool = Pool(8)
    pool.map(main, [num for num in range(2,2201)])
    print('结束当前页面爬取')
    
# 写入爬取错误数据，日后检测是什么原因
for i in eree_list:
    with open(r'G:\big data folder\9-12\eree.txt', 'a') as ff:
        i += '\n'
        ff.write(i)
end = time.time()
print('程序运行了%s秒' %(end-start))
```
