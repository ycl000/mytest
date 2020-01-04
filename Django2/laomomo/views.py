from django.shortcuts import render

# from django.shortcuts import HttpResponse #导入HttpResponse模块
# def index(request):#request是必须带的实例。类似class下方法必须带self一样
#     return HttpResponse("Hello World!!")#通过HttpResponse模块直接返回字符串到前端页面
# Create your views here.

list = [{"name": 'good', 'password': 'python'}, {'name': 'learning', 'password': 'django'}]


def index(request):
    # 获取前端post过来的用户名和密码
    # name = request.POST.get('name', None)
    # password = request.POST.get('password', None)
    #
    # # 把用户和密码组装成字典
    # data = {'name': name, 'password': password}
    # list.append(data)

    return render(request, 'index.html',
                  {'form': list})  # 通过render模块把index.html这个文件返回到前端，并且返回给了前端一个变量form，在写html时可以调用这个form来展示list里的内容


def hello(request):
    content={}
    content["hello"]="hello World"

    return render(request,"hello.html",content)