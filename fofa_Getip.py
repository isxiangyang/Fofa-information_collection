import re
import base64
import requests
from urllib.parse import quote
import random
from pyquery import PyQuery
requests.packages.urllib3.disable_warnings()
'''------------请将cookie填入下方---------------'''
cookie="refresh_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MjUyODcsIm1pZCI6MTAwMDIwMzY3LCJ1c2VybmFtZSI6IkFkb2xwaCIsImV4cCI6MTY0ODM5MjI2MS4wMDkzMzIsImlzcyI6InJlZnJlc2gifQ.cdS6rSy_Sr7A05GBTN095FjR8NaM_uKBYkvo97eSGezpAbD-0mefvbDfgmWWebvSFWELPi3lwELwgjqi6XCEBg; isUpgrade=; Hm_lvt_b5514a35664fd4ac6a893a1e56956c97=1648114026,1648188911,1648214944,1648217857; befor_router=; fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MjUyODcsIm1pZCI6MTAwMDIwMzY3LCJ1c2VybmFtZSI6IkFkb2xwaCIsImV4cCI6MTY0ODMxNzU2My4zNjExNTMxLCJpc3MiOiJyZWZyZXNoIn0.bMLhPjFxhyLEOtBDjwYdPKRj_g_JXi-cMhBJ35QWEYacQHGBRxGRx_umLKWOoX2X_YdgFUHX1VBt3t5yYam3Jw; user=%7B%22id%22%3A25287%2C%22mid%22%3A100020367%2C%22is_admin%22%3Afalse%2C%22username%22%3A%22Adolph%22%2C%22nickname%22%3A%22%22%2C%22email%22%3A%2298adolph%40gmail.com%22%2C%22avatar_medium%22%3A%22https%3A%2F%2Fi.nosec.org%2Favatar%2Fsystem%2Fusers%2Favatars%2F100%2F020%2F367%2Fmedium%2F1.jpg%3F1624501829%22%2C%22avatar_thumb%22%3A%22https%3A%2F%2Fi.nosec.org%2Favatar%2Fsystem%2Fusers%2Favatars%2F100%2F020%2F367%2Fthumb%2F1.jpg%3F1624501829%22%2C%22key%22%3A%227b7e8d351e537143d82cb037e7104bc6%22%2C%22rank_name%22%3A%22%E9%AB%98%E7%BA%A7%E4%BC%9A%E5%91%98%22%2C%22rank_level%22%3A2%2C%22company_name%22%3A%22%22%2C%22coins%22%3A0%2C%22can_pay_coins%22%3A0%2C%22credits%22%3A30074%2C%22expiration%22%3A%22-%22%2C%22login_at%22%3A0%7D; Hm_lpvt_b5514a35664fd4ac6a893a1e56956c97=1648274357"
'''------------请将cookie填入上方---------------'''


headers = {
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cookie': cookie,
'referer': 'https://fofa.info/',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3883.400 QQBrowser/10.8.4559.400',
}

def capture_ip():
    with open("proxy.txt", "w+", encoding="utf-8") as f:
        for i in range(1, 28):
            print("正在爬取第{num}个网页...".format(num=i))
            url = "https://www.89ip.cn/index_{num}.html".format(num=i)
            res = requests.get(url).text
            doc = PyQuery(res)
            for i in range(0, 100, 5):
                ip = doc("tbody tr td").eq(0 + i).text()
                port = doc("tbody tr td").eq(1 + i).text()
                f.write(ip + ":" + port + "\n")
    f.close()
    print("\n代理抓取完毕！")
'''-----------首次运行需要开启一次capture_ip()来抓取代理ip列表-------'''
capture_ip()
'''-----------生成proxy.txt文件后即可注释掉----------'''
def get_proxy():
    proxy=[]
    file = open("proxy.txt", "r+", encoding="utf-8").readlines()
    for i in file:
        proxy.append(i.replace("\n",""))
    return proxy

def getHtml(urls):
    # 代理ip尝试连接次数
    print("---》》使用代理IP《《---")
    retry_count = 3
    proxy = random.sample(get_proxy(),1)
    proxy = {"http": "http://{}".format(proxy[0])
             }
    while retry_count > 0:
        try:
            html = requests.get(url=urls, headers=headers, proxies=proxy, verify=False,timeout=5).text
        # 使用代理访问
            doc = PyQuery(html)
            result_url=doc('span[class="aSpan"]').text().split(" ")
            return result_url
        except Exception as u:
            pass
    # 代理池ip无法请求成功，尝试使用本地ip请求一次，提高容错率
    print('---》》使用本地IP《《---')
    try:
        html = requests.get(url=urls, headers=headers).text
        # 使用代理访问
        doc = PyQuery(html)
        result_url = doc('span[class="aSpan"]').text().split(" ")
        return result_url
    except Exception as u:
        print('lo_err:', u)
        pass
def fofa_search(gs,i):
    url = 'https://fofa.info/result?qbase64='
    search = gs
    search_data_bs = str(base64.b64encode(search.encode("utf-8")), "utf-8")
    search_data_url = quote(search_data_bs)  # url编码
    urls = url + search_data_url+"&page={num}&page_size=20".format(num=i)
    result = getHtml(urls)
    print(result)
    return result

with open("captur.txt","w+",encoding="utf-8") as f:
    for i in range(1,500):###这里输入搜索的页数
        result=fofa_search('domain="tongji.edu.cn"',i)###这里输入搜索内容
        for url in result:
            f.write(url+"\n")
f.close()