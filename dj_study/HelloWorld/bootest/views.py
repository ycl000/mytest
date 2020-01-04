from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader,RequestContext
from bootest.models import BookInfo, HeroInfo
def index(request):
    # 1.获取模板
    # template=loader.get_template('booktest/index.html')
    # 2.定义上下文
    # context=RequestContext(request,{'title':'图书列表','list':range(10)})
    # 3.渲染模板
    books = BookInfo.objects.all()
    return render(request,"bootest/index.html",context={'title':'图书','books':books})

def hero(request,id):
    #id参数从index.html 传过来
    print(id)
    # heros = HeroInfo.book_set.get(id=id)
    book = BookInfo.objects.get(id=id)
    heros = book.heroinfo_set.all()
    return render(request, "bootest/hero.html", context={'title': '英雄', 'heros': heros})