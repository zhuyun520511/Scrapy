import requests, time, csv
from lxml import etree
from multiprocessing import Pool
from retrying import retry

start = time.time()
file_csv = open(r'G:\big data folder\9-12\4_process.csv', 'a' ,newline="", encoding='gbk')
# 设置CSV
writer = csv.writer(file_csv)
writer.writerow(['title','length','Views','Star','Url'])

# 请求头函数，可根据网站反爬情况，选择性加入其它信息
def heade(Referer):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Referer':'{}'.format(Referer)}
    return headers
    
# 修饰函数
@retry(stop_max_attempt_number=5, wait_fixed=60)
def get_response(input_url, Referer):  # 请求，返回相应结果
    data = (requests.get(input_url, headers=heade(Referer))).content.decode()
    response = etree.HTML(data)
    return response

# 解析响应函数
def content_resolve(url):
   # 一般情况下，编码最容易错， 例如"• "这类符号，或是其他特殊符号
    try:
        response = get_response(url,url)
        titles = response.xpath('//li/div/div[3]/span/a/text()')
        durations = response.xpath('//li/div/div[1]/div[2]/div/var/text()')
        viewss = response.xpath('//li/div/div/div/span/var/text()')
        percents = response.xpath('//li/div/div/div/div/div[2]/text()')
        url_links = response.xpath('//li/div/div[3]/span/a/@href')
        # 解包，写入磁盘
        for title, duration, views, percent, url_link in zip(titles, durations, viewss, percents,url_links):
            new_link = 'https://www.xxxxxx.com' + url_link
            writer.writerow([title, duration, views, percent, new_link])
            print('--写入成功'*5)
    except:
        print('提取信息错误，这个url地址是: ', url)

# 主函数
def main(num):
    origin_url = r'https://www.xxxxxx.com/video?page={}'.format(num)
    print('正在抓取的网页url: ',origin_url)
    content_resolve(origin_url)

# 启动4进程
if __name__ == '__main__':
    pool = Pool(4)
    # 这是多进程爬虫，比较耗资源， 但对于小型爬虫来说，足够了，2000个网页，大概5分钟左右能爬取完毕
    pool.map(main, [num for num in range(2,2201)])
    print('结束当前页面爬取')

# 测试程序运行时间
end = time.time()
print('程序运行了%s秒' %(end-start))
