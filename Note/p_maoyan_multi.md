爬虫实例--多进程爬取   
=====

我们先看一段实例代码:     
```Python
from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests

def main(num):
	headers = {'User-Agent': 'yyy', 'Cookie': 'xxxx'}
	url_saves = r"https://maoyan.com/board/4?offset=" + str(num)
	wb_data_new = requests.get(url_saves, headers=headers)
	soup = BeautifulSoup(wb_data_new.text, 'lxml')
	tops = soup.select("i.board-index")
	titles = soup.select('dl.board-wrapper > dd > a ')
	times = soup.select('p.releasetime')
	In_stars = soup.select("p.star")
	
	for top, title, time, star in zip(tops, titles, times, In_stars):
		print(top.get_text(),
			  title.get("title"),
			  time.get_text()[5:],
		      star.get_text()[20:28])


if __name__ == '__main__':
	pool = Pool()
	pool.map(main, [num * 10 for num in range(10)])
```
这里小型爬虫我们使用了多进程爬取, 当爬取的数量不多时, 这样效率也不是太快, 比如说可能就七八个网页的样子   
如果成百上千还是可以考虑开多进程, 但最好是多进程多携程+分布式,  也不能太快,  搞网站的都不容易, 混口饭吃   


## 多进程   
进程的创建上面是其中的一种: 创建进程池   
这种更为高效,  相当于太空循环系统里的水, 可以重复利用      

我们先看一看进程是如何创建的:   
python用起来就是方便, 很多功能别人都写好了, 我们拿来用就行:   
```Python
from multiprocessing import Process
import time 

def run_one():
	while True:
		print('This is one process')
		time.sleep(1)

def run_two():
	while True:
		print('This is two process')
		time.sleep(1)

if __name__ == "__main__":
	p1 = Process(target=run_one)
	p2 = Process(target=run_two)
	p1.start; p2.start
```
导入模块, 使用功能  
创建`Process`对象, 指定启动特定代码快的进程`target=run_one`  
这样就创建了一个进程,  注意, 进程属于独立内存空间, 如果要通信, 需要引入其他方式或者库来实现   

这里, 我们还可以打印它们的进程号, 像这样:  
```Python
import os
print(os.getpid())
```

### 然后说下进程创建里面怎么传入参数:   
我们先看这段简单代码:   
```Python
import socket, threading

def recv_msg(udp_socket):
    while True:
        recv_data = udp_socket.recvfrom(1024)
        print('接收的数据: ' ,recv_data[0].decode('utf-8'))

def send_msg(udp_socket, dest_ip, dest_port):
    while True:
        out = input('q默认')
        if out == 'q':
            continue
        else:
            send_data = '发送内容: 吃了么您嘞 ?'
            udp_socket.sendto(send_data.encode('utf-8'), (dest_ip, dest_port))

def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("192.168.0.105", 8080))
    dest_ip = '192.168.0.102'
    dest_port = int(8080)
    
    t1 = threading.Thread(target=recv_msg, args=(udp_socket, ))
    t2 = threading.Thread(target=send_msg, args=(udp_socket, dest_ip, dest_port))
    t1.start()
    t2.start()
    
if __name__ == '__main__':
    main()   
```
请注意, 进程与线程创建与使用大同小异, 名称不一样罢了     
所以,  进程传参方式就是:   
`p1 = Process(target=FUNC_NMAE, args=(udp_socket, ))`     
注意后面的`args`是一个元祖     

## 进程间通信Queue   
我们先看一段简单代码:   
```Python   
from multiprocessing import Queue

q = Queue(5)
for i in range(10):
	q.put('{}'.format(str(i)))
	
print('This is q.full_1', q.full())
```
我们创建Queue对象, 向里面传入数据`(5)`, 并且表示这个队列容器体积为`5`   
好比我们创建了一所房子, 里面设计就只能住5个人   

如果外边不停的加人数, 代码能运行下去吗?   
就像欧洲的难民不断往德国, 英国等发达国家涌入一样, 他们能不受影响吗?   

事实上, 如果我们加入队列的数量大于容器`5`时, 它就停止了, 就像一个人吃饱了他不会再吃一样   

#### Queue方法知识引导:    
```
Queue.qsize(): 返回当前队列包含的消息数量；
Queue.empty(): 判断空否，返回True，反之False ；
Queue.full(): 判断满否，返回True,反之False；
Queue.get([block[, timeout]]): 获取队列中的一条消息，然后将其从列队中移除，block默认值为True；
1）如果block使用默认值，且没有设置timeout（单位秒），消息列队如果为空，此时程序将被阻塞（停在读取状态），直到从消息列队读到消息为止，
    如果设置了timeout，则会等待timeout秒，若还没读取到任何消息，则抛出"Queue.Empty"异常；
2）如果block值为False，消息列队如果为空，则会立刻抛出"Queue.Empty"异常；
Queue.get_nowait(): 相当Queue.get(False)；

Queue.put(item,[block[, timeout]])：将item消息写入队列，block默认值为True；

> 1）如果block使用默认值，且没有设置timeout（单位秒），消息列队如果已经没有空间可写入，此时程序将被阻塞（停在写入状态），直到从消息列队腾出空间为止，
     如果设置了timeout，则会等待timeout秒，若还没空间，则抛出"Queue.Full"异常；

> 2）如果block值为False, 消息列队如果没有空间可写入，则会立刻抛出"Queue.Full"异常；

Queue.put_nowait(item): 相当Queue.put(item, False)；
```


## Queue例子:  
我们先看一段实例代码:  
```Python  
from multiprocessing import Process, Queue
import time, random

def write(q):
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

def read(q):
    while True:
        if not q.empty():
            value = q.get(True)
            print('Get %s from queue.' % value)
            time.sleep(random.random())
        else:
            break

if __name__=='__main__':
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read,  args=(q,))

    pw.start()
    pw.join()

    pr.start()
    pr.join()

    print('')
    print('所有数据都写入并且读完')
```
这里, 我们结合了进程, 并创建了Queue方法   
像里面添加数据, 并在下面的进程中读取数据   
这样了, 我们就做到了进程中通信   
通信很简单, 有个中间人即可, 像我们现实生活中, 男人和女人就是两个不同的进程, 如何在两个进程之间进行通信, 是进化出了有性生殖  
如何在人与人的思想之间进行通信,  于是产生了书  
如何在群体与群体之间进程通信, 于是产生了货币  
#### 请注意: 中间件是手段, 沟通交流才是目的  
sex机械运动的快感不是目的, 而只是进化出的手段, 目的在于产生群体基因的差异性和大范围分布性, 从而提高群体的存活能力, 基因是`自私`的  
书同样是手段不是目的, 书的目的是为了传达思想, 点燃思维的火焰, 普遍看来我们现代教育, 把脑子当容器去灌, 想想都可怕, 希望以后教育改革, 能够越来有越面向未来的教育   
经济发展到现在的水平, 也好像脱缰的野马了, 人作为远古来的动物, 置身于现代货币体系, 多少有点不自然, 货币纵然可以使生活变好, 但是大多数时候, 请记住, 幸福水平与银行存款没有什么关系   


## 进程池   
上面的猫眼爬取, 就用到了继承池, 两行代码即可, 异常的简单:   
```Python
from multiprocessing import Pool
import time, random

def worker(msg):
    t_start = time.time()
    time.sleep(random.random()*2)
    t_stop = time.time()
    print(msg, "执行完毕，耗时%0.2f" % (t_stop-t_start))

po = Pool(4)
for i in range(0, 10):
    po.apply_async(worker, (i,))

po.close()
po.join()
```

当需要创建的子进程数量不多时，可以直接利用multiprocessing中的Process动态成生多个进程      
但如果是上百甚至上千个目标，手动的去创建进程的工作量巨大，此时就可以用到multiprocessing模块提供的Pool方法    

初始化Pool时，可以指定一个最大进程数，当有新的请求提交到Pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求   
但如果池中的进程数已经达到指定的最大值，那么该请求就会等待，直到池中有进程结束，才会用之前的进程来执行新的任务    


## 进程池中的Queue   
```Python
from multiprocessing import Manager, Pool
import time

def reader(q):
    for i in range(q.qsize()):
        print("reader从Queue获取到消息：%s" % q.get(True))

def writer(q):
    for i in "itcast":
        q.put(i)

if __name__=="__main__":
    queue = Manager().Queue()
    po = Pool()
    
    po.apply_async(writer, (queue, ))
    time.sleep(1)

    po.apply_async(reader, (queue, ))
    
    po.close()
    po.join()

```
