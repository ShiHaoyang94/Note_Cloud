import traceback

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
import re
from django.core import mail

from Note_Cloud import settings

try:

    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if re.match("^/admin/", request.path):
            return None
        elif request.path == '/busy/':

            return None
        elif request.COOKIES.get('res_code'):
            if request.path != '/user/login/' and request.path != '/user/register/' and request.path != '/user/check/' :

                if  request.session.get('username') or request.COOKIES.get('username') :
                    if request.path != '/index/' and request.path != '/user/exit/':

                        return HttpResponseRedirect('/index')
                elif request.path == '/user/register/':
                    return HttpResponseRedirect('/user/register')
                elif request.path != '/user/check/':
                    return HttpResponseRedirect('/user/check')
                else:
                    return HttpResponseRedirect('/user/login/')

        else:

            if request.path != '/user/login/' and request.path != '/user/register/' :

                if  request.session.get('username') or request.COOKIES.get('username') :
                    if request.path != '/index/' and request.path != '/user/exit/':

                        return HttpResponseRedirect('/index')
                else:
                    return HttpResponseRedirect('/user/login/')

# class IpMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         ip_address=request.META['REMOTE_ADDR']
#         print('我的地址'+ip_address)

class ExceptionMW(MiddlewareMixin):
    def process_exception(self,request,exception):

        mail.send_mail(subject='Note_Cloud报错啦~',message=traceback.format_exc(),from_email='352446506@qq.com',recipient_list=settings.EX_EMAIL)
        return HttpResponseRedirect('/busy')