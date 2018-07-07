import requests
import re
import time
from urllib import parse
from bs4 import BeautifulSoup
from multiprocessing import Pool

headers = {
    'Host': 'www.shclearing.com',
    'Connection': 'keep-alive',
    'Content-Length': '478',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Origin': 'http://www.shclearing.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/45.0.2454.93 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': '_ga=GA1.2.1076225437.1465265795; JSESSIONID=24XcXXCb1bkkKWnKn1LLNBqGTR8qnfmcmf'
              '3p5T2pw2TwpNCytnfp!301927905; HDSESSIONID=fhwLXXLPrBqXwsvCyqKL1lCbp5QmGDxxGJ4w'
              'd8vrfhr2ksgJcpvf!1660475047; Hm_lvt_d885bd65f967ea9372fc7200bc83fa81=1465223724;'
              ' Hm_lpvt_d885bd65f967ea9372fc7200bc83fa81=1465354426'
}

url1 = 'http://www.shclearing.com/xxpl/fxpl/index.html'
url2 = ['http://www.shclearing.com/xxpl/fxpl/index_{}.html'.format(str(i)) for i in range(1, 5, 1)]
url2.insert(0, url1)

links = []
host = 'http://www.shclearing.com/xxpl/fxpl/'


def get_link_list(url):
    for item in url:
        web_data = requests.get(item)
        soup = BeautifulSoup(web_data.text, 'lxml')
        list = soup.select('ul.list li a')
        for item in list:
            link = host + item.get('href').split('./')[1]
            links.append(link)


FileName = []
DownName = []
DownName1 = []  # DownName1用于存放转码后的名称


def get_contents(link):
    web_data = requests.get(link)
    soup = BeautifulSoup(web_data.text, 'lxml')
    contents = soup.select('#content > div.attachments > script')[0].get_text()
    a = str(re.findall(r"fileNames = '(.*?)'", contents, re.M)[0])
    b = str(re.findall(r"descNames = '(.*?)'", contents, re.M)[0])
    FileName = a.replace('./', '').split(';;')
    DownName = b.split(';;')  # 先用正则表达式提取出后面post中要用到的两个参数，但是要将中文转化为对应的URL编码
    for item in DownName:
        a = parse.quote(item)
        DownName1.append(a)
    print(FileName, '\\n', DownName, '\\n', DownName1)

    for i, j, k in zip(FileName, DownName1, DownName):
        download_file(i, j, k)


# link='http://www.shclearing.com/xxpl/fxpl/cp/201606/t20160608_159680.html'
# get_contents(link)
# print('The pdf have been downloaded successfully !')


def download_file(a, b, c):
    data = {
        'FileName': a,
        'DownName': b}

    local_filename = c
    post_url = 'http://www.shclearing.com/wcm/shch/pages/client/download/download.jsp'
    time.sleep(0.5)  # 限制下载的频次速度，以免被封
    # NOTE the stream=True parameter
    r = requests.post(post_url, data=data, headers=headers, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):  # 1024 是一个比较随意的数，表示分几个片段传输数据。
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()  # 刷新也很重要，实时保证一点点的写入。
    return local_filename


if __name__ == '__main__':
    get_link_list(url2)
    pool = Pool()
    pool.map(get_contents, links)
    print('The documents have been downloaded successfully !')
