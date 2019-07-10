import requests
from bs4 import BeautifulSoup

urls = []
default_content = [
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="assets/css/bootstrap.min.css"><link rel="stylesheet" href="assets/css/style.css"><title>',
    '</title></head><body><div class="page-title"><div class="d-table"><div class="d-table-cell"><div class="container"><div class="row"><div class="col-lg-12 col-md-12"><h3>',
    '</h3></div></div></div></div></div></div><section class="about-area ptb-80"><div class="container"><div class="row"><div class="col-lg-12 col-md-12"><div class="about-text">',
    '</div></div></div></div></section></body></html>']


# 获取单个网页的内容
def single_find(url):
    url_tmp = url
    header = {'user-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url_tmp, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        n = soup.find('div', {'class': 'article-body'})
        # 格式化内容
        s1 = BeautifulSoup(str(n), 'html.parser')
        return str(s1.prettify())
    except Exception:
        print("爬取失败")


# 获取考研每日一句集合内所有超链接
def fetch_all_url():
    url = "https://kaoyan.wendu.com/2019/0221/131539.shtml"
    header = {'user-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        # 获取tbody里的内容（偷懒筛选）
        n = soup.find('tbody')
        s1 = BeautifulSoup(str(n), 'html.parser')
        # 遍历tbody里的a标签
        global urls
        for i in s1.findAll('a'):
            urls.append(i['href'])
    except Exception:
        print("爬取失败")


def start_fetch():
    fetch_all_url()
    # single_find(urls[9])
    num = 1
    for i in urls:
        f = open(str(num) + ".html", "a+", encoding='utf-8')
        tmp = []
        tmp.append(default_content[0])
        tmp.append("考研何凯文每日一句 ---" + str(num))
        tmp.append(default_content[1])
        tmp.append("考研何凯文每日一句 ---" + str(num))
        tmp.append(default_content[2])
        tmp.append(single_find(i))
        tmp.append(default_content[3])
        f.write("".join(tmp))
        f.close()
        num += 1


start_fetch()
