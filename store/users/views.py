from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import UserLoginForm, UserRegistrationForm


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
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Главная',
        'form': form

    }
    return render(request, 'users/regis.html', context)


def profile(request):
    context = {
        'title': 'Home - Главная',

    }
    return render(request, 'users/profile', context)


def logout(request):

    auth.logout(request)

    return redirect(reverse('main:index'))
