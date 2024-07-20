from django.shortcuts import render

# Creat 'e, our views here.
def login(request) :

    context = {
        'title': 'Home - Главная',

    }
    return render(request, 'users/login.html', context)

def regis(request) :

    context = {
        'title': 'Home - Главная',

    }
    return render(request, 'users/regis.html', context)

def profile(request) :

    context = {
        'title': 'Home - Главная',

    }
    return render(request, 'users/profile', context)

def logout(request) :

    context = {
        'title': 'Home - Главная',

    }
    return render(request, '', context)

