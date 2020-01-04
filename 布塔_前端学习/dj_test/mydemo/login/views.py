import hashlib
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import datetime
# Create your views here.
def make_confirm_string(user):#插入confirmString表插入为进行邮箱确认的用户 并返回一个code
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code
#对用户密码进行加密
def hash_code(s, salt='mysite'):
    #md5,sha1, sha224, sha256, sha384, sha512等算法
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())#将字符串载入到sha256对象中，获得sha256算法加密。
    return h.hexdigest() #作为十六进制数据字符串值
#发送邮箱进行用户确认注册
def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自2425640010@qq.com的注册确认邮件'

    text_content = '''感谢注册2425640010@qq.com，这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>确认注册</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

#用户确认 并从confirmString表删除已确认的用户(对应confirm.html)
def user_confirm(request):
    code = request.GET.get('code', None)#获取网址get请求的参数code(作为get请求参数)  例：http://127.0.0.1:8000/confirm/?code=ksdjhgkjhjgf
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)#根据code查询ConfirmString表
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
def index(request):

    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


#登录模板
def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == "POST":
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():#表单类自带的is_valid()方法一步完成数据验证工作
            ##  验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                # 数据库查询name为username的数据
                user = models.User.objects.get(name=username)
                print("ssss",user)
            except:
                message = '用户不存在！'
                #
                return render(request, 'login/login.html', locals())
            if not user.has_confirmed:#判断是否经过邮箱确认
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                print(username, password)
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()#返回forms.py中的登录表单  login.html可以使用django自动生成form表单里的内容
    # locals()函数，它返回当前所有的本地变量字典 就不用写{'message':message, 'login_form':login_form}
    return render(request, 'login/login.html',locals())

#注册模板
def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请填充完整信息"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            if password1 != password2:
                message = "两次密码不正确"
                return render(request,'login/register.html',locals())
            else:
                same_name_user = models.User.objects.filter(name=username)#判断用户是否已存在
                if same_name_user:
                    message = '用户已存在'
                    return render(request,'login/register.html',locals())
                same_name_email = models.User.objects.filter(name=email)
                if same_name_email:
                    message = '该邮箱已被注册'
                    return render(request,'login/register.html',locals())

                new_user = models.User();
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()#保存注册用户信息
                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
                # return  redirect('/login/')
        else:
            return  render(request,'login/register.html',locals())
    register_form = forms.RegisterForm()

    return render(request, 'login/register.html',locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()#注销 清除session
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']

    return redirect("/login/")#重定向

def starter(request):
    return render(request,'login/starter.html')