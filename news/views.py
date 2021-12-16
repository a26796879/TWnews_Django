from django.shortcuts import render
import requests, json
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
def get_ltn_news(keyword):
    url = 'https://search.ltn.com.tw/list?keyword=' + keyword
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    tit_tag = soup.find_all("a", class_="tit")
    images = soup.select('img.lazy_imgs')
    results = []
    publisher = '自由時報電子報'
    for i in range(len(tit_tag)):
        title = tit_tag[i]['title']
        url = tit_tag[i]['href']
        res = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        publish = soup.select('span.time')[0].text.replace('\n    ','')
        image = images[i].get('data-src')
        dateFormatter = "%Y/%m/%d %H:%M"
        published_date = datetime.strptime(publish, dateFormatter)
        expect_time = datetime.today() - timedelta(hours=40)
        if published_date >= expect_time:
            results.append({
                'title':title,
                'url':url,
                'publisher':publisher,
                'published_date':published_date,
                'image':image
            })
        else:
            break
    return results
def index(request):
    return render(request, 'index.html',{
        'img_list':get_ltn_news('台灣'),
    })