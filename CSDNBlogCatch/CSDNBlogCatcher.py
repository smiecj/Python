#-*- coding: UTF-8 -*- 
import time
import traceback
import functools

from ConnectService import *
from SMTPSender import *
from bs4 import BeautifulSoup

# 静态方法: 获取时间转字符串格式
def getTimeStr(currentTime):
    time_array = time.localtime(int(currentTime))
    return time.strftime('%Y-%m-%d %H:%M:%S', time_array)

# 自定义排序方法
def cmp_csdn_blog(csdnBlog1, csdnBlog2):
    if csdnBlog1.viewNum > csdnBlog2.viewNum:
        return -1
    elif csdnBlog1.viewNum < csdnBlog2.viewNum:
        return 1
    else:
        return 0

class BlogCatcher:
    #@abstractmethod
    def catch(self, time):
        self.catch(time);

    def __init__(self, url):
        self.url = url

class Blog(object):
    def __init__(self, link, viewNum, title):
        self.link = link
        self.viewNum = viewNum
        self.title = title

    def getMsg(self):
        return '博客: 链接: {url}, 标题: {title}, 浏览量: {viewNum}.'.format(url = self.link, title = self.title, viewNum = self.viewNum)

class CSDNBlogCatcher(BlogCatcher):
    def __init__(self, url):
        super().__init__(url)
        print("初始化CSDN 博客 catcher 成功! 爬虫链接: " + url)
        self.QUEUE_MAX_SIZE = 1000000
        self.blogArr = []
        self.CATCH_SIZE = 10

    ## 抓取最新、点击量靠前的博客链接
    def catch(self, beginTime, endTime):
        begin_time_array = time.localtime(int(beginTime))
        end_time_array = time.localtime(int(endTime))
        print("传入的时间为: 开始时间: {}, 结束时间: {}".format(getTimeStr(beginTime), 
            getTimeStr(endTime)))

        ## 调用接口获取当天的博客数据，循环获取
        currentTime = endTime
        while currentTime > beginTime:
            print("问题定位临时用: 当前时间为: " + str(currentTime))
            print("当前解析博客的时间戳为: " + getTimeStr(currentTime))
            currentUrl = self.url + "&shown_offset=" + str(currentTime * 1000000)
            resp = get_request(currentUrl, {})
            
            # 解析获取到的博客信息
            if resp is False:
                print("调用CSDN接口失败！请检查网络连接和URL")
                return None
            else:
                print("调用CSDN接口成功！开始解析博客信息")
                blog_json = json.loads(resp)
                for blogObj in blog_json["articles"]:
                    ## 将数据插入到优先队列中，按照浏览数
                    title = self.getBlogTitle(blogObj["url"])
                    if title:
                        csdnBlog = Blog(blogObj["url"], int(blogObj["views"]), title)
                        #print(csdnBlog.getMsg())

                        self.blogArr.append(csdnBlog)
                            
                    ## 更新当前时间
                    if (currentTime * 1000000 > blogObj["shown_offset"]):
                        currentTime = int(blogObj["shown_offset"] / 1000000)
                        #print("更新之后的时间为: " + getTimeStr(currentTime))
        self.blogArr = sorted(self.blogArr, key=functools.cmp_to_key(cmp_csdn_blog))

## 组装获取到的博客，并将获取到的信息打印出来
    def getCatchedBlogMsg(self):
        arr = []
        content = "昨日博客内容: <br/>"
        for blog in self.blogArr:
            print(blog.getMsg())
            arr.append(blog)
            content = content + blog.getMsg() + "<br/>"
            if len(arr) > self.CATCH_SIZE:
                break
        return content

    ## 获取文章标题
    def getBlogTitle(self, url):
        resp = get_request(url, {})
        # 有的文章在首页还有，但是其实已经删除了。调用接口会返回404，这里需要额外判断一下
        if resp is False:
            return ""
        else:
            soup = BeautifulSoup(resp, 'lxml')
            return soup.head.title.text

# 定义main 方法
if __name__ == '__main__':
    csdnDBCatcher = CSDNBlogCatcher("https://www.csdn.net/api/articles?type=more&category=db")

    # 获取当天时间戳，进行参数组装
    now_time = int(time.time())
    begin_time = now_time - now_time % 86400 + time.timezone
    now_time = int(time.time() + 86400)
    end_time = now_time - now_time % 86400 + time.timezone

    csdnDBCatcher.catch(begin_time, end_time)
    content = csdnDBCatcher.getCatchedBlogMsg()

    send_msg(content)