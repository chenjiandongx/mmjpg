import os
import time
import threading
from multiprocessing import Pool, cpu_count
import requests
from bs4 import BeautifulSoup


headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1"
        " (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}


def save_pic(img_src, pic_cnt):
    """" 将图片下载到本地文件夹 """
    img = requests.get(img_src, headers=headers, timeout=10)
    with open("pic_" + str(pic_cnt + 1) + '.jpg', 'ab') as f:
        f.write(img.content)
        print("pic_" + str(pic_cnt + 1) + '.jpg')


def make_dir(folder_name):
    """ 新建套图文件夹并切换到该目录下 """
    path = os.path.join(r"E:\mmjpg", folder_name)
    is_exists = os.path.exists(path)
    # 如果目录已经存在就不用再次爬取了，去重，提高效率
    if not is_exists:
        os.makedirs(path)       # 新建文件夹
        print(path)
        os.chdir(path)          # 切换到该文件夹
        return True             # 不存在返回True
    else:
        print("This folder have been created!")
        return False            # 存在返回False


lock = threading.Lock()     # 全局资源锁

def urls_crawler(url):
    """ 爬虫入口，主要爬取操作
    本来打算爬取个代理ip网站的代理ip维护一个代理池的
    后来发现一次过，没被服务器蹦掉，所以就算了...
    """
    try:
        respone = requests.get(url, headers=headers, timeout=10).text
        pic_series = BeautifulSoup(respone, 'lxml').find('h2').text     # 套图名，也作为文件夹名
        folder_name = pic_series.encode('ISO-8859-1').decode('utf-8')   # 转换编码

        with lock:
            if make_dir(folder_name):
                # 每套图共有多少张
                max_count = BeautifulSoup(respone, 'lxml').find('div', class_='page').find_all('a')[-2].get_text()
                # 套图里每张图片页面
                page_urls = [url + "/" + str(i) for i in range(1, int(max_count) + 1)]

                img_urls = []       # 图片具体地址
                for index, page_url in enumerate(page_urls):
                    result = requests.get(page_url, headers=headers, timeout=10).text
                    # 最后一张图片没有a标签直接就是img所以分开解析
                    if index + 1 < len(page_urls):
                        img_src = BeautifulSoup(result, 'lxml').find('div', class_='content').find('a').img['src']
                        img_urls.append(img_src)
                    else:
                        img_src = BeautifulSoup(result, 'lxml').find('div', class_='content').find('img')['src']
                        img_urls.append(img_src)

                for cnt, url in enumerate(img_urls):
                    save_pic(url, cnt)

    except Exception as e:
        print(e)


if __name__ == "__main__":

    # 爬取http://mmjpg.com的套图
    urls = ['http://mmjpg.com/mm/{cnt}'.format(cnt=str(cnt)) for cnt in range(1, 801)]      # 爬取的套图地址
    pool = Pool(processes=cpu_count())
    try:
        results = pool.map(urls_crawler, urls)
    except Exception as exception:
        time.sleep(30)
        results = pool.map(urls_crawler, urls)
