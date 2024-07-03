from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'title': 'Home - Главная',
        'content': "Welcome to our online shop"
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'Home - О нас',
        'content': "О нас",
        'text_on_page': "Текст о том почему этот магазин такой классный, и какой хороший товар."
    }

    return render(request, 'main/about.html', context)