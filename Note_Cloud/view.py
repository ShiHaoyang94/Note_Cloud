from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
def index(request):
    html = "<h1>我的主页</h1>"
    return HttpResponse(html)

def login(request):
    return HttpResponseRedirect('/user/login')
