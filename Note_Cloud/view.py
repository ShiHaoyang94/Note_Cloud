from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render


def login(request):
    return HttpResponseRedirect('/user/login')


