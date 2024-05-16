from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'title' : "Home page",
        'content': "Welcome to our web-site! Time to change something",
        'digit': ['one', 'second', 'beka'],
        'leg': True
    }

    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse('about')
