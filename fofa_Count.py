import re
import base64
import requests
from urllib.parse import quote
import random
from pyquery import PyQuery
requests.packages.urllib3.disable_warnings()
'''
#使用此脚本前你需要修改两处代码：
#1.在代码15行与18行中填写你的信息
#2.首次运行需要开启一次代码第46行的抓代理
'''

'''------------请将cookie填入下方---------------'''
cookie="此处替换为你的cookie"

'''------------请将if-none-match填入下方---------------'''
if_none_match="此处替换为你的if-none-match"

headers = {
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cookie': cookie,
'if-none-match': if_none_match,
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
def get_proxy():
    '''-----------首次运行需要开启一次capture_ip()来抓取代理ip列表-------'''
    #capture_ip()
    '''-----------生成proxy.txt文件后即可注释掉----------'''

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
            html = requests.get(url=urls, headers=headers, proxies=proxy, verify=False,timeout=2).text
        # 使用代理访问
            doc = PyQuery(html)
            res = doc("p[class='nav-font-size']").text()
            ip_sum = re.findall('url_key:"(.*?)",resultLists', html)[0]
            num = "https://api.fofa.info/v1/search/stats?" + ip_sum
            num = num.replace("\\u002F", "/")
            num = requests.get(num, headers=headers).json()
            num=num['data']['countries'][0]['count']
            end = re.search("（",res).span()[0]
            return res[:end],num,"条独立IP"
        except Exception as u:
            print('proxy_err:', u)
            retry_count -= 1
    # 代理池ip无法请求成功，尝试使用本地ip请求一次，提高容错率
    print('---》》使用本地IP《《---')
    try:
        html = requests.get(url=urls, headers=headers).text
        # 使用代理访问
        doc = PyQuery(html)
        res = doc("p[class='nav-font-size']").text()
        ip_sum = re.findall('url_key:"(.*?)",resultLists', html)[0]
        num = "https://api.fofa.info/v1/search/stats?" + ip_sum
        num = num.replace("\\u002F", "/")
        num = requests.get(num, headers=headers).json()
        num = num['data']['countries'][0]['count']
        end = re.search("（", res).span()[0]
        return res, num, "条独立IP"
    except Exception as u:
        print('lo_err:', u)
        return None



def fofa_search(gs):
    url = 'https://fofa.info/result?qbase64='
    search = '"' + gs + '"'
    search_data_bs = str(base64.b64encode(search.encode("utf-8")), "utf-8")
    search_data_url = quote(search_data_bs)  # url编码
    urls = url + search_data_url
    result = getHtml(urls)
    return result

def check_gs(gs):
    if re.search('公司', gs):
        gs = gs.replace("公司", "")
    if re.search('责任', gs):
        gs = gs.replace('责任', '')
    if re.search('股份', gs):
        gs = gs.replace('股份', '')
    if re.search('有限', gs):
        gs = gs.replace('有限', '')
    if re.search('（', gs):
        gs = gs.replace('（','')
    if re.search('）', gs):
        gs = gs.replace('）','')
    if re.search('集团',gs):
        gs = gs.replace('集团','')
    else:
        pass
    return gs
if __name__ == '__main__':
    # 打开公司列表，获取公司名称
    print("开始收集--------")
    with open("result.txt", "w+", encoding="utf-8") as f:
        for k in open("gs.txt", "rb").readlines():
            gs = str(k, "utf-8")
            gs = gs.strip()
            gs = check_gs(gs)
            sum = fofa_search(gs)
            print("{gs}-------{sum}\n".format(gs=gs,sum=sum))
            f.write("{gs}-------{sum}\n".format(gs=gs,sum=sum))
        f.close()