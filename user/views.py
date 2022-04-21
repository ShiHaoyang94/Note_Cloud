import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import hashlib
from django.contrib import messages
from django.contrib.messages import get_messages, add_message
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import time

from .models import User
# Create your views here.
def login(request):
    if request.method == 'GET':
        if request.session.get('username') :

            return HttpResponseRedirect('/index')


        elif request.COOKIES.get('username'):

            request.session['username'] = request.COOKIES.get('username')

            return HttpResponseRedirect('/index')
        else:
            return render(request, 'login.html')

    elif request.method == 'POST':

        login_username = request.POST['username']
        login_password = request.POST['password']

        m = hashlib.md5()

        m.update(login_password.encode())

        login_password_m = m.hexdigest()

        if login_password.isspace() or login_username.isspace() or login_password==''or login_username=='':
            messages.error(request, "用户名和密码不能为空")
            return HttpResponseRedirect('/user/login')
        else:
            try:
                user = User.objects.get(username=login_username, is_active=True)

            except Exception as e:

                messages.error(request, "用户名或密码错误，登录失败")

                return HttpResponseRedirect('/user/login')


            if login_password_m == user.password:
                # 记录会话状态
                request.session['username'] = login_username
                # request.session['uid']=User.id

                #存cookies
                if 'remenber'in request.POST:


                    resq = HttpResponseRedirect('/index')
                    resq.set_cookie('username',login_username,60*60*24*3)
                    # resq.set_cookie('uid',User.id)



                    return resq

                else:

                    return HttpResponseRedirect('/index')

            else:

                messages.success(request, "用户名或密码错误，登录失败")

                return HttpResponseRedirect('/user/login')


def register(request):

    if request.method == 'GET':

        return render(request, 'register.html')

    elif request.method == 'POST':

        register_username = request.POST['username']
        register_email = request.POST['email']
        register_password = request.POST['password']
        register_password2 = request.POST['password2']
        if register_email.find("@") == -1 or not register_email.endswith('.com'):
            messages.error(request, "邮箱格式错误，请重新注册")

            return HttpResponseRedirect('/user/register')

        try:
            re = User.objects.get(username=register_username, is_active=True)

            messages.error(request, "用户名已存在，请重新注册")

            return HttpResponseRedirect('/user/register')

        except Exception as e:

            try:
                User.objects.get(email=register_email, is_active=True)

                messages.error(request, "邮箱已注册，请重新注册")

                return HttpResponseRedirect('/user/register')

            except Exception as e:

                if register_password==register_password2:

                    m = hashlib.md5()

                    m.update(register_password.encode())

                    register_password_m = m.hexdigest()

                    my_sender = '352446506@qq.com'
                    my_pass = 'dtfvraluuolybigj'
                    my_user = register_email
                    import random
                    code = random.randint(1000, 9999)

                    msg = MIMEText(
                        '<html><head></head><body><div style="background-color:#262827;"><br><br><br><hr size="5" noshade="noshade" style="border:5px #cccccc dotted;"><h1 style="color: aliceblue;"><strong>尊敬的用户您好!<br><br>欢迎使用本系统<br />本次验证码为:' + str(
                            code) + '</strong></h1><img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpicnew8.photophoto.cn%2F20140511%2Fheisebeijing-shuzhixiaoniao-heisewenlubeijing-02084221_1.jpg&refer=http%3A%2F%2Fpicnew8.photophoto.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1644811756&t=abc196077281a644bddce5e2eac8dbf2" ></div></body></html>',
                        'html', 'utf-8')
                    msg['From'] = formataddr(['ShiHaoyang.top', my_sender])
                    msg['To'] = formataddr(['FK', my_user])
                    msg['Subject'] = '用户注册系统'
                    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
                    server.login(my_sender, my_pass)
                    server.sendmail(my_sender, [my_user], msg.as_string())
                    server.quit()

                    resq = HttpResponseRedirect('/user/check')
                    resq.set_cookie(key='res_username', value=register_username,max_age=None,expires=None)
                    resq.set_cookie(key='res_email', value=register_email,max_age=None,expires=None)
                    resq.set_cookie(key='res_password', value=register_password_m,max_age=None,expires=None)
                    resq.set_cookie(key='res_code', value=code,max_age=None,expires=None)

                    return resq


                else:

                    messages.error(request, "两次密码输入不一致")

                    return HttpResponseRedirect('/user/register')


def check(request):
    if request.method == 'GET':

        return render(request, 'check.html')

    elif request.method == 'POST':
        codes=request.POST['code']
        code=request.COOKIES.get('res_code')
        if code==codes:

            User.objects.create(username=request.COOKIES.get('res_username'),email=request.COOKIES.get('res_email'),password=request.COOKIES.get('res_password'))


            return HttpResponseRedirect('/user/login')
        else:
            messages.error(request, "验证码输入错误")
            return HttpResponseRedirect('/check')

def exit(request):
    resq = HttpResponseRedirect('/user/login')
    if request.COOKIES.get('username'):
        resq.delete_cookie('username')
    if request.session['username']:
        del request.session['username']
    return resq

def busy(request):
    return render(request, 'busy.html')
