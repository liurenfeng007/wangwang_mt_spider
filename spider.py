#美团美食
# -*- coding:UTF-8 -*-
import requests
import time
from bs4 import BeautifulSoup
import json
import csv
import re

url = 'http://gz.meituan.com/'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Host': 'gz.meituan.com',
    'Referer': 'http://gz.meituan.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Content-Type': 'text/html;charset=utf-8',
    'Cookie': '_lxsdk_cuid=165ec83e866c8-0d9c72e74b8d6e-50432518-144000-165ec83e868c8; grap_cookie_phone_ab=13138693214; mtcdn=K; lsu=; oc=uQgK8EgA1oe9MM9qJ3SE1TAv47Z6Vu2ewE1Po5gAjCPN1GBMIckjoCmFRfa7FI4QHw3QDkVCcJCekUYkQ3TOGy_hOqvm21THnc0sL7JxsKT-QzmJFN2H7KJThM1rHG9Exb36eaE8GtQnbcj_7PtcXpweEQLsEqJM5w8Z3QsqOB0; iuuid=047258FD71822CBC183893C172471F6F9D412CCC922421EA89C24142DDD68857; isid=9AC6E793600A1860D6107FF17E998091; logintype=normal; cityname=%E5%B9%BF%E5%B7%9E; _lxsdk=047258FD71822CBC183893C172471F6F9D412CCC922421EA89C24142DDD68857; _ga=GA1.2.345160310.1541420989; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; u=119222346; n=liurenfeng007; lt=xH3Iq5RswOEDbOW4CkUfIPE_Q1wAAAAAWQcAAL_6lvEBhH4ve_oEJp_ym4SCQ6NH2XCb3xCACgY8t7Qi2NUUROYie5GfWY4rFcNQ_g; token2=xH3Iq5RswOEDbOW4CkUfIPE_Q1wAAAAAWQcAAL_6lvEBhH4ve_oEJp_ym4SCQ6NH2XCb3xCACgY8t7Qi2NUUROYie5GfWY4rFcNQ_g; uuid=e09ac54814604108ba0a.1541492872.2.0.0; unc=liurenfeng007; IJSESSIONID=jl8so862uqtfms4eukkqjosz; oops=xH3Iq5RswOEDbOW4CkUfIPE_Q1wAAAAAWQcAAL_6lvEBhH4ve_oEJp_ym4SCQ6NH2XCb3xCACgY8t7Qi2NUUROYie5GfWY4rFcNQ_g; i_extend=H__a100001__b1; latlng=; webp=1; __utma=74597006.345160310.1541420989.1541501325.1541501325.1; __utmc=74597006; __utmz=74597006.1541501325.1.1.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/xing851483876/article/details/81842329; p_token=xH3Iq5RswOEDbOW4CkUfIPE_Q1wAAAAAWQcAAL_6lvEBhH4ve_oEJp_ym4SCQ6NH2XCb3xCACgY8t7Qi2NUUROYie5GfWY4rFcNQ_g; _hc.v=2404cb99-243b-6c9e-c4bd-6374eb664375.1541501347; ci=70; rvct=70%2C20; lat=28.223888; lng=112.988261; _lxsdk_s=166ec387709-7d9-d51-3e1%7C%7C8',
}

# 获取店铺商圈id
def get_minarea(target):
    req = requests.get(url=target, headers=headers)
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    texts = bf.find_all('script')
    text = texts[14].get_text().strip()
    text = text[19:-1]
    result = json.loads(text)
    result = result['filters']
    result = result['areas']
    list = []
    for item in result:
        for i in item['subAreas']:
            if i['name'] == '全部':
                continue
            list.append(i['id'])
    #print(list)
    return list

# 获取店铺详情数据(单个页面解析)
def get_item_info(url):
    req = requests.get(url=url, headers=headers)
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    texts = bf.find_all('script')       #正则# resp = re.sub(r'(.*)window._appState = ', '', html) # text = re.sub(r';</script>([\s\S]*)', '', resp)
    if texts[-3].get_text().strip()=='':
        list = open(r'异类.csv', "w", newline='', encoding='UTF-8')
        list.write(url + '\n')
        list.close()
        return ''
    text2 = texts[-3].get_text().strip()
    text = text2[19:-1]
    result4 = json.loads(text, encoding='utf-8')
    result5 = result4['detailInfo']
    it = result5
    Info_list = []
    if result5:
        Info_list.append(it['longitude'])
        Info_list.append(it['latitude'])
        # print(Info_list)
    time.sleep(2)
    return Info_list

#获取商圈的商户列表
def get_subranch_info(list):
    with open(r'美团-广州-美食.csv',"w", newline='',encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['商家名称','地址','商家logo','经度','纬度'])
        for item in list:
            for i in range(50):
                if i==0:
                    continue
                target='http://gz.meituan.com/meishi/'+'b'+str(item)+'/'+'pn'+str(i)+'/'
                req = requests.get(url=target,headers=headers)
                html=req.text
                bf=BeautifulSoup(html,'lxml')
                texts=bf.find_all('script')
                text=texts[14].get_text().strip()
                text=text[19:-1]
                result=json.loads(text)
                result=result['poiLists']
                result=result['poiInfos']

                if result:
                    print(target)
                    for it in result:
                        Info_list = []
                        Info_list.append('美团')
                        Info_list.append('美食')
                        Info_list.append(it['title'])
                        Info_list.append(it['address'])
                        Info_list.append(it['frontImg'])
                        url='http://gz.meituan.com/meishi/'+str(it['poiId'])+'/'
                        print(url)
                        position=get_item_info(url)
                        Info_list.extend(position)
                        writer.writerow(Info_list)
                    time.sleep(1)
                else:
                    break

if __name__ == '__main__':
    IDlist = []
    target = 'http://gz.meituan.com/meishi/'
    IDlist = get_minarea(target)
    get_subranch_info(IDlist)
    # kk=get_item_info('https://www.meituan.com/cate/91693286/')
    # print(kk)
    print('Done')