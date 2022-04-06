from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')