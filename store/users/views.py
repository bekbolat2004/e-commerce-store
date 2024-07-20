from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from users.forms import UserLoginForm


# Creat 'e, our views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Home - Authorization',
        'form': form
    }
    return render(request, 'users/login.html', context)


def regis(request):
    context = {
        'title': 'Home - Главная',

    }
    return render(request, 'users/regis.html', context)


def profile(request):
    context = {
        'title': 'Home - Главная',

    }
    return render(request, 'users/profile', context)


def logout(request):
    context = {
        'title': 'Home - Главная',

    }
    return render(request, '', context)
