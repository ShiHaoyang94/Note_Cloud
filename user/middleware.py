from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect



try:

    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.COOKIES.get('res_code'):
            if request.path != '/user/login/' and request.path != '/user/register/' and request.path != '/user/check/' :

                if  request.session.get('username') or request.COOKIES.get('username') :
                    if request.path != '/index/' and request.path != '/user/exit/':

                        return HttpResponseRedirect('/index')
                else:
                    return HttpResponseRedirect('/user/login/')
        else:
            if request.path != '/user/login/' and request.path != '/user/register/' :

                if  request.session.get('username') or request.COOKIES.get('username') :
                    if request.path != '/index/' and request.path != '/user/exit/':

                        return HttpResponseRedirect('/index')
                else:
                    return HttpResponseRedirect('/user/login/')