from django.shortcuts import render
from django.shortcuts import redirect
from login.models import User,ConfirmString
from login.form import UserForm,RegisterForm
import hashlib
import datetime
# from django.db import models
# from django.contrib.auth import models
# Create your views here.
# from .models import User

def hash_code(s,salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):
    pass
    return render(request,'login/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect("/index/")
    if request.method == "POST":
        # username = request.POST.get('username', None)
        # password = request.POST.get('password', None)
        login_form = UserForm(request.POST)
        message = "所有字段都必须填写！"
        if login_form.is_valid():  # 确保用户名和密码都不为空
            # username = username.strip()
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = User.objects.get(name__exact=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html',locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = '请检查填写的内容'
        if register_form.is_valid(): #获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2: #判断两次密码是否相同
                message = "两次输入的密码不同"
                return render(request,'login/register.html',locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user: #用户名唯一
                    message = '用户名已经存在，请重新选择用户名！'
                    return render(request,'login/register.html',locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user: #邮箱唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request,'login/register.html',locals())

                # 当一切都正常的情况下，创建新用户

                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email,code)

                return redirect('/login/')
    register_form = RegisterForm()
    return render(request,'login/register.html',locals())

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name,now)
    ConfirmString.objects.create(code=code,user=user,)
    return code

def send_email(email,code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自LeechenLove的温馨提示邮件'
    text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

def logout(request):
    pass
    return redirect('/index/')