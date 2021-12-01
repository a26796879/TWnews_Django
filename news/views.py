from django.shortcuts import render

img_list = ["https://img.ltn.com.tw/Upload/news/300/2021/11/23/3745908_1_1.jpg","https://img.ltn.com.tw/Upload/news/250/2021/11/24/157.jpg"]
def index(request):
    return render(request, 'index.html',{
        'img_list':img_list,
    })